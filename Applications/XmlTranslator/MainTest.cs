using Newtonsoft.Json.Linq;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using static translate.BankTranslator;

namespace BankTranslator
{

    class MainTest
    {


        private static string HOST = "datdb.cphbusiness.dk";
        private static string USERNAME = "guest";
        private static string PASSWORD = "guest";
        private static string[] hej;


        public static void Main()
        {

            ListenForMessages();
        }

        public static void ListenForMessages()
        {
            var factory = new ConnectionFactory() { HostName = HOST, UserName = USERNAME, Password = PASSWORD };
            using (var connection = factory.CreateConnection())
            using (var channel = connection.CreateModel())
            {
                channel.ExchangeDeclare(exchange: "GroupB.translators", type: "direct", durable: true, autoDelete: false, arguments: null);

                var queueName = channel.QueueDeclare().QueueName;
                channel.QueueBind(queue: queueName,
                                  exchange: "GroupB.translators",
                                  routingKey: "xml");

                Console.WriteLine(" [*] Waiting for Message.");

                var consumer = new EventingBasicConsumer(channel);
                consumer.Received += (model, ea) =>
                {
                    Console.WriteLine("message received");
                    var body = ea.Body;
                    var message = Encoding.UTF8.GetString(body);
                    //Check if message is instance of JObject
                    JObject json = JObject.Parse(message);

                    String ssn = json["ssn"].ToString();
                    String creditScore = json["creditScore"].ToString();
                    String loanAmount = json["loanAmount"].ToString();
                    
                    XDocument doc = CreateXML(ssn,creditScore,loanAmount);
                    Debug.WriteLine(doc.ToString());
                    Console.WriteLine("##################################" + doc.ToString());
                    var props = channel.CreateBasicProperties();
                    props.ReplyTo = "GroupB.normalizer.xml";
                    props.CorrelationId = "GroupB.BongoBank";
                    channel.BasicPublish(exchange: "cphbusiness.bankXML",
                                 routingKey: "GroupB_CSharp",
                                 basicProperties: props,
                                 body: Encoding.Default.GetBytes(doc.ToString()));
                };
                    channel.BasicConsume(queue: queueName,
                                         autoAck: true,
                                         consumer: consumer);

                    Console.WriteLine(" Press [enter] to exit.");
                    Console.ReadLine();
                }


        }

        }
    }


