#!/bin/bash

#Build RecipientList
cd "$1/RecipientList"
mvn clean package &

#Install node-packages for TranslatorJson 
cd "$1/TranslatorJson"
npm install &

#Build DotnetTranslator
cd "$1/DotnetTranslator/"
dotnet build