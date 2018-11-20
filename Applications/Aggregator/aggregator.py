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
__ssNumbers = defaultdict(list)
__outputDicts = queue.Queue()
#Time from first learning of an ssn, until a decision is made
__decisionTimeout = 30
    
    
def consumeResponse(message, exchange):
    with message.process():
        dict = json.loads(message.body)
        
        ssn = dict['ssn']
        dict['bankID'] = str(message.correlation_id)
        interestRate = dict['interestRate']
            
        if len(__ssNumbers[ssn]) == 0: #If ssn is unknown, schedule a decision for 1 timeout from now
            decisionThread = threading.Thread(target=bestLoanDecision, args=(ssn, __decisionTimeout), daemon=True)
            #This thread terminates on its own and daemon=True, so fire and forget.
            decisionThread.start()
        __ssNumbers[ssn].append({'ssn':ssn, 'interestRate':interestRate, 'bankID': dict['bankID']})
        log(dict)
        print("Received loan quote")
        
        return

# NOT IMPLEMENTED
def consumeRequest():
    return

def log(msgdict):
    with open('responses.log', 'a') as f:
        f.write(json.dumps(msgdict) + "\n")

async def requestLoop(queue, exchange):
    while False:
        await asyncio.sleep(__timeout)
        await queue.consume(partial(consumeRequest, exchange=exchange))

async def responseLoop(queue, exchange):
    while True:
        await asyncio.sleep(__timeout)
        await queue.consume(partial(consumeResponse, exchange=exchange))
        #Flushing in response loop to ensure speedy print()
        sys.stdout.flush()

async def outputLoop(exchange):
    while True:
        await asyncio.sleep(__timeout)
        for dict in __outputDicts:
            await toBrokerout(msg, exchange)
        
async def toBrokerOut(outdict, exchange):
    await exchange.publish(aio_pika.Message(body = json.dumps(outdict).encode()))
    return
    
def bestLoanDecision(ssn, timeout):
        print("This new thread just started going to sleep.")
        #First, wait for other responses to come in
        time.sleep(timeout)
        print("Woah, awake again!")
        #Then figure out where the best deal is at
        bestRate = min(__ssNumbers[ssn], key= lambda d:d['interestRate'])
        
        #Send bestRate to destination (File for now)
        with open(ssn + ".txt", "w") as loanFile:
            quoteCount = len(__ssNumbers[ssn])
            loanFile.write("Best rate is " + str(bestRate['interestRate']) + " at " + str(bestRate['ssn']) + ", from " + str(quoteCount) + " quotes total\n")
            
        #Then clear list so that new requests with this ssn will start the decision timer again
        __ssNumbers[ssn].clear()
        return

        
async def main(loop):
    connection = await aio_pika.connect_robust("amqp://guest:guest@datdb.cphbusiness.dk:5672/", loop=loop)
    
    channel = await connection.channel()
    
    tempinex = channel.declare_exchange(__inputexchangename, ExchangeType.DIRECT, passive=False, durable=True)
    tempoutex = channel.declare_exchange(__outputexchangename, ExchangeType.FANOUT, passive=False, durable=True)
    tempin_request = channel.declare_queue(auto_delete=True, exclusive=False)
    tempin_response = channel.declare_queue(auto_delete=True, exclusive=False)
    
    inputexchange = await tempinex
    outputexchange = await tempoutex
    inqueue_request = await tempin_request
    inqueue_response= await tempin_response
    
    await inqueue_request.bind(inputexchange, routing_key="request")
    await inqueue_response.bind(inputexchange, routing_key="response")
    
    # Ensuring Ctrl+C closes gratefully
    signal.signal(signal.SIGINT, signal.default_int_handler)
    try:
        requestL = requestLoop(inqueue_request, outputexchange)
        responseL = responseLoop(inqueue_response, outputexchange)
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