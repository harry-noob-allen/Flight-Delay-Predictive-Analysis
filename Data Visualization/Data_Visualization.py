import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

flight_df_with_weather_delay = pd.read_csv("Preprocessed_Data.csv")

# Lets visualize the distribution of temperature before binning
fig = px.box(flight_df_with_weather_delay, y=["origin_temperature", "destination_temperature"],template= 'seaborn')
fig.show()
print("------------------------------------------------------------------------------------------------------------------------------------------------------\n")
fig = px.box(flight_df_with_weather_delay, x = ["departure_delay", "arrival_delay","weather_delay"],template= 'seaborn', title="Box Plots of various delays",color_discrete_sequence=['#ee9b00'])
fig.show()

print("------------------------------------------------------------------------------------------------------------------------------------------------------\n")

categoricals = ['origin_temperature','destination_temperature']

for category in categoricals:
    fig = px.histogram(flight_df_with_weather_delay, x=category,template= 'seaborn',title = f'Histogram of {category}',color_discrete_sequence=['#1A85FF'])
    fig.show()
print("------------------------------------------------------------------------------------------------------------------------------------------------------\n") 
fig = px.violin(flight_df_with_weather_delay, x='origin_temperature', y='weather_delay', points="all")
fig.update_layout(
            template = 'seaborn',
            title = ' Viloin Plot of Temperatures',
            title_x = 0.5,
            yaxis = dict(
                title = 'Weather Delays (in hrs)',
                title_font_size = 14,),
            xaxis = dict(
                title = 'Temperatures',
                title_font_size = 14,
            
            ),
                 
    )
fig.show()

print("------------------------------------------------------------------------------------------------------------------------------------------------------\n")
dep_delay_mean = flight_df_with_weather_delay.groupby('month')['departure_delay'].mean().reset_index()
avg_arr_delay_mean = flight_df_with_weather_delay.groupby('month')['arrival_delay'].mean().reset_index()


fig = go.Figure()

fig.add_trace(go.Scatter(x=dep_delay_mean['month'], y=dep_delay_mean['departure_delay'],
                         mode='lines+markers', name='Departure Delay',
                         line=dict(color='red'), marker=dict(color='red')))


fig.add_trace(go.Scatter(x=avg_arr_delay_mean['month'], y=avg_arr_delay_mean['arrival_delay'],
                         mode='lines+markers', name='Arrival Delay',
                         line=dict(color='blue'), marker=dict(color='blue')))



month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}


fig.update_layout(
    title='Line Plot for Average Departure/Arrival Delays - Monthly',
    title_x=0.455,
    yaxis=dict(
        title='Mean Departure/Arrival Delay (in hrs)',
        title_font_size=14,
    ),
    xaxis=dict(
        tickvals=list(month_dict.keys()),
        ticktext=list(month_dict.values()),
        title='Month',
        title_font_size=14,
    ),
    template='seaborn',
)

fig.show()

print("------------------------------------------------------------------------------------------------------------------------------------------------------\n")
fig = px.scatter(flight_df_with_weather_delay, x='origin_longitude', y='origin_latitude', color = 'origin_state', size='weather_delay', hover_data=['origin_airport_id'],template='seaborn',size_max=40)
fig.update_layout(width = 1200,
                  title='Geographical Distribution of Weather Delays (Origin)')

fig.show()

print("------------------------------------------------------------------------------------------------------------------------------------------------------\n")
fig = px.scatter(flight_df_with_weather_delay, x='destination_longitude', y='destination_latitude', color = 'destination_state', size='weather_delay', hover_data=['destination_airport_id'],template='seaborn',size_max=40)
fig.update_layout(width = 1200,
                  title='Geographical Distribution of Weather Delays (Destination)')

fig.show()
print("------------------------------------------------------------------------------------------------------------------------------------------------------\n")

num_matrix = flight_df_with_weather_delay[['carrier_delay','weather_delay','nas_delay','security_delay']]
corr_matrix = num_matrix.corr()
fig = px.imshow(corr_matrix, text_auto=True,template='seaborn',color_continuous_scale=px.colors.sequential.Cividis_r)
fig.update_layout(title='Heatmap of various delays')
fig.show()

delay_columns = ['carrier_delay', 'weather_delay', 'nas_delay', 'security_delay']
delay_percentages = flight_df_with_weather_delay[delay_columns].mean() / flight_df_with_weather_delay[delay_columns].sum().sum() * 100


delay_data = pd.DataFrame({
    'Delay Type': delay_percentages.index,
    'Percentage': delay_percentages.values
})


fig = go.Figure(data=[go.Pie(labels=delay_data['Delay Type'], values=delay_data['Percentage'], hole=.5,marker=dict(colors=px.colors.sequential.RdBu, line=dict(color='black', width=2)))])

fig.update_layout(
    title='Percentage of Various Delays',
    title_x=0.515,
    template='seaborn',
    legend=dict(
        x=0.9, 
        y=0.5, 
        traceorder='normal',
    )
)
fig.show()
print("------------------------------------------------------------------------------------------------------------------------------------------------------\n")

weather_delay_mean = flight_df_with_weather_delay.groupby('origin_state')['weather_delay'].mean().reset_index()
sorted_df = weather_delay_mean.sort_values(by = ['weather_delay'], ascending = True)
sorted_df = sorted_df.tail(10)


fig = go.Figure()
fig.add_trace(go.Bar(x = sorted_df['weather_delay'], y = sorted_df['origin_state'],   
                     orientation = 'h',marker_color ='#62ba97'))


fig.update_layout(
            title = 'Bar Graph of Top 10 States with Highest Average Weather Delays',
            title_x = 0.5,
            barmode = 'group',
            yaxis = dict(
                title = 'States',
                title_font_size = 14,),
            xaxis = dict(
                title = 'Average Weather Delay (in hr)',
                title_font_size = 14,
            ),
            
            template = 'seaborn'
            
                 
    )

fig.show()
print("------------------------------------------------------------------------------------------------------------------------------------------------------\n")

weather_delay_mean = flight_df_with_weather_delay.groupby('origin_temperature')['weather_delay'].mean().reset_index()
nas_delay_mean = flight_df_with_weather_delay.groupby('origin_temperature')['nas_delay'].mean().reset_index()
carrier_delay_mean = flight_df_with_weather_delay.groupby('origin_temperature')['carrier_delay'].mean().reset_index()
security_delay_mean = flight_df_with_weather_delay.groupby('origin_temperature')['security_delay'].mean().reset_index()

fig = go.Figure()

fig.add_trace(go.Bar(x = weather_delay_mean['origin_temperature'], y = weather_delay_mean['weather_delay'],  
                     name = 'Weather_Delay',marker_color='#D41159'))
fig.add_trace(go.Bar(x = nas_delay_mean['origin_temperature'], y = nas_delay_mean['nas_delay'],  
                     name = 'NAS_Delay'))
fig.add_trace(go.Bar(x = carrier_delay_mean['origin_temperature'], y = carrier_delay_mean['carrier_delay'],  
                     name = 'Carrier_Delay'))
fig.add_trace(go.Bar(x = security_delay_mean['origin_temperature'], y = security_delay_mean['security_delay'],  
                     name = 'Security_Delay'))



fig.update_layout(
            template = 'seaborn',
            legend = dict(y = 0.5),
            title = 'Bar Graph of comparison of various Delays across various temperatures',
            title_x = 0.45,
            barmode = 'relative',
            yaxis = dict(
                title = 'Average Delays (in hrs)',
                title_font_size = 14,),
            xaxis = dict(
                title = 'Temperature',
                title_font_size = 14,
            
            ),
                 
    )


fig.show()

weather_delay_mean = flight_df_with_weather_delay.groupby('description')['weather_delay'].mean().reset_index()
nas_delay_mean = flight_df_with_weather_delay.groupby('description')['nas_delay'].mean().reset_index()

print("------------------------------------------------------------------------------------------------------------------------------------------------------\n")

fig = go.Figure()

fig.add_trace(go.Bar(x=weather_delay_mean['description'], y=weather_delay_mean['weather_delay'], name='Weather Delay',marker_color = "#cc2936"))
fig.add_trace(go.Bar(x=nas_delay_mean['description'], y=nas_delay_mean['nas_delay'], name='NAS Delay',marker_color = "#08415c"))

fig.update_layout(
            template = 'seaborn',
            legend = dict(y = 0.5),
            title = ' Grouped Bar Chart of comparison of Delays across various Airlines',
            title_x = 0.45,
            barmode = 'group',
            yaxis = dict(
                title = 'Average Delays (in hrs)',
                title_font_size = 14,),
            xaxis = dict(
                title = 'Airlines',
                title_font_size = 14,
            
            ),
                 
    )

fig.show()

print("------------------------------------------------------------------------------------------------------------------------------------------------------\n")