#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd

arm_df = pd.read_csv("Preprocessed_Data.csv")
print(arm_df.head())
print("---------------------------------------------------------------------------\n")

# function for labelling origin temperatute
def temperature_labels_origin(row):
    if (row['origin_temperature'] == 'Below 0°F'):
        row['origin_temperature'] = "Very Cold"
    elif (row['origin_temperature'] == '0 - 32°F'):
        row['origin_temperature'] = "Cold"
    elif (row['origin_temperature'] == '32 - 50°F'):
        row['origin_temperature'] = "Cool"
    elif (row['origin_temperature'] == '50 - 70°F'):
        row['origin_temperature'] = "Mild"
    elif (row['origin_temperature'] == '70 - 85°F'):
        row['origin_temperature'] = "Warm"
    elif (row['origin_temperature'] == '85 - 100°F'):
        row['origin_temperature'] = "Hot"
    else:
        row['origin_temperature'] = "Very Hot"
    return row

# applying the function to the dataframe
arm_df = arm_df.apply(temperature_labels_origin,axis=1)

#Printing the top 5 rows for checking the origin_temperature column
print(arm_df.head())
print("---------------------------------------------------------------------------\n")

# function for discretizing the origin weather delay
def delay_labels_origin(row):
    if (row['origin_weather_delay'] >= 5):
        row['origin_weather_delay'] = "High Delay"
    elif 0 < row['origin_weather_delay'] < 5:
        row['origin_weather_delay'] = "Delay"
    else:
        row['origin_weather_delay'] = "No Delay"
    return row

# applying the function to the dataframe     
arm_df = arm_df.apply(delay_labels_origin,axis=1)

#Printing the top 5 rows for checking the origin_weather_delay column
print(arm_df.head())
print("---------------------------------------------------------------------------\n")

# filtering the required columns for ARM
arm_df_origin = arm_df[['description','origin_state','origin_temperature','origin_weather_delay']]

# converting the data to csv and dropping the headers
arm_df_origin.to_csv("arm_origin.csv",index=False,header=False)


# In[ ]:




