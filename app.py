import streamlit as st
import pandas as pd
import numpy as np
import pickle

def main():
  with st.form(key='form'):
    LotArea = st.text_input("LotArea")
    BedroomAbvGr = st.text_input("BedroomAbvGr")
    HalfBath = st.text_input("HalfBath")
    GrLivArea = st.text_input("GrLivArea")
    OverallQual = st.text_input("OverallQual")
    KitchenAbvGr = st.text_input("KitchenAbvGr")
    TotRmsAbvGrd = st.text_input("TotRmsAbvGrd")
    BsmtHalfBath = st.text_input("BsmtHalfBathr")
    FullBath = st.text_input("FullBath")
    BsmtFullBath = st.text_input("BsmtFullBath")
    MoSold = st.text_input("MoSold")
    OverallCond = st.text_input("OverallCond")
    YearBuilt = st.text_input("YearBuilt")
    ThreeSsnPorch = st.text_input("3SsnPorch")
    ScreenPorch = st.text_input("ScreenPorch")
    LowQualFinSF = st.text_input("LowQualFinSF")
    YearRemodAdd = st.text_input("YearRemodAdd")
    GarageArea = st.text_input("GarageArea")
    EnclosedPorch = st.text_input("EnclosedPorch")
    FirstFlrSF = st.text_input("1stFlrSF")
    SecondFlrSF = st.text_input("2ndFlrSF")
    GarageCars = st.text_input("GarageCars")
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
      price = model.predict(data)
      st.write('Predicted house price is: $'+str(price[0]))

main()
