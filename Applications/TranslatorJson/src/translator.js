module.exports.getFormattedJson = function(jsonObject) {
    let ssn = parseInt(jsonObject.ssn) || '';
    let creditScore = jsonObject.creditScore || '';
    let loanAmount = jsonObject.loanAmount || '';
    let loanDuration = jsonObject.loanDuration || 365;

    let formattedJson = {
        loanDuration,
        creditScore,
        loanAmount,
        ssn
    };

    return formattedJson;
}