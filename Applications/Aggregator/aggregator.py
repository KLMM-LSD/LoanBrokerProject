# Author:......KRG
# Description:.Aggregator to receive loan quotes and choose the best one.
import aio_pika
from aio_pika import ExchangeType
from collections import defaultdict
import sys, json, signal, time, threading, asyncio, queue
from functools import partial

__inputexchangename = "GroupB.aggregator"
__outputexchangename = "GroupB.bestquote"
__timeout = 1

#Collection to keep all social security numbers in
__ssNumbers = dict()
__outputDicts = queue.Queue()
#Time from first learning of an ssn, until a decision is made

    
    
def consumeResponse(message):
    with message.process():
        dict = json.loads(message.body)
        
        ssn = dict['ssn']
        dict['bankId'] = str(message.correlation_id)[2:-1]
        interestRate = dict['interestRate']
            
        if ssn in __ssNumbers: #If ssn is known, append quote
            try:
                __ssNumbers[ssn]['quotes'].append({'interestRate':interestRate, 'bankId': dict['bankId']})
                log(__ssNumbers[ssn])
                print("Received loan quote")
            except Exception as e:
                print(e)
        else:
            print('Never heard of this ssn: ' + ssn)
        
    return

# NOT IMPLEMENTED
def consumeRequest(message):
    with message.process():
        d = json.loads(message.body)
        ssn = d['ssn']
        
        if not ssn in __ssNumbers: #If ssn is unknown, schedule a decision for 1 timeout from now
            
            d['quotes'] = []
            d.pop('creditScore', None)
            
            
            waitTime = max(d['banks'], key= lambda d:d['timeout'])['timeout']
            
            __ssNumbers[ssn] = d
            
            decisionThread = threading.Thread(target=bestLoanDecision, args=(ssn, waitTime), daemon=True)
            #This thread terminates on its own and daemon=True, so fire and forget.
            decisionThread.start()
    return

def log(msgdict):
    with open('responses.log', 'a') as f:
        f.write(json.dumps(msgdict) + "\n")

async def requestLoop(queue):
    while True:
        await asyncio.sleep(__timeout)
        await queue.consume(partial(consumeRequest))

async def responseLoop(queue):
    while True:
        await asyncio.sleep(__timeout)
        await queue.consume(partial(consumeResponse))
        #Flushing in response loop to ensure speedy print()
        sys.stdout.flush()

async def outputLoop(exchange):
    while True:
        await asyncio.sleep(__timeout)
        while not __outputDicts.empty():
            outdict = __outputDicts.get()
            print("Sending on best quote: " + json.dumps(outdict))
            try:
                await toBrokerOut(outdict, exchange)
            except Exception as e:
                print("Failed to send message: " + str(e))
            else:
                print("Sent.")
        
async def toBrokerOut(outdict, exchange):
    await exchange.publish(aio_pika.Message(body = json.dumps(outdict).encode()), routing_key='')
    return
    
def bestLoanDecision(ssn, timeout):
        print("This new thread just started going to sleep for " + str(timeout) + " seconds.")
        #First, wait for other responses to come in
        time.sleep(timeout)
        print("Woah, awake again!")
        #Then figure out where the best deal is at
        if __ssNumbers[ssn]['quotes']:
            bestRate = min(__ssNumbers[ssn]['quotes'], key= lambda d:d['interestRate'])
            print("Best rate: " + json.dumps(bestRate))
            
            #Send bestRate to destination (File for now)
            with open(ssn + ".log", "w") as loanFile:
                quoteCount = len(__ssNumbers[ssn]['quotes'])
                loanFile.write("Best rate is " + str(bestRate['interestRate']) + " at " + ssn + ", from " + str(quoteCount) + " quotes total\n")
            
            bank = None
            banks = __ssNumbers[ssn]['banks']
            print(banks)
            for d in  banks:
                print(d)
                if str(d['bankId']) == str(bestRate['bankId']):
                    bank = d
                    break
            #bank = next(filter(lambda b: b['bankId'] == bestRate['bankId'], __ssNumbers[ssn]['banks']))
            
            outDict = {
                        'ssn':int(ssn), 
                        'loanAmount':__ssNumbers[ssn]['loanAmount'], 
                        'loanDuration':__ssNumbers[ssn]['loanDuration'], 
                        'bank':bank['name'], 
                        'quote':bestRate['interestRate']
                      }
            
            print(outDict)
            
            #Leave bestRate on output queue, so it will be sent on
            __outputDicts.put(outDict)
            
        #Then clear list so that new requests with this ssn will start the decision timer again
        __ssNumbers[ssn].pop(ssn, None)
        return
        
        
async def main(loop):
    connection = await aio_pika.connect_robust("amqp://guest:guest@datdb.cphbusiness.dk:5672/", loop=loop)
    
    channel = await connection.channel()
    
    tempinex = channel.declare_exchange(__inputexchangename, ExchangeType.DIRECT, passive=False, durable=True)
    tempoutex = channel.declare_exchange(__outputexchangename, ExchangeType.FANOUT, passive=False, durable=True)
    tempin_request = channel.declare_queue('GroupB.aggregator.request', auto_delete=True, exclusive=False)
    tempin_response = channel.declare_queue('GroupB.aggregator.response', auto_delete=True, exclusive=False)
    inputexchange = await tempinex
    
    outputexchange = await tempoutex
    inqueue_request = await tempin_request
    inqueue_response= await tempin_response
    
    await inqueue_request.bind(inputexchange, routing_key="request")
    await inqueue_response.bind(inputexchange, routing_key="response")
    
    # Ensuring Ctrl+C closes gratefully
    signal.signal(signal.SIGINT, signal.default_int_handler)
    try:
        requestL = requestLoop(inqueue_request)
        responseL = responseLoop(inqueue_response)
        outputL = outputLoop(outputexchange)
        #loop.create_task(jsonL)
        #loop.create_task(xmlL)
        
        await asyncio.wait([requestL, responseL, outputL])
    except KeyboardInterrupt:
        pass
    await connection.close()

    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    while True:
        try:
            loop.run_until_complete(main(loop))
        except (RuntimeError, ConnectionError, ConnectionRefusedError, aio_pika.pika.exceptions.ChannelClosed, aio_pika.pika.exceptions.ConnectionClosed) as e:
            print("Connection failed...: " + str(e))
            time.sleep(5)
    loop.close()