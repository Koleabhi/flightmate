# backend/utils.py
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import joblib
import numpy as np

def prepare_features(form_data, df):
    """Convert form data to model features using only the 6 specified features"""
    # Convert categorical features to codes
    airline_code = df['airline'].astype('category').cat.codes[
        df['airline'] == form_data['airline']].values[0]
    source_code = df['source_city'].astype('category').cat.codes[
        df['source_city'] == form_data['source_city']].values[0]
    dest_code = df['destination_city'].astype('category').cat.codes[
        df['destination_city'] == form_data['destination_city']].values[0]
    time_code = df['departure_time'].astype('category').cat.codes[
        df['departure_time'] == form_data['departure_time']].values[0]
    
    # Convert class and days_left
    class_code = 0 if form_data['class'] == 'Economy' else 1
    days_left = int(form_data['days_left'])
    
    return np.array([airline_code, source_code, dest_code, time_code, class_code, days_left])

def generate_recommendations(input_data):
    """Generate travel recommendations based on user input."""
    try:
        import pandas as pd
        
        # Load cleaned dataset
        df = pd.read_csv('D:\\flightmate\\backend\\datasets\\cleaned_flight_dataset.csv')
        
        # Ensure duration_minutes column exists
        if 'duration_minutes' not in df.columns:
            df['duration_minutes'] = df['duration'].apply(
                lambda x: int(x.split('h')[0])*60 + int(x.split('h')[1].split('m')[0])
            )
        
        # Filter for relevant flights
        filtered = df[
            (df['source_city'] == input_data['source_city']) &
            (df['destination_city'] == input_data['destination_city']) &
            (df['class'] == input_data['class'])
        ].copy()
        
        if filtered.empty:
            return None
        
        # Calculate score
        epsilon = 1e-8
        filtered['score'] = (
            0.6 * (1 / (filtered['price'].rank(pct=True) + epsilon)) +
            0.3 * (filtered['stops'] == 'zero').astype(float) +
            0.1 * (1 / (filtered['duration_minutes'].rank(pct=True) + epsilon))
        )
        
        # Sort by score
        sorted_filtered = filtered.sort_values(by='score', ascending=False).reset_index(drop=True)
        best_plan = sorted_filtered.iloc[0]
        alternatives = sorted_filtered.iloc[1:4]
        
        return {
            'best_plan': {
                'airline': best_plan['airline'],
                'price': round(best_plan['price'], 2),
                'departure_time': best_plan['departure_time'],
                'stops': best_plan['stops'],
                'duration': best_plan['duration'],
                'score': round(best_plan['score'], 3)
            },
            'alternatives': [
                {
                    'airline': alt['airline'],
                    'price': round(alt['price'], 2),
                    'departure_time': alt['departure_time'],
                    'stops': alt['stops'],
                    'duration': alt['duration'],
                    'score': round(alt['score'], 3)
                } for _, alt in alternatives.iterrows()
            ]
        }
    
    except Exception as e:
        print(f"Recommendation generation failed: {str(e)}")
        return None