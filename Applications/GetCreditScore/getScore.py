import zeep
import pika
import json
import sys

def getCreditScoreFromWsdl(ssn):
    wsdl = 'http://datdb.cphbusiness.dk:8080/CreditScoreService/CreditScoreService?wsdl'
    client = zeep.Client(wsdl=wsdl)
    return client.service.creditScore(ssn)

def sendQueue(jsonData):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='datdb.cphbusiness.dk'))
    channel = connection.channel()

    channel.exchange_declare(exchange='GroupB.creditscore.exchange', exchange_type='direct')

    jsonData['creditScore'] = getCreditScoreFromWsdl(jsonData['ssn'])
    channel.basic_publish(exchange='GroupB.creditscore.exchange',
                          routing_key='creditscore',
                          body=json.dumps(jsonData))

    print(" [x] Sent %r" % (jsonData))

    connection.close()

def listenQueue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='datdb.cphbusiness.dk'))
    channel = connection.channel()

    channel.exchange_declare(exchange='GroupB.creditscore.exchange',
                             exchange_type='direct')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='GroupB.creditscore.exchange',
                       queue=queue_name,
                       routing_key='creditscore')

    print(' [*] Waiting for exchange. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()

def main(ssn, loanAmount, loanDuration):
    jsonData = {
        "ssn":ssn,
        "loan-Amount": loanAmount,
        "loan-Duration": loanDuration
    }
    sendQueue(json.loads(json.dumps(jsonData)))
    #listenQueue()

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])