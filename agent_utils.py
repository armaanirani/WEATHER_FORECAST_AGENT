import os
from dotenv import load_dotenv
import requests

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings


# Loading the environment variables from the .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OWM_API_KEY = os.getenv("OWM_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Defining the output schema
class WeatherForecast(BaseModel):
    location: str
    temperature: float
    description: str

# Defining the agent
weather_agent = Agent(
    model='groq:llama-3.3-70b-versatile',
    model_settings=ModelSettings(
        temperature=0.0
    ),
    output_type=WeatherForecast,
    system_prompt="""You are a weather forecast agent. 
    ALWAYS use the 'get_weather_forecast' tool to fetch real data. 
    NEVER generate temperature or location values yourself."""
)

# Weather forecast tool
@weather_agent.tool
def get_weather_forecast(ctx: RunContext, city: str) -> WeatherForecast:
    """
    This function returns the current weather forecast for the given city.
    """
    params = {
        "q": city,
        "appid": OWM_API_KEY,
        "units": 'metric'
    }
    
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()  # Raise exception for bad status codes
    data = response.json()
    
    return WeatherForecast(
        location=data['name'],
        temperature=data['main']['temp'],
        description=data['weather'][0]['description']
    )

# output = get_weather_forecast(ctx=None, city="Moscow")
# print(output)
