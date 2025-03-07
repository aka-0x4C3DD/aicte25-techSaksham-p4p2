"""
Configuration file for model features and mappings.
This helps reconcile differences between form field names and model feature expectations.
"""

# Expected feature lists for each model
MODEL_FEATURES = {
    'diabetes': [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
    ],
    'heart': [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ],
    'hypothyroid': [
        # Complete list of features expected by hypothyroid model - 29 features
        'age', 'sex', 'on_thyroxine', 'query_hypothyroid', 'on_antithyroid_medication', 
        'sick', 'pregnant', 'thyroid_surgery', 'I131_treatment', 'query_hyperthyroid',
        'lithium', 'goitre', 'tumor', 'hypopituitary', 'psych', 'TSH_measured', 'TSH', 
        'T3_measured', 'T3', 'TT4_measured', 'TT4', 'T4U_measured', 'T4U', 'FTI_measured', 
        'FTI', 'TBG_measured', 'TBG', 'referral_source', 'other'
    ],
    'lung': [
        'GENDER', 'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY',
        'PEER_PRESSURE', 'CHRONIC_DISEASE', 'FATIGUE', 'ALLERGY', 'WHEEZING',
        'ALCOHOL_CONSUMING', 'COUGHING', 'SHORTNESS_OF_BREATH', 
        'SWALLOWING_DIFFICULTY', 'CHEST_PAIN'
    ],
    'parkinsons': [
        'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 
        'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP', 
        'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5', 
        'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR', 'RPDE', 'DFA', 
        'spread1', 'spread2', 'D2', 'PPE'
    ]
}

# Mapping from form field names to model feature names
FEATURE_MAPPINGS = {
    'hypothyroid': {
        # Map form fields to model expected features
        'age': 'age',
        'sex': 'sex',
        'on_thyroxine': 'on_thyroxine',
        'query_hypothyroid': 'query_hypothyroid',
        'on_antithyroid_medication': 'on_antithyroid_medication',
        'sick': 'sick',
        'pregnant': 'pregnant',
        'thyroid_surgery': 'thyroid_surgery',
        'TSH': 'TSH',
        'T3': 'T3',
        'TT4': 'TT4',
        'T4U': 'T4U',
        'FTI': 'FTI'
    },
    'diabetes': {
        # Map any inconsistent field names if needed
        'pregnancies': 'Pregnancies',
        'glucose': 'Glucose',
        'blood_pressure': 'BloodPressure',
        'skin_thickness': 'SkinThickness',
        'insulin': 'Insulin',
        'bmi': 'BMI',
        'diabetes_pedigree': 'DiabetesPedigreeFunction',
        'age': 'Age'
    }
}

# Default values for features when missing
DEFAULT_FEATURE_VALUES = {
    'hypothyroid': {
        # Initialize with zeros for all expected features
        'age': 0, 'sex': 0, 'on_thyroxine': 0, 'query_hypothyroid': 0,
        'on_antithyroid_medication': 0, 'sick': 0, 'pregnant': 0, 'thyroid_surgery': 0,
        'I131_treatment': 0, 'query_hyperthyroid': 0, 'lithium': 0, 'goitre': 0,
        'tumor': 0, 'hypopituitary': 0, 'psych': 0, 'TSH_measured': 1, 'TSH': 0.0,
        'T3_measured': 1, 'T3': 0.0, 'TT4_measured': 1, 'TT4': 0.0, 'T4U_measured': 1, 'T4U': 0.0,
        'FTI_measured': 1, 'FTI': 0.0, 'TBG_measured': 0, 'TBG': 0.0, 'referral_source': 0, 'other': 0
    },
    'lung': {
        # Standard defaults for lung cancer model
        'GENDER': 0, 'AGE': 0, 'SMOKING': 0, 'YELLOW_FINGERS': 0, 'ANXIETY': 0,
        'PEER_PRESSURE': 0, 'CHRONIC_DISEASE': 0, 'FATIGUE': 0, 'ALLERGY': 0, 'WHEEZING': 0,
        'ALCOHOL_CONSUMING': 0, 'COUGHING': 0, 'SHORTNESS_OF_BREATH': 0, 'SWALLOWING_DIFFICULTY': 0, 'CHEST_PAIN': 0
    }
}

# Feature display names for UI (if needed)
FEATURE_DISPLAY_NAMES = {
    'DiabetesPedigreeFunction': 'Diabetes Pedigree Function',
    'MDVP:Fo(Hz)': 'Average Vocal Fundamental Frequency',
    'MDVP:Fhi(Hz)': 'Maximum Vocal Fundamental Frequency',
    'MDVP:Flo(Hz)': 'Minimum Vocal Fundamental Frequency',
    'MDVP:Jitter(%)': 'Frequency Variation Percentage',
    'MDVP:Jitter(Abs)': 'Absolute Jitter',
    'MDVP:RAP': 'Relative Amplitude Perturbation',
    'MDVP:PPQ': 'Five-point Period Perturbation Quotient',
    'Jitter:DDP': 'Average Absolute Difference of Differences',
    'MDVP:Shimmer': 'Local Shimmer',
    'MDVP:Shimmer(dB)': 'Shimmer in dB',
    'Shimmer:APQ3': 'Three-point Amplitude Perturbation Quotient',
    'Shimmer:APQ5': 'Five-point Amplitude Perturbation Quotient',
    'MDVP:APQ': 'Amplitude Perturbation Quotient',
    'Shimmer:DDA': 'Average Absolute Differences Between Consecutive Differences',
    'NHR': 'Noise-to-Harmonics Ratio',
    'HNR': 'Harmonics-to-Noise Ratio',
    'RPDE': 'Recurrence Period Density Entropy',
    'DFA': 'Detrended Fluctuation Analysis',
    'spread1': 'Spread1',
    'spread2': 'Spread2',
    'D2': 'Correlation Dimension',
    'PPE': 'Pitch Period Entropy'
}
