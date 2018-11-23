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

    channel.exchange_declare(exchange='GroupB.creditscore.exchange', exchange_type='fanout', durable='true')

    jsonData['creditScore'] = getCreditScoreFromWsdl(jsonData['ssn'])
    jsonData['ssn'] = jsonData['ssn'].replace("-","")
    channel.basic_publish(exchange='GroupB.creditscore.exchange',
                          routing_key='GroupB.creditscore',
                          body=json.dumps(jsonData))

    print(" [x] Sent %r" % (jsonData))

    connection.close()

def main(ssn, loanAmount, loanDuration):
    jsonData = {
        "ssn":ssn,
        "loanAmount": loanAmount,
        "loanDuration": loanDuration
    }
    sendQueue(json.loads(json.dumps(jsonData)))

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])