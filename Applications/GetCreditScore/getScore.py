import zeep
import pika

def getCreditScoreFromWsdl(ssn):
    wsdl = 'http://datdb.cphbusiness.dk:8080/CreditScoreService/CreditScoreService?wsdl'
    client = zeep.Client(wsdl=wsdl)
    return client.service.creditScore(ssn)

def callback_func(self, ch, method, properties, body):
    print("{} received '{}'".format(self.name, body))

def sendQueue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='datdb.cphbusiness.dk'))
    channel = connection.channel()

    channel.exchange_declare(exchange='GroupB.exchange', exchange_type='direct')

    creditscore = getCreditScoreFromWsdl('546372-9807')
    channel.basic_publish(exchange='GroupB.exchange',
                          routing_key='creditscore',
                          body=str(creditscore))

    print(" [x] Sent %r" % (creditscore))

    connection.close()

def listenQueue():
    sendQueue()
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='datdb.cphbusiness.dk'))
    channel = connection.channel()

    channel.exchange_declare(exchange='GroupB.exchange',
                             exchange_type='direct')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='GroupB.exchange',
                       queue=queue_name,
                       routing_key='creditscore')

    print(' [*] Waiting for exchange. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()

def main():
    listenQueue()

if __name__=="__main__":
    main()