import rabbitmq from '../extra/rabbitmq.js';
import timestamp from './timestamp.js';
import producer from './producer.js';

export default function(ampqConn) {
    let ex = rabbitmq.consumer.exchange;
    let bind = rabbitmq.consumer.binding;

    ampqConn.createChannel((err, ch) => {
        let type = rabbitmq.consumer.type

        ch.assertExchange(ex, type, {
            durable: false
        });

        let timeStamp;
        ch.assertQueue('', {
            exclusive: true
        }, (err, que) => {
            timeStamp = timestamp.getTimeStamp();
            console.log(`\nConsumer ${timeStamp}\n [*] Waiting for ${que.queue} messages`);

            ch.bindQueue(que.queue, ex, bind);

            ch.consume(que.queue, (msg) => {
                timeStamp = timestamp.getTimeStamp();
                console.log(`\nConsumer ${timeStamp}:\n [x] got message ${msg.content.toString()}`);
                producer(ampqConn, msg);
            }, {noAck: true});
        });
    });
}