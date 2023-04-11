import streamlit as st
import pandas as pd
import joblib
import json

# load model
with open('compressed_pipeline.pkl', 'rb') as file_1:
    pipeline = joblib.load(file_1)

with open('list_num_cols.txt', 'r') as file_2:
    list_num_cols = json.load(file_2)

with open('list_cat_cols.txt', 'r') as file_2:
    list_cat_cols = json.load(file_2)


df = pd.read_csv('./weatherAUS.csv')


# Run function stelah loading
def run():
    with st.form(key='Rainfall Prediction'):        
        Location = st.selectbox('Where are you', df['Location'].unique())    
        MinTemp =  st.number_input('Minimum temp recorded', key='MinTemp', min_value=-50, max_value=50, value=0)   
        MaxTemp =  st.number_input('Minimum temp recorded', key='MaxTemp', min_value=-50, max_value=50, value=0)     
        Rainfall = st.number_input('Rainfall recorded (mm)', key='Rainfall', min_value=0, max_value=371, value=0)   
        Evaporation =  st.number_input('Class A pan evaporation (mm) in the 24 hours to 9am', key='Evaporation', min_value=0, max_value=145, value=0)
        Sunshine  =  st.number_input('The number of hours of bright sunshine in the day', key='Sunshine', min_value=0, max_value=24, value=0)  
        WindGustDir  = st.selectbox('Wind Direction', df['WindGustDir'].unique())
        WindGustSpeed = st.number_input('The speed (km/h) of the strongest wind gust in the 24 hours to midnight', key='WindGustSpeed', min_value=0, max_value=135, value=0)
        WindDir9am =  st.selectbox('Wind Direction at 9am', df['WindDir9am'].unique()) 
        WindDir3pm  = st.selectbox('Wind Direction at 3pm', df['WindDir3pm'].unique())  
        WindSpeed9am = st.number_input('Wind speed (km/hr) averaged over 10 minutes prior to 9am', key='WindSpeed9am', min_value=0, max_value=130, value=0)
        WindSpeed3pm  = st.number_input('Wind speed (km/hr) averaged over 10 minutes prior to 3pm', key='WindSpeed3pm', min_value=0, max_value=87, value=0)
        Humidity9am  = st.number_input('Humidity (percent) at 9am', key='Humidity9am', min_value=0, max_value=100, value=0)
        Humidity3pm  = st.number_input('Humidity (percent) at 3pm', key='Humidity3pm', min_value=0, max_value=100, value=0)
        Pressure9am  = st.number_input('Atmospheric pressure (hpa) reduced to mean sea level at 9am', key='Pressure9am', min_value=0, max_value=1041, value=0)
        Pressure3pm  = st.number_input('Atmospheric pressure (hpa) reduced to mean sea level at 3pm', key='Pressure3pm', min_value=0, max_value=1039, value=0)
        Cloud9am  = st.number_input('Fraction of sky obscured by cloud at 9am.', key='Cloud9am', min_value=0, max_value=9, value=0)   
        Cloud3pm  = st.number_input('Fraction of sky obscured by cloud at 3pm.', key='Cloud3pm', min_value=0, max_value=9, value=0)   
        Temp9am = st.number_input('Temperature (degrees C) at 9am', key='Temp9am', min_value=-50, max_value=50, value=0)    
        Temp3pm = st.number_input('Temperature (degrees C) at 3pm', key='Temp3pm', min_value=-50, max_value=50, value=0)     
        RainToday = st.radio('Is today raining?', options = ('Yes', 'No'))
        
        submitted = st.form_submit_button('Predict')

    data_inf = {        
        'Location' :  Location,    
        'MinTemp' :   MinTemp,   
        'MaxTemp'  :  MaxTemp,    
        'Rainfall' :   Rainfall,   
        'Evaporation'  : Evaporation,
        'Sunshine'  :  Sunshine,   
        'WindGustDir' : WindGustDir,  
        'WindGustSpeed' : WindGustSpeed,
        'WindDir9am'  : WindDir9am,  
        'WindDir3pm' : WindDir3pm,   
        'WindSpeed9am' : WindSpeed9am, 
        'WindSpeed3pm' : WindSpeed3pm, 
        'Humidity9am' :  Humidity9am, 
        'Humidity3pm' : Humidity3pm,  
        'Pressure9am' : Pressure9am,  
        'Pressure3pm' : Pressure3pm,  
        'Cloud9am' :  Cloud9am,    
        'Cloud3pm' : Cloud3pm,     
        'Temp9am' :  Temp9am,     
        'Temp3pm' : Temp3pm,      
        'RainToday' : RainToday
}  
    
    data_inf = pd.DataFrame([data_inf])
    st.dataframe(data_inf)

    if submitted:
        # Create a dictionary to map radio button choices to integer values
        radio_dict = {'Yes': 1, 'No': 0}

       
        data_inf_final = data_inf.drop(['Rainfall', 'Temp9am', 'Temp3pm', 'Pressure9am', 'Location'], axis=1)       
        y_pred_inf = pipeline.predict(data_inf_final)



        if y_pred_inf.any() == 1:
            st.write('## Prepare your umbrella because it will be rain  ')
        else:
            st.write('## Have fun plan your day ahead in a bright day')


# calling function
if __name__ == '__main__':
   run()