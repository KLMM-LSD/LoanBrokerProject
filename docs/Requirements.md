
# Todo

* Loan Broker Project (Pipe and Filter Architecture on a RabbitMQ Server). 

All elements inside the Loan broker as separate processes. The Loan Broker component itself must be implemented as a service (with messaging components inside) that can be accessed through a simple web site or a test client.

The Loan broker component must contact the banks using a distribution strategy. This means using a rule based recipient list where the broker decides upon which banks to contact based on the credit score for each customer request. It would for instance be a waste of time sending a quote request for a customer with a poor credit rating to a bank specializing in premier customers. You must make up the banking rules yourself. Keep them simple. You need to find a way to include knowledge about the banks into the Rule Base web service. The credit score scale ranges from 0 to 800 (800 being the highest and best score).

### The flow of the project goes as a following. 

1. Receive the consumer's loan quote request (ssn, loan amount, loan duration)
2. Obtain credit score from credit agency (ssn  credit score)
3. Determine the most appropriate banks to contact from the Rule Base web service
4. Send a request to each selected bank (ssn, credit score, loan amount, loan duration)
5. Collect response from each selected bank
6. Determine the best response
7. Pass the result back to the consumer

Each bank has its own format so you must make sure to translate the loan quote request into the proper format for each bank using a Message Translator (as shown in the Loan Broker Design above). Also, a Normalizer must be used to translate the individual bank responses into a common format. An Aggregator will collect all responses from the banks for a specific customer request and determine the best quote. All the parts inside the Loan Broker component are connected through messaging. So you end up with a number of independent programs that need to be started up as individual processes.

### Additionally, following external components has to be implemented:

• Credit Bureau (SOAP web service).
• Two banks (RabbitMQ implementations using XML and JSON respectively).

### XML and JSON format of Loan Requests and Response examples

For xml: 

```
<LoanRequest>
<ssn>12345678</ssn>
<creditScore>685</creditScore>
<loanAmount>1000.0</loanAmount>
<loanDuration>1973-01-01 01:00:00.0 CET</loanDuration>
</LoanRequest>
```

```
<LoanResponse>
<interestRate>4.5600000000000005</interestRate>
<ssn>12345678</ssn>
</LoanResponse>
```

For JSON:
```
{
"ssn":1605789787,
"creditScore":598,
"loanAmount":10.0,
"loanDuration":360
}
```
```
{
"interestRate":5.5,
"ssn":1605789787
}
```
