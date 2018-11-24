/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.recipientlist;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

/**
 *
 * @author Mart_
 */
public class Access {

    private QueueProvider provider;
    private Producer producer;
    private RecipientList recipient;

    public Access() throws IOException, TimeoutException {
        provider = new QueueProvider();
        producer = new Producer();
        recipient = new RecipientList();

        Thread consuming = new Thread();
        consuming.run();
    }

    public void consumeMessage() {
        
    }

}
