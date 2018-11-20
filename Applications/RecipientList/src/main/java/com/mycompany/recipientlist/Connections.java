package com.mycompany.recipientlist;

import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import java.io.IOException;
import java.util.concurrent.TimeoutException;
import java.util.logging.Level;
import java.util.logging.Logger;

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

    public Connections() throws IOException, TimeoutException {
       
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost(HOST);
        factory.setUsername(USERNAME);
        factory.setPassword(PASSWORD);

        connection = factory.newConnection();
        channel = connection.createChannel();
    }

    public Channel getChannel() {
        if(channel == null){
            try {
                channel = connection.createChannel();
            } catch (IOException ex) {
                Logger.getLogger(Connections.class.getName()).log(Level.WARNING, "IOException, when trying to create a channel", ex);
            }
        }
        return channel;
    }
    
    public Connection getConnection(){
        return connection;
    }

}
