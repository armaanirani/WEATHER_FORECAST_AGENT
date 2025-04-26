import streamlit as st
from agent_utils import weather_agent
from datetime import datetime

st.set_page_config(
    page_title="Weather Forecast Agent",
    page_icon="⛅",
    layout="centered"
)

st.title("⛅ Weather Forecast Agent")

# Sidebar for additional info
with st.sidebar:
    st.header("About")
    st.markdown("""
    This weather agent provides current weather conditions 
    for any location worldwide using OpenWeatherMap API.
    """)

location = st.text_input("Enter a city name:", placeholder="e.g. London, New York, Tokyo")

if st.button("Get Weather Forecast"):
    if location.strip():
        with st.spinner(f"Fetching weather for {location}..."):
            try:
                # Get the weather forecast
                response = weather_agent.run(location)
                
                # Display the results in a nice format
                with st.container():
                    st.markdown(f"## 🌍 Weather in {response.location}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"<div class='big-font'>🌡️ {response.temperature}°C</div>", unsafe_allow_html=True)
                        st.markdown(f"**Condition:** {response.description.capitalize()}")
                        st.markdown(f"**Humidity:** {response.humidity}%")
                        
                    with col2:
                        st.markdown(f"**Wind Speed:** {response.wind_speed} m/s")
                        st.markdown(f"**Pressure:** {response.pressure} hPa")
                        st.markdown(f"**Visibility:** {response.visibility/1000} km")
                    
                    # Additional weather details
                    with st.expander("More Details"):
                        st.markdown(f"**Cloudiness:** {response.cloudiness}%")
                        st.markdown(f"**Sunrise:** {datetime.fromtimestamp(response.sunrise).strftime('%H:%M')}")
                        st.markdown(f"**Sunset:** {datetime.fromtimestamp(response.sunset).strftime('%H:%M')}")
                        st.markdown(f"**Timezone:** GMT{response.timezone/3600:+}")
                        
            except Exception as e:
                st.error(f"Error fetching weather data: {str(e)}")
    else:
        st.warning("Please enter a city name.")