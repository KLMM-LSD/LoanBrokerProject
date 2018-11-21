/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package rulebase;

import java.io.Serializable;
import java.util.HashMap;
import javax.jws.WebMethod;
import javax.jws.WebParam;
import javax.jws.WebService;
import org.apache.commons.lang.SerializationUtils;

/**
 *
 * @author Micha
 */
@WebService(serviceName = "GetBankWebServices")
public class CreditScoreWebService {
    
    @WebMethod(operationName = "getBankRules")
    public byte[] getCreditScore(@WebParam(name = "creditScore") int creditScore) {
        System.out.println("\n{RuleBase} -- getCreditScore");
        System.out.println("Received message (credit score): " + creditScore);
        AllBankRules service = new AllBankRules();
        HashMap bankResults = service.getCreditScoreFromBanks(creditScore);
        return SerializationUtils.serialize((Serializable) bankResults);
    }
}
