using System;
using System.Collections.Generic;
using System.Text;
using System.Xml.Linq;

namespace DotnetTranslator
{
    class BankTranslator
    { 
        public static XDocument CreateXML(String ssn, String creditScore, String loaningAmount)
    {
        var myDate = DateTime.Today.ToString("yyyy-MM-dd");
        var myTime = DateTime.Now.ToString("HH:mm:ss");

        XDocument doc = new XDocument(new XElement("LoanRequest", new XElement("ssn", ssn),
                                         new XElement("creditScore", creditScore),
                                         new XElement("loanAmount", loaningAmount),
                                         new XElement("loanDuration", myDate + " " + myTime + ".0 CET")));
        return doc;
    }

}
}
