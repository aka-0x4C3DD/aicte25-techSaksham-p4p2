import os
import pickle
import logging
import numpy as np
import tensorflow as tf
from typing import Union, Any, Dict, Optional, Tuple

logger = logging.getLogger("MedicalDiagnosisServer")

def load_model(model_path: str) -> Any:
    """
    Load a machine learning model from the specified path.
    
    Args:
        model_path: Path to the model file
        
    Returns:
        The loaded model object
        
    Raises:
        FileNotFoundError: If the model file doesn't exist
        Exception: If there's an error loading the model
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
        
    try:
        if model_path.endswith(('.h5', '.keras')):
            model = tf.keras.models.load_model(model_path)
            logger.info(f"Loaded TensorFlow model from {model_path}")
        else:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            logger.info(f"Loaded scikit-learn model from {model_path}")
        return model
    except Exception as e:
        logger.error(f"Error loading model from {model_path}: {str(e)}")
        raise

def load_scaler(scaler_path: str) -> Any:
    """
    Load a scaler object from the specified path.
    
    Args:
        scaler_path: Path to the scaler file
        
    Returns:
        The loaded scaler object or None if file doesn't exist
        
    Raises:
        Exception: If there's an error loading the scaler
    """
    if not os.path.exists(scaler_path):
        logger.warning(f"Scaler file not found: {scaler_path}")
        return None
        
    try:
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        logger.info(f"Loaded scaler from {scaler_path}")
        return scaler
    except Exception as e:
        logger.error(f"Error loading scaler from {scaler_path}: {str(e)}")
        raise

def validate_numeric_input(value: Union[str, float, int], name: str = "value") -> float:
    """
    Validate and convert a numeric input.
    
    Args:
        value: Input value to validate
        name: Name of the parameter (for error messages)
        
    Returns:
        Validated float value
        
    Raises:
        ValueError: If the value is not a valid number
    """
    try:
        float_value = float(value)
        return float_value
    except (ValueError, TypeError):
        raise ValueError(f"Invalid numeric value for {name}: {value}")

def validate_binary_input(value: Union[str, int], name: str = "value") -> int:
    """
    Validate and convert a binary (0/1) input.
    
    Args:
        value: Input value to validate
        name: Name of the parameter (for error messages)
        
    Returns:
        Validated binary value (0 or 1)
        
    Raises:
        ValueError: If the value is not 0 or 1
    """
    try:
        # Convert to integer first
        int_value = int(value)
        
        # Check if the value is 0 or 1
        if int_value not in [0, 1]:
            raise ValueError(f"Binary value for {name} must be 0 or 1, got {value}")
        
        return int_value
    except (ValueError, TypeError):
        raise ValueError(f"Invalid binary value for {name}: {value}")

def format_prediction_result(prediction: int, prediction_label: str, 
                            confidence: Optional[float] = None,
                            input_data: Optional[Dict] = None) -> Dict:
    """
    Format prediction results into a standardized dictionary.
    
    Args:
        prediction: Raw prediction value (typically 0 or 1)
        prediction_label: Human-readable label for the prediction
        confidence: Confidence score (if available)
        input_data: Dictionary of input values used for prediction
        
    Returns:
        Dictionary containing formatted prediction results
    """
    result = {
        'prediction': int(prediction),
        'prediction_label': prediction_label
    }
    
    if confidence is not None:
        result['confidence'] = float(confidence)
        
    if input_data is not None:
        result['input_data'] = input_data
        
    return result

def make_prediction(model, input_data, label_mapping=None):
    """Make a prediction using the model"""
    try:
        # For TensorFlow models
        if hasattr(model, 'predict'):
            raw_prediction = model.predict(input_data)
            if isinstance(raw_prediction, np.ndarray) and raw_prediction.size == 1:
                confidence = float(raw_prediction[0])
                prediction = 1 if confidence >= 0.5 else 0
            else:
                prediction = 1 if raw_prediction[0][0] >= 0.5 else 0
                confidence = float(raw_prediction[0][0]) if prediction == 1 else 1 - float(raw_prediction[0][0])
        # For sklearn models
        else:
            try:
                # Try to get probability scores
                proba = model.predict_proba(input_data)[0]
                prediction = 1 if proba[1] >= 0.5 else 0
                confidence = float(proba[1]) if prediction == 1 else float(proba[0])
            except:
                # Fall back to simple prediction
                prediction = int(model.predict(input_data)[0])
                confidence = 0.8  # Default confidence when probability not available
        
        # Ensure confidence is between 0 and 1 (0-100%)
        confidence = min(max(confidence, 0.0), 1.0)
        
        # Map the numeric prediction to a label
        prediction_label = None
        if label_mapping and prediction in label_mapping:
            prediction_label = label_mapping[prediction]
        elif prediction == 1:
            prediction_label = "Positive"
        elif prediction == 0:
            prediction_label = "Negative"
        else:
            prediction_label = "Unknown"
            
        # Remove the "(2)" part that might be appended to the prediction label
        if prediction_label and " (" in prediction_label:
            prediction_label = prediction_label.split(" (")[0]
            
        # For hypothyroid predictions, map prediction_label appropriately
        if prediction_label == "Positive":
            if label_mapping and "hypothyroid" in str(label_mapping).lower():
                prediction_label = "Hypothyroidism"
        
        return prediction, prediction_label, confidence
        
    except Exception as e:
        import traceback
        logging.error(f"Prediction error: {str(e)}")
        logging.error(traceback.format_exc())
        raise
