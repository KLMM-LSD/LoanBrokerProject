# Author:......KRG
# Description:.Normalizer to receive loan quotes in different formats and send them on as JSON.
import aio_pika
from aio_pika import ExchangeType
import sys, json, asyncio, signal
import xml.etree.ElementTree as ET
from functools import partial

__exchangename = "GroupB.normalizer"
__outputexchangename = "GroupB.aggregator"
__timeout = 1

def log(msgdict):
    with open('normalized.log', 'a') as f:
        f.write(json.dumps(msgdict) + "\n")

async def jsonQuote(message, exchange):
    print("JSON")
    with message.process():
        dict = json.loads(message.body)
        print(dict)
        await toAggregator(dict, exchange, message.correlation_id)
    return

    
async def xmlQuote(message, exchange):
    print("XML")
    with message.process():
        dict = {}
        
        root = ET.fromstring(message.body)
        dict['interestRate'] = float(root.find('interestRate').text)
        dict['ssn'] = str(root.find('ssn').text)
        print(dict)
        await toAggregator(dict, exchange, message.correlation_id)
    return
    
async def jsonLoop(queue, exchange):
    while True:
        await asyncio.sleep(__timeout)
        await queue.consume(partial(jsonQuote, exchange=exchange))
        sys.stdout.flush()
        
async def xmlLoop(queue, exchange):
    while True:
        await asyncio.sleep(__timeout)
        await queue.consume(partial(xmlQuote, exchange=exchange))
    
async def toAggregator(outdict, exchange, correlationID):
    await exchange.publish(aio_pika.Message(body = json.dumps(outdict).encode(), correlation_id = correlationID), routing_key='response')
    log(outdict)
    return
    
async def main(loop):
    connection = await aio_pika.connect_robust("amqp://guest:guest@datdb.cphbusiness.dk:5672/", loop=loop)
    
    channel = await connection.channel()
    
    tempoutex = channel.declare_exchange(__outputexchangename, ExchangeType.DIRECT, passive=False, durable=True)
    tempin_json = channel.declare_queue("GroupB.normalizer.json", auto_delete=True, exclusive=False)
    tempin_xml = channel.declare_queue("GroupB.normalizer.xml", auto_delete=True, exclusive=False)
    
    outputexchange = await tempoutex
    inqueue_json = await tempin_json
    inqueue_xml = await tempin_xml
    
    # Ensuring Ctrl+C closes gratefully
    signal.signal(signal.SIGINT, signal.default_int_handler)
    try:
        jsonL = jsonLoop(inqueue_json, outputexchange)
        xmlL = xmlLoop(inqueue_xml, outputexchange)
        #loop.create_task(jsonL)
        #loop.create_task(xmlL)
        
        await asyncio.wait([jsonL, xmlL])
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

