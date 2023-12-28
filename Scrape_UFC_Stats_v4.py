"""
Spyder Editor

This is a temporary script file.
"""

#import numpy as np
#import pandas as pd
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
from datetime import date
import random
import requests 


#We use the event level table (table_rows). Given the numeric starting_point and end_point fields (corresponding to rows in the event table),
#We get all the fight level statistics for all the fights that occured in an event and append those details to the dataframe (df)
def scrape_ufc_stats(table_rows,starting_point,end_point,accumulator):
    #Get today's date, this will be used to determine which entries to add
    today=datetime.today()
    today=today.replace(hour=0, minute=0, second=0, microsecond=0)
    #change last range parameter to end_point
    for number in range (starting_point,end_point):
        row_info=table_rows.find_all('tr')[number]
        #Establish intial Variables
        ###Take the a element content
        Event=row_info.find('a').contents[0].strip()
        print(number, Event)
        ###Take the href element of the a element
        Link=row_info.find('a')['href']
        ###Take the span element content
        Date=row_info.find('span').contents[0].strip()
        ###Take the second column/td element content
        Location=row_info.find_all('td')[1].contents[0].strip()
        #Iterate through each fight if it already occured
        ###Convert the date to datetime 
        fight_date=datetime.strptime(Date,'%B %d, %Y')
        ###Account for case when the scrapping occurs on the day of a fight that has not yet occured
        fight_date=fight_date.replace(hour=1, minute=0, second=0, microsecond=0)
        #Iterate through each fight if it already occured
        if fight_date<today:
            delay=random.uniform(0.1,1)
            time.sleep(delay)
            #Attempt to establish a connection for the event
            try:
                result=requests.get(Link, timeout=5)
                src=result.content
                soup=BeautifulSoup(src, 'lxml')
                #Get the table (event table)
                event_table=soup.find('table',{'class':"b-fight-details__table b-fight-details__table_style_margin-top b-fight-details__table_type_event-details js-fight-table"})
                #Get the rows in the table
                event_table_rows = event_table.find('tbody')
                #Get the number of rows in the table (each row is a fight)
                event_table_end_point=len(event_table_rows.find_all('tr'))
                for fight in range(0,event_table_end_point): 
                    #This is a temporary dictionary that is populated for each fight and becomes a single row in df
                    new_dictionary={}
                    #Since the event link worked 
                    new_dictionary['Event - Connection']='Successful'
                    #for each fight we get a row which corresponds to fight details
                    fight_info=event_table_rows.find_all('tr')[fight]
                    #Fight information is stored in the p classes
                    P_class_entries= fight_info.find_all('p')
                    new_dictionary['Weight Class']=P_class_entries[11].contents[0].strip()
                    new_dictionary['Method']=P_class_entries[12].contents[0].strip()
                    new_dictionary['Details']=P_class_entries[13].contents[0].strip()
                    new_dictionary['Round']=P_class_entries[14].contents[0].strip()
                    new_dictionary['Time']=P_class_entries[15].contents[0].strip()
                    Fight_Link=P_class_entries[0].find('a')['href']
                    # Assign the Initial Variables
                    new_dictionary['Fight Link']=Fight_Link
                    new_dictionary['Event']=Event
                    new_dictionary['Event Link']=Link
                    new_dictionary['Date']=Date
                    new_dictionary['Location']=Location
                    #Assign Full Date for Audit (we will use this to track data quality and ensure coverage between runs)
                    new_dictionary['Location']=Location
                    #####Get fight level details
                    try:
                        result=requests.get(Fight_Link,timeout=5)
                        src=result.content
                        soup=BeautifulSoup(src, 'lxml')
                        #Get the name info (Fight result for each fighter)
                        name_info=soup.find_all('div',{'class':'b-fight-details__person'})
                        #Fighter 1
                        fighter_1_block=name_info[0]
                        fighter_1_name=fighter_1_block.find('a').contents[0].strip()
                        fighter_1_result=fighter_1_block.find('i').contents[0].strip()
                        fighter_1_link=fighter_1_block.find('a')['href']
                        new_dictionary['Fight - Connection']='Successful'
                        new_dictionary['Fighter 1']=fighter_1_name
                        new_dictionary['Fighter 1 - Result']=fighter_1_result
                        new_dictionary['Fighter 1 - Link']=fighter_1_link
                        try:
                            result_fighter1=requests.get(fighter_1_link,timeout=5)
                            src_fighter1=result_fighter1.content
                            soup_fighter1=BeautifulSoup(src_fighter1, 'lxml')
                            #############Fighter 1 Demographic details
                            height1=soup_fighter1.find_all('li')[3].contents[2].strip()
                            weight1=soup_fighter1.find_all('li')[4].contents[2].strip()
                            reach1=soup_fighter1.find_all('li')[5].contents[2].strip()
                            stance1=soup_fighter1.find_all('li')[6].contents[2].strip()
                            DOB1=soup_fighter1.find_all('li')[7].contents[2].strip()
                            new_dictionary['Fighter 1 - Height']=height1
                            new_dictionary['Fighter 1 - Weight']=weight1
                            new_dictionary['Fighter 1 - Reach']=reach1
                            new_dictionary['Fighter 1 - STANCE']=stance1
                            new_dictionary['Fighter 1 - DOB']=DOB1
                            new_dictionary['Fighter 1 - Connection']='Successful'
                        #Pandas behavior is to fill in NaN for dictionaries that are missing columns: height, weight, etc.
                        except requests.exceptions.Timeout:
                            print(fighter_1_link+" - Unsuccessful Connection")
                            new_dictionary['Fighter 1 - Connection']='Unsuccessful'
                        #Fighter 2
                        fighter_2_block=name_info[1]
                        fighter_2_name=fighter_2_block.find('a').contents[0].strip()
                        fighter_2_result=fighter_2_block.find('i').contents[0].strip()
                        fighter_2_link=fighter_2_block.find('a')['href']
                        new_dictionary['Fighter 2']=fighter_2_name
                        new_dictionary['Fighter 2 - Result']=fighter_2_result
                        new_dictionary['Fighter 2 - Link']=fighter_2_link
                        try:
                            result_fighter2=requests.get(fighter_2_link,timeout=5)
                            src_fighter2=result_fighter2.content
                            soup_fighter2=BeautifulSoup(src_fighter2, 'lxml')
                            #############Fighter 2 Demographic details
                            height2=soup_fighter2.find_all('li')[3].contents[2].strip()
                            weight2=soup_fighter2.find_all('li')[4].contents[2].strip()
                            reach2=soup_fighter2.find_all('li')[5].contents[2].strip()
                            stance2=soup_fighter2.find_all('li')[6].contents[2].strip()
                            DOB2=soup_fighter2.find_all('li')[7].contents[2].strip()
                            new_dictionary['Fighter 2 - Height']=height2
                            new_dictionary['Fighter 2 - Weight']=weight2
                            new_dictionary['Fighter 2 - Reach']=reach2
                            new_dictionary['Fighter 2 - STANCE']=stance2
                            new_dictionary['Fighter 2 - DOB']=DOB2
                            new_dictionary['Fighter 2 - Connection']='Successful'
                        #Pandas behavior is to fill in NaN for dictionaries that are missing columns: height, weight, etc.
                        except requests.exceptions.Timeout:
                            print(fighter_2_link+" - Unsuccessful Connection")
                            new_dictionary['Fighter 2 - Connection']='Unsuccessful'
                    #Get Fight stats
                        fight_info=soup.find_all('tr',{'class':'b-fight-details__table-row'})
                    #Verify table header 
                        try:
                            table_header=fight_info[0]
                            header_list=table_header.find_all('th')
                            element_list=[]
                            for header in header_list:
                                element=header.contents[0].strip()
                                element_list=element_list+[element]
                            verified_element_list= ['Fighter','KD','Sig. str.','Sig. str. %','Total str.','Td','Td %','Sub. att','Rev.','Ctrl']
                            if verified_element_list==element_list:
                                #fight stats can be found in fight_info[1]
                                table_1_details=fight_info[1].find_all('td')
                                #exclude first p element (this just relates to names)
                                table_1_details=table_1_details[1:]
                                verified_element_list=verified_element_list[1:]
                                count=0
                                for column in table_1_details:
                                    column_details=column.find_all('p')
                                    Fighter_1_variable='Fighter 1 - '+verified_element_list[count]
                                    Fighter_2_variable='Fighter 2 - '+verified_element_list[count]
                                    new_dictionary[Fighter_1_variable]=column_details[0].contents[0].strip()
                                    new_dictionary[Fighter_2_variable]=column_details[1].contents[0].strip()
                                    count=count+1
                                new_dictionary['Detailed Fight Stats']='Successful'
                        except IndexError:
                            table_header='null'
                            print(Fight_Link+" - Table Error")
                            new_dictionary['Detailed Fight Stats']='Unsuccessful'
                    except requests.exceptions.Timeout:
                        new_dictionary['Fight - Connection']='Unsuccessful'
                    #Append row to accumulator
                    accumulator.append(new_dictionary)
            #If we fail to load an event create create a row highlighting with just event details and failure to load event
            except requests.exceptions.Timeout:
                print(Link + " Unsuccessful Connection")
                new_dictionary={}
                new_dictionary['Event - Connection']='Unsuccessful'
                new_dictionary['Event']=Event
                new_dictionary['Event Link']=Link
                new_dictionary['Date']=Date
                new_dictionary['Location']=Location
                #Append row to accumulator
                accumulator.append(new_dictionary)
                