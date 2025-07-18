import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style
sns.set(style="whitegrid")

# Streamlit page title
st.title('🌦️ Weather Forecast Dashboard')

# User input for city name
city = st.text_input('Enter City Name:', 'London')

# Your OpenWeatherMap API key
API_KEY = '1d62988d7ade66ea4d870ca61082abc1'

# Fetch Data Function
def fetch_weather(city, api_key):
    URL = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Fetch data
data = fetch_weather(city, API_KEY)

if data:
    st.success(f"Weather data fetched for {city}!")

    # Process data
    time_stamps = [entry['dt_txt'] for entry in data['list']]
    temperatures = [entry['main']['temp'] for entry in data['list']]

    # Create DataFrame
    df = pd.DataFrame({
        'DateTime': pd.to_datetime(time_stamps),
        'Temperature (°C)': temperatures
    })

    # Line Chart
    st.subheader('Temperature Forecast')
    st.line_chart(df.set_index('DateTime'))

    # Optional: Display Data Table
    if st.checkbox("Show Raw Data Table"):
        st.dataframe(df)

    # Optional: Seaborn Plot
    st.subheader('Temperature Trend (Seaborn Plot)')
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='DateTime', y='Temperature (°C)', data=df, marker='o')
    plt.xticks(rotation=45)
    st.pyplot(plt)

else:
    st.error("❌ Failed to fetch data. Check your API key or city name.")
