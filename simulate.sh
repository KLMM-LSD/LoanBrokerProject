#!/bin/bash

cd "$1/GetCreditScore/"
while True
do
	sleep 5
	#Run GetCreditScore
	python3 getScore.py "$RANDOM" 50000 30
done