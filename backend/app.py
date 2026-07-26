# Import necessary libraries
import os
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API
import numpy as np # For numerical operations (though not directly used for prediction output in SuperKart)

# Initialize the Flask application
app = Flask(__name__)

# Load the pre-trained model
# IMPORTANT: Use a relative path for the model when deployed inside a Docker container
saved_model_path = 'superkart_sales_model_v1_0.joblib'
model = joblib.load(os.path.join(os.getcwd(), saved_model_path))

# Define a route for the home page (GET request)
@app.route('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Prediction API!"

# Define an endpoint for single prediction (POST request)
@app.route('/predict', methods=['POST'])
def predict():
    """
    This function handles POST requests to the '/predict' endpoint.
    It expects a JSON payload containing product and store details and returns
    the predicted sales as a JSON response.
    """
    try:
        # Get JSON data from the request
        json_ = request.json
        # Convert JSON to DataFrame
        # Ensure the keys in json_ match the model's expected feature names
        df_inference = pd.DataFrame(json_)

        # Make predictions
        predictions = model.predict(df_inference)

        # Return predictions as JSON. Round to 2 decimal places.
        return jsonify(predictions.round(2).tolist())

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Define an endpoint for batch prediction (POST request)
@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """
    This function handles POST requests to the '/predict_batch' endpoint.
    It expects a CSV file containing product and store details for multiple entries
    and returns the predicted sales as a dictionary in the JSON response.
    """
    try:
        # Get the uploaded CSV file from the request
        file = request.files['file']

        # Read the CSV file into a Pandas DataFrame
        input_data = pd.read_csv(file)

        # Make predictions for all products in the DataFrame
        predictions = model.predict(input_data).tolist()

        # Create a dictionary of predictions with a unique identifier for each row
        # Since Product_Id is dropped during preprocessing, we use a simple numerical index.
        output_dict = {f"product_idx_{i}": round(pred, 2) for i, pred in enumerate(predictions)}

        # Return the predictions dictionary as a JSON response
        return jsonify(output_dict)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    # In a production environment, use a WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)
