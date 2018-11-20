module.exports = {
    consumer: {
        type: 'fanout',
        exchange: 'GroupB.translators',
        binding: 'DatBank'
    },
    producer: {
        exchangeType: 'fanout',
        exchange: 'cphbusiness.bankJSON',
        replyTo: 'GroupB.normalizer.json',
        bankID: 'bankJSON',
        type: 'json'
    },
    connection: {
        HOST: 'datdb.cphbusiness.dk',
        PORT: '15672',
        USERNAME: 'guest',
        PASSWORD: 'guest'
    }
}