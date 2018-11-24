#!/bin/bash     
 
  # Run RuleBase
cd "$1/RuleBase"
java -jar RuleBase-1.0-SNAPSHOT.jar &

# Run Recipient List
cd "$1/RecipientList"
mvn exec:java &

# Run XML Translator
cd "$1/DotnetTranslator/"
dotnet run & 

# Run Svedbank Translator

# Run JsonTranslator
cd "$1/TranslatorJson"
npm install 
npm start &

# Run Normalizer
cd "$1/Normalizer"
python normalizer.py &

#Run Aggregator
cd "$1/Aggregator/run"
sh runScript.sh &

#Run GetCreditScore
cd "$1/GetCreditScore/"
python getScore.py 123456-7899 50000 30 &

