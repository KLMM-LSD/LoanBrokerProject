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
public class ConsumeProduce {

    private static Connections conn;
    
    
    public ConsumeProduce() throws IOException, TimeoutException {
        
        this.conn = new Connections();
        
    }
    
    

    
}
