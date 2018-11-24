#!/bin/bash

cd "$1/GetCreditScore/"
while True
do
	sleep 2
	#Run GetCreditScore
	python getScore.py 123456-7899 50000 30
done