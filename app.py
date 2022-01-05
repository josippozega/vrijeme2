# Moduli
import streamlit as st
import requests
from datetime import datetime, timedata
import pandas as pd

#API_key
#8a3c08e182bbee243d335c7316fa9d26
api_key = 8a3c08e182bbee243d335c7316fa9d26

#API poziv sa OPEN WEATHER web-stranice
url = 'http = api.openweathermap.org/data/2.5/weather?q={city name}&appid={api_key}'
url_1 = 'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api_key}'

#funkcija za dohvaćanje TRENITNE PROGNOZE VREMENA
def getweather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        #st.write(json)
        country = json['sys']['country']
        temp = json['main']['temp'] - 273.15
        temp_feels = json['main']['feels_like'] - 273.15
        humid = json['main']['humidity'] - 273.15
        icon = json['weather'][0]['icon']
        lon = json['coord']['lon']
        lat = json['coord']['lat']
        des = json['weather'][0]['description']
        res = [country, round(temp,1),round(temp_feels,1),
                humid,lon,lat,icon,des]
        return res , json
    else:
        print("error in search !")

#funkcija za dohvaćanje podataka unazad 5 dana
def get_hist_data(lat,lon,start):
    res = requests.get(url_1.format(lat,lon,start,8a3c08e182bbee243d335c7316fa9d26))
    data = res.json()
    temp = []
    for hour in data["hourly"]:
        t = hour["temp"]
        temp.append(t)
    return data , temp


#pišemo aplikaciju
st.header('Streamlit Weather Report')
st.markdown('https://openweathermap.org/api')

im1,im2 = st.columns(2)
with im2:
    image0 = 'storm.jpg'
    st.image(image0,use_column_width=True,caption = 'Somewhere in The Netherlands.')
with im1:
    image1 = 'vakula.jpg'
    st.image(image1, caption='We will use Open Weather Map API as our Data Resource.',use_column_width=True)

col1, col2 = st.columns(2)
