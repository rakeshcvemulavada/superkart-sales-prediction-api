
import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# Load the pre-trained model
saved_model_path = r'/content/drive/MyDrive/Colab Notebooks/Model Deployment/backend/superkart_sales_model_v1_0.joblib'
model = joblib.load(saved_model_path)

@app.route('/')
def home():
    return "Welcome to the SuperKart Sales Prediction API!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from the request
        json_ = request.json
        # Convert JSON to DataFrame
        df_inference = pd.DataFrame(json_)

        # Make predictions
        predictions = model.predict(df_inference)

        # Return predictions as JSON
        return jsonify(predictions.tolist())

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    try:
        # Get the uploaded CSV file from the request
        file = request.files['file']

        # Read the CSV file into a Pandas DataFrame
        input_data = pd.read_csv(file)

        # Make predictions for all products in the DataFrame
        predictions = model.predict(input_data).tolist()

        # Create a dictionary of predictions with a unique identifier for each row
        # Since Product_Id is dropped, we can use a generated index or assume an 'id' column.
        # For this example, let's use a simple numerical index.
        output_dict = {f"product_idx_{i}": pred for i, pred in enumerate(predictions)}

        # Return the predictions dictionary as a JSON response
        return jsonify(output_dict)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Run the app locally for testing
    # In a production environment, use a WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)
