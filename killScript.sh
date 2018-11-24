#!/bin/bash

#Loop over PIDs in file, killing everything
while read -r line
do
	kill -SIGINT "$line"
	sleep 1
	kill "$line"
done < "$1/Applications/.PIDs.log"
