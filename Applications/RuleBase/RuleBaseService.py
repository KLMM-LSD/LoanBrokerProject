import RuleBase
import json
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/GetBankWebServices', methods=['GET'])
def getCreditScore():
    creditScore = int(request.args.get('creditScore'))
    print('\n{RuleBase} -- getCreditsScore');
    print('Received message (credit score): ')
    bankResults = RuleBase.getCreditScoreFromBanks(creditScore)
    return json.dumps(bankResults)

if __name__ == '__main__':
    app.run(debug=True)
