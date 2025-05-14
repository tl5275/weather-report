import streamlit as st
st.set_page_config(page_title="City Weather Lookup", layout="centered")  # ✅ MUST BE FIRST

import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime

# Configuration
cities = ["Mumbai", "Delhi", "Bangalore", "Kolkata", "Chennai", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]
conditions = ["Clear", "Cloudy", "Rainy", "Sunny", "Snowy", "Foggy"]
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 3, 31)  # 3 months of data

# Generate date range
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Generate synthetic data
data = []
for date in date_range:
    for city in cities:
        base_temp = {
            "Mumbai": random.uniform(20, 35),
            "Delhi": random.uniform(10, 30),
            "Bangalore": random.uniform(15, 28),
            "Kolkata": random.uniform(15, 30),
            "Chennai": random.uniform(20, 35),
            "Hyderabad": random.uniform(18, 32),
            "Pune": random.uniform(15, 28),
            "Ahmedabad": random.uniform(20, 35),
            "Jaipur": random.uniform(10, 30),
            "Lucknow": random.uniform(10, 30),
        }[city]
        temperature = round(base_temp + random.uniform(-3, 3), 1)
        humidity = random.randint(30, 90)
        condition = random.choice(conditions)
        data.append([date.strftime("%Y-%m-%d"), city, temperature, humidity, condition])

# Create and save DataFrame
df = pd.DataFrame(data, columns=["date", "city", "temperature", "humidity", "condition"])
df.to_csv("weather_data.csv", index=False)

# Load cached data
@st.cache_data
def load_data():
    df = pd.read_csv("weather_data.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# Streamlit UI
st.title("🌦️ City Weather Report")

# User input
city_input = st.text_input("Enter city name (e.g., Mumbai)", "").strip()

if city_input:
    city_df = df[df['city'].str.lower() == city_input.lower()]

    if not city_df.empty:
        st.success(f"Showing weather data for: {city_input.title()}")

        latest = city_df.sort_values('date', ascending=False).iloc[0]
        st.metric("Latest Temperature (°C)", latest['temperature'])
        st.metric("Humidity (%)", latest['humidity'])
        st.metric("Condition", latest['condition'])

        city_df = city_df.sort_values('date')
        city_df['7-day avg'] = city_df['temperature'].rolling(7).mean()

        st.subheader("📈 Temperature Trend")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(city_df['date'], city_df['temperature'], label="Daily Temp")
        ax.plot(city_df['date'], city_df['7-day avg'], label="7-Day Avg", color="orange")
        ax.set_xlabel("Date")
        ax.set_ylabel("Temperature (°C)")
        ax.legend()
        st.pyplot(fig)

        st.subheader("🌤️ Condition Frequency")
        st.bar_chart(city_df['condition'].value_counts())
    else:
        st.warning("City not found in the data. Please try again.")
else:
    st.info("Please enter a city name to get started.")

# Footer
st.markdown("---")
st.caption("Built with Streamlit")
