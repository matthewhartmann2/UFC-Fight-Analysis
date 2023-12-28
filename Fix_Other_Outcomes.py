#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 17:21:27 2023

@author: matthewhartmann
"""
import requests
from bs4 import BeautifulSoup

def fix_other_outcomes(df):
    ###Fix Dataframe for NC and Decisions - The formatting is slightly different for these fights
    df2=df[df['Fighter 1 - Result'].isin(['NC', 'D'])]
    #entries in dataframe not loaded properly
    index_list=(df2.index).tolist()
    #Get the number of rows in the table (each row is a fight)
    for number in index_list:
        Link=df.at[number,'Fight Link']
        result=requests.get(Link, timeout=5)
        src=result.content
        soup=BeautifulSoup(src, 'lxml')
        #Get the table (event table)
        detail_table=soup.find_all('p',{'class':"b-fight-details__text"})
        detail_table_1=detail_table[0]
        detail_table_2=detail_table[1]
        #Get Weight Class
        Weight=soup.find_all('i',{'class':"b-fight-details__fight-title"})
        Weight=Weight[0].contents[0].strip()
        output_1=detail_table_1.find_all('i')
        #Method
        Method=output_1[2].contents[0].strip()
        #Details
        Details=detail_table_2.contents[2].strip()
        #Round 
        Round=output_1[3].contents[2].strip()
        #Time 
        Time=output_1[5].contents[2].strip()
        #Make updates
        df.at[number,'Weight Class']=Weight
        df.at[number,'Method']=Method
        df.at[number,'Details']=Details
        df.at[number,'Round']=Round
        df.at[number,'Time']=Time
    return df