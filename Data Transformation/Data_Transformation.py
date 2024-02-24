import pandas as pd

flight_df_with_weather_delay = pd.read_csv("Cleaned_Data.csv")

# coverting temperature from celcius to farenheit
flight_df_with_weather_delay['origin_temperature'] = (flight_df_with_weather_delay['origin_temperature']*1.8) + 32
flight_df_with_weather_delay['destination_temperature'] = (flight_df_with_weather_delay['destination_temperature']*1.8) + 32

# Instead of having temperatures as individual values lets bin them together.
# For this I am going to use US Measures
#Very Cold: Below 0°F
#Cold: 0°F to 32°F
#Cool: 32°F to 50°F
#Mild: 50°F to 70°F
#Warm: 70°F to 85°F
#Hot: 85°F to 100°F
#Very Hot: Above 100°F

# setting bin edges and labels
edges = [-float('inf'), 0, 32, 50, 70, 85, 100, float('inf')]
labels = ['Below 0°F', '0 - 32°F', '32 - 50°F', '50 - 70°F', '70 - 85°F', '85 - 100°F', 'Above 100°F']

# converting temperature column into category
flight_df_with_weather_delay['origin_temperature'] = pd.cut(flight_df_with_weather_delay['origin_temperature'], bins=edges, labels=labels, right=False)
flight_df_with_weather_delay['destination_temperature'] = pd.cut(flight_df_with_weather_delay['destination_temperature'], bins=edges, labels=labels, right=False)

print("After Binning of temperatures :\n")
print("---------------------------------------------------------------------------\n")
print(flight_df_with_weather_delay.head(),"\n")
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


print(flight_df_with_weather_delay.info(),"\n")
print("---------------------------------------------------------------------------\n")

flight_df_with_weather_delay.to_csv("Preprocessed_Data.csv",index=False)
