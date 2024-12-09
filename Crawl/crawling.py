import requests
import pandas as pd
import mysql.connector
import sqlalchemy
from bs4 import BeautifulSoup
from datetime import datetime
from .config import *
url = 'https://www.cbinsights.com/research-unicorn-companies'

data = requests.get(url, headers=headers).text

soup = BeautifulSoup(data, 'html.parser')
for table in soup.find_all('table'):
    print(table.get('class'))

table = soup.find('table',class_ = 'sortable-theme-bootstrap')
df = pd.DataFrame(columns=['Company','Valuation','Date_Joined','Country','City','Industry','Selector_Investors'])
for row in table.find_all('tr'):
    columns = row.find_all('td')
    if(columns != []):
        company = columns[0].text.strip()
        valuation = columns[1].text.strip()
        date_Joined = columns[2].text.strip()
        country = columns[3].text.strip()
        city = columns[4].text.strip()
        industry = columns[5].text.strip()
        selector = columns[6].text.strip()
        
        # Create a DateFrame from a new record
        new_data = pd.DataFrame([{
            'Company': company,
            'Valuation': valuation,
            'Date_Joined': datetime.strptime(date_Joined, "%M/%d/%Y"),
            'Country': country,
            'City': city,
            'Industry': industry,
            'Selector_Investors': selector
        }])
        # Concatenate new DateFrame to the source DateFrame
        df = pd.concat([df, new_data], ignore_index=True)

database_username = mysql_user
database_password = mysql_password
database_ip       = mysql_host
database_name     = mysql_database

database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name), pool_recycle=1, pool_timeout=57600).connect()
df.to_sql(con = database_connection, name = mysql_table_name, if_exists='append',chunksize=100 ) 
database_connection.close()
