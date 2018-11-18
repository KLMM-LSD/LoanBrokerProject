package com.mycompany.recipientlist;

import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import java.io.IOException;
import java.util.concurrent.TimeoutException;

/**
 *
 * @author Mart_
 */
public class Connections {

    private final String HOST = "datdb.cphbusiness.dk";
    private final String USERNAME = "guest";
    private final String PASSWORD = "guest";

    private Channel channel;
    private Connection connection;
    private String endPointName;

    public Connections(String accessPoint) throws IOException, TimeoutException {
        this.endPointName = accessPoint;

        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost(HOST);
        factory.setUsername(USERNAME);
        factory.setPassword(PASSWORD);

        connection = factory.newConnection();
        channel = connection.createChannel();
        channel.queueDeclare(accessPoint, false, false, false, null);
    }

    public Channel getChannel() {
        return channel;
    }

}
