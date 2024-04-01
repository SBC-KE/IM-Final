import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import folium_static
from sklearn.preprocessing import StandardScaler  # or import your scaler

# Function to get color based on vaccination status
def get_color(Vaccination_Status):
    if Vaccination_Status == 'Full_Defaulter':
        return 'red'
    elif Vaccination_Status == 'Partial_Defaulter':
        return 'orange'
    else:
        return 'green'

# Load your trained model (ensure the path is accessible from your app's deployment environment)
model_path = 'random_forest_model_updated_2.0.joblib'
model = joblib.load(model_path)

# Assuming the scaler is saved similarly
scaler_path = 'X_validation_scaled.joblib'
scaler = joblib.load(scaler_path)

# Streamlit app title
st.title('Vaccination Status Prediction')

# Upload CSV file
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Assuming the uploaded file is a CSV, adjust for other formats
    df2 = pd.read_csv(uploaded_file)

# Select columns for prediction
    defaulter_pred = df2[['number_of_polio_doses_received',
                      'number_of_pentavalen_doses_received',
                      'number_of_pneumococcal_doses_received',
                      'number_of_rotavirus_dosers_received',
                      'latitude', 'longitude',
                      'number_of_measles_doses_received']]

# Scale features using the scaler object
    X_validation_scaled = defaulter_pred


    # Make predictions
    y_pred = model.predict(X_validation_scaled)

    # Add predictions to the DataFrame
    status_mapping = {0: 'Full_Defaulter', 1: 'Partial_Defaulter', 2: 'Non_Defaulter'}
    df2['Predicted_Status'] = [status_mapping[pred] for pred in y_pred]

    # Generate map
    mean_lat = df2['latitude'].mean()
    mean_long = df2['longitude'].mean()
    vaccination_map = folium.Map(location=[mean_lat, mean_long], zoom_start=6)

    for idx, row in df2.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            color=get_color(row['Predicted_Status']),
            fill=True,
            fill_color=get_color(row['Predicted_Status']),
            fill_opacity=0.7,
            popup=row['Predicted_Status']
        ).add_to(vaccination_map)

    # Display map in Streamlit
    folium_static(vaccination_map)
