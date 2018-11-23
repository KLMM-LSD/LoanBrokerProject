import zeep
from zeep import Settings
import pika
import json


def requestSoapService(body):
    wsdl = 'http://localhost:8081/ws/rules.wsdl'
    client = zeep.Client(wsdl=wsdl)
    return client.service.GetRules(float(body['loanAmount']), int(body['loanDuration']), int(body['creditScore']))


def addBanks(banks, json):
    json['banks'] = []
    for bank in banks:
        json['banks'].append({"name": bank.name, "bankId": bank.bankId, "timeout": bank.timeout})
    return json


def addBankToQueue(banks):
    connection = pika.BlockingConnection(pika.ConnectionParameters('datdb.cphbusiness.dk'))
    channel = connection.channel()

    channel.exchange_declare(exchange='GroupB.getBanks', exchange_type='fanout', durable=True)

    channel.basic_publish(exchange='GroupB.getBanks', routing_key='', body=json.dumps(banks))

    print(" [X] Sent: %r" % (banks))
    connection.close()


def connect():
    connection = pika.BlockingConnection(pika.ConnectionParameters('datdb.cphbusiness.dk'))
    channel = connection.channel()

    channel.exchange_declare(exchange='GroupB.creditscore.exchange', exchange_type='fanout', durable='true')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='GroupB.creditscore.exchange', queue=queue_name, routing_key='')

    print(' [*] Waiting for answer. To exit press CTRL+C')

    channel.basic_consume(callback, queue=queue_name)

    channel.start_consuming()


def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    body = body.decode('utf-8')
    banks = requestSoapService(json.loads(body))
    jsonBody = addBanks(banks, json.loads(body))
    addBankToQueue(jsonBody)


if __name__ == "__main__":
    connect()