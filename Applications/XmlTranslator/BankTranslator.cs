﻿using System;
using System.Diagnostics;
using System.Xml.Linq;

namespace translate
{
    class BankTranslator
    {
        public static XDocument CreateXML(String ssn, String creditScore, String loaningAmount)
        {
            var dateAndTime = DateTime.Now;
            var date = dateAndTime.Date;

            XDocument doc = new XDocument(new XElement("LoanRequest",  new XElement("ssn", ssn),
                                             new XElement("creditScore", creditScore),
                                             new XElement("loanAmount", loaningAmount),
                                             new XElement("loanDuration", date)));
            Debug.WriteLine(doc);
            return doc;
        }

    }
}
