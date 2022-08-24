#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 23 17:24:59 2022

@author: marian-linux
"""
#import libraries
import pandas as pd
import argparse
# Parse arguments in from command line
parser = argparse.ArgumentParser()
parser.add_argument(
    '-i',
    '--input_file')
args = parser.parse_args()

# read in downloaded runs file
combined=pd.read_csv(args.input_file)
# get rid of firat column - nonsense
combined = combined.drop(columns=combined.columns[0])

#get rid of extra headers
combined=combined[combined["SampleDescription"]!="SampleDescription"]

# columns to drop
to_drop = ['Affection_Status',
 'Analyte_Type',
 'SampleType',
 'Histological_Type',
 'Body_Site',
 'Study_Pubmed_id','g1k_pop_code',
 'source',
 'g1k_analysis_group',
 'Subject_ID',
 'Sex',
 'Disease',
 'Tumor',
 'dbgap_study_accession',
 'Consent',
          'InsertSize',
          'InsertDev'
]

combined = combined.drop(to_drop,axis=1)

# make sure transcriptomic data
combined = combined[combined["LibrarySource"]=="TRANSCRIPTOMIC"]

# reset index
combined = combined.reset_index(drop=True)

# Make a column of combined TAXID and scientific name
combined["name_TaxID"]= combined["TaxID"]+ " " + combined["ScientificName"]

# make a column for Pubmed retrieval
combined["Pubmed_ID_pull"] = combined["Pubmed ID"].apply(lambda x:"https://pubmed.ncbi.nlm.nih.gov/"+ str(x))

# make the index the runs
combined=combined.set_index('Run',drop=False)
combined.index.name="Runs"
combined.to_csv("cleaned_combined.csv")
combined.BioProject.unique().tolist()
bioprojects=combined.BioProject.unique().tolist()
# save to a text file in a list
with open("bioproject.txt", "w") as output:
    for s in bioprojects:
        output.write( s +'\n')
