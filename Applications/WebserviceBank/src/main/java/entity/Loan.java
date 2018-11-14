/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package entity;

/**
 *
 * @author Mart_
 */
public class Loan {

    public String ssn;
    public float loanAmount;
    public int loanDuration;
    public int creditScore;

    public Loan(String ssn, float loanAmount, int loanDuration, int creditScore) {
        this.ssn = ssn;
        this.loanAmount = loanAmount;
        this.loanDuration = loanDuration;
        this.creditScore = creditScore;
    }

    public String getSsn() {
        return ssn;
    }

    public void setSsn(String ssn) {
        this.ssn = ssn;
    }

    public float getLoanAmount() {
        return loanAmount;
    }

    public void setLoanAmount(float loanAmount) {
        this.loanAmount = loanAmount;
    }

    public int getLoanDuration() {
        return loanDuration;
    }

    public void setLoanDuration(int loanDuration) {
        this.loanDuration = loanDuration;
    }

    public int getCreditScore() {
        return creditScore;
    }

    public void setCreditScore(int creditScore) {
        this.creditScore = creditScore;
    }

}
