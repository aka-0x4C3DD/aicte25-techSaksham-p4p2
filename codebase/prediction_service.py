import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from sklearn.preprocessing import StandardScaler

# Import utility functions
from utils import validate_numeric_input, validate_binary_input, make_prediction
from model_config import MODEL_FEATURES, FEATURE_MAPPINGS, DEFAULT_FEATURE_VALUES

logger = logging.getLogger("MedicalDiagnosisServer")

class PredictionService:
    """Service class for making predictions"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
    
    def prepare_input_data(self, disease: str, form_data: Dict) -> Dict:
        """Prepare and validate input data from form submission"""
        input_data = {}
        model_info = self.model_manager.get_model_info(disease)
        
        if not model_info:
            raise ValueError(f"No model info found for disease: {disease}")
            
        expected_features = model_info['features']
        logger.info(f"Expected features for {disease}: {expected_features}")
        logger.info(f"Form data keys: {list(form_data.keys())}")
        
        # Create exact mapping between form fields and expected feature names
        for feature in expected_features:
            # Try exact match
            if feature in form_data:
                value = form_data[feature]
            else:
                # Try case-insensitive match
                field_key = next((k for k in form_data.keys() if k.lower() == feature.lower()), None)
                if field_key:
                    value = form_data[field_key]
                else:
                    # If no match, use default value
                    logger.warning(f"Missing feature {feature} in form data, using default value 0")
                    value = 0
            
            # Validate based on feature type
            if feature.lower() in ['sex', 'gender', 'fbs', 'exang', 'smoking', 
                             'yellow_fingers', 'anxiety', 'peer_pressure', 
                             'chronic_disease', 'fatigue', 'allergy', 'wheezing', 
                             'alcohol_consuming', 'coughing', 'shortness_of_breath', 
                             'swallowing_difficulty', 'chest_pain', 'on_thyroxine', 
                             'query_hypothyroid', 'on_antithyroid_medication', 'sick', 
                             'pregnant', 'thyroid_surgery']:
                input_data[feature] = validate_binary_input(value, feature)
            else:
                input_data[feature] = validate_numeric_input(value, feature)
        
        return input_data
    
    def predict(self, disease: str, input_data: Dict) -> Dict:
        """Make a prediction for the given disease and input data"""
        model = self.model_manager.get_model(disease)
        scaler = self.model_manager.get_scaler(disease)
        model_info = self.model_manager.get_model_info(disease)
        
        if not model:
            raise ValueError(f"No model found for disease: {disease}")
            
        if not model_info:
            raise ValueError(f"No model info found for disease: {disease}")
        
        # Get complete list of expected features for this model from config
        expected_features = MODEL_FEATURES.get(disease, model_info['features'])
        
        # Special handling for hypothyroid model
        if disease == 'hypothyroid':
            # Create a dataframe with all required features
            aligned_input = DEFAULT_FEATURE_VALUES.get('hypothyroid', {}).copy()
            
            # Update with the actual input values
            for key, value in input_data.items():
                # Map form field to model feature name if mapping exists
                feature_name = FEATURE_MAPPINGS.get('hypothyroid', {}).get(key, key)
                aligned_input[feature_name] = value
            
            # Ensure all required features are present
            for feature in expected_features:
                if feature not in aligned_input:
                    aligned_input[feature] = 0
                    logger.warning(f"Using default value 0 for missing feature: {feature}")
        else:
            # Standard processing for other models
            aligned_input = {}
            for feature in expected_features:
                # Direct match
                if feature in input_data:
                    aligned_input[feature] = input_data[feature]
                else:
                    # Try case-insensitive match
                    key = next((k for k in input_data.keys() if k.lower() == feature.lower()), None)
                    if key:
                        aligned_input[feature] = input_data[key]
                    else:
                        # Default value if feature is missing
                        aligned_input[feature] = 0
                        logger.warning(f"Using default value 0 for missing feature: {feature}")
        
        # Create dataframe with exact column names needed by the model
        df = pd.DataFrame([aligned_input], columns=expected_features)
        logger.info(f"Input dataframe columns: {df.columns.tolist()}")
        
        # Special handling for heart model scaler which may not be fitted
        if disease == 'heart' and not hasattr(scaler, 'mean_'):
            logger.info("Fitting new scaler for heart model")
            scaler = StandardScaler()
            # Just fit with the input data so it can transform
            scaler.fit(df)
            self.model_manager.scalers[disease] = scaler
        
        # Scale input data
        try:
            input_scaled = scaler.transform(df)
        except Exception as e:
            logger.error(f"Error in scaling: {e}")
            logger.info(f"Dataframe used for scaling: {df}")
            logger.info(f"Dataframe dtypes: {df.dtypes}")
            # Fallback: if scaling fails, try using raw data
            input_scaled = df.values
            
        # Get prediction
        try:
            prediction, prediction_label, confidence = make_prediction(
                model, input_scaled, model_info['label_mapping']
            )
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise
        
        result = {
            'prediction': int(prediction),
            'prediction_label': prediction_label,
            'confidence': confidence,
            'input_data': {k: v for k, v in aligned_input.items() if k in model_info['features']}
        }
        
        return result
