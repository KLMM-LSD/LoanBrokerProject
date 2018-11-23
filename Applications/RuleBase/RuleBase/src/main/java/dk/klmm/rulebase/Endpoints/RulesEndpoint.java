/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dk.klmm.rulebase.Endpoints;

import io.spring.guides.gs_producing_web_service.GetRulesRequest;
import io.spring.guides.gs_producing_web_service.GetRulesResponse;
import io.spring.guides.gs_producing_web_service.Rules;
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
    
    private List<Rules> getBankInfo(double lAmount, int lDuration, int creditScore){
        List<Rules> banks = new ArrayList();
        if(creditScore >= 0 && creditScore <= 800) {
            if((lAmount >= (double) 50000) && (creditScore >= 700) && ((lDuration <= 360) && (lDuration >= 0))) {
                Rules rabbitBank = new Rules();
                rabbitBank.setName("Svedbanken");
                rabbitBank.setBankId("GroupB.Svedbanken");
                rabbitBank.setTimeout(50);
                banks.add(rabbitBank);
            } 
            if (((lAmount >= (double) 25000)) && (creditScore >= 500) && ((lDuration <= 360) && (lDuration >= 0))){
                Rules jsonBank = new Rules();
                jsonBank.setName("DatBank");
                jsonBank.setBankId("GroupB.DatBank");
                jsonBank.setTimeout(40);
                banks.add(jsonBank);
            }
            if (((lAmount >= (double) 10000)) && (creditScore >= 250) && ((lDuration <= 360) && (lDuration >= 0))){
                Rules xmlBank = new Rules();
                xmlBank.setName("BongoBank");
                xmlBank.setBankId("GroupB.BongoBank");
                xmlBank.setTimeout(30);
                banks.add(xmlBank);
            } 
            if ((lAmount >= (double) 100) && (creditScore >= 0) && ((lDuration <= 360) && (lDuration >= 0))){
                Rules webBank = new Rules();
                webBank.setName("Bankerot");
                webBank.setBankId("GroupB.Bankerot");
                webBank.setTimeout(20);
                banks.add(webBank);
            }
        }
        System.out.println(banks.size());
        System.out.println(banks);
        return banks;
    }
}
