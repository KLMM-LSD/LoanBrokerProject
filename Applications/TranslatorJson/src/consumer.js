import rabbitmq from '../extra/rabbitmq.js';
import timestamp from './timestamp.js';
import producer from './producer.js';


export default function(ampqConn) {
    let ex = rabbitmq.consumer.exchange;
    let bind = rabbitmq.consumer.binding;

    ampqConn.createChannel((err, ch) => {
        let type = rabbitmq.consumer.type

        ch.assertExchange(ex, type, {
            durable: true
        });

        let timeStamp;
        ch.assertQueue('', {
            exclusive: true
        }, (err, que) => {
            timeStamp = timestamp.getTimeStamp();
            console.log(`\nConsumer ${timeStamp}\n[*] Waiting for ${que.queue} messages`);

            ch.bindQueue(que.queue, ex, bind);

            ch.consume(que.queue, (message) => {
                timeStamp = timestamp.getTimeStamp();
                console.log(`\nConsumer ${timeStamp}:\n [x] got message ${message.content.toString()}`);
                producer(ampqConn, message);
            }, {noAck: true});
        });
    });
}