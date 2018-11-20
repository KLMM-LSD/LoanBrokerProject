/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.recipientlist;

import com.rabbitmq.client.*;
import com.rabbitmq.client.AMQP.Queue;
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

    private static final String EXCHANGE_NAME = "GroupB.creditscore.exchange";
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
        channel.exchangeDeclare(EXCHANGE_NAME, "direct", true, false, null);
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

                try {
                    json = (JSONObject) jParser.parse(message);
                } catch (ParseException ex) {
                    System.out.println("Exception in handleDelivery - RecipientList: " + ex.getMessage());
                }

                JSONArray jArr = (JSONArray) json.get("banks");
                sendToTranslate(jArr);

                JSONObject toAgre = json;
                sendToAggregator(toAgre);
            }
        };
        channel.basicConsume(queueName, true, consumer);
    }

    // Forwards messages to the translators, as well as provides info to aggregator
    private static void sendToTranslate(JSONArray array) {
        array.forEach(item -> {
            try {
                JSONObject json = (JSONObject) item;
                switch (json.get("BankName").toString().toLowerCase()) {
                    case "bongobank":
                        channel.basicPublish("GroupB.translators", "", null, json.toJSONString().getBytes());
                        break;
                    case "svedbanken":
                        channel.basicPublish("", "", null, null);
                        break;
                    case "datbank":
                        //channel.basicPublish("", "", bp, bytes);
                        break;
                    case "bankerot":
                        //channel.basicPublish("", "", bp, bytes);
                        break;
                    default:
                        System.out.println("Bank Ikke Genkendt");
                        break;
                }
            } catch (IOException ex) {
                Logger.getLogger(Main.class.getName()).log(Level.SEVERE, "IOEXception in SendMessageToTranslators", ex);
            }
        });
    }

    private static void sendToAggregator(JSONObject json) throws IOException {
        System.out.println("I receieved this json: " + json);
        channel.basicPublish("GroupB.aggregator", "", null, json.toJSONString().getBytes());
    }
}
