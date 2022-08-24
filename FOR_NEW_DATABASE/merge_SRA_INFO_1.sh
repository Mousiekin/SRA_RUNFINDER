#!/bin/bash 
FILE="$1" 
PHRASE="$2"
for line in $(cat "$FILE" )    
do
    echo "$line"
	python merge_files_SRA2.py -s tempplay/"$line" -p "$PHRASE"
done
cat tempplay/*merge.csv > combined.csv
rm -r tempplay
python cleaning_combined_1.py -i combined.csv
