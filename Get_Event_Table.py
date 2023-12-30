"""
Spyder Editor

This is a temporary script file.
"""

from bs4 import BeautifulSoup
import requests 

#We get a table at the event level for all ufc events 
def get_all_events():
    result=requests.get("http://ufcstats.com/statistics/events/completed?page=all")
    src=result.content
    soup=BeautifulSoup(src, 'lxml')
    table=soup.find('table',{'class':'b-statistics__table-events'})
    table_rows = table.find('tbody')
    return table_rows