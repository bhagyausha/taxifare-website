import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import pydeck as pdk
spell = st.secrets['lewagon']
key = st.secrets.some_magic_api.key
# Title for the web page
st.title("Taxi Fare Prediction")

# Introduction
st.markdown('''
This application predicts taxi fares based on user input. Use the controls below to input your ride details and get a fare prediction.
''')

# Form for user input
st.subheader("Enter Ride Details:")

# Input fields for ride details
pickup_date = st.date_input("Pickup Date", value=datetime.now().date())
pickup_time = st.time_input("Pickup Time", value=datetime.now().time())
pickup_datetime = datetime.combine(pickup_date, pickup_time)

pickup_longitude = st.number_input("Pickup Longitude", format="%.6f")
pickup_latitude = st.number_input("Pickup Latitude", format="%.6f")
dropoff_longitude = st.number_input("Dropoff Longitude", format="%.6f")
dropoff_latitude = st.number_input("Dropoff Latitude", format="%.6f")
passenger_count = st.number_input("Number of Passengers", min_value=1, max_value=8, value=1, step=1)

# Button to make prediction
if st.button("Predict Fare"):
    # URL of the prediction API
    url = 'https://taxifare.lewagon.ai/predict'  # Replace with your own API if running locally

    # Build the parameters dictionary
    params = {
        "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    # Make the API request
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        prediction = response.json().get("fare", "No prediction returned")

        # Display the prediction result
        st.success(f"Predicted Fare: ${prediction:.2f}")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

# Map Section
st.subheader("Ride Map")

if pickup_latitude and pickup_longitude and dropoff_latitude and dropoff_longitude:
    # Create a DataFrame with the coordinates
    map_data = pd.DataFrame({
        "latitude": [pickup_latitude, dropoff_latitude],
        "longitude": [pickup_longitude, dropoff_longitude]
    })

    # Option 1: Simple map using st.map()
    st.map(map_data)

    # Option 2: Advanced map using pydeck

    # Define the map view
    view_state = pdk.ViewState(
        latitude=pickup_latitude,
        longitude=pickup_longitude,
        zoom=12,
        pitch=50,
    )

    # Render the map
else:
    st.warning("Please provide valid latitude and longitude values to display the map.")


# import streamlit as st

# '''
# # TaxiFareModel front
# '''

# st.markdown('''
# Remember that there are several ways to output content into your web page...

# Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
# ''')

# '''
# ## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

# 1. Let's ask for:
# - date and time
# - pickup longitude
# - pickup latitude
# - dropoff longitude
# - dropoff latitude
# - passenger count
# '''

# '''
# ## Once we have these, let's call our API in order to retrieve a prediction

# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

# 🤔 How could we call our API ? Off course... The `requests` package 💡
# '''

# url = 'https://taxifare.lewagon.ai/predict'

# if url == 'https://taxifare.lewagon.ai/predict':

#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...

# 3. Let's call our API using the `requests` package...

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

# ## Finally, we can display the prediction to the user
# '''
