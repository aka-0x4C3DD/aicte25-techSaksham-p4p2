import os
import re
import pickle
import logging
import traceback
from typing import Dict, Tuple, List, Any, Optional
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

# Import utility functions
from utils import load_model, load_scaler
from model_config import MODEL_FEATURES

logger = logging.getLogger("MedicalDiagnosisServer")

class ModelManager:
    """Class to manage machine learning models"""
    
    def __init__(self, model_dir: str):
        # Remove any trailing/leading whitespace
        self.model_dir = model_dir.strip() if model_dir else "models"
        self.models = {}
        self.scalers = {}
        self.model_info = {}
        self.available_models = {}
        self.model_count = 0
        
        # Base model information structure with correct feature lists from model_config.py
        self.base_model_info = {
            'diabetes': {
                'label_mapping': {0: 'No Diabetes', 1: 'Diabetes'},
                'features': MODEL_FEATURES.get('diabetes', [])
            },
            'heart': {
                'label_mapping': {0: 'No Heart Disease', 1: 'Heart Disease'},
                'features': MODEL_FEATURES.get('heart', [])
            },
            'hypothyroid': {
                'label_mapping': {0: 'No Hypothyroidism', 1: 'Hypothyroidism'},
                'features': MODEL_FEATURES.get('hypothyroid', [])
            },
            'lung': {
                'label_mapping': {0: 'No Lung Cancer', 1: 'Lung Cancer'},
                'features': MODEL_FEATURES.get('lung', [])
            },
            'parkinsons': {
                'label_mapping': {0: 'No Parkinson\'s', 1: 'Parkinson\'s'},
                'features': MODEL_FEATURES.get('parkinsons', [])
            }
        }
    
    def detect_model_files(self) -> Dict:
        """Scan the models directory to detect available model files"""
        model_files = {}
        
        if not os.path.exists(self.model_dir):
            logger.error(f"Models directory does not exist: {self.model_dir}")
            return model_files
            
        logger.info(f"Scanning models directory: {self.model_dir}")
        
        # List all files in the models directory
        files = os.listdir(self.model_dir)
        logger.info(f"Found {len(files)} files in models directory")
        
        # Pattern to match model files and extract disease and algorithm type
        model_pattern = re.compile(r'(diabetes|heart|hypothyroid|lung|parkinsons)_(\w+)_model\.(pkl|h5|keras)')
        
        # Scan for model files
        for file in files:
            match = model_pattern.match(file)
            if match:
                disease = match.group(1)
                algorithm = match.group(2)
                file_ext = match.group(3)
                
                if disease not in model_files:
                    model_files[disease] = []
                    
                model_files[disease].append({
                    'algorithm': algorithm,
                    'file': file,
                    'format': 'tensorflow' if file_ext in ['h5', 'keras'] else 'sklearn'
                })
                
                logger.info(f"Found {algorithm} model for {disease}: {file}")
        
        return model_files
        
    def load_all_models(self) -> Tuple[Dict, int]:
        """Load all available models into memory"""
        self.available_models = {}
        self.model_count = 0
        
        # Check if models directory exists
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
            logger.warning(f"Created models directory: {self.model_dir}")
        
        # Detect model files in the directory
        model_files = self.detect_model_files()
        
        # Initialize model_info from base structure
        self.model_info = {disease: info.copy() for disease, info in self.base_model_info.items()}
        
        # Process each detected model
        for disease, model_list in model_files.items():
            if disease not in self.base_model_info:
                logger.warning(f"Unknown disease type in model file: {disease}")
                continue
                
            # Sort models to prioritize certain algorithms (e.g., use random_forest if available)
            model_list.sort(key=lambda x: 0 if x['algorithm'] == 'random_forest' else 1)
            
            if model_list:
                # Use the first available model (highest priority)
                selected_model = model_list[0]
                model_path = os.path.join(self.model_dir, selected_model['file'])
                scaler_path = os.path.join(self.model_dir, f"{disease}_scaler.pkl")
                
                # Update model_info with the selected model file
                self.model_info[disease]['file'] = selected_model['file']
                self.model_info[disease]['algorithm'] = selected_model['algorithm']
                self.model_info[disease]['format'] = selected_model['format']
                
                logger.info(f"Selected {selected_model['algorithm']} model for {disease}")
                
                try:
                    # Load model based on format
                    self.models[disease] = load_model(model_path)
                    
                    # Load scaler if exists
                    self.scalers[disease] = load_scaler(scaler_path)
                    if self.scalers[disease] is None:
                        logger.warning(f"No scaler found for {disease}. Using default StandardScaler.")
                        self.scalers[disease] = StandardScaler()
                        
                    self.available_models[disease] = True
                    self.model_count += 1
                    
                except Exception as e:
                    logger.error(f"Error loading {disease} model: {str(e)}")
                    logger.error(traceback.format_exc())
                    self.available_models[disease] = False
            else:
                logger.warning(f"No model file found for {disease}")
                self.available_models[disease] = False
        
        logger.info(f"Loaded {self.model_count} models")
        return self.available_models, self.model_count
    
    def get_model(self, disease: str) -> Optional[Any]:
        """Get a model by disease type"""
        return self.models.get(disease)
    
    def get_scaler(self, disease: str) -> Optional[Any]:
        """Get a scaler by disease type"""
        return self.scalers.get(disease)
    
    def get_model_info(self, disease: str) -> Optional[Dict]:
        """Get model info by disease type"""
        return self.model_info.get(disease)
