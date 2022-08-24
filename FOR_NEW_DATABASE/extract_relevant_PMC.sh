#!/bin/bash
mkdir tempplay1
mkdir tempplay2
FILE1="$1" 
FILE2="$2"
for line in $(cat "$FILE1" )    
do
    echo "$line"
	esearch -db pmc -query "$line" | efetch -format runinfo > tempplay1/"$line".txt

done
cd tempplay1
for i in *.txt; do echo $ ${i%.*} @ ;echo;cat "$i"; done > bigfile1
mv bigfile1 ..
cd ..
rm -r tempplay1

for line in $(cat "$FILE2" )    
do
    echo "$line"
	esearch -db pmc -query "$line" | efetch -format runinfo > tempplay2/"$line".txt
done
cd tempplay2

for i in *.txt; do echo $ ${i%.*} @ ;echo;cat "$i"; done > bigfile2
mv bigfile2 ..
cd ..
rm -r tempplay2


