import streamlit as st
from agent_utils import weather_agent, WeatherForecast
from datetime import datetime
import asyncio

st.set_page_config(
    page_title="Weather Forecast Agent",
    page_icon="⛅",
    layout="centered"
)

st.title("⛅ Weather Forecast Agent")

async def get_weather(location: str):
    """Helper function to run the async weather agent"""
    result = await weather_agent.run(location)
    return result.output

location = st.text_input("Enter a city name:", placeholder="e.g. London, New York, Tokyo")

if st.button("Get Weather Forecast"):
    if location.strip():
        with st.spinner(f"Fetching weather for {location}..."):
            try:
                # Get the weather forecast
                response = asyncio.run(get_weather(location))
                
                if response:  # Check if we got a valid response
                    # Display the results in a card-like format
                    with st.container():
                        st.markdown(f"## 🌍 Weather in {response.location}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"<div class='big-font'>🌡️ {response.temperature}°C</div>", 
                                        unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"**Condition:** {response.description.capitalize()}")
                        
                        # Additional weather details could be added here
                else:
                    st.error("No weather data received")
                        
            except requests.exceptions.RequestException as e:
                st.error(f"Network error: {str(e)}")
            except KeyError as e:
                st.error(f"Data format error: {str(e)}")
            except Exception as e:
                st.error(f"Error fetching weather data: {str(e)}")
    else:
        st.warning("Please enter a city name.")