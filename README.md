# Group 2. LoanBrokerProject
> We use Github issues and it's project board design to structure our project. You can find our project board here:<br/>
> Link https://github.com/KLMM-LSD/LoanBrokerProject/projects/1
>
> This is our repository for the System Integration Loan broker project in Cphbusiness, PBA in software development.

---

### Authors:
 - Michael Boje Veilis
 - Lasse André Hansen
 - Martin Hansen
 - Kristjan Reinert Gásadal

---

### Table of content
- [Loan Broker Documentation](#Loan-Broker-Documentation)
- TBD
- TBD

---

## 1. Loan Broker Documentation
> See the full description of the Loan Broker project here: https://github.com/KLMM-LSD/LoanBrokerProject/blob/master/docs/Loan%20Broker%20Project.pdf
> 
> The link mostly explains what the Loan Broker is and what has to be done to make it.
> It comes from the book Enterprise Integration Patterns, it takes a loan request, determines the best banks that would grant the user a loan with a corresponding interest rate. The request will go through many independent components to the banks, aswell as the responses from the banks. This is described further below.

#### Run project
To run this project you need some prerequisites. When running it'll start up all the individual components in the correct order.

#### Prerequisites
- Java 8
- Python 3
- C#
- Maven
- TBD

#### Project execution
1. Clone the project
2. ``cd`` into the root directory
3. Run ``TBD``

### Design of the Loan Broker
The loan broker application is designed to integrate multiple smaller components through a mixture of rabbitMQ messaging as well as SOAP webservices. The idea is to have every component loosely coupled together. This way, we can have multiple teams working on different components - without needing a high level of communication, because every message send from one component to another has a clear and predefined format. 

Placeholder below.

![diagram](https://raw.githubusercontent.com/KLMM-LSD/LoanBrokerProject/master/Resources/LoanBrokerDesign.JPG)

### Loan quote process flow
1. Receive the consumer's loan quote request(ssn, loan amount, loan duration)
2. Obtain credit score from credit agency(ssn -> credit score)
3. Determine the most appropriate banks to contact from the Rule Base web service
4. Send a request to each selected bank(ssn, credit score, loan amount, loan duration)
5. Collect response from each selected bank
6. Detemine the best response
7. Pass the result back to the consumer

### Components in the Loan Broker and External components
- Client/Frontend
> something something

- [Get Credit Score](https://github.com/KLMM-LSD/LoanBrokerProject/blob/master/Applications/GetCreditScore/getScore.py)
> Get Credit score related to given Social Security Number

- [Rule Base](https://github.com/KLMM-LSD/LoanBrokerProject/tree/master/Applications/RuleBase)
> Sets the rules for each bank (Least amount of creditscore allowed etc.) 

- [Get Banks](https://github.com/KLMM-LSD/LoanBrokerProject/tree/master/Applications/GetBanks)
> To acquire all relevant banks (according to rulebase)

- [Recipient List](https://github.com/KLMM-LSD/LoanBrokerProject/tree/master/Applications/RecipientList)
> Delegates each request to the correct translator for each bank.

- Translators
> Formats the request to the correct format for each bank and sends the loanRequest, incl. 
[XML-translator](https://github.com/KLMM-LSD/LoanBrokerProject/tree/master/Applications/TranslatorJson), [JSON-translator](https://github.com/KLMM-LSD/LoanBrokerProject/tree/master/Applications/TranslatorJson), [Webservice-translator](TBD) and [RabbitMQ-translator](TBD).

- Banks 
> 2 given banks accessible from http://datdb.cphbusiness.dk:15672 as well as the 2 banks we developed. [Webservice-Bank](https://github.com/KLMM-LSD/LoanBrokerProject/tree/master/Applications/bank_webservice) and [RabbitMQ-bank](https://github.com/KLMM-LSD/LoanBrokerProject/blob/master/Applications/Svedbanken/svedbanken.py).

- [Normalizer](https://github.com/KLMM-LSD/LoanBrokerProject/blob/master/Applications/Normalizer/normalizer.py) 
>  The normalizer makes sure that each message has the same format, a format that the aggregator can read. 

- [Aggregator](https://github.com/KLMM-LSD/LoanBrokerProject/tree/master/Applications/Aggregator)
> The aggregator receives messages from the normalizer, when it has received each message (or after the timeout period), it sends the best quote back to the client, providing the best option for a loan. 

## THIS WILL BE DONE VERY SOON!

## Process flow screen dumps
TBD

## Testing

TBD
