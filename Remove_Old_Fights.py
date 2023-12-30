#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 11:03:29 2023

@author: matthewhartmann
"""
import pandas as pd
from datetime import date

#The standardized 5 min round system occurred after UFC 20
#This function removes all fights occuring before that date
def remove_old_fights(df):
    df['Date']=pd.to_datetime(df['Date'])
    df['Date']=df['Date'].dt.date
    #Date of UFC 20: 1995, 5, 7
    UFC_20_date=date(1999,5,7)
    df=df[df['Date']>UFC_20_date]
    return df
    

