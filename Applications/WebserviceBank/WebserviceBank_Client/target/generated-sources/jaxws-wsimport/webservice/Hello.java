
package webservice;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for hello complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="hello">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="ssn" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="creditScore" type="{http://www.w3.org/2001/XMLSchema}int"/>
 *         &lt;element name="loanAmount" type="{http://www.w3.org/2001/XMLSchema}float"/>
 *         &lt;element name="LoanDuration" type="{http://www.w3.org/2001/XMLSchema}int"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "hello", propOrder = {
    "ssn",
    "creditScore",
    "loanAmount",
    "loanDuration"
})
public class Hello {

    protected String ssn;
    protected int creditScore;
    protected float loanAmount;
    @XmlElement(name = "LoanDuration")
    protected int loanDuration;

    /**
     * Gets the value of the ssn property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSsn() {
        return ssn;
    }

    /**
     * Sets the value of the ssn property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSsn(String value) {
        this.ssn = value;
    }

    /**
     * Gets the value of the creditScore property.
     * 
     */
    public int getCreditScore() {
        return creditScore;
    }

    /**
     * Sets the value of the creditScore property.
     * 
     */
    public void setCreditScore(int value) {
        this.creditScore = value;
    }

    /**
     * Gets the value of the loanAmount property.
     * 
     */
    public float getLoanAmount() {
        return loanAmount;
    }

    /**
     * Sets the value of the loanAmount property.
     * 
     */
    public void setLoanAmount(float value) {
        this.loanAmount = value;
    }

    /**
     * Gets the value of the loanDuration property.
     * 
     */
    public int getLoanDuration() {
        return loanDuration;
    }

    /**
     * Sets the value of the loanDuration property.
     * 
     */
    public void setLoanDuration(int value) {
        this.loanDuration = value;
    }

}
