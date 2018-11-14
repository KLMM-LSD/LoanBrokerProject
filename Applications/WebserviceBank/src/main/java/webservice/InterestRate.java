/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package webservice;

import org.json.JSONObject;

/**
 *
 * @author Mart_
 */
class InterestRate {

    private static float maxRate = 15.0f;
    private static float minRate = 2.0f;
    private static int maxCreditScore = 800;

    public InterestRate() {
    }

    // Higher CreditScore Equals a better rate
    public static float calculateInterestRate(int actualCredit) {
        
        return maxRate - (maxRate * (maxCreditScore - actualCredit) / maxCreditScore);
        //return interest;
    }

    public static JSONObject getInterestRate(String ssn, int creditScore) {
        float interestRate = calculateInterestRate(creditScore);
        JSONObject response = new JSONObject();
        response.put("interestRate", interestRate);
        response.put("ssn", ssn);
        System.out.println("{LoanCalculator} - " + response);
        return response;
    }
    public static void main(String[] args) {
        System.out.println("hej hej: " + getInterestRate("232323-2323", 400));
    }

}
