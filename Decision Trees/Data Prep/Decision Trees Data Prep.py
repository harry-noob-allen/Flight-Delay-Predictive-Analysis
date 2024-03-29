#!/usr/bin/env python
# coding: utf-8

# In[17]:


# importing necessary libraries
import pandas as pd

flight_df_with_weather_delay = pd.read_csv("Cleaned_Data.csv")

# coverting temperature from celcius to farenheit
flight_df_with_weather_delay['origin_temperature'] = (flight_df_with_weather_delay['origin_temperature']*1.8) + 32
flight_df_with_weather_delay['destination_temperature'] = (flight_df_with_weather_delay['destination_temperature']*1.8) + 32

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


flight_df_with_weather_delay['total_weather_delay'] = flight_df_with_weather_delay['origin_weather_delay'] + flight_df_with_weather_delay['destination_weather_delay']



# since model wont work properly when outliers are present even though they are true outliers needs to be removed. 
#And theres a article which states any delay after 12 hrs calls for automatic cancellation of flights
flight_df_with_weather_delay_filtered = flight_df_with_weather_delay[flight_df_with_weather_delay['total_weather_delay'] < 12]

# rounding up the delays
flight_df_with_weather_delay_filtered['total_weather_delay'] = round(flight_df_with_weather_delay_filtered['total_weather_delay'])


data_decision_trees = flight_df_with_weather_delay_filtered[['origin_latitude','origin_longitude','destination_latitude','destination_longitude',
                                                    'origin_temperature','destination_temperature','total_weather_delay']]

# displaying the data
print(data_decision_trees.head())

print("---------------------------------------------------------------------------\n")


# function for discretizing the weather delays into category
def delay_labels(row):
    if (row['total_weather_delay'] >= 1):
        row['total_weather_delay'] = "Extended Delay"
    else:
        row['total_weather_delay'] = "Short Delay"
    return row


# applying the function to the dataframe     
data_decision_trees = data_decision_trees.apply(delay_labels,axis=1)
# converting it to csv
data_decision_trees.to_csv("decision_trees_data.csv",index=False)



# In[ ]:




