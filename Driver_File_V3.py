#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:28:18 2023

@author: matthewhartmann
"""
import pandas as pd
from datetime import datetime
from Get_Event_Table import get_all_events
#from Initialize_DF import initialize_df
from Scrape_UFC_Stats_v4 import scrape_ufc_stats
from Remove_Old_Fights import remove_old_fights
from Fix_Failed_Connections_Duplicatesv2 import fix_failed_connects
from Fix_Failed_Connections_Duplicatesv2 import remove_duplicates
from Fix_Other_Outcomes import fix_other_outcomes
from Scrape_Fight_OddsV3 import scrape_fight_odds

###(1) Run this section first to generate the dataset (Often has to be run multiple times due to connection time outs)

table_rows=get_all_events()
#We set the end point to be the number of events in the table (all the ufc events that occurred)
end_point=len(table_rows.find_all('tr'))
#Initialize an accumulator. We will add each fight to the accumulator as a dictionary then convert the entire accumulator to a DF
accumulator=[]
#Run the function to append the existing function, rerun as needed given connection disruptions
###Tweak as needed depending on logged error messages and disconnections
scrape_ufc_stats(table_rows,602,end_point,accumulator)

###(2) Run this section to convert accumulator to df for each run

accumulator_df=pd.DataFrame(accumulator)
#Add column for data audit showing time of conversion to (distinguish between runs)
today=datetime.today()
accumulator_df['Time for Data Audit']=today

###(3) Run this section to export to csv for each run

#Run the selected code to convert the accumulator to a df
accumulator_df.to_csv(('ufc_fights'+" "+str(today)+'.csv'),index=False)

###(4) Run this section to concatenate the files from the different runs (requires some manual inputs)

#In my case I ran the scraping 4 times due to connection timeouts

#Run 1 occurred up to 126 (126 UFC Fight Night: Overeem vs. Volkov)
df_1=pd.read_csv('ufc_fights 2023-12-20 09:46:08.715122.csv')
df_1['Event']
#Run 2 occurred from (126 UFC Fight Night: Overeem vs. Volkov) to (419 UFC 168: Weidman vs Silva 2)
df_2=pd.read_csv('ufc_fights 2023-12-20 12:03:37.939798.csv')
df_2['Event']
#Run 3 occurred from (419 UFC 168: Weidman vs Silva 2) to (602 UFC 61: Bitter Rivals)
df_3=pd.read_csv('ufc_fights 2023-12-20 13:50:27.215179.csv')
df_3['Event']
#Run 4 occurred from (602 UFC 61: Bitter Rivals) to (674 UFC 2: No Way Out)
df_4=pd.read_csv('ufc_fights 2023-12-20 15:04:50.047193.csv')
df_4['Event']

#Concatenate the dataframes 
accumulator_df=pd.concat([df_1, df_2,df_3,df_4], ignore_index=True)
accumulator_df.to_csv('Consolidated Preprocessed.csv',index=False)



###(3) Run this section to clean the data 
###########Add remove dupiclates, logic for draws, etc,

#Run to read in preprocessed DF from Previous session if needed 
accumulator_df=pd.read_csv('Consolidated Preprocessed.csv')


#Remove Old Fights 
accumulator_df=remove_old_fights(accumulator_df)

#Fix Unsuccessful Connections
accumulator_df=fix_failed_connects(accumulator_df)

#Remove Duplicates
accumulator_df=remove_duplicates(accumulator_df)

#Export

#Fix Results for Other Outcomes (the web structure is different when the result is not a win or a loss: NC Draw, etc.)
accumulator_df=fix_other_outcomes(accumulator_df)

accumulator_df.to_csv('Consolidated Cleaned.csv',index=False)


###(4) Run this section to scrape odds from fightodds.com for each fight

accumulator_df=pd.read_csv('Consolidated Cleaned.csv')

#v1: Merge with existing dataset generated from jupyter notebook
previous_dataset_with_odds=pd.read_csv('data111123-v1updated.csv')
columns_to_include=['Event',
                    'Fighter 1',
                    'Fighter 2',
                    'Fighter 1 Odds - Open',
                    'Fighter 1 Odds - Close Lower',
                    'Fighter 1 Odds - Close Upper',
                    'Fighter 1 Odds - Link',
                    'Fighter 2 Odds - Open',
                    'Fighter 2 Odds - Close Lower',
                    'Fighter 2 Odds - Close Upper',
                    'Fight to Odds Match']
accumulator_df=pd.merge(accumulator_df,previous_dataset_with_odds[columns_to_include],on=['Event','Fighter 1','Fighter 2'], how='left')
accumulator_df=accumulator_df.sort_values(by='Date',ascending=False)
accumulator_df=accumulator_df.reset_index(drop=True)
accumulator_df.to_csv('Consolidated_Cleaned_Merged.csv',index=False)

accumulator_df=pd.read_csv('Consolidated_Cleaned_Merged.csv')

#v2: Run function to get odds for additional fights
scrape_fight_odds(accumulator_df,6580)

