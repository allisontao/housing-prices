import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.title('House Price Prediction')

def main():
  with st.form(key='form'):
    OverallQual = st.sidebar.selectbox('Select rating for overall quality:',(1,2,3,4,5,6,7,8,9,10))
    MoSold = st.sidebar.selectbox('Select Month Sold:',(1,2,3,4,5,6,7,8,9,10,11,12)) 
    OverallCond = st.sidebar.selectbox('Select Overall Condition Rating:',(1,2,3,4,5,6,7,8,9,10)) 
    BsmtHalfBath = st.sidebar.selectbox('Select Basement half bathrooms:',(0,1,2)) 

    LotArea = st.sidebar.text_input('LotArea') 
    BedroomAbvGr = st.sidebar.number_input('BedroomAbvGr', step=1) 
    HalfBath = st.sidebar.number_input('HalfBath', step=1) 
    GrLivArea = st.sidebar.text_input('GrLivArea')  
    KitchenAbvGr = st.sidebar.number_input('KitchenAbvGr', step=1)  
    TotRmsAbvGrd = st.sidebar.number_input('TotRmsAbvGrd', step=1) 
    FullBath = st.sidebar.number_input('FullBath', step=1) 
    BsmtFullBath = st.sidebar.number_input('BsmtFullBath', step=1)  
    YearBuilt = st.sidebar.text_input('YearBuilt')
    ThreeSsnPorch = st.sidebar.text_input('3SsnPorch')
    ScreenPorch = st.sidebar.text_input('ScreenPorch',)
    LowQualFinSF = st.sidebar.text_input('LowQualFinSF')
    YearRemodAdd = st.sidebar.text_input('YearRemodAdd')
    GarageArea = st.sidebar.text_input('GarageArea')
    EnclosedPorch = st.sidebar.text_input('EnclosedPorch')
    FirstFlrSF = st.sidebar.text_input('1stFlrSF')
    SecondFlrSF = st.sidebar.text_input('2ndFlrSF')
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
      model = pickle.load(open('model.sav', 'rb'))
      try:
        price = model.predict(data)
        st.subheader('Predicted house price:')
        st.subheader('$'+str(np.round(price[0],2)))
      except:
        st.write('Must fill out all fields to predict the price.')

main()

