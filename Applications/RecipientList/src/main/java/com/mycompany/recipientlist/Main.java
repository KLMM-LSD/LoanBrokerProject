/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.recipientlist;

import com.rabbitmq.client.*;
import java.io.IOException;
import java.util.concurrent.TimeoutException;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

/**
 *
 * @author Mart_
 */
public class Main {

    private static final String EXCHANGE_NAME = "GroupB.getBanks";
    private static final JSONParser jParser = new JSONParser();
    private static Channel channel;
    private static Connections conn;
    private static ConsumeProduce cp;

    public static void main(String[] args) throws IOException, TimeoutException {
        conn = new Connections();
        cp = new ConsumeProduce();
        listenForMessage();
    }

    public static void listenForMessage() throws IOException, TimeoutException {

        channel = conn.getChannel();
        channel.exchangeDeclare(EXCHANGE_NAME, "fanout", true, false, null);
        String queueName = channel.queueDeclare().getQueue();
        channel.queueBind(queueName,
                EXCHANGE_NAME,
                "");

        System.out.println(" [*] Waiting for messages. Listening till application stopped");

        Consumer consumer = new DefaultConsumer(channel) {
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {

                String message = new String(body, "UTF-8");
                JSONObject json = null;
                System.out.println("I got a message: " + message);

                try {
                    json = (JSONObject) jParser.parse(message);
                } catch (ParseException ex) {
                    System.out.println("Exception in handleDelivery - RecipientList: " + ex.getMessage());
                }

                JSONArray jArr = (JSONArray) json.get("banks");
                JSONObject loanInfo = json;
                loanInfo.remove("banks");
                sendToTranslate(jArr, loanInfo);

                sendToAggregator(message);
            }
        };
        channel.basicConsume(queueName, true, consumer);
    }

    // Forwards messages to the translators, as well as provides info to aggregator
    @SuppressWarnings("empty-statement")
    private static void sendToTranslate(JSONArray array, JSONObject jsonInfo) throws IOException {

        array.forEach(item -> {
            try {
                JSONObject obj = (JSONObject) item;
                String bankName = obj.get("name").toString();

                switch (bankName.toLowerCase()) {
                    case "bongobank":
                       channel.basicPublish("GroupB.translators", "xml", null, jsonInfo.toJSONString().getBytes());
                        break;
                    case "datbank":
                        channel.basicPublish("GroupB.translators", "DatBank", null, jsonInfo.toJSONString().getBytes());
                        break;
                    case "bankerot":
                        //channel.basicPublish("GroupB.translators", "", bp, bytes);
                        break;
                    case "svedbanken":
                        channel.basicPublish("GroupB.translators", "", null, "".getBytes());
                        break;
                    default:
                        System.out.println("Bank Ikke Genkendt");
                        break;
                }
            } catch (IOException ex) {
                Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, ex);
            }
        });
    }

    private static void sendToAggregator(String msg) throws IOException {
        System.out.println("Send to aggregator: " + msg);
        channel.basicPublish("GroupB.aggregator", "request", null, msg.getBytes());
    }
}
