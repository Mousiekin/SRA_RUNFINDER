#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 19 20:49:47 2022

@author: marian-linux
"""
# required libraries
import webbrowser
from tkinter import *
from tkinter import ttk
import pandas as pd
from tkinter.scrolledtext import ScrolledText
from bs4 import BeautifulSoup
import tkinter.font as tkFont
import os
import sys

# global variables and initial states
global count
global combined
global lb
global save_list
save_list=[]
count=0
current_project =""
phrase=""
phrase2 =""


#set up tkinter main page as win
win=Tk()
win.title('SRA_RUNFINDER')
win.geometry("1370x860+10+10")

# functions

# restart: resets all 
def restart():
    #This line will unconditionally restart the running program from scratch:
    os.execl(sys.executable, sys.executable, *sys.argv)

# selected_item: Gets strain and library type and populates the BioProject listbox    
def selected_item():
    global selected_strains
    selected_strains=[]
    global selected_library
    selected_library=[]
    for i in lb.curselection():
        selected_strains.append(lb.get(i))
    print(selected_strains)
    if (pairedv.get())==1:
       selected_library.append("PAIRED")
    if (singlev.get())==1:
       selected_library.append("SINGLE")
    print(selected_library)  
    combined2 = combined[(combined.ScientificName.isin(selected_strains))&(combined.LibraryLayout.isin(selected_library))]
    number_runs= len(combined2)
    number_projects = len(combined2.BioProject.unique())
    display_text = "BioProjects = "+ str(number_projects) + "\n"+"Runs = "+ str(number_runs)
    label_bs.config(text= display_text )
    print(display_text )
    cb_choi.delete(0, END)   
    choices=list(set(combined2.BioProject))
    for thing in choices:
    	cb_choi.insert(END, thing)

# webbrowser_get: populates the BioProject info page
# Strips xml extras from text
# Works out if there is a Pubmed id in which case it activates the Pubmed button
def webbrowser_get():
    ab=cb_choi.get(ANCHOR)
    pubmed_ID = list(set(combined["Pubmed ID"][combined.BioProject==ab]))[0]
    print(pubmed_ID)
    if pd.isna(pubmed_ID):
        pubmed_ID2 = list(set(combined["PMC_address"][combined.BioProject==ab]))[0]
        if pd.isna(pubmed_ID2):
            button1_bs['state'] = DISABLED
        else:
            button1_bs['state'] = NORMAL
    else:
        pubmed_www = list(set(combined["Pubmed_ID_pull"][combined.BioProject==ab]))[0]
        print(pubmed_www)
        button1_bs['state'] = NORMAL
    retrieve1= list(set(combined["STUDY_ABSTRACT"][combined.BioProject==ab]))[0]
    retrieve2= list(set(combined["DESIGN_DESCRIPTION"][combined.BioProject==ab]))[0]
    retrieve3= list(set(combined["LIBRARY_CONSTRUCTION_PROTOCOL"][combined.BioProject==ab]))[0]
    st.delete('0.0', END)
    my_lst_str = ''.join(map(lambda x: ' '+ str(x), selected_strains))
    phrase="Selected strains: " + my_lst_str +"\n"
    st.insert(INSERT,phrase)
    my_lst_str = ''.join(map(lambda x: ' '+ str(x), selected_library))
    phrase="Selected Library Type: " + my_lst_str +"\n"
    st.insert(INSERT,phrase)
    phrase= "STUDY ABSTRACT\n"
    st.insert(INSERT,phrase)
    try:
        phrase= BeautifulSoup(retrieve1, "lxml").text
        st.insert(INSERT,phrase)
    except:
        phrase="N/A"
    phrase= "\nDESIGN DESCRIPTION\n"
    st.insert(INSERT,phrase)
    try:
        phrase= BeautifulSoup(retrieve2, "lxml").text
    except:
        phrase="N/A"
    st.insert(INSERT,phrase)
    phrase= "\nLIBRARY_CONSTRUCTION_PROTOCOL\n"
    st.insert(INSERT,phrase)
    try:
        phrase= BeautifulSoup(retrieve3, "lxml").text
    except:
        phrase="N/A"
    st.insert(INSERT,phrase)
    BioProject=[]
    BioProject= combined[combined.BioProject==ab]
    BioProject=(BioProject.index.tolist())
    run_lb.delete(0, END)
    for thing in BioProject:
    	run_lb.insert(END, thing)
    global current_project
    current_project=ab


# pubmed_retrieve: opens pubmed abstracts
def pubmed_retrieve():
    button1_bs['state'] = DISABLED
    ab=cb_choi.get(ANCHOR)
    pubmed_ID = list(set(combined["Pubmed ID"][combined.BioProject==ab]))[0]
    if pd.isna(pubmed_ID):
        pubmed_www = list(set(combined["PMC_address"][combined.BioProject==ab]))[0]
        webbrowser.open(pubmed_www)
    else:
        pubmed2_www = list(set(combined["Pubmed_ID_pull"][combined.BioProject==ab]))[0]

        webbrowser.open(pubmed2_www)

   
     
# run_details: populates the Run Info Box with run details        
def run_details():
    run_infolb.delete('0.0', END)
    run_name=str(run_lb.get(ANCHOR))  
    run_infolb.insert(INSERT,"BioProject: \n")
    retrieve5= combined.loc[run_name,'BioProject']
    run_infolb.insert(INSERT,retrieve5)
    run_infolb.insert(INSERT,"\nRun: \n")
    retrieve5= combined.loc[run_name,'Run']
    run_infolb.insert(INSERT,retrieve5)
    run_infolb.insert(INSERT,"\nSampleDescription: \n")
    retrieve5= combined.loc[run_name,'BioProject']
    run_infolb.insert(INSERT,retrieve5)
    run_infolb.insert(INSERT,"\nInitial Description: \n")
    retrieve5= combined.loc[run_name,'Initial_desc']
    run_infolb.insert(INSERT,retrieve5)
    run_infolb.insert(INSERT,"\nPlatform: \n")
    retrieve5= combined.loc[run_name,'Platform']
    run_infolb.insert(INSERT,retrieve5)
    run_infolb.insert(INSERT,"\nModel: \n")
    retrieve5= combined.loc[run_name,'Model']
    run_infolb.insert(INSERT,retrieve5)
    run_infolb.insert(INSERT,"\nCenterName: \n")
    retrieve5= combined.loc[run_name,'CenterName']
    run_infolb.insert(INSERT,retrieve5)
    run_infolb.insert(INSERT,"\nSample: \n")
    retrieve5= combined.loc[run_name,'Sample']
    run_infolb.insert(INSERT,retrieve5)
    run_infolb.insert(INSERT,"\nBioSample: \n")
    retrieve5= combined.loc[run_name,'BioSample']
    run_infolb.insert(INSERT,retrieve5)
    run_infolb.insert(INSERT,"\nSampleName: \n")
    retrieve5= combined.loc[run_name,'SampleName']
    run_infolb.insert(INSERT,retrieve5)
    run_infolb.insert(INSERT,"\nREAD RUN INFO: \n")
    retrieve5= combined.loc[run_name,'READ_RUN_INFO']
    run_infolb.insert(INSERT,retrieve5)
    


# SRA_details: opens up the run info on SRA website   
def SRA_details():
     ab=run_lb.get(ANCHOR)
     if len(ab)>0:
         ab=str(combined.loc[ab,"BioSample"])
         SRA_www = "https://www.ncbi.nlm.nih.gov/sra/?term="+ab
         webbrowser.open(SRA_www)
         
#  keep_run: puts selected run in export box for potential saving and removes it from the list of runs      
def keep_run():
    ab=run_lb.get(ANCHOR)
    try:
        idx = save_lb.get(0, END).index(ab)
    except:
        save_lb.insert(END, ab)
    idx = run_lb.get(0, END).index(ab)
    run_lb.delete(idx)
    global save_list
    save_list.append(ab)

# remove_run: deletes run from the list of runs
def remove_run():
    ab=run_lb.get(ANCHOR)
    idx = run_lb.get(0, END).index(ab)
    run_lb.delete(idx)
    
# refresh_run: restores all the run list to as it was before
def refresh_run():
     BioProject=[]
     BioProject= combined[combined.BioProject== current_project]
     BioProject=(BioProject.index.tolist())
     run_lb.delete(0, END)
     for thing in BioProject:
     	run_lb.insert(END, thing)
         
# remove_keeps: clears runs to export
def remove_keeps():
    save_lb.delete(0, END)
    global save_list
    save_list=[]

#enter_csv: lets you enter a presorted list so you can recheck, or used original dataframe as default    
def enter_csv():
   global combined
   try:
       combined= pd.read_csv(entry1.get(),index_col=0)
       ScientificNames = list(set(list(combined.ScientificName)))
       LibraryLayout = list(set(list(combined.LibraryLayout)))
       
       x=ScientificNames 
       for thing in ScientificNames:
       	lb.insert(END, thing)
   except:
       combined = pd.read_csv("Combined_pmc.csv",index_col=0)
       ScientificNames = list(set(list(combined.ScientificName)))
       LibraryLayout = list(set(list(combined.LibraryLayout)))
      
       x=ScientificNames 
       for thing in ScientificNames:
       	lb.insert(END, thing)
      
# add_runs: adds runs from "runs to export" to a csv file named by user. 
#This can be used repeatedly, duplicates do not matter.        
def add_runs():
    global count
    save_info_file= entry2.get()
    if len(save_info_file)>0:
        save_info_file=save_info_file.strip()
        if len(save_list)>0:
            if count==0:
                df=combined.loc[save_list,]
                df.to_csv(save_info_file, mode='a')
            else:
                df=combined.loc[save_list,]
                df.to_csv(save_info_file, mode='a', header=None)
            count+=1
        save_lb.delete(0, END)
        
# export_csv: deduplicates the saved runs and saved as user defined
def export_csv():
    save_info_file= entry2.get()
    if len(save_info_file)>0:
        save_info_file=save_info_file.strip()
        df=pd.read_csv(save_info_file,index_col=0)         
        df=df.drop_duplicates(keep=False)
        df.to_csv(save_info_file)
        
# search_project_ID: searches dataframe for used entered BioProject ID           
def search_project_ID():
    global combined
    projectx=entry3.get()
    if len(projectx)>0:
        projectx2=projectx.strip()
        current_project=projectx2.upper()
        temp_project=combined[combined.BioProject== current_project]
        if len(temp_project)>0:
            cb_choi.delete(0, END)   
            cb_choi.insert(END, current_project)
        else:
            st.delete('0.0', END)
            phrase="Not Found: " + entry3.get()
            st.insert(INSERT,phrase)
            
# search_run_ID: searches dataframe for used entered run ID           
def search_run_ID():
    global combined
    runx=entry4.get()
    
    if len(runx)>0:
        print(runx)
        runx2=runx.strip()
        current_run=runx2.upper()
        temp_run=combined.BioProject.loc[current_run]
        if len(temp_run)>0:
            run_lb.delete(0, END)
            run_lb.insert(END, current_run)
        else:
            run_infolb.delete('0.0', END)
            phrase="Not Found: " + entry4.get()
            run_infolb.insert(INSERT,phrase)
            
    
# Many fonts do not work well on Linux, found "fangsong ti" in tkFont okay
fontExample = tkFont.Font(family='fangsong ti',size=20,weight="bold")
fontExample1 = tkFont.Font(family='fangsong ti',size=16,weight="bold")
fontExample2 = ("Courier", 16)


#frames - organised on page
frame1 = Frame(win)
frame1.grid(row=1,column=0, ipadx=5, ipady=5,sticky="nsew")

frame1a = Frame(frame1,highlightbackground="blue", highlightthickness=2)
frame1a.grid(row=2,column=0, ipadx=5, ipady=5,padx=5,sticky="nsew")
 
frame2 = Frame(frame1,highlightbackground="green", highlightthickness=2)
frame2.grid(row=2,column=1, ipadx=5, ipady=5,padx=5, sticky="nsew") 
  
frame3 = Frame(win)
frame3.grid(row=2,column=0, columnspan=2, ipadx=5, ipady=5,sticky="nsew")

frame0 = Frame(win)
frame0.grid(row=0,column=0, columnspan=6,ipadx=5, ipady=5,sticky="nsew")
      
frame4=Frame(win,highlightbackground="red", highlightthickness=2)
frame4.grid(row=1,column=3, columnspan=1, ipadx=5, sticky="nsew") 

frame4a= Frame(frame4)
frame4a.grid(row=1,column=0, columnspan=1, ipadx=5, ipady=5,sticky="sw") 

frame4b= Frame(frame4)
frame4b.grid(row=1,column=1, columnspan=2, ipadx=5, ipady=5,sticky="sw") 



frame5 = Frame(win)
frame5.grid(row=2,column=3, columnspan=2, ipadx=5, ipady=5,sticky="nsew")        

#Frame0 Start menu and save menu

# Entrybox for own csv to check
entry1 = Entry(frame0,width=60)
entry1.grid(column=1,row=1,ipadx=5, ipady=5,padx=5)
lbl_entry1=Label(frame0, text='Enter own.csv dataframe (optional)')
lbl_entry1.config(font=fontExample2) 
lbl_entry1.grid(column=1, row=0)

button_Entry = Button(frame0,text='START', command=enter_csv, state=NORMAL)
button_Entry.config(background="black", foreground="white", font=fontExample2)
button_Entry.grid(column=2,row=0, ipadx=5, ipady=5,padx=2,pady=2)

# Restart Button to clear all
button_Restart = Button(frame0,text='RESTART', command=restart)
button_Restart.config(background="black", foreground="white", font=fontExample2)
button_Restart.grid(column=0,row=0, ipadx=5, ipady=5,padx=2,pady=2)

# Deduplicate saved runs
button_export= Button(frame0,text='EXPORT RUNS', command=export_csv, state=NORMAL)
button_export.config(background="black", foreground="white", font=fontExample2)
button_export.grid(column=6,row=0, ipadx=5, ipady=5,padx=2,pady=2)

entry2 = Entry(frame0,width=60) 
entry2.grid(column=5,row=1,ipadx=5, ipady=5,padx=2)

lbl_entry2=Label(frame0, text='filename for saving (mandatory)')
lbl_entry2.config(font=fontExample2) 
lbl_entry2.grid(column=5, row=0)  


# frame1 - Screening for strains and library type

# Listbox strain library choices
lb = Listbox(frame1a, selectmode='multiple', state= NORMAL)
lb.config(bd=3,background="skyblue1", foreground="black", font=fontExample2, width=30, height=8)
lb.grid(column=0, row=1, columnspan=3,padx=10,sticky="nsew")

# Button to register choices
btn = Button(frame1a, relief=RAISED, text='DONE', command=selected_item)
btn.config(background="blue", foreground="white",font=fontExample2)
btn.grid(column=0, row=3, ipadx=5, ipady=5, sticky="s")

# Printing number of BioProjects selected
global label_bs
label_bs = Label(frame1a, text='BioProjects = * \n Runs = * ')
label_bs.config(font=fontExample2)
label_bs.grid(column=1, row=3, columnspan=2,ipadx=10, ipady=10, padx=10,sticky="nsew")

# Title for listbox
lbl_choi=Label(frame1a, text='Strains')
lbl_choi.config(background="blue", foreground="white", font=fontExample)
lbl_choi.grid(column=0, row=0, columnspan=3,ipadx=10, ipady=10, padx=10,pady=10,sticky="nsew")

#choosing library type
pairedv=IntVar()
singlev=IntVar()
paired = Checkbutton(frame1a, text = "Paired", variable=pairedv)
paired.config(font=fontExample2)
single= Checkbutton(frame1a, text = "Single", variable=singlev)
single.config(font=fontExample2)
paired.grid(column=0, row=2, ipadx=10, ipady=6,padx=6)
single.grid(column=1, row=2, ipadx=10, ipady=6,padx=6)


# Frame2  Exploring Bioprojects

# BioProject listbox, Label for listbox
lbl_choi2=Label(frame2, text='BioProjects')
lbl_choi2.config(background="green", foreground="white", font=fontExample)
lbl_choi2.grid(column=0, row=0, columnspan=2, ipadx=10, ipady=10,padx=10,pady=10, sticky="nsew")

# listbox projects
cb_choi = Listbox(frame2,width=30, height=8)
cb_choi.config(bd=3, background="DarkSeaGreen1", foreground="black",font=fontExample2)
cb_choi.grid(column=0, row=1, columnspan=2, padx=10,sticky="nsew")

# explore label
button2_choi= Button(frame2, relief=RAISED,text="EXPLORE", command=webbrowser_get)
button2_choi.config(background="green", foreground="white", font=fontExample2)
button2_choi.grid(column=0, row=2, ipadx=4, ipady=4,pady=2)

# Pubmed access button
button1_bs= Button(frame2, text="PUBMED", command=pubmed_retrieve, state=DISABLED)
button1_bs.config(background="DarkSeaGreen1", font=fontExample2)
button1_bs.grid(column=1,row=2,ipadx=4, ipady=4,pady=2)

# search project
entry3 = Entry(frame2,width=25) 
entry3.grid(column=0,row=3,ipadx=5, ipady=5,padx=2,sticky="nsew")
button_entry3= Button(frame2, relief=RAISED,text="Search BP_ID", command=search_project_ID)
button_entry3.config(background="DarkSeaGreen1", foreground="black", font=fontExample2)
button_entry3.grid(column=0, row=4, ipadx=4, ipady=4,pady=2,sticky="nsew")


#frame3 BioProject info page
# Scrolled text for project info
st = ScrolledText(frame3, width=65,  height=10, wrap='word',  font=fontExample1)
st.config(spacing3=10,background='DarkSeaGreen1', foreground="black")
st.grid(row=2,column=0,ipadx=10, ipady=10,padx=10, sticky="nsew")
st.insert(INSERT,phrase)

# Scrollbox label
Proj_info=Label(frame3, text='BioProject Info')
Proj_info.config(background="green", foreground="white", font=fontExample)
Proj_info.grid(column=0, row=0, ipadx=10, ipady=10,padx=10, sticky="nsew")


#Frame4 - analysing and viewing run information

# label for frame
run_infolbl2=Label(frame4, text='Runs')
run_infolbl2.config(background="red", foreground="white", font=fontExample)
run_infolbl2.grid(column=0, row=0, columnspan=4,ipadx=10, ipady=10, padx=10,pady=10,sticky="nsew")

# Frame4a Control buttons
# Get Run Info
button_run_info= Button(frame4a, text="  RUN INFO  ", command=run_details)
button_run_info.config(background="pink", foreground="black", font=fontExample2)
button_run_info.grid(column=0, row=0, ipadx=4, ipady=4,padx=10,pady=2,sticky="nw")

# Get run info from SRA
button_run_info2= Button(frame4a, text="  SRA LINK  ", command=SRA_details)
button_run_info2.config(background="pink", foreground="black", font=fontExample2)
button_run_info2.grid(column=0, row=1, ipadx=4, ipady=4,padx=10,pady=2,sticky="nw")

# put run in 'RUNS TO EXPORT' and remove from Run listbox
button_run_keep= Button(frame4a, text="  KEEP RUN  ", command=keep_run)
button_run_keep.config(background="pink", foreground="black", font=fontExample2)
button_run_keep.grid(column=0, row=2, ipadx=4, ipady=4,padx=10,pady=2,sticky="nw")

# Remove from run list box
button_run_remove= Button(frame4a, text=" REMOVE RUN ", command=remove_run)
button_run_remove.config(background="pink", foreground="black", font=fontExample2)
button_run_remove.grid(column=0, row=3, ipadx=4, ipady=4,padx=10,pady=2,sticky="nw")

# Refresh runs so all cleared runs are returned
button_run_remove= Button(frame4a, text="REFRESH RUNS", command=refresh_run)
button_run_remove.config(background="pink", foreground="black", font=fontExample2)
button_run_remove.grid(column=0, row=4, ipadx=4, ipady=4,padx=10,pady=2,sticky="nsew")

# Clear the "RUNS TO EXPORT" list box
button_clear= Button(frame4a, text="CLEAR KEEPS", command=remove_keeps, state=NORMAL)
button_clear.config(background="pink", foreground="black", font=fontExample2)
button_clear.grid(column=0,row=5,ipadx=4, ipady=4,padx=10,pady=2,sticky="nsew")


# Frame4b Run list boxes, run search tool and run add to csv

# runs in project meeting criteria
run_lb = Listbox(frame4b,height=8, state= NORMAL)
run_lb.config(bd=3, background="pink", foreground="black",font=fontExample2)
run_lb.grid(row=1, column=0,sticky='nw', padx=5, pady=5)

# runs to potentially export
save_lb = Listbox(frame4b, height=8,state= NORMAL)
save_lb.config(bd=3, background="pink", foreground="black",font=fontExample2)
save_lb.grid(row=1, column=1,sticky='nw', padx=5, pady=5)

# label for listbox
run_infolbl3=Label(frame4b, text='RUNS')
run_infolbl3.config(background="red", foreground="white", font=fontExample2)
run_infolbl3.grid(column=0, row=0, padx=5,sticky="nsew")

# label for list box
run_infolbl4=Label(frame4b, text='RUNS TO EXPORT')
run_infolbl4.config(background="red", foreground="white", font=fontExample2)
run_infolbl4.grid(column=1, row=0,padx=5,sticky="nsew")

# to save to temporary csv. Duplicates allowed. cleared on export
button_addruns= Button(frame4b,text='ADD RUNS', command=add_runs, state=NORMAL)
button_addruns.config(background="red", foreground="white", font=fontExample2)
button_addruns.grid(column=1,row=2, ipadx=2, ipady=2,padx=2,pady=2)

# search runs
entry4 = Entry(frame4b,width=25) 
entry4.grid(column=0,row=2,padx=2,sticky="nsew")
button_entry4= Button(frame4b, relief=RAISED,text="Search run_ID", command=search_run_ID)
button_entry4.config(background="pink", foreground="black", font=fontExample2)
button_entry4.grid(column=0, row=3, ipadx=4, ipady=4,pady=2,sticky="nsew")

# Frame5 run information 

# Scrolled text for run info
run_infolb = ScrolledText(frame5, width=60, height=10,  wrap='word',  font=fontExample1)
run_infolb.config(spacing3=10,background='pink', foreground="black")
run_infolb.grid(row=2,column=1,ipadx=10, ipady=10)
run_infolb.insert(INSERT,phrase2)

# label for run info
run_infolbl=Label(frame5, text='Run Info')
run_infolbl.config(background="red", foreground="white", font=fontExample)
run_infolbl.grid(column=1, row=0, ipadx=10, ipady=10, sticky="nsew")


win.mainloop()