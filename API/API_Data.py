# importing necessary libraries
import pandas as pd
import requests



# function for fetching weather data from API
def get_average_temperature(df):
    
    # initializing api url
    api_url = "https://archive-api.open-meteo.com/v1/archive"
    
    # setting the API parameters
    api_params = {
        'latitude': df['latitude'],
        'longitude': df['longitude'],
        'start_date': df['FL_DATE'],
        'end_date': df['FL_DATE'],
        'hourly': 'temperature_2m'
    }
    
    # Sendig API request
    response = requests.get(api_url, params=api_params)
    
    # Check for the response
    if response.status_code == 200:
        #Extracting data in json
        data = response.json()
        # Extracting temperature data and calculating average
        hourly_temperatures = data.get('hourly', {}).get('temperature_2m', [])
        if hourly_temperatures:
            average_temperature = sum(hourly_temperatures) / len(hourly_temperatures)
            return round(average_temperature, 2)
        
    # if response fails print the response code
    else:
        print(api_params)
        print(f"Error: {response.status_code}")
        return None



result_df = pd.read_csv("API_Input.csv")
# function for applying the function on the dataframe
# since the records are more and it takes time for api to fetch the records i divided and ran this code into 3 differnt system and has obtained the data in csv.
#final_df = pd.DataFrame()

#for i in range(0, len(result_df), 1000):
    #final_df = pd.concat([final_df,
                         #pd.concat([result_df.iloc[i:i+1000], result_df.iloc[i:i+20, :].apply(get_average_temperature, axis=1)], axis=1)], 
                         #ignore_index=True)

#final_df.columns = list(df.columns)+['temperature']

# since the records are more and it takes time for api to fetch the records i divided and ran this code into 3 differnt system and has obtained the data in csv.

# reading the api csv files
api_df1 = pd.read_csv("system1api.csv")
api_df2 = pd.read_csv("system2api.csv")
api_df3 = pd.read_csv("system3api.csv")
api_df4 = pd.read_csv("system4api.csv")
api_df5 = pd.read_csv("system5api.csv")
api_df6 = pd.read_csv("system6api.csv")

api_df5 = api_df5.drop(['Unnamed: 0'], axis=1)

# concatting all the api files
temperature_df = pd.concat([api_df1,api_df2,api_df3,api_df4,api_df5,api_df6]).drop_duplicates(subset=['FL_DATE','state', 'latitude', 'longitude'])

temperature_df = temperature_df.sort_values(by=['FL_DATE','state']).reset_index().drop(['index'],axis =1)

# coverting date to proper date time object
temperature_df['FL_DATE'] = pd.to_datetime(temperature_df['FL_DATE'])
temperature_df['FL_DATE'] = temperature_df['FL_DATE'].dt.date

# converting it into csv file
temperature_df.to_csv("API_Output.csv",index=False)