# Author KRG
# 'Svedbanken' 

import aio_pika
from aio_pika import ExchangeType
import asyncio, signal, json

__exchangename = "GroupB.svedbanken.requests"


def calculateEligible(creditScore):
    if creditScore > 500:
        return True
    return False

def calculateRate(creditScore, loanAmount, loanDuration):
    rate = (300.0 - (creditScore - 500.0)) / 100.0 + 0.01
	
    if loanDuration < 120:
        rate+= 1.0
    elif loanDuration  < 60:
        rate+= 5.0
    
    if loanAmount > 10000.0:
        rate = rate / 2
    
    
    return rate

async def handleQuote(message):
    with message.process():
        dict = json.loads(message.body)
        #raise Exception(str(message.body))
        
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
            await message.channel.default_exchange.publish(aio_pika.Message(body = outbody, correlation_id = message.correlation_id), routing_key = message.reply_to)
            
            
async def main(loop):
    connection = await aio_pika.connect_robust("amqp://guest:guest@datdb.cphbusiness.dk:5672/", loop=loop)
    
    channel = await connection.channel()
    
    #These could happen in parallel ( async.wait()? )
    sb_exchange = await channel.declare_exchange(__exchangename, ExchangeType.FANOUT, passive=True, durable=True)
    inqueue = await channel.declare_queue(auto_delete=True, exclusive=True)
    
    await inqueue.bind(sb_exchange)
    
    # Ensuring Ctrl+C closes gratefully
    signal.signal(signal.SIGINT, signal.default_int_handler)
    try:
        while True:
            await inqueue.consume(handleQuote)
    except KeyboardInterrupt:
        connection.close()

    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()