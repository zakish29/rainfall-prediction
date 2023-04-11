import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
import json
import requests
import altair as alt


with open('list_cat_cols.txt', 'r') as file_1:
    list_cat_cols = json.load(file_1)

with open('list_num_cols.txt', 'r') as file_2:
    list_num_cols = json.load(file_2)

st.set_page_config(
    page_title=' Rain Prediction',
    layout= 'wide',
    initial_sidebar_state= 'expanded'
)


# Create Run Function
def run():
    # Membuat Title
    st.title('Rain Prediction')

    # Subheader
    st.subheader('EDA Rain in Australia')

    # Menambahkan gambar
    image = Image.open('deployment/rain.jpg')
    st.image(image)

    # Menambahkan deskripsi
    st.write('## Introduction')
    st.write(
    '''
    "Rain or shine, the weather always manages to surprise us. While some people may embrace the rain and find joy in its pitter-patter, others may just feel drenched and miserable."
     
    But what if we could predict the weather with greater accuracy and precision? With advancements in technology and data science, we now have the ability to forecast the weather with greater confidence. In this quest to predict the unpredictable, we turn our attention to Australia, a country known for its diverse climate and weather patterns. So, let's take a deep dive into the world of weather forecasting and see if we can predict when the next storm will hit Down Under.
    
    '''
    )
    # Membuat garis lurus
    st.markdown('-'*42)

    st.write('## Table')
    # Show DF
    df = pd.read_csv('weatherAUS.csv')
    st.dataframe(df)
    # # API endpoint for current weather data for Sydney, Australia
    # url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"

    # # Make API request and load response into a Pandas dataframe
    # response = requests.get(url)
    # data = response.json()
    # df = pd.json_normalize(data)


    # # Display current weather conditions in Streamlit app
    # st.write("Current weather conditions for Sydney, Australia:")
    # st.write(f"Temperature: {df['main.temp'][0]} K")
    # st.write(f"Description: {df['weather.0.description'][0]}")
    # st.write(f"Humidity: {df['main.humidity'][0]}%")
    # st.write(f"Wind speed: {df['wind.speed'][0]} m/s")
    
    st.write('## Rain Trend From 2007-2017')
    # change column date to datatype
    df['Date'] = pd.to_datetime(df['Date'])
    # Change Yes and No to 1 and 0
    # Define a lambda function to map the values to 1 or 0
    map_function = lambda x: 1 if x == 'Yes' else 0

    # Apply the lambda function to the RainTomorrow column
    df['RainTomorrow'] = df['RainTomorrow'].apply(map_function)
    # Apply the lambda function to the RainToday column
    df['RainToday'] = df['RainToday'].apply(map_function)
    # Add New column
    df['Year'] = df['Date'].dt.year  

    # Group the data by year and sum the rainfall
    df_by_year = df.groupby('Year')['RainTomorrow'].sum().reset_index()
    # Create a line chart using Plotly Express
    fig = px.line(df_by_year, x='Year', y='RainTomorrow', title='Total Rainfall per Year')
    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1 year", step="year", stepmode="backward"),
                    dict(count=5, label="5 years", step="year", stepmode="backward"),
                    dict(count=10, label="10 years", step="year", stepmode="backward"),
                    dict(count=20, label="20 years", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    # Show the plot
    st.plotly_chart(fig)
    st.write(
        '''
        The number of rainfall in the Australia is significantly increased during 2018 and decreased from 2016 until 2017
        '''
    )

    st.write('## Rain Trend From By Location')
    # Group the data by location and count the number of records for each location
    df_by_location = df.groupby('Location')['RainTomorrow'].count().sort_values(ascending=False).head(10).reset_index()
    df_by_location = df_by_location.rename(columns={'RainTomorrow': 'Count'})
    # Create a bar chart using Plotly Express
    fig = px.bar(df_by_location, x='Count', y='Location',title='Top 10 Locations by Rain Data Count')
    # Show the plot
    st.plotly_chart(fig)


    # # Set your Mapbox access token
    # mapbox_token = 'sk.eyJ1IjoiemFraXNoIiwiYSI6ImNsZms0cnViZzA3ZWo0MXF4ZTk5dHh0eW4ifQ.Gz6mA_Zz4Fkz_DTervy-YQ'

    # # Loop through each location in the dataframe
    # for location in df['Location']:
    #     # Make a request to the Mapbox Geocoding API to get the coordinates for the location
    #     response = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?access_token={mapbox_token}')
    #     response_json = response.json()

    #     # Check if there are any features returned in the response
    #     if 'features' in response_json:
    #         # Get the latitude and longitude coordinates from the first feature
    #         features = response_json['features']
    #         latitude = features[0]['center'][1]
    #         longitude = features[0]['center'][0]

    #          # Add the latitude and longitude values to the DataFrame
    #         df.loc[df['Location'] == location, 'Latitude'] = latitude
    #         df.loc[df['Location'] == location, 'Longitude'] = longitude
    #     else:
    #         print(f'Error: No features found for {location}')

    # # Create a scatter mapbox plot with markers for each location
    # fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude', hover_name='Location', zoom=3,
    #                         title='Map of Locations')
    # fig.update_layout(mapbox_style='mapbox://styles/mapbox/light-v10')
    # st.plotly_chart(fig)




# calling function
if __name__ == '__main__':
   run()