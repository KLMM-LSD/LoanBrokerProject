using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Channels;
using RabbitMQ;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using translate;
using System.Xml.Linq;
using System.Xml;
using System.Diagnostics;

public class Connection
{
    private static readonly String HOST = "datdb.cphbusiness.dk";
    private static readonly String USERNAME = "guest";
    private static readonly String PASSWORD = "guest";
    private static readonly String TYPE = "direct";
//    Channel channel;

    private Connection connection;
    private String endPointName;
 //  protected String queueName;
 //  protected String queueName;
 //  protected String queueName;

    public Connection()
    {

    }

    public static void Main() {
        Produce();
        Consume();

    }

    public static void Consume()
    {
        var factory = new ConnectionFactory() { HostName = HOST, UserName = USERNAME, Password = PASSWORD };
        using (var connection = factory.CreateConnection())
        using (var channel = connection.CreateModel())
        {
            channel.QueueDeclare(queue: "GroupB_CSharp",
                                 durable: false,
                                 exclusive: false,
                                 autoDelete: false,
                                 arguments: null);
            
            var consumer = new EventingBasicConsumer(channel);
            consumer.Received += (model, ea) =>
            {
                var body = ea.Body;
                var message = Encoding.UTF8.GetString(body);
                Debug.WriteLine(" [x] Received {0}", message);
            };
            channel.BasicConsume(queue: "GroupB_CSharp",
                                 autoAck: true,
                                 consumer: consumer);

            Debug.WriteLine(" Press [enter] to exit.");
            //Console.ReadLine();
        }
    }

    public static void Produce() {

        var factory = new ConnectionFactory() { HostName = HOST, UserName = USERNAME, Password = PASSWORD };
        using (var connection = factory.CreateConnection())
        using (var channel = connection.CreateModel()) {
            channel.QueueDeclare(queue: "GroupB_CSharp",
                                 durable: false,
                                 exclusive: false,
                                 autoDelete: false,
                                 arguments: null);

            XDocument message = translate.BankTranslator.CreateXML("123456-1234","500","200");
            var bytes = Encoding.Default.GetBytes(ToXMLfromLinq(message).OuterXml);

            channel.BasicPublish(exchange: "cphbusiness.bankXML",
                                 routingKey: "GroupB_CSharp",
                                 basicProperties: null,
                                 body: bytes);
            Debug.WriteLine(" [x] Sent {0}", message);
        }

    }

    private static XmlDocument ToXMLfromLinq(XDocument xdoc)
    {
        XmlDocument newXML = new XmlDocument();
        using (var xmlReader = xdoc.CreateReader())
        {
            newXML.Load(xmlReader);
        }
        return newXML;
    }

}

