def bankCreation():
    banks = {}
    list = []

    bankOne = {}
    bankTwo = {}
    bankThree = {}
    bankFour = {}

    bankOne["bankName"]= "Bankerot"
    bankOne["bankId"]= "bank-Bankerot"
    bankOne["minCreditScore"]= 0
    bankOne["requestWaitTime"]=  30

    bankTwo["bankName"] = "BongoBank"
    bankTwo["bankId"] = "bank-BongoBank"
    bankTwo["minCreditScore"] = 250
    bankTwo["requestWaitTime"] = 45

    bankThree["bankName"] = "DatBank"
    bankThree["bankId"] = "bank-DatBank"
    bankThree["minCreditScore"] = 500
    bankThree["requestWaitTime"] = 50

    bankFour["bankName"] = "Svedbanken"
    bankFour["bankId"] = "bank-Svedbanken"
    bankFour["minCreditScore"] = 700
    bankFour["requestWaitTime"] = 120

    list.append(bankOne)
    list.append(bankTwo)
    list.append(bankThree)
    list.append(bankFour)

    banks["banks"]= list

    return banks

def getCreditScoreFromBanks(creditScore):
    allBanks = bankCreation()["banks"]
    bankResults = {}
    bankList = []

    for bank in allBanks:
        bankCreditScore = bank["minCreditScore"]
        if bankCreditScore <= creditScore:
            bankList.append(bank)

    bankResults["banks"]= bankList

    return bankResults

#def main():
    #creditScoreOne = 100;
    #creditScoreTwo = 270;
    #creditScoreThree = 400;
    #creditScoreFour = 795;

    #print(getCreditScoreFromBanks(creditScoreTwo))

#    return getCreditScoreFromBanks(100)

#if __name__ == "__main__":
#    main()
