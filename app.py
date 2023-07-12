import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
import seaborn as sns
import matplotlib.pyplot as plt

st.title('House Price Prediction')

def main():
    # Create the form with 20 features
    with st.form(key='form'):
        YearBuilt = st.sidebar.number_input(
            'Year of original construction date:', min_value=1500, max_value=2023, value=2010, step=1)
        YearRemodAdd = st.sidebar.number_input('Year of remodel date (if it has not been remodeled, enter the year of original construction):', min_value=YearBuilt,
                                               max_value=2023, value=YearBuilt, step=1, help='This value should be greater than or equal to the original construction year')
        YrSold = st.sidebar.number_input(
            'Year the house was sold:', min_value=1500, max_value=2023, value=YearBuilt + 5, step=1)
        MoSold = st.sidebar.selectbox(
            'Select month sold (1 corresponds to January and 12 corresponds to December, etc):', (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
        MSSubClass = st.sidebar.selectbox(
            'Building class:', (20, 30, 40, 45, 50, 60, 70, 75, 80, 85,  90, 120, 150, 160, 180, 190))
        GrLivArea = st.sidebar.number_input(
            'Ground living area in square feet:', min_value=0, value = 2000)
        MasVnrArea = st.sidebar.number_input(
            'Masonry veneer area in square feet:', min_value=0, value = 500)
        PoolArea = st.sidebar.number_input(
            'Pool area in square feet:', min_value=0, value = 1000)
        TotRmsAbvGrd = st.sidebar.number_input(
            'Total rooms above ground (not including bathrooms):', step=1, min_value=0, value = 8)
        BedroomAbvGr = st.sidebar.number_input(
            'Number of bedrooms above ground:', step=1, min_value=0, value = 4)
        KitchenAbvGr = st.sidebar.number_input(
            'Number of kitchens above ground:', step=1, min_value=0, value = 1)
        Fireplaces = st.sidebar.number_input(
            'Number of fireplaces:', step=1, min_value=0, value =2)
        BsmtFullBath = st.sidebar.number_input(
            'Number of full bathrooms in the basement:', step=1, min_value=0, value =2)
        FullBath = st.sidebar.number_input(
            'Number of full bathrooms above ground:', step=1, min_value=0, value = 3)
        HalfBath = st.sidebar.number_input(
            'Number of half baths above ground:', step=1, min_value=0, value =1)
        BsmtHalfBath = st.sidebar.number_input(
            'Select the number of half bathrooms in the basement:', step=1, value =0)
        ScreenPorch = st.sidebar.number_input(
            'Screen porch area in square feet:', min_value=0, value = 500)
        GarageCars = st.sidebar.number_input(
            'Size of garage in car capacity:', step=1, min_value=0, value =2)
        OverallCond = st.sidebar.slider(
            'Select overall condition rating:', min_value=1, max_value=10, step=1, value =8)
        OverallQual = st.sidebar.slider(
            'Select rating for overall material and finish quality:', min_value=1, max_value=10, step=1,value=8 )

        st.markdown(
            "Click the submit button below after inputting your house construction specifications on the left sidebar to get the predicted house price!")
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

            # Create dataframe from user data submitted in the form
            data = pd.DataFrame(user_data, index=[0])
            # Import model and raw data 
            model = pickle.load(open('model.sav', 'rb'))
            raw_data = pd.read_csv('raw_data.csv')
            
            startTime = time.time()
            
            # Predict the price using the user inputted data
            price = model.predict(data)
            predictEndTime = time.time()
            
            # Display predicted price
            formatted_price = "{:,.2f}".format(price[0])
            col1, col2 = st.columns(2)
            col1.metric("Predicted house price:", '$'+formatted_price, delta=None, delta_color="off",
                        label_visibility="visible", help=None)

            # Hard coded accuracy from the model
            col2.metric("Prediction Accuracy", "85.05%", delta=None, delta_color="off",
                        help='85% of the variation in price can be attributed to these features', label_visibility="visible")

            # Dataframe containing each feature and their respective coefficients from the model
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

            st.markdown(
                "#### Impact of Features on Price Prediction")
            st.markdown("The bar chart shows the importance of features to the house prediction price based on their coefficients. This provides a comprehensive overview of the features that significantly influence the pricing of construction projects.")
            # Bar chart with 'Features' on the x-axis and 'Coefficients' on the y-axis
            # bar_chart = df.set_index('Features')['Coefficients']
            st.bar_chart(data=df.set_index('Features')['Coefficients'])

            # Get the top 5 features
            top_5_features = df['Features'].values[:5]

            # Calculate the correlation matrix of the top 5 features
            corr_matrix = raw_data[top_5_features].corr()

            st.markdown(
                "#### Heatmap of Correlation Between 5 Most Significant Features")
            st.markdown('The heatmap  offers a visual depiction of the connections between the top 5 most significant house features. By examining the strength and direction of these correlations, construction builders can discern the influential factors and make well-informed decisions.')
            # Create a heatmap of the correlation matrix
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
            st.pyplot(plt)

            # Features to consider for the plot
            features = ['OverallQual', 'GarageCars', 'KitchenAbvGr', 'BedroomAbvGr', 'BsmtFullBath',
                            'OverallCond', 'TotRmsAbvGrd', 'Fireplaces', 'FullBath', 'HalfBath']

            # Define the size of the plot
            n = len(features)
            ncols = 2
            nrows = n // ncols if n % ncols == 0 else n // ncols + 1

            # Create subplots
            fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(20, 20))

            # For each feature create a subplot
            for i, feature in enumerate(features):
                r, c = i // ncols, i % ncols
                ax = axes[r, c]
                # Plot with a regression line
                sns.regplot(ax=ax, data=raw_data, x=feature, y='SalePrice')
                ax.set_title(f'SalePrice vs {feature}', fontsize=14)

            # Remove empty subplots
            if n % ncols != 0:
                for j in range(r*ncols+c+1, nrows*ncols):
                    fig.delaxes(axes[j // ncols, j % ncols])

            st.markdown(
                "#### Effect of 10 Most Significant Features on Sale Price")
            
            st.markdown('These scatterplots allow us to understand how the 10 most significant house features, like number of bedrooms or overall quality, impacts the final house price. By studying these plots, we can easily spot strong relationships between features and price, as well as any outliers that might affect our predictions.')
            
            plt.tight_layout()
            st.pyplot(fig)

            # Function to create metric that compares modified price and original price
            def create_metric(modified_data, original_price):
                data = pd.DataFrame(modified_data, index=[0])
                new_price = model.predict(data)
                f_new_price = "{:,.2f}".format(new_price[0])
                change_price = (
                    (new_price[0] - original_price[0])/original_price[0])*100
                f_delta_price = "{:,.2f}".format(change_price) + "%"
                return f_new_price, f_delta_price

            # Sample user data with overallqual + 1 point
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

            # Sample user data with overallqual - 1 point
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

            # Sample user data with + 1 garage capacity
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

            # Sample user data with - 1 garage capacity     
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
            
            # Sample user data with + 1 kitchen
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

            # Sample user data with - 1 kitchen
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

            # Sample user data with + 1 bedroom
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

            # Sample user data with - 1 bedroom
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

            # Sample user data with + 1 basement full bath
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

            # Sample user data with - 1 basement full bath
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

            # Predict all metrics based on the above sample data
            st.markdown("#### Feature Variation Metrics for 5 Most Significant Features")
            st.markdown("Our feature variation metrics offer developers tangible insights into how altering the 5 most significant property features, such as garage car capacity, influences the predicted house price. For example, by showcasing how an addition or subtraction of 1 garage car capacity could affect the house's value, developers can better strategize their building plans.")
            col_1, col_2 = st.columns(2)

            add_OverallQual_price, add_OverallQual_change = create_metric(
                add_OverallQual, price)
            subtract_OverallQual_price, subtract_OverallQual_change = create_metric(
                subtract_OverallQual, price)

            col_1.metric("Predicted Value of Improving the Finish Quality by 1", '$'+add_OverallQual_price,
                        delta=add_OverallQual_change, delta_color="normal", help=None, label_visibility="visible")
            col_2.metric("Predicted Value of Decreasing the Finish Quality by 1", '$'+subtract_OverallQual_price,
                        delta=subtract_OverallQual_change, delta_color="normal", help=None, label_visibility="visible")

            col_3, col_4 = st.columns(2)

            add_GarageCars_price, add_GarageCars_change = create_metric(
                add_GarageCars, price)
            subtract_GarageCars_price, subtract_GarageCars_change = create_metric(
                subtract_GarageCars, price)

            col_3.metric("Predicted Value of Adding Garage Car Capacity by 1", '$'+add_GarageCars_price,
                        delta=add_GarageCars_change, delta_color="normal", help=None, label_visibility="visible")
            col_4.metric("Predicted Value of Decreasing Garage Car Capacity by 1", '$'+subtract_GarageCars_price,
                        delta=subtract_GarageCars_change, delta_color="normal", help=None, label_visibility="visible")

            col_5, col_6 = st.columns(2)

            add_KitchenAbvGr_price, add_KitchenAbvGr_change = create_metric(
                add_KitchenAbvGr, price)
            subtract_KitchenAbvGr_price, subtract_KitchenAbvGr_change = create_metric(
                subtract_KitchenAbvGr, price)

            col_5.metric("Predicted Value of Adding 1 Kitchen Above Grade", '$'+add_KitchenAbvGr_price,
                        delta=add_KitchenAbvGr_change, delta_color="normal", help=None, label_visibility="visible")
            col_6.metric("Predicted Value of Decreasing 1 Kitchen Above Grade", '$'+subtract_KitchenAbvGr_price,
                        delta=subtract_KitchenAbvGr_change, delta_color="normal", help=None, label_visibility="visible")

            col_7, col_8 = st.columns(2)

            add_BedroomAbvGr_price, add_BedroomAbvGr_change = create_metric(
                add_BedroomAbvGr, price)
            subtract_BedroomAbvGr_price, subtract_BedroomAbvGr_change = create_metric(
                subtract_BedroomAbvGr, price)

            col_7.metric("Predicted Value of Adding 1 Bedroom Above Grade", '$'+add_BedroomAbvGr_price,
                        delta=add_BedroomAbvGr_change, delta_color="normal", help=None, label_visibility="visible")
            col_8.metric("Predicted Value of Decreasing 1 Bedroom Above Grade", '$'+subtract_BedroomAbvGr_price,
                        delta=subtract_BedroomAbvGr_change, delta_color="normal", help=None, label_visibility="visible")

            col_9, col_10 = st.columns(2)

            add_BsmtFullBath_price, add_BsmtFullBath_change = create_metric(
                add_BsmtFullBath, price)
            subtract_BsmtFullBath_price, subtract_BsmtFullBath_change = create_metric(
                subtract_BsmtFullBath, price)

            col_9.metric("Predicted Value of Adding 1 Basement Full Bath", '$'+add_BsmtFullBath_price,
                        delta=add_BsmtFullBath_change, delta_color="normal", help=None, label_visibility="visible")
            col_10.metric("Predicted Value of Decreasing 1 Basement Full Bath", '$'+subtract_BsmtFullBath_price,
                        delta=subtract_BsmtFullBath_change, delta_color="normal", help=None, label_visibility="visible")

            # Display run time
            endTime = time.time()
            TotalRunTime = round(endTime - startTime, 3)
            ModelRunTime = round(predictEndTime - startTime, 3)
            
            st.markdown('### Run Time')
            col_11, col_12 = st.columns(2)
            col_11.metric("Total Run Time (including visualizations):", str(TotalRunTime) + ' seconds', delta=None, delta_color="off",
                    help=None, label_visibility="visible")
            col_12.metric("Run Time to predict price:", str(ModelRunTime) + ' seconds', delta=None, delta_color="off",
                    help=None, label_visibility="visible")

main()
