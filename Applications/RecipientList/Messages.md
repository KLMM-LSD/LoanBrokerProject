## Recipient list messages
### Reply from GetBankWebServices(creditScore):
#### Body:
```
{
"banks": [
        {"bankName": "Bankerot", "bankId": "bank-Bankerot", "minCreditScore": 0, "requestWaitTime": 30},
        {"bankName": "BongoBank", "bankId": "bank-BongoBank", "minCreditScore": 250, "requestWaitTime": 45},
        {"bankName": "DatBank", "bankId": "bank-DatBank", "minCreditScore": 500, "requestWaitTime": 50}
        ]
}
```
### Message to translators:
#### Properties:
`correlation_id={bankId}`
#### Body:
```
{
"ssn":"230800-0336",
"creditScore":598,
"loanAmount":10.0,
"loanDuration":360
}
```

### Message to Aggregator:
#### Properties:
```
{
"ssn":"230800-0336",
"creditScore":598,
"loanAmount":10.0,
"loanDuration":360
"banks": [
        {"bankName": "Bankerot", "bankId": "bank-Bankerot", "minCreditScore": 0, "requestWaitTime": 30},
        {"bankName": "BongoBank", "bankId": "bank-BongoBank", "minCreditScore": 250, "requestWaitTime": 45},
        {"bankName": "DatBank", "bankId": "bank-DatBank", "minCreditScore": 500, "requestWaitTime": 50}
        ]
}
```
