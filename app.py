import streamlit as st
import numpy as np
from joblib import load 
import streamlit.components.v1 as components
# Title for your Streamlit app
st.title('Default Map')

# Assuming your HTML file is located in the same directory as your Streamlit app
# and named 'interactive_map.html'
file_path = 'vaccination_map_updated.html'

# Open the HTML file and read its contents
with open(file_path, 'r', encoding='utf-8') as f:
    html_string = f.read()

# Use the components.html function to display the HTML content
components.html(html_string, height=600)

# Load the AdaBoost model
model = load('gradient_boost_model_updated (1).joblib')

# App title
st.title('Vaccination Status Prediction App')

import streamlit as st

# Streamlit header for input collection
st.header('Please enter the following details:')

# Collecting user inputs for each vaccine
number_of_polio_doses_received = st.number_input('Number of polio doses received', min_value=0, max_value=4)
number_of_pentavalent_doses_received = st.number_input('Number of pentavalent doses received', min_value=0, max_value=5)
number_of_pneumococcal_doses_received = st.number_input('Number of pneumococcal doses received', min_value=0, max_value=4)
number_of_rotavirus_doses_received = st.number_input('Number of rotavirus doses received', min_value=0, max_value=3)
number_of_measles_doses_received = st.number_input('Number of measles doses received', min_value=0, max_value=2)

# Define the vaccination status based on the criteria given
def determine_vaccination_status(doses_received, full_defaulter_threshold, partial_defaulter_threshold):
    if doses_received <= full_defaulter_threshold:
        return 'Full Defaulter'
    elif doses_received <= partial_defaulter_threshold:
        return 'Partial Defaulter'
    else:
        return 'Up to Date'

# Check each vaccination status
polio_status = determine_vaccination_status(number_of_polio_doses_received, 0, 2)
pentavalent_status = determine_vaccination_status(number_of_pentavalent_doses_received, 0, 2)
pneumococcal_status = determine_vaccination_status(number_of_pneumococcal_doses_received, 0, 2)
rotavirus_status = determine_vaccination_status(number_of_rotavirus_doses_received, 0, 1)
measles_status = determine_vaccination_status(number_of_measles_doses_received, 0, 1)

# Display the vaccination status for each vaccine when the user clicks the 'Predict Vaccination Status' button
if st.button('Predict Vaccination Status'):
    st.subheader('Vaccination Status:')
    st.write(f"Polio: {polio_status}")
    st.write(f"Pentavalent: {pentavalent_status}")
    st.write(f"Pneumococcal: {pneumococcal_status}")
    st.write(f"Rotavirus: {rotavirus_status}")
    st.write(f"Measles: {measles_status}")
