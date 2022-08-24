#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 20:30:32 2022

@author: marian-linux
"""

import pandas as pd
import re
import numpy as np

# Extract form Bioproject searches
bigfile_list=[]
with  open('bigfile1') as fp:
    contents = fp.read()
    for entry in contents.split('$'):
        bigfile_list.append(entry)
df=pd.DataFrame(bigfile_list)
df.columns=["temp"]
df[['BioProject','Abstract']] = df['temp'].str.split("@", expand=True)
df=df.iloc[1:,1:]
def findmatches(x):
    match=[]
    match = re.findall(r'PMC\d+', x)
    y=[]
    for mat in match:
        y.append(mat)
    return y
df["PMC_BP"]=df.Abstract.apply(lambda x : findmatches(x))
df=df.iloc[:,[0,2]]
df.BioProject=df.BioProject.str.strip()
combined=pd.read_csv("cleaned_combined.csv", index_col=0)
result = pd.merge(combined, df, on="BioProject")

# Extract from SRA study searches
bigfile_list=[]
with  open('bigfile2') as fp:
    contents = fp.read()
    for entry in contents.split('$'):
        bigfile_list.append(entry)
df=pd.DataFrame(bigfile_list)
df.columns=["temp"]
df[['SRAStudy','Abstract']] = df['temp'].str.split("@", expand=True)
df=df.iloc[1:,1:]
def findmatches(x):
    match=[]
    match = re.findall(r'PMC\d+', x)
    y=[]
    for mat in match:
        y.append(mat)
    return y
df["PMC_SRA"]=df.Abstract.apply(lambda x : findmatches(x))
df=df.iloc[:,[0,2]]
df.SRAStudy=df.SRAStudy.str.strip()
result = pd.merge(result, df, on="SRAStudy")


result["PMC"]=result["PMC_SRA"]+ result["PMC_BP"]
result=result.drop(columns=["PMC_SRA", "PMC_BP"])
string="https://www.ncbi.nlm.nih.gov/pmc/"
result["PMC_address"]=string + result["PMC"].apply(lambda x: np.nan if len(x)<1 else x[0]).str.strip()


# reset index
result=result.set_index('Run',drop=False)
result.index.name="Runs"
# save to csv
result.to_csv("Combined_pmc.csv")