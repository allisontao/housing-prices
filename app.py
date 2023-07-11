import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
import seaborn as sns
import matplotlib.pyplot as plt


st.title('House Price Prediction')


def main():
    with st.form(key='form'):
        YearBuilt = st.sidebar.number_input(
            'Year of original construction date:', min_value=1500, max_value=2023, value=2010, step=1)
        YearRemodAdd = st.sidebar.number_input('Year of remodel date (if it has not been remodeled, enter the year of original construction):', min_value=YearBuilt,
                                               max_value=2023, value=YearBuilt, step=1, help='This value should be greater than or equal to the original construction year')
        YrSold = st.sidebar.number_input(
            'Year the house was sold:', min_value=1500, max_value=2023, value=2010, step=1)
        MoSold = st.sidebar.selectbox(
            'Select month sold (1 corresponds to January and 12 corresponds to December, etc):', (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
        MSSubClass = st.sidebar.selectbox(
            'Building class:', (20, 30, 40, 45, 50, 60, 70, 75, 80, 85,  90, 120, 150, 160, 180, 190))
        GrLivArea = st.sidebar.number_input(
            'Ground living area in square feet:', min_value=0)
        MasVnrArea = st.sidebar.number_input(
            'Masonry veneer area in square feet:', min_value=0)
        PoolArea = st.sidebar.number_input(
            'Pool area in square feet:', min_value=0)
        TotRmsAbvGrd = st.sidebar.number_input(
            'Total rooms above ground (not including bathrooms):', step=1, min_value=0)
        BedroomAbvGr = st.sidebar.number_input(
            'Number of bedrooms above ground:', step=1, min_value=0)
        KitchenAbvGr = st.sidebar.number_input(
            'Number of kitchens above ground:', step=1, min_value=0)
        Fireplaces = st.sidebar.number_input(
            'Number of fireplaces:', step=1, min_value=0)
        BsmtFullBath = st.sidebar.number_input(
            'Number of full bathrooms in the basement:', step=1, min_value=0)
        FullBath = st.sidebar.number_input(
            'Number of full bathrooms above ground:', step=1, min_value=0)
        HalfBath = st.sidebar.number_input(
            'Number of half baths above ground:', step=1, min_value=0)
        BsmtHalfBath = st.sidebar.number_input(
            'Select the number of half bathrooms in the basement:', step=1)
        ScreenPorch = st.sidebar.number_input(
            'Screen porch area in square feet:', min_value=0)
        GarageCars = st.sidebar.number_input(
            'Size of garage in car capacity:', step=1, min_value=0)
        OverallCond = st.sidebar.slider(
            'Select overall condition rating:', min_value=1, max_value=10, step=1)
        OverallQual = st.sidebar.slider(
            'Select rating for overall material and finish quality:', min_value=1, max_value=10, step=1)

        st.markdown(
            "Press submit button below after inputting house data on the left to get the predicted house price!")
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:

            user_data = {
                'OverallQual': OverallQual,
                'GarageCars': GarageCars,
                'KitchenAbvGr': KitchenAbvGr,
                'BedroomAbvGr': BedroomAbvGr,
                'BsmtFullBath': BsmtFullBath,
                'OverallCond': OverallCond,
                'TotRmsAbvGrd': TotRmsAbvGrd,
                'Fireplaces': Fireplaces,
                'FullBath': FullBath,
                'HalfBath': HalfBath,
                'BsmtHalfBath': BsmtHalfBath,
                'YrSold': YrSold,
                'YearBuilt': YearBuilt,
                'MSSubClass': MSSubClass,
                'YearRemodAdd': YearRemodAdd,
                'ScreenPorch': ScreenPorch,
                'MoSold': MoSold,
                'PoolArea': PoolArea,
                'GrLivArea': GrLivArea,
                'MasVnrArea': MasVnrArea
            }

            data = pd.DataFrame(user_data, index=[0])
            model = pickle.load(open('model.sav', 'rb'))
            # try:
            # startTime = time.time()
            price = model.predict(data)
            formatted_price = "{:,.2f}".format(price[0])
            st.subheader('Predicted house price:')
            st.subheader('$'+formatted_price)
            modelCoefficients = model.coef_
            print(modelCoefficients)
            column_names = ['OverallQual', 'BsmtFullBath', 'GarageCars', 'BedroomAbvGr', 'BsmtHalfBath',
                            'KitchenAbvGr', 'Fireplaces', 'TotRmsAbvGrd', 'OverallCond', 'FullBath',
                            'HalfBath', 'YrSold', 'YearBuilt', 'MSSubClass', 'YearRemodAdd', 'GrLivArea',
                            'ScreenPorch', 'MasVnrArea', 'MoSold', 'PoolArea']

            # Create a pandas DataFrame with your data
            df = pd.DataFrame({
                'Features': ['OverallQual', 'GarageCars', 'KitchenAbvGr', 'BedroomAbvGr', 'BsmtFullBath',
                             'OverallCond', 'TotRmsAbvGrd', 'Fireplaces', 'FullBath', 'HalfBath',
                             'BsmtHalfBath', 'YrSold', 'YearBuilt', 'MSSubClass', 'YearRemodAdd',
                             'ScreenPorch', 'MoSold', 'PoolArea', 'GrLivArea'],
                'Coefficients': [19659.381016, 11500.819277, -7778.314665, -11060.122583, 18817.239377,
                                 4762.050670, 5598.605698, 5706.370483, 4227.823147, -4168.690288,
                                 8407.988769, -355.294434, 329.969885, -223.304144, 137.435422,
                                 48.841289, 34.401331, 2.431497, 49.683259]
            })

            # Sort the DataFrame by 'Coefficients' in descending order
            # Calculate the absolute values of 'Coefficients'
            df['AbsCoefficients'] = np.abs(df['Coefficients'])

            # Sort the DataFrame by 'AbsCoefficients' in descending order
            df = df.sort_values('AbsCoefficients', ascending=False)

            # Create a bar chart with 'Features' on the x-axis and 'Coefficients' on the y-axis
            st.bar_chart(df.set_index('Features')['Coefficients'])

            # Feature Bar Chart Title
            st.markdown(
                "#### Scaled Impact of Features on Price Prediction")

            # Compute the correlation matrix from the coefficients DataFrame
            # corr = coef_df.corr()
           # print(corr)

            # Create a heatmap
            # st.header(
            #     'Correlation Heatmap of Linear Regression Coefficients')
            # fig, ax = plt.subplots()
            # sns.heatmap(corr, annot=True, fmt=".2f",
            #             cmap='coolwarm', ax=ax)
            # st.pyplot(fig)

            st.metric("Prediction Accuracy", "83.78%", delta=None, delta_color="off",
                      help=None, label_visibility="visible")  # hard coded accuracy

            def create_metric(modified_data, original_price):
                data = pd.DataFrame(modified_data, index=[0])
                new_price = model.predict(data)
                f_new_price = "{:,.2f}".format(new_price[0])
                change_price = (
                    (new_price[0] - original_price[0])/original_price[0])*100
                f_delta_price = "{:,.2f}".format(change_price) + "%"
                return f_new_price, f_delta_price

            add_OverallQual = {
                'OverallQual': OverallQual + 1,
                'GarageCars': GarageCars,
                'KitchenAbvGr': KitchenAbvGr,
                'BedroomAbvGr': BedroomAbvGr,
                'BsmtFullBath': BsmtFullBath,
                'OverallCond': OverallCond,
                'TotRmsAbvGrd': TotRmsAbvGrd,
                'Fireplaces': Fireplaces,
                'FullBath': FullBath,
                'HalfBath': HalfBath,
                'BsmtHalfBath': BsmtHalfBath,
                'YrSold': YrSold,
                'YearBuilt': YearBuilt,
                'MSSubClass': MSSubClass,
                'YearRemodAdd': YearRemodAdd,
                'ScreenPorch': ScreenPorch,
                'MoSold': MoSold,
                'PoolArea': PoolArea,
                'GrLivArea': GrLivArea,
                'MasVnrArea': MasVnrArea
            }

            subtract_OverallQual = {
                'OverallQual': OverallQual - 1,
                'GarageCars': GarageCars,
                'KitchenAbvGr': KitchenAbvGr,
                'BedroomAbvGr': BedroomAbvGr,
                'BsmtFullBath': BsmtFullBath,
                'OverallCond': OverallCond,
                'TotRmsAbvGrd': TotRmsAbvGrd,
                'Fireplaces': Fireplaces,
                'FullBath': FullBath,
                'HalfBath': HalfBath,
                'BsmtHalfBath': BsmtHalfBath,
                'YrSold': YrSold,
                'YearBuilt': YearBuilt,
                'MSSubClass': MSSubClass,
                'YearRemodAdd': YearRemodAdd,
                'ScreenPorch': ScreenPorch,
                'MoSold': MoSold,
                'PoolArea': PoolArea,
                'GrLivArea': GrLivArea,
                'MasVnrArea': MasVnrArea
            }

            add_GarageCars = {
                'OverallQual': OverallQual,
                'GarageCars': GarageCars + 1,
                'KitchenAbvGr': KitchenAbvGr,
                'BedroomAbvGr': BedroomAbvGr,
                'BsmtFullBath': BsmtFullBath,
                'OverallCond': OverallCond,
                'TotRmsAbvGrd': TotRmsAbvGrd,
                'Fireplaces': Fireplaces,
                'FullBath': FullBath,
                'HalfBath': HalfBath,
                'BsmtHalfBath': BsmtHalfBath,
                'YrSold': YrSold,
                'YearBuilt': YearBuilt,
                'MSSubClass': MSSubClass,
                'YearRemodAdd': YearRemodAdd,
                'ScreenPorch': ScreenPorch,
                'MoSold': MoSold,
                'PoolArea': PoolArea,
                'GrLivArea': GrLivArea,
                'MasVnrArea': MasVnrArea
            }

            subtract_GarageCars = {
                'OverallQual': OverallQual,
                'GarageCars': GarageCars - 1,
                'KitchenAbvGr': KitchenAbvGr,
                'BedroomAbvGr': BedroomAbvGr,
                'BsmtFullBath': BsmtFullBath,
                'OverallCond': OverallCond,
                'TotRmsAbvGrd': TotRmsAbvGrd,
                'Fireplaces': Fireplaces,
                'FullBath': FullBath,
                'HalfBath': HalfBath,
                'BsmtHalfBath': BsmtHalfBath,
                'YrSold': YrSold,
                'YearBuilt': YearBuilt,
                'MSSubClass': MSSubClass,
                'YearRemodAdd': YearRemodAdd,
                'ScreenPorch': ScreenPorch,
                'MoSold': MoSold,
                'PoolArea': PoolArea,
                'GrLivArea': GrLivArea,
                'MasVnrArea': MasVnrArea
            }

            add_KitchenAbvGr = {
                'OverallQual': OverallQual,
                'GarageCars': GarageCars,
                'KitchenAbvGr': KitchenAbvGr + 1,
                'BedroomAbvGr': BedroomAbvGr,
                'BsmtFullBath': BsmtFullBath,
                'OverallCond': OverallCond,
                'TotRmsAbvGrd': TotRmsAbvGrd,
                'Fireplaces': Fireplaces,
                'FullBath': FullBath,
                'HalfBath': HalfBath,
                'BsmtHalfBath': BsmtHalfBath,
                'YrSold': YrSold,
                'YearBuilt': YearBuilt,
                'MSSubClass': MSSubClass,
                'YearRemodAdd': YearRemodAdd,
                'ScreenPorch': ScreenPorch,
                'MoSold': MoSold,
                'PoolArea': PoolArea,
                'GrLivArea': GrLivArea,
                'MasVnrArea': MasVnrArea
            }

            subtract_KitchenAbvGr = {
                'OverallQual': OverallQual,
                'GarageCars': GarageCars,
                'KitchenAbvGr': KitchenAbvGr - 1,
                'BedroomAbvGr': BedroomAbvGr,
                'BsmtFullBath': BsmtFullBath,
                'OverallCond': OverallCond,
                'TotRmsAbvGrd': TotRmsAbvGrd,
                'Fireplaces': Fireplaces,
                'FullBath': FullBath,
                'HalfBath': HalfBath,
                'BsmtHalfBath': BsmtHalfBath,
                'YrSold': YrSold,
                'YearBuilt': YearBuilt,
                'MSSubClass': MSSubClass,
                'YearRemodAdd': YearRemodAdd,
                'ScreenPorch': ScreenPorch,
                'MoSold': MoSold,
                'PoolArea': PoolArea,
                'GrLivArea': GrLivArea,
                'MasVnrArea': MasVnrArea
            }

            add_BedroomAbvGr = {
                'OverallQual': OverallQual,
                'GarageCars': GarageCars,
                'KitchenAbvGr': KitchenAbvGr,
                'BedroomAbvGr': BedroomAbvGr + 1,
                'BsmtFullBath': BsmtFullBath,
                'OverallCond': OverallCond,
                'TotRmsAbvGrd': TotRmsAbvGrd,
                'Fireplaces': Fireplaces,
                'FullBath': FullBath,
                'HalfBath': HalfBath,
                'BsmtHalfBath': BsmtHalfBath,
                'YrSold': YrSold,
                'YearBuilt': YearBuilt,
                'MSSubClass': MSSubClass,
                'YearRemodAdd': YearRemodAdd,
                'ScreenPorch': ScreenPorch,
                'MoSold': MoSold,
                'PoolArea': PoolArea,
                'GrLivArea': GrLivArea,
                'MasVnrArea': MasVnrArea
            }

            subtract_BedroomAbvGr = {
                'OverallQual': OverallQual,
                'GarageCars': GarageCars,
                'KitchenAbvGr': KitchenAbvGr,
                'BedroomAbvGr': BedroomAbvGr - 1,
                'BsmtFullBath': BsmtFullBath,
                'OverallCond': OverallCond,
                'TotRmsAbvGrd': TotRmsAbvGrd,
                'Fireplaces': Fireplaces,
                'FullBath': FullBath,
                'HalfBath': HalfBath,
                'BsmtHalfBath': BsmtHalfBath,
                'YrSold': YrSold,
                'YearBuilt': YearBuilt,
                'MSSubClass': MSSubClass,
                'YearRemodAdd': YearRemodAdd,
                'ScreenPorch': ScreenPorch,
                'MoSold': MoSold,
                'PoolArea': PoolArea,
                'GrLivArea': GrLivArea,
                'MasVnrArea': MasVnrArea
            }

            add_BsmtFullBath = {
                'OverallQual': OverallQual,
                'GarageCars': GarageCars,
                'KitchenAbvGr': KitchenAbvGr,
                'BedroomAbvGr': BedroomAbvGr,
                'BsmtFullBath': BsmtFullBath + 1,
                'OverallCond': OverallCond,
                'TotRmsAbvGrd': TotRmsAbvGrd,
                'Fireplaces': Fireplaces,
                'FullBath': FullBath,
                'HalfBath': HalfBath,
                'BsmtHalfBath': BsmtHalfBath,
                'YrSold': YrSold,
                'YearBuilt': YearBuilt,
                'MSSubClass': MSSubClass,
                'YearRemodAdd': YearRemodAdd,
                'ScreenPorch': ScreenPorch,
                'MoSold': MoSold,
                'PoolArea': PoolArea,
                'GrLivArea': GrLivArea,
                'MasVnrArea': MasVnrArea
            }

            subtract_BsmtFullBath = {
                'OverallQual': OverallQual,
                'GarageCars': GarageCars,
                'KitchenAbvGr': KitchenAbvGr,
                'BedroomAbvGr': BedroomAbvGr,
                'BsmtFullBath': BsmtFullBath - 1,
                'OverallCond': OverallCond,
                'TotRmsAbvGrd': TotRmsAbvGrd,
                'Fireplaces': Fireplaces,
                'FullBath': FullBath,
                'HalfBath': HalfBath,
                'BsmtHalfBath': BsmtHalfBath,
                'YrSold': YrSold,
                'YearBuilt': YearBuilt,
                'MSSubClass': MSSubClass,
                'YearRemodAdd': YearRemodAdd,
                'ScreenPorch': ScreenPorch,
                'MoSold': MoSold,
                'PoolArea': PoolArea,
                'GrLivArea': GrLivArea,
                'MasVnrArea': MasVnrArea
            }

            col_1, col_2 = st.columns(2)

            add_OverallQual_price, add_OverallQual_change = create_metric(
                add_OverallQual, price)
            subtract_OverallQual_price, subtract_OverallQual_change = create_metric(
                subtract_OverallQual, price)

            col_1.metric("Predicted Value of Improving the Finish Quality by 1", add_OverallQual_price,
                         delta=add_OverallQual_change, delta_color="normal", help=None, label_visibility="visible")
            col_2.metric("Predicted Cost Savings in Decreasing the Finish Quality by 1", subtract_OverallQual_price,
                         delta=subtract_OverallQual_change, delta_color="normal", help=None, label_visibility="visible")

            col_3, col_4 = st.columns(2)

            add_GarageCars_price, add_GarageCars_change = create_metric(
                add_GarageCars, price)
            subtract_GarageCars_price, subtract_GarageCars_change = create_metric(
                subtract_GarageCars, price)

            col_3.metric("Predicted Value of Adding Garage Car Capacity by 1", add_GarageCars_price,
                         delta=add_GarageCars_change, delta_color="normal", help=None, label_visibility="visible")
            col_4.metric("Predicted Decrease in Value Decreasing Garage Car Capacity by 1", subtract_GarageCars_price,
                         delta=subtract_GarageCars_change, delta_color="normal", help=None, label_visibility="visible")

            col_5, col_6 = st.columns(2)

            add_KitchenAbvGr_price, add_KitchenAbvGr_change = create_metric(
                add_KitchenAbvGr, price)
            subtract_KitchenAbvGr_price, subtract_KitchenAbvGr_change = create_metric(
                subtract_KitchenAbvGr, price)

            col_5.metric("Predicted Value of Adding 1 Kitchen Above Grade", add_KitchenAbvGr_price,
                         delta=add_KitchenAbvGr_change, delta_color="normal", help=None, label_visibility="visible")
            col_6.metric("Predicted Decrease in Value of Decreasing 1 Kitchen Above Grade", subtract_KitchenAbvGr_price,
                         delta=subtract_KitchenAbvGr_change, delta_color="normal", help=None, label_visibility="visible")

            col_7, col_8 = st.columns(2)

            add_BedroomAbvGr_price, add_BedroomAbvGr_change = create_metric(
                add_BedroomAbvGr, price)
            subtract_BedroomAbvGr_price, subtract_BedroomAbvGr_change = create_metric(
                subtract_BedroomAbvGr, price)

            col_7.metric("Predicted Value of Adding 1 Bedroom Above Grade", add_BedroomAbvGr_price,
                         delta=add_BedroomAbvGr_change, delta_color="normal", help=None, label_visibility="visible")
            col_8.metric("Predicted Decrease in Value in Decreasing Bedrooms Above Grade by 1", subtract_BedroomAbvGr_price,
                         delta=subtract_BedroomAbvGr_change, delta_color="normal", help=None, label_visibility="visible")

            col_9, col_10 = st.columns(2)

            add_BsmtFullBath_price, add_BsmtFullBath_change = create_metric(
                add_BsmtFullBath, price)
            subtract_BsmtFullBath_price, subtract_BsmtFullBath_change = create_metric(
                subtract_BsmtFullBath, price)

            col_9.metric("Predicted Value of Adding 1 Basement Full Bath", add_BsmtFullBath_price,
                         delta=add_BsmtFullBath_change, delta_color="normal", help=None, label_visibility="visible")
            col_10.metric("Predicted Decrease in Value of Decreasing Basement Full Baths by 1", subtract_BsmtFullBath_price,
                          delta=subtract_BsmtFullBath_change, delta_color="normal", help=None, label_visibility="visible")

            # endTime = time.time()
            # modelRunTime = endTime - startTime
            # st.metric("Run Time", modelRunTime, delta = None, delta_color = "off", help = None, label_visibility = "visible") #model run time
            # except:
            #     st.write('Must fill out all fields to predict the price.')


main()
