# importing necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# reading the merged dataset
flight_df_with_weather_delay = pd.read_csv("Merged_Dataset.csv")

# checking for nulls
flight_df_with_weather_delay.isnull().sum()

# since our focus is on delay other columns like cancelled,cancellation code,diverted can be removed
flight_df_with_weather_delay = flight_df_with_weather_delay.drop(
                                                            ['CANCELLED',
                                                             'CANCELLATION_CODE',
                                                             'DIVERTED'],axis=1)

# removing insignificant columns: tailnum, dep time, arrival time, distance, airtime
flight_df_with_weather_delay = flight_df_with_weather_delay.drop(
                                                            ['CRS_DEP_TIME',
                                                             'DEP_TIME',
                                                             'CRS_ARR_TIME',
                                                             'ARR_TIME',
                                                             'CRS_ELAPSED_TIME',
                                                             'ACTUAL_ELAPSED_TIME',
                                                             'AIR_TIME',
                                                             'DISTANCE',
                                                             'TAXI_OUT',
                                                             'TAXI_IN',
                                                             'WHEELS_OFF',
                                                             'WHEELS_ON'],axis=1)


# % of null values in LATE_AIRCRAFT_DELAY 
print("% of null values in LATE_AIRCRAFT_DELAY is :",(flight_df_with_weather_delay['LATE_AIRCRAFT_DELAY'].isnull().sum()/flight_df_with_weather_delay.shape[0])*100,"\n")

# Since 83% of values are null LATE_AIRCRAFT_DELAY must be dropped
flight_df_with_weather_delay = flight_df_with_weather_delay.drop(['LATE_AIRCRAFT_DELAY'],axis=1)

print("---------------------------------------------------------------------------\n")

# checking for nulls
print(flight_df_with_weather_delay.isnull().sum(),"\n")

print("---------------------------------------------------------------------------\n")

# checking the data types of columns
print(flight_df_with_weather_delay.info(),"\n")

print("---------------------------------------------------------------------------\n")


# changing the datatype of FL_DATE to datetime datatype
flight_df_with_weather_delay['FL_DATE'] = pd.to_datetime(flight_df_with_weather_delay['FL_DATE'],format='%m/%d/%Y %I:%M:%S %p')

# date transformation
flight_df_with_weather_delay['month'] = flight_df_with_weather_delay['FL_DATE'].dt.month
flight_df_with_weather_delay['day'] = flight_df_with_weather_delay['FL_DATE'].dt.day
flight_df_with_weather_delay['week'] = flight_df_with_weather_delay['FL_DATE'].dt.isocalendar().week
flight_df_with_weather_delay['FL_DATE'] = flight_df_with_weather_delay['FL_DATE'].dt.date

# checking the data types of columns
print(flight_df_with_weather_delay.info(),"\n")

print("---------------------------------------------------------------------------\n")


# adding latitude and longitude data from webscraping
# url for web scraping
url = "https://developers.google.com/public-data/docs/canonical/states_csv"
# creating a variable for reading html
tables = pd.read_html(url)
if tables:
    # since our required data is in the only table present in the site, directly storing it in dataframe
    latlon_df = tables[0]
else:
    print("No tables found on the webpage.")
    
    
# displaying web scraped data
print(latlon_df.head(),"\n")

print("---------------------------------------------------------------------------\n")

# checking for nulls
print(latlon_df.info(),"\n")

print("---------------------------------------------------------------------------\n")

# function for joining latitude longitude details to the main dataset
def merge_latlon_data(flight_df, latlon_df,left_table,origin_or_destination):
    merged_df = pd.merge(flight_df, 
                         latlon_df, 
                         left_on=left_table, 
                         right_on='state', 
                         how='left').rename(columns=
                                            {'latitude': origin_or_destination +
                                             '_latitude', 'longitude': origin_or_destination +
                                             '_longitude','name' : origin_or_destination +
                                             '_state'})
    return merged_df.drop(['state'], axis=1, errors='ignore')

# joining for origin city
flight_df_with_weather_delay = merge_latlon_data(flight_df_with_weather_delay,latlon_df,'ORIGIN_STATE_ABR','origin')
# joining for destination city
flight_df_with_weather_delay = merge_latlon_data(flight_df_with_weather_delay,latlon_df,'DEST_STATE_ABR','destination')


# filtering out the null columns
null_latlon_df = flight_df_with_weather_delay[flight_df_with_weather_delay['origin_latitude'].isnull()]

# plotting box plot to figure which states informatio is missing
sns.countplot(x=null_latlon_df['ORIGIN_STATE_ABR'])
plt.title("States without Latitude Information", fontsize=16)
plt.xlabel("State Code")
plt.ylabel("Count")
plt.show()

print("---------------------------------------------------------------------------\n")

# Upon further analysis the state VI stands for U.S. Virgin Islands and TT stands for Trusted territories
# The other issue is though the latitude and longitude of TT is a set of numbers as these are group of islands.
# Since the proportion of TT is very low it can be removed and latitude longitude information of Virgin Islands can be manually added

latlon_df.loc[len(latlon_df.index)] = ['VI', 8.3358, 64.8963,'U.S. Virgin Islands'] 


# removing the state code TT
flight_df_with_weather_delay = flight_df_with_weather_delay[flight_df_with_weather_delay['ORIGIN_STATE_ABR'] != 'TT']
flight_df_with_weather_delay = flight_df_with_weather_delay[flight_df_with_weather_delay['DEST_STATE_ABR'] != 'TT']

# filtering out the null columns
null_latlon_df = flight_df_with_weather_delay[flight_df_with_weather_delay['origin_latitude'].isnull()]

# plotting box plot to figure which states informatio is missing
sns.countplot(x=null_latlon_df['ORIGIN_STATE_ABR'])
plt.title("States without Latitude Information", fontsize=16)
plt.xlabel("State Code")
plt.ylabel("Count")
plt.show()

print("---------------------------------------------------------------------------\n")

# fill na values
flight_df_with_weather_delay.loc[:, ['origin_latitude', 'destination_latitude']] = flight_df_with_weather_delay[['origin_latitude', 'destination_latitude']].fillna(8.3358)
flight_df_with_weather_delay.loc[:, ['origin_longitude', 'destination_longitude']] = flight_df_with_weather_delay[['origin_longitude', 'destination_longitude']].fillna(64.8963)
flight_df_with_weather_delay.loc[:, ['origin_state', 'destination_state']] = flight_df_with_weather_delay[['origin_state', 'destination_state']].fillna("U.S. Virgin Islands")

# since the state name of destination and origin is available the state abr can be removed
flight_df_with_weather_delay = flight_df_with_weather_delay.drop(['DEST_STATE_ABR','ORIGIN_STATE_ABR'],axis=1)

# checking the value counts of OP_UNIQUE_CARRIER
flight_df_with_weather_delay['OP_UNIQUE_CARRIER'].value_counts()

# checking the value counts of OP_CARRIER_AIRLINE_ID
flight_df_with_weather_delay['OP_CARRIER_AIRLINE_ID'].value_counts()

# since both columns offers the same information one of the columns can be removed. Dropping OP_CARRIER_AIRLINE_ID
flight_df_with_weather_delay = flight_df_with_weather_delay.drop(['OP_CARRIER_AIRLINE_ID'],axis=1)

# instead of carrier code its better to have carrier name
carrier_df = pd.read_csv("carriers.csv")

# function for joining latitude longitude details to the main dataset
def merge_carrier_data(flight_df, carrier_df):
    merged_df = pd.merge(flight_df, carrier_df, left_on='OP_UNIQUE_CARRIER', right_on='Code', how='left')
    return merged_df

# joining carrier data
flight_df_with_weather_delay = merge_carrier_data(flight_df_with_weather_delay,carrier_df)

# OP_UNIQUE_CARRIER and code can be dropped
flight_df_with_weather_delay = flight_df_with_weather_delay.drop(['OP_UNIQUE_CARRIER','Code'],axis=1)


# since the number of records are huge and api limit is 10000 grouping by unique records on the basis of date,latitude,longitude,state

temp_df = flight_df_with_weather_delay[['FL_DATE','origin_state','origin_latitude','origin_longitude']].drop_duplicates(subset=['FL_DATE','origin_state','origin_latitude','origin_longitude'])
temp_df=temp_df.rename(columns={'origin_state':'state', 'origin_latitude': 'latitude','origin_longitude' : 'longitude'})
temp_df1 = flight_df_with_weather_delay[['FL_DATE','destination_state','destination_latitude','destination_longitude']].drop_duplicates(subset=['FL_DATE','destination_state','destination_latitude','destination_longitude'])
temp_df1=temp_df1.rename(columns={'destination_state':'state', 'destination_latitude': 'latitude','destination_longitude' : 'longitude'})
result_df = pd.concat([temp_df, temp_df1]).drop_duplicates(subset=['FL_DATE','state', 'latitude', 'longitude'])

result_df.to_csv("API_Input.csv",index=False)

# function for joining latitude longitude details to the main dataset
def merge_temperature_data(flight_df, temperature_df,origin_or_destination):
    if (origin_or_destination == "origin"):
        merged_df = pd.merge(flight_df, temperature_df, left_on=['FL_DATE','origin_state'], right_on=['FL_DATE','state'], how='left').rename(columns={'temperature' : origin_or_destination +'_temperature'})
    else:
        merged_df = pd.merge(flight_df, temperature_df, left_on=['FL_DATE','destination_state'], right_on=['FL_DATE','state'], how='left').rename(columns={'temperature' : origin_or_destination +'_temperature'})
    return merged_df.drop(['state','latitude','longitude'], axis=1, errors='ignore')

# reading API data
temperature_df = pd.read_csv("API_Output.csv")

# converting into proper data types for merging
temperature_df['FL_DATE'] = pd.to_datetime(temperature_df['FL_DATE'])
temperature_df['FL_DATE'] = temperature_df['FL_DATE'].dt.date

# merging temperature to the main dataframe
flight_df_with_weather_delay = merge_temperature_data(flight_df_with_weather_delay,temperature_df,'origin')
flight_df_with_weather_delay = merge_temperature_data(flight_df_with_weather_delay,temperature_df,'destination')

print(flight_df_with_weather_delay.head(),"\n")

# changing the airport ids to categorical
flight_df_with_weather_delay['ORIGIN_AIRPORT_ID'] = flight_df_with_weather_delay['ORIGIN_AIRPORT_ID'].astype('category')
flight_df_with_weather_delay['DEST_AIRPORT_ID'] = flight_df_with_weather_delay['DEST_AIRPORT_ID'].astype('category')

print("---------------------------------------------------------------------------\n")

# filtering columns in which delay validation fails
rows_to_drop = flight_df_with_weather_delay[
    (flight_df_with_weather_delay['WEATHER_DELAY'] > flight_df_with_weather_delay['DEP_DELAY']) &
    (flight_df_with_weather_delay['ARR_DELAY'] != (flight_df_with_weather_delay['CARRIER_DELAY'] + flight_df_with_weather_delay['WEATHER_DELAY'] + flight_df_with_weather_delay['NAS_DELAY'] + flight_df_with_weather_delay['SECURITY_DELAY']))
].index

# dropping columns columns in which delay validation fails
flight_df_with_weather_delay.drop(index=rows_to_drop, inplace=True)

# replacing negative departure values as 0 as it doesnt mean any delay
flight_df_with_weather_delay['DEP_DELAY'] = flight_df_with_weather_delay['DEP_DELAY'].apply(lambda x: max(0, x))

# function for computing origin and destination weather delay
def origin_delay(row):
    if row['DEP_DELAY'] < row['ARR_DELAY']:
        if row['WEATHER_DELAY'] <= row['DEP_DELAY']:
            return row['WEATHER_DELAY'], 0
        else:
            return row['DEP_DELAY'], row['WEATHER_DELAY'] - row['DEP_DELAY']
    else:
        return row['WEATHER_DELAY'], 0

flight_df_with_weather_delay[['origin_weather_delay', 'destination_weather_delay']] = flight_df_with_weather_delay.apply(lambda row: pd.Series(origin_delay(row), index=['origin_weather_delay', 'destination_weather_delay']), axis=1)

# dropping weather_delay column
flight_df_with_weather_delay = flight_df_with_weather_delay.drop(['WEATHER_DELAY'],axis=1)

print(flight_df_with_weather_delay.head(),"\n")

print("---------------------------------------------------------------------------\n")
flight_df_with_weather_delay.to_csv("Cleaned_Data.csv",index=False)


