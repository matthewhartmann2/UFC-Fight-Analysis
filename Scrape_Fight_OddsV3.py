#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 14:18:15 2023

@author: matthewhartmann
"""

import cloudscraper
import random
import time 
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def scrape_fight_odds(df,starting_index):
    filtereddf=df[df.index > starting_index]
    for index, row in filtereddf.iterrows():
        #Note each Fighter 1 and Event Date
        delay=random.uniform(5,7)
        time.sleep(delay)
        fighter_1_name=row['Fighter 1'].lower()
        event_date=row['Date']
        fighter_2_name=row['Fighter 2'].lower()
        event_date=datetime.strptime(event_date, "%Y-%m-%d").date()
        #Establish a Connection with fight odds using fighter 1 name
        query_string='https://www.bestfightodds.com/search?query= '+fighter_1_name
        scraper = cloudscraper.create_scraper()
        response = scraper.get(query_string)
        content = response.text 
        #content
        soup=BeautifulSoup(content, 'lxml')
        tbody=soup.find_all('tr')
        full_link=''
        for row in tbody:
            #Check if the search took directly to odds page
            header_of_interest=soup.find('div', {'class':'content-header team-stats-header'})
            if header_of_interest is not None:
                header_of_interest_text=header_of_interest.contents[0].text
                header_of_interest_text=header_of_interest_text.lower()
                if header_of_interest_text==fighter_1_name:
                    full_link=query_string
                break
            #Through analysis of web structure, name is present in the third element
            #Find the proper link the odds page
            else:
                content=row.contents[3].get_text()
                content=content.lower()
                if content==fighter_1_name:
                    outer_link = row.find('a')['href']
                    #This is the link to be redirected to the fighters list of fights
                    full_link='https://www.bestfightodds.com'+outer_link
                    break
        #Establish connection with fighter page given the link
        df.at[index,'Fighter 1 Odds - Link']=full_link
        print(index)
        print('This is the full link'+full_link)
        print(response)
        print('')
        if full_link !='':
            query_string=full_link
            delay=random.uniform(5,7)
            time.sleep(delay)
            scraper = cloudscraper.create_scraper() 
            response = scraper.get(query_string)
            content = response.text 
            soup=BeautifulSoup(content, 'lxml')
            table_rows = soup.find('tbody')
            #Debugging 
            print(response)
            print('This is the soup')
            print(soup)
            row_list=table_rows.find_all('tr')
            count=0
            #Initialize Fight odds match to be date not found (this will update if date is found)
            df.at[index,'Fight to Odds Match']='NM - Date Not Found'
            #Look at every 3rd entry (this is where the date info is stored)
            row_list_event_titles=row_list[0::3]
            for entry in row_list_event_titles:
                content=entry.contents[0].get_text()
                content= content.split()
                #Look at the last 3 words (this correponds to month, day, and year)
                content=content[-3:]
                content=' '.join(content)
                if content != "Future Events":
                    content = content.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
                    content=datetime.strptime(content,"%b %d %Y").date()
                    date_difference = abs(content - event_date)
                    #Account for the case where the fight days have a one day descrepancy (fight starts after midnight)
                    if (content==event_date) or (date_difference==timedelta(days=1)):
                        #We expect this row to contain fighter 1 details
                        expected_fighter_1_info=row_list[(count*3)+1]
                        #We expect this row to contain fighter 2 details 
                        expected_fighter_2_info=row_list[(count*3)+2]
                        expected_fighter_1_name=((expected_fighter_1_info.find('th')).contents[0].get_text()).lower()
                        expected_fighter_2_name=((expected_fighter_2_info.find('th')).contents[0].get_text()).lower()
                        if (expected_fighter_1_name==fighter_1_name) and (expected_fighter_2_name==fighter_2_name):
                            print(fighter_1_name+' vs. '+fighter_2_name+' - match')
                            df.at[index,'Fight to Odds Match']='M'
                            #df.at[index,'Fighter 1 Odds']=
                            print(expected_fighter_1_info.find_all('td')[0])
                            print(expected_fighter_1_info.find_all('td')[1])
                            print(expected_fighter_1_info.find_all('td')[3])
                            df.at[index,'Fighter 1 Odds - Open']=expected_fighter_1_info.find_all('td')[0].contents[0].get_text()
                            df.at[index,'Fighter 1 Odds - Close Lower']=expected_fighter_1_info.find_all('td')[1].contents[0].get_text()
                            df.at[index,'Fighter 1 Odds - Close Upper']=expected_fighter_1_info.find_all('td')[3].contents[0].get_text()
                            df.at[index,'Fighter 2 Odds - Open']=expected_fighter_2_info.find_all('td')[0].contents[0].get_text()
                            df.at[index,'Fighter 2 Odds - Close Lower']=expected_fighter_2_info.find_all('td')[1].contents[0].get_text()
                            df.at[index,'Fighter 2 Odds - Close Upper']=expected_fighter_2_info.find_all('td')[3].contents[0].get_text()
                            break
                        else:
                            print(fighter_1_name+' vs. '+fighter_2_name+' - no match')
                            df.at[index,'Fight to Odds Match']='NM - Date Found, names not matching'
                count=count+1