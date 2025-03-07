from flask import Flask, jsonify, request, render_template, url_for, redirect, flash
import os
import logging
import traceback
from datetime import datetime

# Import our custom modules
from model_manager import ModelManager
from prediction_service import PredictionService
from utils import format_prediction_result

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MedicalDiagnosisServer")

app = Flask(__name__)
app.secret_key = 'medical_diagnosis_secret_key'

# Get models directory from environment variable or use default
MODEL_DIR = os.environ.get('MODELS_PATH', 'models')
if not os.path.isabs(MODEL_DIR):
    MODEL_DIR = os.path.abspath(MODEL_DIR)

# Strip any whitespace to avoid path issues
MODEL_DIR = MODEL_DIR.strip()

logger.info(f"Using models directory: {MODEL_DIR}")

# Initialize model manager and load models
model_manager = ModelManager(MODEL_DIR)
available_models, model_count = model_manager.load_all_models()

# Initialize prediction service
prediction_service = PredictionService(model_manager)

@app.route('/')
def index():
    """Render the home page"""
    # Add model algorithm type to the template context
    model_algorithms = {
        disease: info.get('algorithm', 'unknown') 
        for disease, info in model_manager.model_info.items() 
        if available_models.get(disease, False)
    }
    
    return render_template(
        'index.html', 
        available_models=available_models,
        model_count=model_count,
        model_algorithms=model_algorithms
    )

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_available': model_count > 0
    })

@app.route('/models')
def get_models():
    """Return info about available models"""
    return jsonify({
        'available_models': available_models,
        'count': model_count
    })

@app.route('/predict/<disease>', methods=['GET', 'POST'])
def predict(disease):
    """Handle disease prediction"""
    # Check if disease model exists
    if disease not in model_manager.model_info:
        flash(f"Unknown disease type: {disease}", "danger")
        return redirect(url_for('index'))
    
    if not available_models.get(disease, False):
        flash(f"The {disease} model is not available", "danger") 
        return redirect(url_for('index'))
    
    # For GET requests, render the input form
    if request.method == 'GET':
        return render_template(
            f"{disease}.html", 
            features=model_manager.model_info[disease]['features']
        )
    
    # For POST requests, process the prediction
    try:
        # Prepare input data from form
        input_data = prediction_service.prepare_input_data(disease, request.form)
        
        # Make prediction
        result = prediction_service.predict(disease, input_data)
        
        return render_template(
            'result.html', 
            result=result,
            disease=disease,
            disease_name=disease.replace('_', ' ').title()
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        logger.error(traceback.format_exc())
        flash(f"Error making prediction: {str(e)}", "danger")
        return render_template(f"{disease}.html", error=str(e))

@app.route('/api/predict/<disease>', methods=['POST'])
def api_predict(disease):
    """API endpoint for prediction"""
    if disease not in model_manager.model_info:
        return jsonify({'error': f"Unknown disease type: {disease}"}), 400
    
    if not available_models.get(disease, False):
        return jsonify({'error': f"The {disease} model is not available"}), 404
    
    try:
        # Get input data from JSON request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': "Missing input data"}), 400
        
        # Check if all required features are provided
        features = model_manager.model_info[disease]['features']
        for feature in features:
            if feature not in data:
                return jsonify({'error': f"Missing required feature: {feature}"}), 400
        
        # Make prediction
        result = prediction_service.predict(disease, data)
        
        # Return result (exclude input_data)
        return jsonify({
            'prediction': result['prediction'],
            'prediction_label': result['prediction_label'],
            'confidence': result['confidence']
        })
        
    except Exception as e:
        logger.error(f"API prediction error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info(f"Starting Medical Diagnosis Server with {model_count} models from {MODEL_DIR}")
    app.run(debug=True, host='0.0.0.0', port=5000)
