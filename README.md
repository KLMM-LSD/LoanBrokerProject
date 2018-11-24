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
<!--ts-->
* [Loan Broker Documentation](#Loan-Broker-Documentation)
* [Running the Loan Broker process](#Running-the-Loan-Broker-process)
  * [Prerequisites](#Prerequisites)
  * [Running the application (smart)](#Running-the-application-smart)
  * [Running the application (Manual)](#Running-the-application-Manual)
* [Design of the Loan Broker with seperation between business and messaging logic](#Design-of-the-Loan-Broker-with-seperation-between-business-and-messaging-logic)
  * [Loan quote process flow](#Loan-quote-process-flow)
  * [Process flow screen dumps](#Process-flow-screen-dumps)
  * [Components in the Loan Broker and External components](#Components-in-the-Loan-Broker-and-External-components)
* [Description of the Loan Broker Webservice](#Description-of-the-Loan-Broker-Webservice)
* [Identification of potential bottlenecks](#Identification-of-potential-bottlenecks)
* [Testability](#Testability)
* [Error handling](#Error-handling)
  
<!--ts-->

---

## Loan Broker Documentation
> See the full description of the Loan Broker project here: https://github.com/KLMM-LSD/LoanBrokerProject/blob/master/docs/Loan%20Broker%20Project.pdf
> 
> The link mostly explains what the Loan Broker is and what has to be done to make it.
> It comes from the book Enterprise Integration Patterns, it takes a loan request, determines the best banks that would grant the user a loan with a corresponding interest rate. The request will go through many independent components to the banks, aswell as the responses from the banks. This is described further below.

### Running the Loan Broker process
To run this project you need some prerequisites. When running it'll start up all the individual components in the correct order.

This project at the moment only runs with the jsonBank and the xmlBank. The Rabbimq bank and the web service bank wil be operational very soon as well as a Client.

#### Prerequisites
- Java 8
- Maven
- Python 3
- .Net(C#)
- Node.js


#### Running the application (smart)
 
1. First clone the project.
2. Navigate to the projects root folder.
3. Run these scripts with your path to /applications as an argument, i.e. :  

```From droplet
./startScript.sh $PWD/Applications
```
```For the host-machine
./buildscript.sh $PWD/Applications
./startScriptHost.sh $PWD/Applications
```
**You have to manually start the external components for now but will be changed in to a script later**
```Manual start of external components
Navigate into the Applications/RuleBase/RuleBase folder and run the commands: **mvn clean package** => **mvn spring-boot:run**
Navigate into the Applications/Svedbanken folder and run the command: **python svedbanken.py**
```

#### Running the application (Manual)
1. First clone the project.
2. Go into the Applications folder where you can see all the internal and external components.
3. Go to RuleBase/RuleBase and start this component with these commands: **mvn clean package** and then **mvn spring-boot:run**.
4. Go to the folder svedbanken and start this rabbitmq bank with this command: **python svedbanken.py**
4. Go to GetBanks folder and start this component with this command: **python getBanks.py**.
5. Go to Recipientlist folder and start this component with these commands: **mvn clean package** and then **mvn exec:java**.
6. Go to xmlTranslator folder and start this component with these commands: **dotnet build** => **cd bin/Debug/netcoreapp2.1** => **dotnet DotnetTranslator.dll**.
7. Go to translatorjson folder and start this component with this command: **npm install** => **npm start**.
8. other translators **TBD**
9. Go to Normalizer folder and start this component with this command: **python nomralizer.py**
10. Go to Aggregator folder and start this component with this command: **python aggregator.py**
11. Last go to GetCreditScore folder and try and send a request to see if it goes through everything: **python getScore.py 123456-7899 50000 30**

#### At the moment you send credit score from the the GetCreditScore component and receive the response from the aggregator. This will change when we get a Client up and running. Same with the bank Bankerot and the translators for the rabbitmq bank and webservice bank, only these three components doesn't really work yet atm. but all of them will be up and running soon aswell

---

### Design of the Loan Broker with seperation between business and messaging logic
The loan broker application is designed to integrate multiple smaller components through a mixture of rabbitMQ messaging as well as SOAP webservices. The idea is to have every component loosely coupled together. This way, we can have multiple teams working on different components - without needing a high level of communication, because every message send from one component to another has a clear and predefined format. 

Placeholder below.

![diagram](https://raw.githubusercontent.com/KLMM-LSD/LoanBrokerProject/master/Resources/LoanBrokerDesign.JPG)

#### Loan quote process flow
1. Receive the consumer's loan quote request(ssn, loan amount, loan duration)
2. Obtain credit score from credit agency(ssn -> credit score)
3. Determine the most appropriate banks to contact from the Rule Base web service
4. Send a request to each selected bank(ssn, credit score, loan amount, loan duration)
5. Collect response from each selected bank
6. Detemine the best response
7. Pass the result back to the consumer

#### Process flow screen dumps
TBD

#### Components in the Loan Broker and External components
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

---

### Description of the Loan Broker Webservice

---

### Identification of potential bottlenecks

---

### Testability

---

### Error handling
