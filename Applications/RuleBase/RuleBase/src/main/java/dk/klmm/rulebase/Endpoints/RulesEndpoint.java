/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dk.klmm.rulebase.Endpoints;

import dk.klmm.rulebase.ruleClasses.GetRulesRequest;
import dk.klmm.rulebase.ruleClasses.GetRulesResponse;
import dk.klmm.rulebase.ruleClasses.Rules;
import java.util.ArrayList;
import java.util.List;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

/**
 *
 * @author Micha
 */

@Endpoint
public class RulesEndpoint {
    private static final String NAMESPACE_URI = "http://spring.io/guides/gs-producing-web-service";
    
    
    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "GetRulesRequest")
    @ResponsePayload
    public GetRulesResponse getRule(@RequestPayload GetRulesRequest request) {
        List<Rules> ruleDetails = getBankInfo(request.getLoanAmount(), request.getLoanDuration(), request.getCreditScore());
        GetRulesResponse response = new GetRulesResponse();
        
        for (Rules rule : ruleDetails) {
            response.getRules().add(rule);
        }
        return response;
    }
    
    private List<Rules> getBankInfo(int lAmount, int lDuration, int creditScore){
        List<Rules> banks = new ArrayList();
        if(creditScore >= 0 && creditScore <= 800) {
            if((lAmount >= (double) 50000) && (creditScore >= 700) && ((lDuration <= 360) && (lDuration >= 0))) {
                Rules rabbitBank = new Rules();
                rabbitBank.setName("GroupB.Svedbanken");
                banks.add(rabbitBank);
            } else if (((lAmount >= (double) 25000) && (lAmount <= (double) 50000)) && (creditScore >= 500) && ((lDuration <= 360) && (lDuration >= 0))){
                Rules jsonBank = new Rules();
                jsonBank.setName("GroupB.DatBank");
                banks.add(jsonBank);
            } else if (((lAmount >= (double) 10000) && (lAmount <= (double) 25000)) && (creditScore >= 250) && ((lDuration <= 360) && (lDuration >= 0))){
                Rules xmlBank = new Rules();
                xmlBank.setName("GroupB.BongoBank");
                banks.add(xmlBank);
            } else if ((lAmount >= (double) 100) && (creditScore >= 0) && ((lDuration <= 360) && (lDuration >= 0))){
                Rules webBank = new Rules();
                webBank.setName("GroupB.Bankerot");
                banks.add(webBank);
            } else {
                System.out.println("No Banks here!");
            }
        }
        return banks;
    }
}
