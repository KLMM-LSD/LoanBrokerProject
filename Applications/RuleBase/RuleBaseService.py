import RuleBase
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/GetBankWebServices', methods=['GET'])
def getCreditScore():
    creditScore = request.args.get('creditScore')
    print('\n{RuleBase} -- getCredistScore');
    print('Received message (credit score): ')
    bankResults = RuleBase.getCreditScoreFromBanks(100)
    return bankResults

if __name__ == '__main__':
    app.run(debug=True)