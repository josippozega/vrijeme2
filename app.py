# Moduli
import streamlit as st
import requests
#from datetime import datetime, timedata
import pandas as pd

#API_key
#8a3c08e182bbee243d335c7316fa9d26
api_key = 0x8a3c08e182bbee243d335c7316fa9d26

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
    res = requests.get(url_1.format(lat,lon,start,api_key))
    data = res.json()
    temp = []
    for hour in data["hourly"]:
        t = hour["temp"]
        temp.append(t)
    return data , temp


#pišemo aplikaciju
st.header('Streamlit Weather Report')
st.markdown('https://openweathermap.org/api')

col1, col2 = st.columns(2)

with col1:
    city_name = st.text_input("Enter a city name")
    #show_hist = st.checkbox('Show me history')
with col2:  
		if city_name:
		        res , json = getweather(city_name)
		        #st.write(res)
		        st.success('Current: ' + str(round(res[1],2)))
		        st.info('Feels Like: ' + str(round(res[2],2)))
		        #st.info('Humidity: ' + str(round(res[3],2)))
		        st.subheader('Status: ' + res[7])
		        web_str = "![Alt Text]"+"(http://openweathermap.org/img/wn/"+str(res[6])+"@2x.png)"
		        st.markdown(web_str)  
		
if city_name:        
    show_hist = st.expander(label = 'Last 5 Days History')
    with show_hist:
            start_date_string = st.date_input('Current Date')
            #start_date_string = str('2021-06-26')
            date_df = []
            max_temp_df = []
            for i in range(5):
                        date_Str = start_date_string - timedelta(i)
                        start_date = datetime.strptime(str(date_Str),"%Y-%m-%d")
                        timestamp_1 = datetime.timestamp(start_date)
                        #res , json = getweather(city_name)
                        his , temp = get_hist_data(res[5],res[4],int(timestamp_1))
                        date_df.append(date_Str)
                        max_temp_df.append(max(temp) - 273.5)
                
            df = pd.DataFrame()
            df['Date'] = date_df
            df['Max temp'] = max_temp_df
            st.table(df)

	st.map(pd.DataFrame({'lat' : [res[5]] , 'lon' : [res[4]]},columns = ['lat','lon']))



