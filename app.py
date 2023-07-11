import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time

st.title('House Price Prediction')

def main():
  with st.form(key='form'):
    YearBuilt = st.sidebar.number_input('Year of original construction date:', min_value= 1500, max_value=2023, value= 2010, step=1)
    YearRemodAdd = st.sidebar.number_input('Year of remodel date (if it has not been remodeled, enter the year of original construction):', min_value= YearBuilt, max_value=2023, value= YearBuilt, step=1, help='This value should be greater than or equal to the original construction year') 
    YrSold = st.sidebar.number_input('Year the house was sold:', min_value= 1500, max_value=2023, value= 2010, step=1)
    MoSold = st.sidebar.selectbox('Select month sold (1 corresponds to January and 12 corresponds to December, etc):',(1,2,3,4,5,6,7,8,9,10,11,12))
    MSSubClass = st.sidebar.number_input('Building class:', min_value=0)
    GrLivArea = st.sidebar.number_input('Ground living area in square feet:', min_value=0)
    MasVnrArea = st.sidebar.number_input('Masonry veneer area in square feet:', min_value=0)
    PoolArea = st.sidebar.number_input('Pool area in square feet:', min_value=0)
    TotRmsAbvGrd = st.sidebar.number_input('Total rooms above ground (not including bathrooms):', step=1, min_value=0) 
    BedroomAbvGr = st.sidebar.number_input('Number of bedrooms above ground:', step=1, min_value=0) 
    KitchenAbvGr = st.sidebar.number_input('Number of kitchens above ground:', step=1, min_value=0)
    Fireplaces = st.sidebar.number_input('Number of fireplaces:', step=1, min_value=0)
    BsmtFullBath = st.sidebar.number_input('Number of full bathrooms in the basement:', step=1, min_value=0)  
    FullBath = st.sidebar.number_input('Number of full bathrooms above ground:', step=1, min_value=0) 
    HalfBath = st.sidebar.number_input('Number of half baths above ground:', step=1, min_value=0) 
    BsmtHalfBath = st.sidebar.number_input('Select the number of half bathrooms in the basement:', step=1) 
    ScreenPorch = st.sidebar.number_input('Screen porch area in square feet:', min_value=0)
    GarageCars = st.sidebar.number_input('Size of garage in car capacity:', step=1, min_value=0)
    OverallCond = st.sidebar.slider('Select overall condition rating:', min_value=1, max_value=10, step=1) 
    OverallQual = st.sidebar.slider('Select rating for overall material and finish quality:', min_value=1, max_value=10, step=1)
    
    st.markdown("Press submit button below after inputting house data on the left to get the predicted house price!")
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
   
      user_data = {
      'OverallQual':OverallQual, 
      'GarageCars':GarageCars, 
      'KitchenAbvGr':KitchenAbvGr, 
      'BedroomAbvGr':BedroomAbvGr,
      'BsmtFullBath':BsmtFullBath, 
      'OverallCond':OverallCond, 
      'TotRmsAbvGrd':TotRmsAbvGrd, 
      'Fireplaces':Fireplaces, 
      'FullBath':FullBath, 
      'HalfBath':HalfBath, 
      'BsmtHalfBath':BsmtHalfBath, 
      'YrSold':YrSold, 
      'YearBuilt':YearBuilt, 
      'MSSubClass':MSSubClass,
      'YearRemodAdd':YearRemodAdd, 
      'ScreenPorch':ScreenPorch, 
      'MoSold':MoSold, 
      'PoolArea':PoolArea, 
      'GrLivArea':GrLivArea,
      'MasVnrArea':MasVnrArea
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

        # modelCoefficients = model.coef_
        # print(modelCoefficients)
        # column_names = ['LotArea', 'BedroomAbvGr', 'HalfBath', 'GrLivArea', 'OverallQual', 'KitchenAbvGr',
        #         'TotRmsAbvGrd', 'BsmtHalfBath', 'FullBath', 'BsmtFullBath', 'MoSold', 'OverallCond',
        #         'YearBuilt', '3SsnPorch', 'ScreenPorch', 'LowQualFinSF', 'YearRemodAdd', 'GarageArea',
        #         'EnclosedPorch', '1stFlrSF', '2ndFlrSF', 'GarageCars']
        # # Create a pandas DataFrame with your data
        # coef_df = pd.DataFrame({
        #     'Features': column_names,
        #     'Coefficients': modelCoefficients
        # })

        # # Set 'Features' as index
        # coef_df = coef_df.set_index('Features')

        # # Convert index to CategoricalIndex with categories in original order
        # coef_df.index = pd.CategoricalIndex(coef_df.index, categories=column_names, ordered=True)

        # # Sort index according to the category order specified
        # coef_df = coef_df.sort_index()

        # # Use DataFrame in Streamlit
        # st.bar_chart(coef_df)

      
        # user_data_addedArea = { #taking user lot area parameter and adding 100 sqft, comparing new prediction with based prediction to see effect
        # 'LotArea':LotArea + 100,
        # 'BedroomAbvGr':BedroomAbvGr,
        # 'HalfBath':HalfBath,
        # 'GrLivArea':GrLivArea,
        # 'OverallQual':OverallQual,
        # 'KitchenAbvGr':KitchenAbvGr,
        # 'TotRmsAbvGrd':TotRmsAbvGrd,
        # 'BsmtHalfBath':BsmtHalfBath,
        # 'FullBath':FullBath,
        # 'BsmtFullBath':BsmtFullBath,
        # 'MoSold':MoSold,
        # 'OverallCond':OverallCond,
        # 'YearBuilt':YearBuilt,
        # 'ThreeSsnPorch':ThreeSsnPorch,
        # 'ScreenPorch':ScreenPorch,
        # 'LowQualFinSF':LowQualFinSF,
        # 'YearRemodAdd':YearRemodAdd,
        # 'GarageArea':GarageArea,
        # 'EnclosedPorch':EnclosedPorch,
        # 'FirstFlrSF':FirstFlrSF,
        # 'SecondFlrSF':SecondFlrSF,
        # 'GarageCars':GarageCars,
        # }
        # data_addedArea = pd.DataFrame(user_data_addedArea, index=[0])
        # price_addedArea = model.predict(data_addedArea)
        # f_price_addedArea = "{:,.2f}".format(price_addedArea[0])
        # st.metric("Value of Adding 100sq.feet", f_price_addedArea, delta = formatted_price, delta_color = "normal", help = None, label_visibility = "visible")

        # user_data_addBedAbvGr = {
        # 'LotArea':LotArea,
        # 'BedroomAbvGr':BedroomAbvGr + 1,
        # 'HalfBath':HalfBath,
        # 'GrLivArea':GrLivArea,
        # 'OverallQual':OverallQual,
        # 'KitchenAbvGr':KitchenAbvGr,
        # 'TotRmsAbvGrd':TotRmsAbvGrd,
        # 'BsmtHalfBath':BsmtHalfBath,
        # 'FullBath':FullBath,
        # 'BsmtFullBath':BsmtFullBath,
        # 'MoSold':MoSold,
        # 'OverallCond':OverallCond,
        # 'YearBuilt':YearBuilt,
        # 'ThreeSsnPorch':ThreeSsnPorch,
        # 'ScreenPorch':ScreenPorch,
        # 'LowQualFinSF':LowQualFinSF,
        # 'YearRemodAdd':YearRemodAdd,
        # 'GarageArea':GarageArea,
        # 'EnclosedPorch':EnclosedPorch,
        # 'FirstFlrSF':FirstFlrSF,
        # 'SecondFlrSF':SecondFlrSF,
        # 'GarageCars':GarageCars,
        # }
        # data_addBedAbvGr = pd.DataFrame(user_data_addBedAbvGr, index=[0])
        # price_addBedAbvGr = model.predict(data_addBedAbvGr)
        # f_price_addBedAbvGr = "{:,.2f}".format(price_addBedAbvGr[0])
        # st.metric("Value of Adding a Bedroom Above the Garage", f_price_addBedAbvGr, delta = formatted_price, delta_color = "normal", help = None, label_visibility = "visible")

        # user_data_addHalfBath = {
        # 'LotArea':LotArea,
        # 'BedroomAbvGr':BedroomAbvGr,
        # 'HalfBath':HalfBath + 1,
        # 'GrLivArea':GrLivArea,
        # 'OverallQual':OverallQual,
        # 'KitchenAbvGr':KitchenAbvGr,
        # 'TotRmsAbvGrd':TotRmsAbvGrd,
        # 'BsmtHalfBath':BsmtHalfBath,
        # 'FullBath':FullBath,
        # 'BsmtFullBath':BsmtFullBath,
        # 'MoSold':MoSold,
        # 'OverallCond':OverallCond,
        # 'YearBuilt':YearBuilt,
        # 'ThreeSsnPorch':ThreeSsnPorch,
        # 'ScreenPorch':ScreenPorch,
        # 'LowQualFinSF':LowQualFinSF,
        # 'YearRemodAdd':YearRemodAdd,
        # 'GarageArea':GarageArea,
        # 'EnclosedPorch':EnclosedPorch,
        # 'FirstFlrSF':FirstFlrSF,
        # 'SecondFlrSF':SecondFlrSF,
        # 'GarageCars':GarageCars,
        # }
        # data_addHalfBath = pd.DataFrame(user_data_addHalfBath, index=[0])
        # price_addHalfBath = model.predict(data_addHalfBath)
        # f_price_addHalfBath = "{:,.2f}".format(price_addHalfBath[0])
        # st.metric("Value of Adding a Half-Bathroom", f_price_addHalfBath, delta = formatted_price, delta_color = "normal", help = None, label_visibility = "visible")

        # user_data_addGrLivArea = {
        # 'LotArea':LotArea,
        # 'BedroomAbvGr':BedroomAbvGr,
        # 'HalfBath':HalfBath,
        # 'GrLivArea':GrLivArea + 100,
        # 'OverallQual':OverallQual,
        # 'KitchenAbvGr':KitchenAbvGr,
        # 'TotRmsAbvGrd':TotRmsAbvGrd,
        # 'BsmtHalfBath':BsmtHalfBath,
        # 'FullBath':FullBath,
        # 'BsmtFullBath':BsmtFullBath,
        # 'MoSold':MoSold,
        # 'OverallCond':OverallCond,
        # 'YearBuilt':YearBuilt,
        # 'ThreeSsnPorch':ThreeSsnPorch,
        # 'ScreenPorch':ScreenPorch,
        # 'LowQualFinSF':LowQualFinSF,
        # 'YearRemodAdd':YearRemodAdd,
        # 'GarageArea':GarageArea,
        # 'EnclosedPorch':EnclosedPorch,
        # 'FirstFlrSF':FirstFlrSF,
        # 'SecondFlrSF':SecondFlrSF,
        # 'GarageCars':GarageCars,
        # }
        # data_addGrLivArea = pd.DataFrame(user_data_addGrLivArea, index=[0])
        # price_addGrLivArea = model.predict(data_addGrLivArea)
        # f_price_addGrLivArea = "{:,.2f}".format(price_addGrLivArea[0])
        # st.metric("Value of Adding 100sq.feet to the Ground Floor Living Space", f_price_addGrLivArea, delta = formatted_price, delta_color = "normal", help = None, label_visibility = "visible")

        # user_data_GarageYrBlt = {
        # 'LotArea':LotArea,
        # 'BedroomAbvGr':BedroomAbvGr,
        # 'HalfBath':HalfBath,
        # 'GrLivArea':GrLivArea,
        # 'OverallQual':OverallQual + 1,
        # 'KitchenAbvGr':KitchenAbvGr,
        # 'TotRmsAbvGrd':TotRmsAbvGrd,
        # 'BsmtHalfBath':BsmtHalfBath,
        # 'FullBath':FullBath,
        # 'BsmtFullBath':BsmtFullBath,
        # 'MoSold':MoSold,
        # 'OverallCond':OverallCond,
        # 'YearBuilt':YearBuilt,
        # 'ThreeSsnPorch':ThreeSsnPorch,
        # 'ScreenPorch':ScreenPorch,
        # 'LowQualFinSF':LowQualFinSF,
        # 'YearRemodAdd':YearRemodAdd,
        # 'GarageArea':GarageArea,
        # 'EnclosedPorch':EnclosedPorch,
        # 'FirstFlrSF':FirstFlrSF,
        # 'SecondFlrSF':SecondFlrSF,
        # 'GarageCars':GarageCars,
        # }
        # data_addQual = pd.DataFrame(user_data_addQual, index=[0])
        # price_addQual = model.predict(data_addQual)
        # f_price_addQual = "{:,.2f}".format(price_addQual[0])
        # st.metric("Value of Improving the Finish Quality by 1", f_price_addQual, delta = formatted_price, delta_color = "normal", help = None, label_visibility = "visible")

        # #st.metric("Prediction Accuracy", model.score(data, ), delta = None, delta_color = "off", help = None, label_visibility = "visible")
        # st.metric("Prediction Accuracy", "84.18%", delta = None, delta_color = "off", help = None, label_visibility = "visible") #hard coded accuracy

        # endTime = time.time()
        # modelRunTime = endTime - startTime
        # st.metric("Run Time", modelRunTime, delta = None, delta_color = "off", help = None, label_visibility = "visible") #model run time

main()
