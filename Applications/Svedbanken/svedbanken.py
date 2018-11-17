# Author KRG
# 'Svedbanken' 

import aio_pika
from aio_pika import ExchangeType
import asyncio, signal, json
from functools import partial

__exchangename = "GroupB.svedbanken.requests"


def calculateEligible(creditScore):
    if creditScore > 500:
        return True
    return False

def calculateRate(creditScore, loanAmount, loanDuration):
    rate = (300.0 - (creditScore - 500.0)) / 100.0 + 1.2
    
    if loanDuration  < 31:
        # Because we value having you as a customer <3
        rate+= 8.33
    elif loanDuration  < 60:
        rate+= 5.0
    elif loanDuration < 120:
        rate+= 1.0

    
    if loanAmount > 10000.0:
        rate = rate / 2
        
    return rate

async def handleQuote(message, channel):
    with message.process():
        dict = json.loads(message.body)
        
        if calculateEligible(dict['creditScore']):
            outbody = json.dumps(
                                    {
                                        'interestRate': calculateRate(  dict['creditScore'], 
                                                                        dict['loanAmount'], 
                                                                        dict['loanDuration']
                                                                      ), 
                                        'ssn': dict['ssn']
                                    }
                                )
            await channel.default_exchange.publish(aio_pika.Message(body = outbody.encode(), correlation_id = message.correlation_id), routing_key = message.reply_to)
            
            
async def main(loop):
    connection = await aio_pika.connect_robust("amqp://guest:guest@datdb.cphbusiness.dk:5672/", loop=loop)
    
    channel = await connection.channel()
    
    #These could happen in parallel ( async.wait()? )
    tempex = channel.declare_exchange(__exchangename, ExchangeType.FANOUT, passive=True, durable=True)
    tempin = channel.declare_queue(auto_delete=True, exclusive=True)
    
    sb_exchange = await tempex
    inqueue = await tempin
    
    
    await inqueue.bind(sb_exchange)
    
    # Ensuring Ctrl+C closes gratefully
    signal.signal(signal.SIGINT, signal.default_int_handler)
    try:
        while True:
            await asyncio.sleep(1)
            await inqueue.consume(partial(handleQuote, channel=channel))
    except KeyboardInterrupt:
        connection.close()

    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()