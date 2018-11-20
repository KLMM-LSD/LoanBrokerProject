
import com.mycompany.recipientlist.Connections;
import java.io.IOException;
import java.util.concurrent.TimeoutException;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
/**
 *
 * @author Mart_
 */
public class TestMyThing {

    public static void main(String[] args) throws IOException, TimeoutException {

        Connections c = new Connections();
        com.rabbitmq.client.Channel channel = c.getChannel();
        //channel.queueDeclare("GrouB.test" , false, false, false, null);
        channel.queueDeclare();
        String message = "Hello World!";
        JSONArray jArr = new JSONArray();
        JSONObject json = new JSONObject();
        json.put("information","hej Michael");
        JSONObject json2 = new JSONObject();
        json.put("Kinfomation","hej Dichael");
        JSONObject json3 = new JSONObject();
        json.put("Rnformation","hej Lichael");
        
        jArr.add(json);
        jArr.add(json2);
        jArr.add(json3);
        
        //String test = "Hello World";
        //channel.basicPublish("GroupB.translators", "", null, test.getBytes());
        //System.out.println("Message send: " + test);
        System.out.println(" [x] Sent '" + json + "'");
        channel.basicPublish("GroupB.getBanks", "", null, json.toJSONString().getBytes());
        
    }
}
