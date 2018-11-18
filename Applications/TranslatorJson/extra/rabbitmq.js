module.exports = {
    consumer: {
        type: 'direct',
        exchange: '<enpointname>',
        binding: 'DatBank'
    },
    producer: {
        exchangeType: 'fanout',
        exchange: 'cphbusiness.bankJSON',
        replyTo: '<endpointname>',
        bankID: 'bankJSON',
        type: 'json'
    },
    connection: {
        host: 'datdb.cphbusiness.dk',
        port: '15672',
        username: 'guest',
        password: 'guest'
    }
}