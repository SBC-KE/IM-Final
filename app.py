import streamlit as st
import numpy as np
from joblib import load

# Load the AdaBoost model
model = load('ada_boost_model.joblib')

# App title
st.title('Vaccination Status Prediction App')

# User inputs
st.header('Please enter the following details:')

# Collecting user inputs
received_measles_vaccine = st.selectbox('Have you received the measles vaccine?', ('Yes', 'No'))
number_of_polio_doses_received = st.number_input('Number of polio doses received', min_value=0, max_value=10, value=4)
number_of_rotavirus_doses_received = st.number_input('Number of rotavirus doses received', min_value=0, max_value=5, value=2)

# Encoding binary inputs
received_measles_vaccine = 1 if received_measles_vaccine == 'Yes' else 0

# Initialize an array with default values for all 111 features
default_values = np.zeros(111)  # Adjust based on actual default values for your model

# Update the default_values array with the actual values from user input
# Replace placeholder indices with the correct indices for your features
default_values[0] = received_measles_vaccine
default_values[1] = number_of_polio_doses_received
default_values[2] = number_of_rotavirus_doses_received

# Prepare the input data for prediction
input_data = default_values.reshape(1, -1)  # Reshape if necessary for a single prediction

# Prediction button and display
if st.button('Predict Vaccination Status'):
    prediction = model.predict(input_data)
    prediction_probability = model.predict_proba(input_data)
    
    st.subheader('Prediction:')
    # Interpret prediction output according to your model's classes
    # Assuming 0 = 'Partially Vaccinated' and 1 = 'Fully Vaccinated'
    if prediction[0] == 0:
        st.write('Partially Vaccinated')
        st.write(f'Prediction Probability: {prediction_probability[0][0]}')
    else:
        st.write('Fully Vaccinated')
        st.write(f'Prediction Probability: {prediction_probability[0][1]}')
