
import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(layout="wide")
st.title('SuperKart Sales Prediction UI')

# Configuration for the backend API
# IMPORTANT: Update this URL with the actual deployed URL of your Flask backend.
BACKEND_API_BASE_URL = "http://backend:7860" # Placeholder: Change to your deployed backend base URL

st.markdown("### Single Prediction")
st.markdown("Enter the details below to get a sales prediction for a product in a store.")

with st.form("prediction_form"):
    st.subheader("Product Details")
    product_weight = st.number_input('Product Weight', min_value=4.0, max_value=22.0, value=12.0, step=0.1)
    product_sugar_content = st.selectbox('Product Sugar Content', ['Low Sugar', 'Regular', 'No Sugar'])
    product_allocated_area = st.number_input('Product Allocated Area', min_value=0.004, max_value=0.298, value=0.06, step=0.001, format="%.3f")
    product_mrp = st.number_input('Product MRP', min_value=31.0, max_value=266.0, value=150.0, step=1.0)
    product_id_char = st.selectbox('Product ID Character', ['FD', 'NC', 'DR']) # Changed to Product_Id_char
    product_category = st.selectbox('Product Category', ['Non-Perishables', 'Perishables'])

    st.subheader("Store Details")
    store_size = st.selectbox('Store Size', ['Medium', 'High', 'Small'])
    store_location_city_type = st.selectbox('Store Location City Type', ['Tier 1', 'Tier 2', 'Tier 3'])
    store_type = st.selectbox('Store Type', ['Supermarket Type1', 'Supermarket Type2', 'Departmental Store', 'Food Mart'])
    store_age_years = st.number_input('Store Age (Years)', min_value=15, max_value=40, value=20, step=1)

    submitted = st.form_submit_button("Predict Sales")

    if submitted:
        input_data = {
            "Product_Weight": [product_weight],
            "Product_Sugar_Content": [product_sugar_content],
            "Product_Allocated_Area": [product_allocated_area],
            "Product_MRP": [product_mrp],
            "Store_Size": [store_size],
            "Store_Location_City_Type": [store_location_city_type],
            "Store_Type": [store_type],
            "Product_Id_char": [product_id_char], # Changed to Product_Id_char
            "Store_Age_Years": [store_age_years],
            "Product_Category": [product_category]
        }

        try:
            # Send data to Flask API for single prediction
            headers = {'Content-Type': 'application/json'}
            response = requests.post(f"{BACKEND_API_BASE_URL}/predict", data=json.dumps(input_data), headers=headers)
            response.raise_for_status() # Raise an exception for HTTP errors
            predictions = response.json()

            if predictions:
                st.success(f"Predicted Sales: ${predictions[0]:,.2f}")
            else:
                st.error("No predictions received from the API.")

        except requests.exceptions.ConnectionError:
            st.error(f"Connection Error: Could not connect to the backend API at {BACKEND_API_BASE_URL}/predict. Please ensure the backend is running and the URL is correct.")
        except requests.exceptions.Timeout:
            st.error(f"Timeout Error: The request to the backend API at {BACKEND_API_BASE_URL}/predict timed out.")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred during the API request: {e}")
        except json.JSONDecodeError:
            st.error(f"Failed to decode JSON response. API returned: {response.text}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

st.markdown("--- # Section for batch prediction")
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        try:
            # Send file to Flask API for batch prediction
            files = {'file': uploaded_file.getvalue()}
            response = requests.post(f"{BACKEND_API_BASE_URL}/predict_batch", files=files)
            response.raise_for_status() # Raise an exception for HTTP errors
            predictions = response.json()

            if predictions:
                st.success("Batch predictions completed!")
                st.json(predictions) # Display the predictions as JSON
            else:
                st.error("No predictions received from the API.")

        except requests.exceptions.ConnectionError:
            st.error(f"Connection Error: Could not connect to the backend API at {BACKEND_API_BASE_URL}/predict_batch. Please ensure the backend is running and the URL is correct.")
        except requests.exceptions.Timeout:
            st.error(f"Timeout Error: The request to the backend API at {BACKEND_API_BASE_URL}/predict_batch timed out.")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred during the API request: {e}")
        except json.JSONDecodeError:
            st.error(f"Failed to decode JSON response. API returned: {response.text}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

