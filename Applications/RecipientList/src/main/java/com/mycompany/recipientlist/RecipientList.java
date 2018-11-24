/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.recipientlist;

import java.util.ArrayList;
import java.util.HashMap;
import org.json.simple.JSONObject;

public class RecipientList {

    private QueueProvider queue;
    private Producer producer;

    public RecipientList() {
        //Modtager Banks
        //Uddelegere dem til de banker der tillader said creditScore
        //Sender det videre til translators.
    }

    public JSONObject getLoan(HashMap banksAndRules) {
        HashMap details = (HashMap) banksAndRules.get("details");
        ArrayList<HashMap> banks = (ArrayList<HashMap>) banksAndRules.get("banks");

        JSONObject reponse = new JSONObject();
        reponse.put("ssn", (String) details.get("ssn"));
        reponse.put("creditScore", (int) details.get("creditScore"));
        reponse.put("loanAmount", (double) details.get("loanAmount"));
        reponse.put("loanDuration", (int) details.get("loanDuration"));
        return reponse; 
    }
}
