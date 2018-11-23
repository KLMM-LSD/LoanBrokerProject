import rabbitmq from '../extra/rabbitmq.js';
import timestamp from './timestamp.js';
import translator from './translator.js';

export default function (ampqConn, message) {
    let replyTo = rabbitmq.producer.replyTo;

    ampqConn.createChannel((err, ch) => {
        let timeStamp = timestamp.getTimeStamp();
        if(err) {
            ampqConn.close();
            console.error(`\nproducer ${timeStamp}:\n[AMPQ] connection error (producer) - closing; ${err}`);
        }

        let type = rabbitmq.producer.type
        let exType = rabbitmq.producer.exchangeType;
        let bankID = rabbitmq.producer.bankID;
        let ex = rabbitmq.producer.exchange;
        let hearders = {
            type,
            bankID
        };
 
        ch.assertExchange(ex, exType, {
            durable: false
        });

        let jsonObject = JSON.parse(message.content.toString());
        let formattedObject = translator.getFormattedJson(jsonObject);

        ch.publish(ex, '', Buffer.from(JSON.stringify(formattedObject)), {
            hearders: hearders,
            replyTo: replyTo
        });
        console.log(`\nproducer ${timeStamp}:\n [+] Successfully sent message ${JSON.stringify(formattedObject)}`);
    });
}