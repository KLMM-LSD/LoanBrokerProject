using System;
using System.Text;
using System.Xml.Linq;

namespace translate
{
    class BankTranslator
    {
        public static XDocument CreateXML(String ssn, String creditScore, String loaningAmount)
        {

            var dateAndTime = DateTime.Now;
            var date = dateAndTime.Date;

            XDocument doc = new XDocument(new XElement("body",
                                             new XElement("ssn", ssn),
                                             new XElement("creditScore", creditScore),
                                             new XElement("loanings", loaningAmount),
                                             new XElement("loanDuration", date)));
            return doc;
        }
    }
}

