import requests
import pandas as pd
import mysql.connector
import sqlalchemy
from bs4 import BeautifulSoup
from datetime import datetime
url='https://www.cbinsights.com/research-unicorn-companies'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}
data = requests.get(url, headers=headers).text

soup = BeautifulSoup(data, 'html.parser')
for table in soup.find_all('table'):
    print(table.get('class'))

table=soup.find('table',class_='sortable-theme-bootstrap')
df=pd.DataFrame(columns=['Company','Valuation','Date_Joined','Country','City','Industry','Selector_Investors'])
for row in table.find_all('tr'):
    columns=row.find_all('td')
    if(columns!=[]):
        company=columns[0].text.strip()
        valuation=columns[1].text.strip()
        date_Joined=columns[2].text.strip()
        country=columns[3].text.strip()
        city=columns[4].text.strip()
        industry=columns[5].text.strip()
        selector=columns[6].text.strip()
        
        # Tạo một DataFrame từ dictionary
        new_data = pd.DataFrame([{
        'Company': company,
        'Valuation': valuation,
        'Date_Joined': datetime.strptime(date_Joined, "%m/%d/%Y"),
        'Country': country,
        'City': city,
        'Industry': industry,
        'Selector_Investors': selector
        }])

# Nối DataFrame mới với DataFrame hiện tại
        df = pd.concat([df, new_data], ignore_index=True)
database_username = 'root'
database_password = 'root'
database_ip       = 'mysql'
database_name     = 'startup_db'

database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name), pool_recycle=1, pool_timeout=57600).connect()
df.to_sql(con=database_connection, name='startups', if_exists='append',chunksize=100)
database_connection.close()
