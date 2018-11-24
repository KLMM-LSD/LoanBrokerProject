#!/bin/bash

#Loop over PIDs in file, killing everything
while read -r line
do
	kill -SIGINT "$line"
	sleep 1
	kill "$line"
done < "$1/.PIDs.log"

#Special line for stubborn node
kill -9 $(ps aux | grep '\snode\s' | awk '{print $2}')

#Then empty out the file
echo "" > "$1/.PIDs.log"
