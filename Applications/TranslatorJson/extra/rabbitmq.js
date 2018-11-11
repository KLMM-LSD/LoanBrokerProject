export const consumer = {
    type: 'direct',
    exchange: '<enpointname>',
    binding: 'DatBank'
};
export const producer = {
    exchangeType: 'fanout',
    exchange: 'cphbusiness.bankJSON',
    replyTo: '<endpointname>',
    bankID: 'bankJSON',
    type: 'json'
};
export const connection = {
    host: 'datdb.cphbusiness.dk',
    port: '15672',
    username: 'guest',
    password: 'guest'
};