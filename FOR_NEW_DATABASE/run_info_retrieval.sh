#!/bin/bash 
FILE="$1" 
mkdir tempplay
for line in $(cat "$FILE" )
  
do
    echo "$line"
	esearch -db sra -query "$line" | efetch -format runinfo > tempplay/"$line".csv
	esearch -db sra -query "$line" | efetch -format natural > tempplay/"$line".xml
done



