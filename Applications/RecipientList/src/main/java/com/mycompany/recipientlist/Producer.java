/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.recipientlist;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import java.io.IOException;
import java.util.HashMap;
import java.util.concurrent.TimeoutException;
import org.json.simple.JSONObject;

/**
 *
 * @author Mart_
 */
public class Producer {

    private ConnectionFactory factory; 
    private final Connections connection;
    private Channel channel;
    private String endPoint;

    public Producer() throws IOException, TimeoutException {
        this.connection = new Connections(endPoint);
        this.channel = connection.getChannel();
    }

    //Send Messages Asynchronous. 
    public void sendMessage(HashMap header, String binding, JSONObject jsObject) {
        Thread t = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    AMQP.BasicProperties props = new AMQP.BasicProperties.Builder().headers(header).build();
                    channel.basicPublish(endPoint, binding, props, jsObject.toJSONString().getBytes());
                } catch (IOException ex) {
                    System.out.println("IOException in sendMessage: " + ex.getMessage());
                }
            }
        });
        t.run();
    }
}
