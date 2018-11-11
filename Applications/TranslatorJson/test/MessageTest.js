module.exports = getMessageTest();

function getMessageTest() {
    let ssn = '080594-4545';
    let creditScore = '230';
    let loanAmount = '500.0';
    let date = new Date();
    let loanDuration = date;

    let message = JSON.stringify({
        ssn: ssn,
        creditScore,
        creditScore,
        loanAmount: loanAmount,
        loanDuration: loanDuration
    });
    return message;
}