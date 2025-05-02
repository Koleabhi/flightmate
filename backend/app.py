from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import matplotlib as plt
import seaborn as sns
import numpy as np
import os
from io import BytesIO
import base64
from utils import prepare_features
from utils import generate_recommendations


app = Flask(__name__)

# Load data and model
df = pd.read_csv('D:\\flightmate\\backend\\datasets\\cleaned_flight_dataset.csv')
model = joblib.load('D:\\flightmate\\backend\\models\\price_model.pkl')
recommender = joblib.load(r'D:\\flightmate\backend\\models\\recommender_knn.pkl')
#recommender_data = pd.read_csv(r'D:\\flightmate\\backend\\datasets\\recommender_data.csv')

@app.route('/')
def home():
    airlines = sorted(df['airline'].unique())
    cities = sorted(df['source_city'].unique())
    times = sorted(df['departure_time'].unique())
    classes = sorted(df['class'].unique())
    
    return render_template('index.html',
                         airlines=airlines,
                         cities=cities,
                         times=times,
                         classes=classes)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get only the required fields
        form_data = {
            'airline': request.form.get('airline'),
            'source_city': request.form.get('source_city'),
            'destination_city': request.form.get('destination_city'),
            'departure_time': request.form.get('departure_time'),
            'class': request.form.get('class'),
            'days_left': request.form.get('days_left')
        }
        
        # Validate all required fields
        for field in ['airline', 'source_city', 'destination_city', 
                    'departure_time', 'class', 'days_left']:
            if not form_data[field]:
                return "Missing required field: " + field, 400
        
        # Prepare features and predict
        features = prepare_features(form_data, df)
        price = round(model.predict([features])[0], 2)
        
        # Return JSON response if template fails
        try:
            return render_template('results.html',
                                prediction=price,
                                input_data=form_data)
        except:
            return {
                "prediction": price,
                "input_data": form_data
            }
    
    except Exception as e:
        # Return error as JSON if template rendering fails
        return {
            "error": str(e),
            "message": "Prediction failed but function executed"
        }, 500

# Add this new route alongside your existing ones
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Get only the required fields for recommendations
        rec_data = {
            'source_city': request.form.get('source_city'),
            'destination_city': request.form.get('destination_city'),
            'days_left': int(request.form.get('days_left')),
            'class': request.form.get('class')
        }
        
        # Generate recommendations
        recommendations = generate_recommendations(rec_data)
        
        return render_template('recommendations.html',
                            input_data=rec_data,
                            recommendations=recommendations)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)