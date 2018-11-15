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

    bankTwo["bankName"] = "BongoBank"
    bankTwo["bankId"] = "bank-BongoBank"
    bankTwo["minCreditScore"] = 250

    bankThree["bankName"] = "DatBank"
    bankThree["bankId"] = "bank-DatBank"
    bankThree["minCreditScore"] = 500

    bankFour["bankName"] = "Svedbanken"
    bankFour["bankId"] = "bank-Svedbanken"
    bankFour["minCreditScore"] = 700

    list.append(bankOne)
    list.append(bankTwo)
    list.append(bankThree)
    list.append(bankFour)

    banks["banks"]= list

    return banks

def getCreditScoreFromBanks(creditScore):
    allBanks = bankCreation().get("banks")
    bankResults = {}
    bankList = []

    for bank in allBanks:
        bankCreditScore = bank["minCreditScore"]
        if bankCreditScore <= creditScore:
            bankList.append(bank)

    bankResults["banks"]= bankList

    return bankResults

def main():
    getCreditScoreFromBanks()

if __name__ == "__main__":
    main()
