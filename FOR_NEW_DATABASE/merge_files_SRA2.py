#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 23 14:54:36 2022

@author: marian-linux
"""


import pandas as pd
from bs4 import BeautifulSoup
import argparse
# Parse arguments in from command line
parser = argparse.ArgumentParser()
parser.add_argument('-s','--sra_string')
parser.add_argument('-p',
                    '--phrase',
                    type=str,
                    default='not_chosen')
args = parser.parse_args()

file_1 = args.sra_string + ".xml"
file_2 = args.sra_string + ".csv"
file_3 = args.sra_string + "merge" + ".csv"
# Reading the data inside the xml
# file to a variable under the name
# data
try:
        
    with open(file_1, 'r') as f:
        data = f.read()
    # Passing the stored data inside
    # the beautifulsoup parser, storing
    # the returned object
    Bs_data = BeautifulSoup(data, "xml")
    # Finding all instances of tag
    # Title
    title = Bs_data.find_all('TITLE')
    title2=[]
    for l in title:
        title2.append(l.text)
    #To preserve order
    a=Bs_data.find_all("RUN_SET")
    Run_names = []
    for i in a:
        Run_names.append(i.find("RUN").get("accession"))
    y=int(len(title2)/len(Run_names))
    # LIBRARY_CONSTRUCTION_PROTOCOL
    LIBRARY_CONSTRUCTION_PROTOCOL = Bs_data.find_all('LIBRARY_CONSTRUCTION_PROTOCOL')
    LIBRARY_CONSTRUCTION_PROTOCOL2=[]
    for l in LIBRARY_CONSTRUCTION_PROTOCOL:
        LIBRARY_CONSTRUCTION_PROTOCOL2.append(l.text)
    # Design-description
    DESIGN_DESCRIPTION= Bs_data.find_all('DESIGN_DESCRIPTION')
    DESIGN_DESCRIPTION2=[]
    for l in DESIGN_DESCRIPTION:
       DESIGN_DESCRIPTION2.append(l.text) 
        # STUDY_ABSTRACT
    STUDY_ABSTRACT = Bs_data.find_all('STUDY_ABSTRACT')
    STUDY_ABSTRACT2=[]
    for l in STUDY_ABSTRACT:
       STUDY_ABSTRACT2.append(l.text)
    #To get Pubmed ID
    PMID=Bs_data.find_all("XREF_LINK")
    found_pmid = "N/A"
    for pmid in PMID:
        if "pubmed" == pmid.find("DB").text:
            found_pmid = pmid.find("ID").text
            
    #To get directionality of library
    a=Bs_data.findAll("SPOT_DESCRIPTOR")
    read_run_info=[]
    for i in a:
        read_info = ""
        read_info+="SPOT_LENGTH: "
        read_info+=((i.find("SPOT_LENGTH").text))
        for reads in i:
            read_info+= ", Read_Index:"
            for x in (i.find_all("READ_INDEX")):
                    
                read_info+=(" "+ x.text+" ")
            read_info+= ", Read_TYPE: "
            for x in (i.find_all("READ_TYPE")):  
                read_info+=(" "+ x.text+" ")            
            read_info+= ", BASE_COORD: "
            for x in (i.find_all("BASE_COORD")):  
                read_info+=(" "+ x.text+" ")            
        read_run_info.append(read_info)
    
    
    # making a dataframe
    #title is mentioned twice so take first
    m=0
    if y>1:
        m=1
    natural_scrape=pd.DataFrame(title2[m::y],columns=["SampleDescription"])
    natural_scrape["Initial_desc"]=title2[::y]
    natural_scrape["Run"]=Run_names
    # adding in library construction protocol and abstract - may not be available
    try:
        natural_scrape["LIBRARY_CONSTRUCTION_PROTOCOL"]=LIBRARY_CONSTRUCTION_PROTOCOL2
    except:
        natural_scrape["LIBRARY_CONSTRUCTION_PROTOCOL"]= "N/A"
    try:
        natural_scrape["STUDY_ABSTRACT"]=STUDY_ABSTRACT2
    except:
        natural_scrape["STUDY_ABSTRACT"]= "N/A"
    try:
        natural_scrape["DESIGN_DESCRIPTION"]=DESIGN_DESCRIPTION2
    except:
        natural_scrape["DESIGN_DESCRIPTION"]= "N/A" 
        
    try:
        natural_scrape["READ_RUN_INFO"]=read_run_info
    except:
        natural_scrape["READ_RUN_INFO"]= "N/A"
        
    natural_scrape["Pubmed ID"]= found_pmid
    #merge with data there - some may be now repeated but at least all info there
    run_info=pd.read_csv(file_2)
    result = pd.merge(natural_scrape, run_info, on="Run")
    result1=result
    if args.phrase != 'not_chosen':
        phrase= args.phrase.upper()
        result=result[result["ScientificName"].apply(lambda x: phrase  in x.upper())]
        if len(result)>0:
            result.to_csv(file_3)	
        else:
            print("No " + args.phrase + " in this study")       
except:
    print("problem with: " + args.sra_string)
