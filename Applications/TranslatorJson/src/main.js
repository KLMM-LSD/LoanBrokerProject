import amqp from 'amqplib/callback_api';
import rabbitmq from '../extra/rabbitmq.js';
import consumer from './consumer.js';

export function main() {
    let HOST = rabbitmq.connection.HOST;
    let USERNAME = rabbitmq.connection.USERNAME;
    let PASSWORD = rabbitmq.connection.PASSWORD;
    let connection = `amqp://${USERNAME}:${PASSWORD}@${HOST}`;

    amqp.connect(connection, (err, conn) => {
        if(err) {
            console.error(`[AMPQ] error:`, err.message);

            return setTimeout(main(), 1000);
        }
        conn.on('error', (err) => {
            if(err.message !== 'Connection closing') {
                console.error('[AMPQ] connection error: ', err.message);
            }
        });
        conn.on('close', () => {
            console.error('[AMPQ] reconnecting');
            return setTimeout(main(), 1000);
        });
        console.log('[AMPQ] connected - TranslatorJSON');
        consumer(conn);
    });
}