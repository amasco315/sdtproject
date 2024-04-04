import streamlit as st
import pandas as pd
import plotly.express as px

vehicles = pd.read_csv('./vehicles_us.csv')
vehicles['is_4wd'] = vehicles['is_4wd'].fillna(0)
vehicles['paint_color'] = vehicles['paint_color'].fillna('n/a')
vehicles['odometer'] = vehicles['odometer'].fillna('n/a')
vehicles['model_year'] = vehicles['model_year'].fillna('n/a')
vehicles['cylinders'] = vehicles['cylinders'].fillna('n/a')
vehicles['manufacturer']=vehicles['model'].apply(lambda x: x.split()[0])
# Text Header
st.header('Data Viewer')
# display dataframe 
st.dataframe(vehicles)

st.header('Price of vehicles by model year for each manufacturer')
# create plotly scatterplot
fig1 = px.scatter(vehicles,
                  x='model_year',
                  y='price',
                  color='manufacturer',
                  color_discrete_sequence=px.colors.qualitative.Alphabet)
fig1.update_layout(xaxis_range=[1900,2020])
# display scatterplot
st.write(fig1)

st.header('Compare Condition of Vehicles between Manufacturers')
# get a list of car manufacturers
manufac_list = sorted(vehicles['manufacturer'].unique())
# get user's inputs from a dropdown menu
manufacturer_1 = st.selectbox(
                              label='Select manufacturer 1', # title of the select box
                              options=manufac_list, # options listed in the select box
                              index=manufac_list.index('chevrolet') # default pre-selected option
                              )
# repeat for the second dropdown menu
manufacturer_2 = st.selectbox(
                              label='Select manufacturer 2',
                              options=manufac_list, 
                              index=manufac_list.index('hyundai')
                              )
# filter the dataframe 
mask_filter = (vehicles['manufacturer'] == manufacturer_1) | (vehicles['manufacturer'] == manufacturer_2)
vehicles_filtered = vehicles[mask_filter]

# add a checkbox if a user wants to normalize the histogram
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None

# create a plotly histogram figure
fig2 = px.histogram(vehicles_filtered,
                      x='condition',
                      nbins=30,
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay')
# display the figure with streamlit
st.write(fig2)
