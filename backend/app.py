
import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the pre-trained model
saved_model_path = r'/content/drive/MyDrive/Colab Notebooks/Model Deployment/superkart_sales_model_v1_0.joblib'
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

if __name__ == '__main__':
    # Run the app locally for testing
    # In a production environment, use a WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)
