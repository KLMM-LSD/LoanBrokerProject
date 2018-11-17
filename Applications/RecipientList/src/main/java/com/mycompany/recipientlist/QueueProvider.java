/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.recipientlist;

import com.rabbitmq.client.Channel;
import java.io.IOException;
import java.util.concurrent.TimeoutException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Mart_
 */
class QueueProvider implements Runnable {

    private Connections connection;
    private Channel channel;
    private String endPoint;

    public QueueProvider() throws IOException, TimeoutException {
        this.connection = new Connections(endPoint);
        this.channel = connection.getChannel();
    }

    @Override
    public void run() {
        try {
            channel.basicConsume(endPoint, true, (com.rabbitmq.client.Consumer) this);
        } catch (IOException ex) {
            Logger.getLogger(QueueProvider.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
