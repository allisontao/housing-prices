import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.title('House Price Prediction')
st.sidebar.header('House Data')


def main():
  with st.form(key='form'):
    OverallQual = st.sidebar.selectbox('Select rating for overall quality:',(1,2,3,4,5,6,7,8,9,10))
    MoSold = st.sidebar.selectbox('Select Month Sold:',(1,2,3,4,5,6,7,8,9,10,11,12)) 
    OverallCond = st.sidebar.selectbox('Select Overall Condition Rating:',(1,2,3,4,5,6,7,8,9,10)) 
    BsmtHalfBath = st.sidebar.selectbox('Select Basement half bathrooms:',(0,1,2)) 

    LotArea = st.sidebar.number_input('LotArea', step=1) 
    BedroomAbvGr = st.sidebar.number_input('BedroomAbvGr', step=1) 
    HalfBath = st.sidebar.number_input('HalfBath', step=1) 
    GrLivArea = st.sidebar.number_input('GrLivArea', step=1)  
    KitchenAbvGr = st.sidebar.number_input('KitchenAbvGr', step=1)  
    TotRmsAbvGrd = st.sidebar.number_input('TotRmsAbvGrd', step=1) 
    FullBath = st.number_input('FullBath', step=1) 
    BsmtFullBath = st.sidebar.number_input('BsmtFullBath', step=1)  
    YearBuilt = st.sidebar.number_input('YearBuilt', min_value= 1600, max_value=2023, value= 2000, step=1)
    ThreeSsnPorch = st.sidebar.number_input('3SsnPorch', step=1)
    ScreenPorch = st.sidebar.number_input('ScreenPorch', step=1)
    LowQualFinSF = st.sidebar.number_input('LowQualFinSF', step=1)
    YearRemodAdd = st.sidebar.number_input('YearRemodAdd', step=1)
    GarageArea = st.sidebar.number_input('GarageArea', step=1)
    EnclosedPorch = st.sidebar.number_input('EnclosedPorch', step=1)
    FirstFlrSF = st.sidebar.number_input('1stFlrSF', step=1)
    SecondFlrSF = st.sidebar.number_input('2ndFlrSF', step=1)
    GarageCars = st.sidebar.number_input('GarageCars', step=1)
    
    submit_button = st.form_submit_button(label='Enter')

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
      return data
    
  
house_data = main()
st.write(house_data)

model = pickle.load(open('model.sav', 'rb'))
price = model.predict(house_data)
st.subheader('Predicted house price:')
st.subheader('$'+str(np.round(price[0],2)))