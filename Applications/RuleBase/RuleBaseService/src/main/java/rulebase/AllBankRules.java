/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package rulebase;

import java.util.ArrayList;
import java.util.HashMap;

/**
 *
 * @author Micha
 */
public class AllBankRules {
    public HashMap<String, ArrayList> createBanks () {
        HashMap banks = new HashMap<String, ArrayList>();

        ArrayList list = new ArrayList();
        HashMap bankOne = new HashMap();
        bankOne.put("bankName", "Bankerot");
        bankOne.put("bankId", "bank-Bankerot");
        bankOne.put("minCreditScore", 0);
        
        HashMap bankTwo = new HashMap();
        bankTwo.put("bankName", "BongoBank");
        bankTwo.put("bankId", "bank-Bongobank");
        bankTwo.put("minCreditScore", 250);
        
        HashMap bankThree = new HashMap();
        bankThree.put("bankName", "DatBank");
        bankThree.put("bankId", "bank-DatBank");
        bankThree.put("minCreditScore", 500);
        
        HashMap bankFour = new HashMap();
        bankFour.put("bankName", "Svedbanken");
        bankFour.put("bankId", "bank-Svedbanken");
        bankFour.put("minCreditScore", 700);
        
        list.add(bankOne);
        list.add(bankTwo);
        list.add(bankThree);
        list.add(bankFour);
        
        banks.put("banks", list);
        
        return banks;
    }
    
    public HashMap getCreditScoreFromBanks (int creditScore) {
        ArrayList<HashMap> allBankRules = createBanks().get("banks");
        
        HashMap bankResults = new HashMap<String, ArrayList>();
        ArrayList<HashMap> bankList = new ArrayList();
        
        for(HashMap bank: allBankRules) {
            int bankCreditScore = (Integer)bank.get("minCreditScore");
            if (bankCreditScore <= creditScore) {
                bankList.add(bank);
            }
        }
        
        bankResults.put("banks", bankList);
        
        return bankResults;
    }
    
    public static void main(String[] args) {
        AllBankRules app = new AllBankRules();

//        app.getCreditScoreFromBanks(100);
        System.out.println(app.getCreditScoreFromBanks(100));
    }
    
}
