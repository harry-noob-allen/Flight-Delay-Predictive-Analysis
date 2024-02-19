# importing necessary libraries
import glob
import pandas as pd

# reading all the monthly files for the year 2022 and 2023 files and concatenating it
flight_df = pd.concat(map(pd.read_csv, glob.glob('*.csv')))

# Since our focus is on weather delated delays we are filtering the rows only with weather delay
flight_df_with_weather_delay = flight_df[flight_df['WEATHER_DELAY'] > 0]

# Converting the merged data into csv for further process
flight_df_with_weather_delay.to_csv("Merged_Dataset.csv",index=False)