#!/bin/bash     

#Making sure to kill all runnning processes first
./killScript.sh "$1"

# Run GetBanks
cd "$1/GetBanks"
python3 getBanks.py &
printf "$!\n" >> "$1/.PIDs.log"

# Run Recipient List
cd "$1/RecipientList"
mvn exec:java &
printf "$!\n" >> "$1/.PIDs.log"

# Run XML Translator
cd "$1/DotnetTranslator/"
dotnet build
cd bin/Debug/netcoreapp2.1
dotnet DotnetTranslator.dll &
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
python3 normalizer.py &
printf "$!\n" >> "$1/.PIDs.log"

#Run Aggregator
cd "$1/Aggregator"
python3 aggregator.py &
printf "$!\n" >> "$1/.PIDs.log"


