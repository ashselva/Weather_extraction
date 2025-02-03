# Weather_extraction
Python script that extracts Tokyo weather data from a weather api.

The script extracts predictive weather data hourly for the next 3 days and stores it in a postgres database. The script can be run hourly to gather new data quickly however it isnt very useful. Running the script every 12 hours will give early insight to the weather of a new day. Please run the script every 12 hours.

Project Plan:
- Initially planned to have user input to decide the location of the requested data but I've had to fix the data request to one location for the extraction, however this will hopefully be changeable once the streamlit app is completed.
- Insights on recommended clothing and accessories, such as umbrellas and sunscreen based on precipitation and UV Index levels.
- Providing insights on any relationships between data groups, E.g Humidity and Temperature.
- Visualise the data with colourful easy to read graphs
- Include a switch to display an image to represent the weather.
