#!/bin/bash     

#Making sure to kill all runnning processes first
./killScript.sh "$1"

# Run RuleBase
#cd "$1/RuleBase/RuleBase"
#mvn spring-boot:run &
#printf "$!\n" >> "$1/.PIDs.log"

# Run GetBanks
cd "$1/GetBanks"
python getBanks.py &
printf "$!\n" >> "$1/.PIDs.log"

# Run Recipient List
cd "$1/RecipientList"
mvn exec:java &
printf "$!\n" >> "$1/.PIDs.log"

# Run XML Translator
cd "$1/DotnetTranslator/bin/Debug/netcoreapp2.1"
dotnet DotnetTranslator.dll &
printf "$!\n" >> "$1/.PIDs.log"

# Run TranslatorSvedbanken
# Edit config file prior to running?

# Run Normalizer
cd "$1/Normalizer"
python normalizer.py &
printf "$!\n" >> "$1/.PIDs.log"

#Run Aggregator
cd "$1/Aggregator"
python aggregator.py &
printf "$!\n" >> "$1/.PIDs.log"

#Run Svedbanken
#cd "$1/Svedbanken"
#python svedbanken.py &
#printf "$!\n" >> "$1/.PIDs.log"

# Run JsonTranslator
cd "$1/TranslatorJson"
npm start &
printf "$!\n" >> "$1/.PIDs.log"

