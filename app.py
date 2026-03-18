import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

MODEL_PATH = 'model.pkl'
model = None

@app.before_request
def load_model():
    global model
    if model is None and os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
        except Exception as e:
            print(f"Error loading model: {e}")

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not yet available. Please wait or train the model.'}), 500
    
    try:
        data = request.json
        # Convert numerical fields to appropriate types
        df_input = pd.DataFrame([{
            'Year': float(data.get('year', 2023)),
            'Duration': float(data.get('duration', 120)),
            'Genre': str(data.get('genre', 'Drama')),
            'Votes': float(data.get('votes', 100)),
            'Director': str(data.get('director', 'Unknown')),
            'Actor 1': str(data.get('actor1', 'Unknown')),
            'Actor 2': str(data.get('actor2', 'Unknown')),
            'Actor 3': str(data.get('actor3', 'Unknown'))
        }])
        
        # Predict using the loaded model
        prediction = model.predict(df_input)[0]
        
        return jsonify({
            'success': True,
            'prediction': round(float(prediction), 1)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
