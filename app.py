import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.title('House Price Prediction')

def main():
  with st.form(key='form'):
    LotArea = st.sidebar.number_input('Lot size in square feet:', min_value=0)
    LowQualFinSF = st.sidebar.number_input('Low quality finished in square feet (all floors):', min_value=0)
    FirstFlrSF = st.sidebar.number_input('Number of square feet on the first floor:', min_value=0)
    SecondFlrSF = st.sidebar.number_input('Number of square feet on the second floor:', min_value=0)
    GrLivArea = st.sidebar.number_input('Ground living area in square feet:', min_value=0)
    YearBuilt = st.sidebar.number_input('Year of original construction date:', min_value= 1500, max_value=2023, value= 2010, step=1)
    YearRemodAdd = st.sidebar.number_input('Year of remodel date (if it has not been remodeled, enter the year of original construction):', min_value= YearBuilt, max_value=2023, value= 2010, step=1, help='This value should be greater than or equal to the original construction year') 
    MoSold = st.sidebar.selectbox('Select month sold (1 corresponds to January and 12 corresponds to December, etc):',(1,2,3,4,5,6,7,8,9,10,11,12)) 
    TotRmsAbvGrd = st.sidebar.number_input('Total rooms above ground (not including bathrooms):', step=1, min_value=0) 
    BedroomAbvGr = st.sidebar.number_input('Number of bedrooms above ground:', step=1, min_value=0) 
    KitchenAbvGr = st.sidebar.number_input('Number of kitchens above ground:', step=1, min_value=0)  
    BsmtFullBath = st.sidebar.number_input('Number of full bathrooms in the basement:', step=1, min_value=0)  
    FullBath = st.sidebar.number_input('Number of full bathrooms above ground:', step=1, min_value=0) 
    HalfBath = st.sidebar.number_input('Number of half baths above ground:', step=1, min_value=0) 
    BsmtHalfBath = st.sidebar.number_input('Select the number of half bathrooms in the basement:', step=1) 
    ScreenPorch = st.sidebar.number_input('Screen porch area in square feet:', min_value=0)
    ThreeSsnPorch = st.sidebar.number_input('3 Season porch area in square feet:', min_value=0)
    EnclosedPorch = st.sidebar.number_input('Enclosed porch area in square feet:', min_value=0)
    GarageArea = st.sidebar.number_input('Size of garage in square feet:', min_value=0)
    GarageCars = st.sidebar.number_input('Size of garage in car capacity:', step=1, min_value=0)
    OverallCond = st.sidebar.slider('Select overall condition rating:', min_value=1, max_value=10, step=1) 
    OverallQual = st.sidebar.slider('Select rating for overall material and finish quality:', min_value=1, max_value=10, step=1)
    
    text = st.markdown("Press submit button below after inputting house data on the left")
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
      user_data = {
        'LotArea':LotArea,
        'BedroomAbvGr':BedroomAbvGr,
        'HalfBath':HalfBath,
        'GrLivArea':GrLivArea,
        'OverallQual':OverallQual,
        'KitchenAbvGr':KitchenAbvGr,
        'TotRmsAbvGrd':TotRmsAbvGrd,
        'BsmtHalfBath':BsmtHalfBath,
        'FullBath':FullBath,
        'BsmtFullBath':BsmtFullBath,
        'MoSold':MoSold,
        'OverallCond':OverallCond,
        'YearBuilt':YearBuilt,
        'ThreeSsnPorch':ThreeSsnPorch,
        'ScreenPorch':ScreenPorch,
        'LowQualFinSF':LowQualFinSF,
        'YearRemodAdd':YearRemodAdd,
        'GarageArea':GarageArea,
        'EnclosedPorch':EnclosedPorch,
        'FirstFlrSF':FirstFlrSF,
        'SecondFlrSF':SecondFlrSF,
        'GarageCars':GarageCars,
      }

      data = pd.DataFrame(user_data, index=[0])
      model = pickle.load(open('model.sav', 'rb'))
      try:
        price = model.predict(data)
        formatted_price = "{:,.2f}".format(price[0])
        st.subheader('Predicted house price:')
        st.subheader('$'+formatted_price)
      except:
        st.write('Must fill out all fields to predict the price.')

main()

