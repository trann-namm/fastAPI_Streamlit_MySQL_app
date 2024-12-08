# frontend/app.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# API Base URL
API_BASE_URL = "http://backend:8000"

def main():
    st.title("Startup Valuations Dashboard")
    
    # Fetch startup data
    try:
        startups_response = requests.get(f"{API_BASE_URL}/startups")
        startups_data = startups_response.json()
        
        # Convert to DataFrame
        df = pd.DataFrame(startups_data)
        # Sidebar for filtering
        st.sidebar.header("Filters")
        selected_country = st.sidebar.selectbox(
            "Select Country", 
            ["All"] + list(df['Country'].unique())
        )
        
        # Filter data
        if selected_country != "All":
            df = df[df['Country'] == selected_country]
        
        # Main display
        st.header("Startup Details")
        st.dataframe(df)
        
        # Country-wise Analysis
        st.header("Country-wise Analysis")
        country_response = requests.get(f"{API_BASE_URL}/startups/by_country")
        country_data = pd.DataFrame(country_response.json())
        
        # Country Distribution
        fig_country = px.bar(
            country_data, 
            x='Country', 
            y='Count', 
            title='Number of Startups by Country',
            labels={'Count': 'Number of Startups'}
        )
        st.plotly_chart(fig_country)
        
        # Industry-wise Analysis
        st.header("Industry-wise Analysis")
        industry_response = requests.get(f"{API_BASE_URL}/startups/by_industry")
        industry_data = pd.DataFrame(industry_response.json())
        
        # Industry Distribution
        fig_industry = px.bar(
            industry_data, 
            x='Industry', 
            y='Count', 
            title='Number of Startups by Industry',
            labels={'Count': 'Number of Startups'}
        )
        st.plotly_chart(fig_industry)
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")

if __name__ == "__main__":
    main()
