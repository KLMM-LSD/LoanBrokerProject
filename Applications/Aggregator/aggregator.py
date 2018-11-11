# Author:......KRG
# Description:.Aggregator to receive loan quotes and choose the best one.
from collections import defaultdict
import time, threading, cherrypy, logging

class Aggregator:
    #Collection to keep all social security numbers in
    ssNumbers = defaultdict(list)
    #Time from first learning of an ssn, until a decision is made
    decisionTimeout = 10
    
    @cherrypy.expose
    @cherrypy.tools.json_in()   
    def postQuote(self):
        cherrypy.response.status = 200
        
        try:
            ssn = cherrypy.request.json['ssn']
            bankName = cherrypy.request.json['bankName']
            interestRate = cherrypy.request.json['interestRate']
        except KeyError:
            cherrypy.log(msg="Error: Received malformed JSON", context='', severity=logging.DEBUG, traceback=False)
            cherrypy.response.status = 400
            return
        except AttributeError:
            cherrypy.log(msg="Error: Expected JSON", context='', severity=logging.DEBUG, traceback=False)
            cherrypy.response.status = 400
            return
            
        if len(self.ssNumbers[ssn]) == 0: #If ssn is unknown, schedule a decision for 1 timeout from now
            decisionThread = threading.Thread(target=self.bestLoanDecision, args=(ssn, self.decisionTimeout), daemon=True)
            #This thread terminates on its own, so fire and forget.
            decisionThread.start()
        self.ssNumbers[ssn].append((bankName, interestRate))
        
        print("Received loan quote")
        
        return

    def bestLoanDecision(self, ssn, timeout):
        #First, wait for other responses to come in
        time.sleep(timeout)
        
        #Then figure out where the best deal is at
        bestRate = None
        for tup in self.ssNumbers[ssn]:
            if bestRate == None or bestRate[1] < tup[1]:
                bestRate = tup
        
        #Send bestRate to destination (File for now)
        with open(ssn + ".txt", "w") as loanFile:
            quoteCount = len(self.ssNumbers[ssn])
            loanFile.write("Best rate is " + str(bestRate[1]) + " at " + str(bestRate[0]) + ", from " + str(quoteCount) + " quotes total\n")
            
        #Logging does not seem to work across threads out of the box
        cherrypy.log(msg="Best rate found!  " + str(bestRate), context='', severity=logging.DEBUG, traceback=False)
        
        #Then clear list so that new requests with this ssn will start the decision timer
        self.ssNumbers[ssn].clear()
        return


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8081, 'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(Aggregator(), '/')