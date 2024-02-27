#!/usr/bin/env python
# coding: utf-8

# In[1]:


# importing necessary libraries
import pandas as pd

flight_df_with_weather_delay = pd.read_csv("Cleaned_Data.csv")

# coverting temperature from celcius to farenheit
flight_df_with_weather_delay['origin_temperature'] = (flight_df_with_weather_delay['origin_temperature']*1.8) + 32
flight_df_with_weather_delay['destination_temperature'] = (flight_df_with_weather_delay['destination_temperature']*1.8) + 32

print(flight_df_with_weather_delay['origin_state'].value_counts())

print("---------------------------------------------------------------------------\n")


# transforming delays from minutes to hours
flight_df_with_weather_delay['DEP_DELAY'] = flight_df_with_weather_delay['DEP_DELAY']/60
flight_df_with_weather_delay['ARR_DELAY'] = flight_df_with_weather_delay['ARR_DELAY']/60
flight_df_with_weather_delay['CARRIER_DELAY'] = flight_df_with_weather_delay['CARRIER_DELAY']/60
flight_df_with_weather_delay['origin_weather_delay'] = flight_df_with_weather_delay['origin_weather_delay']/60
flight_df_with_weather_delay['destination_weather_delay'] = flight_df_with_weather_delay['destination_weather_delay']/60
flight_df_with_weather_delay['NAS_DELAY'] = flight_df_with_weather_delay['NAS_DELAY']/60
flight_df_with_weather_delay['SECURITY_DELAY'] = flight_df_with_weather_delay['SECURITY_DELAY']/60

# for ease of use renaming the columns
flight_df_with_weather_delay.rename(columns=
                                            {"FL_DATE": "flight_date", 
                                            "OP_CARRIER_FL_NUM": "flight_num",
                                            "ORIGIN_AIRPORT_ID": "origin_airport_id",
                                            "DEST_AIRPORT_ID":"destination_airport_id",
                                            "DEP_DELAY":"departure_delay",
                                            "ARR_DELAY":"arrival_delay",
                                            "CARRIER_DELAY":"carrier_delay",
                                            "NAS_DELAY":"nas_delay",
                                            "SECURITY_DELAY":"security_delay",
                                            "Description":"description"},inplace=True)

# filtering origin state florida
data_florida = flight_df_with_weather_delay[flight_df_with_weather_delay['origin_state'] == 'Florida']

# filtering the columns which will be used for clustering
data_kmeans = data_florida[['origin_temperature',
                            'origin_weather_delay']]

# displaying the data
print(data_kmeans.head())

print("---------------------------------------------------------------------------\n")

# converting it to csv
data_kmeans.to_csv("clustering_data.csv",index=False)


# In[ ]:




