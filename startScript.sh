#!/bin/bash     

#Making sure to kill all runnning processes first
./killScript.sh "$1"

# Run RuleBase
cd "$1/RuleBase/target"
java -jar RuleBase-1.0-SNAPSHOT.jar &
printf "$!\n" > "$1/.PIDs.log"

# Run GetBanks
cd "$1/getBanks"
python getBanks.py &
printf "$!\n" >> "$1/.PIDs.log"

# Run Recipient List
cd "$1/RecipientList"
mvn exec:java &
printf "$!\n" >> "$1/.PIDs.log"

# Run XML Translator
cd "$1/DotnetTranslator/"
dotnet run & 
printf "$!\n" >> "$1/.PIDs.log"

# Run JsonTranslator
cd "$1/TranslatorJson"
npm install 
npm start &
printf "$!\n" >> "$1/.PIDs.log"

# Run TranslatorSvedbanken
# Edit config file prior to running?

# Run Normalizer
cd "$1/Normalizer"
python normalizer.py &
printf "$!\n" >> "$1/.PIDs.log"

#Run Aggregator
cd "$1/Aggregator"
python3 aggregator.py &
printf "$!\n" >> "$1/.PIDs.log"

#Run Svedbanken
cd "$1/Svedbanken"
python3 svedbanken.py &
printf "$!\n" >> "$1/.PIDs.log"

