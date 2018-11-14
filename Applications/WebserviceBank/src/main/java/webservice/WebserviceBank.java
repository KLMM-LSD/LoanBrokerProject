/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package webservice;

import javax.jws.WebService;
import javax.jws.WebMethod;
import javax.jws.WebParam;
import javax.ejb.Stateless;
import org.apache.commons.lang.SerializationUtils;
import org.json.JSONObject;

/**
 *
 * @author Mart_
 */
@WebService(serviceName = "WebserviceBank")
@Stateless()
public class WebserviceBank {

    /**
     * This is a sample web service operation
     */
    @WebMethod(operationName = "hello")
    public byte[] loanRequest(@WebParam(name = "ssn") String ssn, @WebParam(name = "creditScore") int creditScore, @WebParam(name = "loanAmount") float loanAmount, @WebParam(name = "LoanDuration") int LoanDuration) {
        InterestRate rateCalc = new InterestRate();
        JSONObject bankResults = rateCalc.getInterestRate(ssn, creditScore);
        return SerializationUtils.serialize(bankResults.toString());
    }
}
