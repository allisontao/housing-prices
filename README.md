# housing-prices
Requirements:

``pip install -q streamlit``

``npm install localtunnel``

To run frontend:

``streamlit run app.py``

# Code Structure
**model.ipynb:**
This file includes code for the linear regression model. We imported the necessary packages of numpy, pandas, and sklearn. 
It then select the top 20 features based on the absolute coefficient values for model predictions. The model takes 70% of the data as training set and 30% of the data as testing set. 
The prediction score of the linear regression model is 85%.

**app.py:**
This file connects to the linear regression model in model.ipynb and uses streamlit to create user interface for users to input values and output the predicted house prices as well as the prediction score. It also generates visualizations including a bar chart that demonstrate the scaled impact of features on the price prediction, a heatmap for the correlation between the top 5 features, scatter plots between sale price and house factors, and sensitivity analysis between the house price and house factors.

Users will also be able to observe the run time of the model on streamlit. 
