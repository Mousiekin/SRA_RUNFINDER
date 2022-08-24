#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 23 14:54:36 2022

@author: marian-linux
"""

#import libraries
import pandas as pd
# read in downloaded runs file
runs=pd.read_csv("/home/marian-linux/Documents/Project2/checking_pipeline/SraRunTable.txt")
# get unique SRA studies
runs=runs[runs["LibrarySource"]=="TRANSCRIPTOMIC"]
runs=runs.reset_index(drop=True)
runs=list(set(list(runs["SRA Study"])))
# save to a text file in a list
with open("SRA_STUDY.txt", "w") as output:
    for s in runs:
        output.write( s +'\n')
