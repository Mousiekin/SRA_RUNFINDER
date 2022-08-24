#!/bin/bash

esearch -db SRA -query \"$1\" | efetch -format runinfo > SraRunTable.txt 
