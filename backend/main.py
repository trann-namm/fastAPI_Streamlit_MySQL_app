from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from typing import List, Dict
from pydantic import BaseModel, Field
from .config import *
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host = mysql_host,
            user = mysql_user,
            password = mysql_password,
            database = mysql_database
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        raise

# Pydantic model for type validation
class Startup(BaseModel):
    index: int
    Company: str
    Valuation: str
    Date_Joined: str = Field(description="Date in dd-MM-yyyy format")
    Country: str
    City: str
    Industry: str
    Selector_Investors: str

@app.get("/startups", response_model = List[Startup])
def get_startups():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute(f"SELECT * FROM {mysql_table_name}")
    startups = cursor.fetchall()
    
    # Convert date to string
    for startup in startups:
        startup['Date_Joined'] = startup['Date_Joined'].strftime('%d-%m-%Y')
    
    cursor.close()
    connection.close()
    
    return startups

@app.get("/startups/by_country", response_model = List[Dict])
def get_startups_by_country():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary = True)
    
    cursor.execute(f"""
        SELECT Country, COUNT(*) as Count, 
               AVG(CAST(REPLACE('$225.0', '$', '') AS DECIMAL(10, 2))) as Average_Valuation 
        FROM {mysql_table_name} 
        GROUP BY Country
    """)
    country_stats = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return country_stats

@app.get("/startups/by_industry", response_model = List[Dict])
def get_startups_by_industry():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary = True)
    
    cursor.execute(f"""
        SELECT Industry, COUNT(*) as Count, 
               AVG(Valuation) as Average_Valuation 
        FROM {mysql_table_name} 
        GROUP BY Industry
    """)
    industry_stats = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return industry_stats