#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 16:43:01 2023

@author: matthewhartmann
"""
import pandas as pd
from Get_Event_Table import get_all_events
from Scrape_UFC_Stats_v4 import scrape_ufc_stats
from datetime import datetime
from Get_Total_Fights import get_total_fights


def fix_failed_connects(df):
    ###General Process
    #Get total number of unsuccessful entries 
    df_unsuccessful=df[(df['Fight - Connection']=='Unsuccessful') |(df['Fighter 1 - Connection']=='Unsuccessful')|(df['Fighter 2 - Connection']=='Unsuccessful')]
    #Find Unique entries of Events with Dates
    unique_events=df[['Event','Date']].drop_duplicates()
    #Get the most recent event in our existing dataset
    unique_events=unique_events.sort_values(by='Date',ascending=False)
    most_recent_event=unique_events.at[0,'Event']
    #Look at the current UFC website and determine the total number of logged events
    table_rows=get_all_events()
    table_rows_len=len(table_rows.find_all('tr'))
    #initialize count to be '', update with the proper starting point
    count=''
    #Find the row in the UFC website that maps to our most recent event in the dataset (start at row 1, since row 0 is blank)
    for number in range (1,table_rows_len):
        row_info=table_rows.find_all('tr')[number]
        Resulting_Event=row_info.find('a').contents[0].strip()
        if Resulting_Event==most_recent_event:
            #initialize count to 
            count=number
            break
    if count=='':
        return 'Error could not find most recent event on website'
    #Create a dictionary that maps number in order to each event
    event_dictionary={}
    #Create a dictionary with each event and the count to map existing events in the datset to index on current website
    for index, row in unique_events.iterrows():
        event_for_dict=unique_events.at[index,'Event']
        event_dictionary[event_for_dict]=count
        count=count+1
    #While we have unsuccessful entries, we need to rerun the scrape for those entries and append
    for index, row in df_unsuccessful.iterrows():
        #Get the Event and Event Link for each unsuccessful entry
        Unsuccessful_Event=df_unsuccessful.at[index,'Event']
        Unsuccessful_Event_Link=df_unsuccessful.at[index,'Event Link']
        #Use the mapping in our dictionary to get event information from the current website
        Count_for_Scrape=event_dictionary[Unsuccessful_Event]
        row_info=table_rows.find_all('tr')[Count_for_Scrape]
        Resulting_Event=row_info.find('a').contents[0].strip()
        #If we found the right event, run the scrape for it until all fights are successefully documented
        if Unsuccessful_Event==Resulting_Event:
            success_for_unsuccessful_entry=False
            while success_for_unsuccessful_entry==False:
                #Call Web Scraper for that event, count for scrape end is just noting we call the scrape just for event of interest
                accumulator=[]
                Count_for_Scrape_End=Count_for_Scrape+1
                scrape_ufc_stats(table_rows,Count_for_Scrape,Count_for_Scrape_End,accumulator)
                accumulator_df=pd.DataFrame(accumulator)
                #Add column for data audit showing time of conversion to (distinguish between runs)
                today=datetime.today()
                accumulator_df['Time for Data Audit']=today
                #In the PY file "remove old fights" we convert the date strings to date objects, repeat this here for consistency 
                accumulator_df['Date']=pd.to_datetime(accumulator_df['Date'])
                accumulator_df['Date']=accumulator_df['Date'].dt.date
                #Append to df
                df=pd.concat([df, accumulator_df], ignore_index=True)
                #Get total amount of fights within the event of interest
                total_fights_by_event=get_total_fights(Unsuccessful_Event_Link)
                #Check if all fights were documented properly for the event
                condition_for_specific_entry=(
                    (df['Event']==Unsuccessful_Event) &
                    (df['Time for Data Audit']==today) &
                    (df['Fighter 1 - Connection']=='Successful') &
                    (df['Fighter 2 - Connection']=='Successful') &
                    (df['Detailed Fight Stats']=='Successful') &
                    (df['Fight - Connection']=='Successful') &
                    (df['Event - Connection']=='Successful')
                )
                filtered_df_for_entry=df[condition_for_specific_entry]
                if len(filtered_df_for_entry)==total_fights_by_event:
                    success_for_unsuccessful_entry=True
                    print('   ',Unsuccessful_Event,' Connection Successful')
                    #Drop all other entries outside of time audit for that event
                    condition_for_specific_entry=(
                        (df['Event']==Unsuccessful_Event) &
                        (df['Time for Data Audit']!=today)
                    )
                    df=df.drop(df[condition_for_specific_entry].index)
                else:
                    print('   Connection unsuccessful')
                    print('   Fights by Event ',total_fights_by_event)
                    print('   Fights in dataset ',len(filtered_df_for_entry))
                    #Drop all entries for that event so can be repeated with the next scrape
                    condition_for_specific_entry=(
                        (df['Event']==Unsuccessful_Event)
                    )
                    df=df.drop(df[condition_for_specific_entry].index)      
        else:
           print('Mapping Error with '+str(Unsuccessful_Event))
    df_unsuccessful=df[(df['Fight - Connection']=='Unsuccessful') |(df['Fighter 1 - Connection']=='Unsuccessful')|(df['Fighter 2 - Connection']=='Unsuccessful')]
    df_unsuccessful.to_csv('Unsuccessful_entries_post_fix.csv')
    return df

def remove_duplicates(df):
    ###Find duplicates looking at just 3 main columns
    #confirm no unsuccessful connections
    total_df_length=len(df)
    condition_for_specific_entry=(
        (df['Fighter 1 - Connection']=='Successful') &
        (df['Fighter 2 - Connection']=='Successful') &
        (df['Detailed Fight Stats']=='Successful') &
        (df['Fight - Connection']=='Successful') &
        (df['Event - Connection']=='Successful')
    )
    len_success=len(df[condition_for_specific_entry])
    if total_df_length==len_success:
        #Only Successful entries
        duplicate_df=df[df.duplicated(subset=['Fighter 1', 'Fighter 2', 'Event'], keep=False)]
        duplicate_df.to_csv('Duplicates_dropped.csv')
        df=df.drop_duplicates(subset=['Fighter 1', 'Fighter 2', 'Event'],keep='first')
        print('Duplicates dropped - check Duplicates_dropped.csv')
    else:
        print('Unsuccessful Connections Detected - check fix_failed_connections')
    return df