"""
ML-Based Risk Calculator - Enhanced with Machine Learning Models
Supports XGBoost, LightGBM, CatBoost, Random Forest, and Logistic Regression
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
import warnings
warnings.filterwarnings('ignore')

class MLRiskCalculator:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.model_path = os.path.join(os.path.dirname(__file__), 'models')
        os.makedirs(self.model_path, exist_ok=True)
        
    def create_synthetic_data(self, insurance_type, n_samples=5000):
        """Create synthetic training data for ML models"""
        np.random.seed(42)
        
        if insurance_type == 'auto':
            data = {
                'vehicle_age': np.random.randint(0, 20, n_samples),
                'driver_age': np.random.randint(18, 80, n_samples),
                'accident_history': np.random.randint(0, 5, n_samples),
                'mileage': np.random.randint(5000, 50000, n_samples),
                'vehicle_value': np.random.randint(200000, 2000000, n_samples),
                'location_risk': np.random.choice(['Low', 'Medium', 'High'], n_samples),
                'gender': np.random.choice(['Male', 'Female'], n_samples),
                'marital_status': np.random.choice(['Single', 'Married'], n_samples)
            }
            
        elif insurance_type == 'property':
            data = {
                'property_age': np.random.randint(0, 50, n_samples),
                'property_value': np.random.randint(1000000, 10000000, n_samples),
                'location_risk': np.random.choice(['Low', 'Medium', 'High'], n_samples),
                'construction_type': np.random.choice(['Concrete', 'Brick', 'Wood', 'Other'], n_samples),
                'flood_zone': np.random.choice([0, 1], n_samples),
                'security_systems': np.random.choice([0, 1], n_samples),
                'fire_safety': np.random.choice([0, 1], n_samples)
            }
            
        elif insurance_type == 'health':
            data = {
                'age': np.random.randint(18, 80, n_samples),
                'bmi': np.random.normal(25, 5, n_samples),
                'smoking': np.random.choice([0, 1], n_samples),
                'exercise_frequency': np.random.choice([0, 1, 2, 3, 4], n_samples),
                'chronic_conditions': np.random.randint(0, 3, n_samples),
                'family_history': np.random.choice([0, 1], n_samples),
                'occupation_risk': np.random.choice(['Low', 'Medium', 'High'], n_samples),
                'income': np.random.randint(200000, 2000000, n_samples)
            }
            
        elif insurance_type == 'life':
            data = {
                'age': np.random.randint(18, 80, n_samples),
                'gender': np.random.choice(['Male', 'Female'], n_samples),
                'occupation': np.random.choice(['Low Risk', 'Medium Risk', 'High Risk'], n_samples),
                'lifestyle': np.random.choice(['Healthy', 'Average', 'Risky'], n_samples),
                'coverage_amount': np.random.randint(500000, 10000000, n_samples),
                'medical_exams': np.random.choice([0, 1], n_samples),
                'smoking': np.random.choice([0, 1], n_samples),
                'income': np.random.randint(300000, 3000000, n_samples)
            }
            
        elif insurance_type == 'cyber':
            data = {
                'num_employees': np.random.randint(1, 1000, n_samples),
                'has_security_policy': np.random.choice([0, 1], n_samples),
                'past_incidents': np.random.randint(0, 5, n_samples),
                'uses_mfa': np.random.choice([0, 1], n_samples),
                'industry_risk': np.random.choice(['Low', 'Medium', 'High'], n_samples),
                'revenue': np.random.randint(1000000, 100000000, n_samples),
                'data_sensitivity': np.random.choice(['Low', 'Medium', 'High'], n_samples)
            }
            
        df = pd.DataFrame(data)
        
        # Generate realistic risk scores and premiums
        risk_score, premium = self._generate_target_variables(df, insurance_type)
        df['risk_score'] = risk_score
        df['premium'] = premium
        
        return df
    
    def _generate_target_variables(self, df, insurance_type):
        """Generate realistic target variables based on features"""
        n = len(df)
        
        if insurance_type == 'auto':
            risk_base = 5.0
            risk_score = risk_base - (df['vehicle_age'] * 0.1) + (df['accident_history'] * 1.5)
            risk_score += np.where(df['driver_age'] < 25, 2, 0)
            risk_score += np.where(df['driver_age'] > 65, 1, 0)
            risk_score += np.where(df['location_risk'] == 'High', 2, 0)
            premium = 15000 + risk_score * 3000 + df['vehicle_value'] * 0.02
            
        elif insurance_type == 'property':
            risk_base = 5.0
            risk_score = risk_base + (df['property_age'] * 0.05)
            risk_score += np.where(df['location_risk'] == 'High', 3, 0)
            risk_score += np.where(df['flood_zone'] == 1, 2, 0)
            risk_score -= np.where(df['security_systems'] == 1, 1, 0)
            premium = 25000 + risk_score * 5000 + df['property_value'] * 0.005
            
        elif insurance_type == 'health':
            risk_base = 5.0
            risk_score = risk_base + (df['age'] - 30) * 0.1
            risk_score += np.where(df['bmi'] > 30, 2, 0)
            risk_score += np.where(df['smoking'] == 1, 3, 0)
            risk_score += df['chronic_conditions'] * 1.5
            premium = 8000 + risk_score * 2000 + df['age'] * 300
            
        elif insurance_type == 'life':
            risk_base = 5.0
            risk_score = risk_base + (df['age'] - 30) * 0.15
            risk_score += np.where(df['occupation'] == 'High Risk', 3, 0)
            risk_score += np.where(df['lifestyle'] == 'Risky', 2, 0)
            risk_score += np.where(df['smoking'] == 1, 2, 0)
            premium = (df['coverage_amount'] / 1000) * (10 + risk_score)
            
        elif insurance_type == 'cyber':
            risk_base = 5.0
            risk_score = risk_base + (df['num_employees'] * 0.01)
            risk_score += df['past_incidents'] * 2
            risk_score -= np.where(df['has_security_policy'] == 1, 2, 0)
            risk_score -= np.where(df['uses_mfa'] == 1, 1, 0)
            premium = 50000 + risk_score * 10000 + df['num_employees'] * 500
            
        # Add some noise and ensure reasonable ranges
        risk_score += np.random.normal(0, 0.5, n)
        risk_score = np.clip(risk_score, 1, 10)
        premium = np.maximum(premium, 1000)
        
        return risk_score, premium
    
    def prepare_features(self, df, insurance_type, is_training=True):
        """Prepare features for ML models"""
        df_processed = df.copy()
        
        # Encode categorical variables
        categorical_cols = df_processed.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            if col in ['risk_score', 'premium']:
                continue
                
            encoder_key = f"{insurance_type}_{col}_encoder"
            
            if is_training:
                encoder = LabelEncoder()
                df_processed[col] = encoder.fit_transform(df_processed[col])
                self.encoders[encoder_key] = encoder
            else:
                if encoder_key in self.encoders:
                    # Handle unseen categories
                    unique_vals = set(df_processed[col])
                    known_vals = set(self.encoders[encoder_key].classes_)
                    new_vals = unique_vals - known_vals
                    
                    if new_vals:
                        # Replace unknown values with the most frequent known value
                        most_frequent = self.encoders[encoder_key].classes_[0]
                        df_processed[col] = df_processed[col].replace(list(new_vals), most_frequent)
                    
                    df_processed[col] = self.encoders[encoder_key].transform(df_processed[col])
        
        # Scale numerical features
        numerical_cols = df_processed.select_dtypes(include=[np.number]).columns
        numerical_cols = [col for col in numerical_cols if col not in ['risk_score', 'premium']]
        
        scaler_key = f"{insurance_type}_scaler"
        
        if is_training:
            scaler = StandardScaler()
            df_processed[numerical_cols] = scaler.fit_transform(df_processed[numerical_cols])
            self.scalers[scaler_key] = scaler
        else:
            if scaler_key in self.scalers:
                df_processed[numerical_cols] = self.scalers[scaler_key].transform(df_processed[numerical_cols])
        
        return df_processed
    
    def train_models(self, insurance_type, use_existing_data=False):
        """Train ML models for risk prediction"""
        print(f"Training ML models for {insurance_type} insurance...")
        
        # Generate or load training data
        if use_existing_data:
            # In a real scenario, you'd load actual historical data
            df = self.create_synthetic_data(insurance_type, n_samples=10000)
        else:
            df = self.create_synthetic_data(insurance_type, n_samples=10000)
        
        # Prepare features
        df_processed = self.prepare_features(df, insurance_type, is_training=True)
        
        # Separate features and targets
        feature_cols = [col for col in df_processed.columns if col not in ['risk_score', 'premium']]
        X = df_processed[feature_cols]
        y_risk = df_processed['risk_score']
        y_premium = df_processed['premium']
        
        # Split data
        X_train, X_test, y_risk_train, y_risk_test, y_premium_train, y_premium_test = train_test_split(
            X, y_risk, y_premium, test_size=0.2, random_state=42
        )
        
        models_config = {
            'random_forest': {
                'risk': RandomForestRegressor(n_estimators=100, random_state=42),
                'premium': RandomForestRegressor(n_estimators=100, random_state=42)
            },
            'xgboost': {
                'risk': xgb.XGBRegressor(n_estimators=100, random_state=42),
                'premium': xgb.XGBRegressor(n_estimators=100, random_state=42)
            },
            'lightgbm': {
                'risk': lgb.LGBMRegressor(n_estimators=100, random_state=42, verbose=-1),
                'premium': lgb.LGBMRegressor(n_estimators=100, random_state=42, verbose=-1)
            },
            'catboost': {
                'risk': cb.CatBoostRegressor(iterations=100, random_state=42, verbose=False),
                'premium': cb.CatBoostRegressor(iterations=100, random_state=42, verbose=False)
            }
        }
        
        best_model = None
        best_score = float('inf')
        
        for model_name, model_dict in models_config.items():
            try:
                # Train risk model
                risk_model = model_dict['risk']
                risk_model.fit(X_train, y_risk_train)
                risk_pred = risk_model.predict(X_test)
                risk_mse = mean_squared_error(y_risk_test, risk_pred)
                
                # Train premium model
                premium_model = model_dict['premium']
                premium_model.fit(X_train, y_premium_train)
                premium_pred = premium_model.predict(X_test)
                premium_mse = mean_squared_error(y_premium_test, premium_pred)
                
                total_mse = risk_mse + premium_mse
                print(f"{model_name}: Risk MSE: {risk_mse:.4f}, Premium MSE: {premium_mse:.4f}")
                
                if total_mse < best_score:
                    best_score = total_mse
                    best_model = model_name
                
                # Save models
                self.models[f"{insurance_type}_{model_name}_risk"] = risk_model
                self.models[f"{insurance_type}_{model_name}_premium"] = premium_model
                
                # Save to disk
                joblib.dump(risk_model, os.path.join(self.model_path, f"{insurance_type}_{model_name}_risk.pkl"))
                joblib.dump(premium_model, os.path.join(self.model_path, f"{insurance_type}_{model_name}_premium.pkl"))
                
            except Exception as e:
                print(f"Error training {model_name}: {str(e)}")
        
        # Save encoders and scalers
        joblib.dump(self.encoders, os.path.join(self.model_path, f"{insurance_type}_encoders.pkl"))
        joblib.dump(self.scalers, os.path.join(self.model_path, f"{insurance_type}_scalers.pkl"))
        
        print(f"Best model for {insurance_type}: {best_model}")
        return best_model
    
    def load_models(self, insurance_type, model_type='lightgbm'):
        """Load trained models from disk"""
        try:
            risk_model_path = os.path.join(self.model_path, f"{insurance_type}_{model_type}_risk.pkl")
            premium_model_path = os.path.join(self.model_path, f"{insurance_type}_{model_type}_premium.pkl")
            encoders_path = os.path.join(self.model_path, f"{insurance_type}_encoders.pkl")
            scalers_path = os.path.join(self.model_path, f"{insurance_type}_scalers.pkl")
            
            if all(os.path.exists(path) for path in [risk_model_path, premium_model_path, encoders_path, scalers_path]):
                self.models[f"{insurance_type}_{model_type}_risk"] = joblib.load(risk_model_path)
                self.models[f"{insurance_type}_{model_type}_premium"] = joblib.load(premium_model_path)
                self.encoders.update(joblib.load(encoders_path))
                self.scalers.update(joblib.load(scalers_path))
                return True
            else:
                print(f"Models not found for {insurance_type}. Training new models...")
                self.train_models(insurance_type)
                return True
        except Exception as e:
            print(f"Error loading models: {str(e)}")
            return False
    
    def predict_risk(self, insurance_type, features, model_type='lightgbm'):
        """Predict risk score and premium using ML models"""
        try:
            # Ensure models are loaded
            if not self.load_models(insurance_type, model_type):
                return None, None, "Error loading models"
            
            # Create DataFrame from features
            df = pd.DataFrame([features])
            
            # Prepare features
            df_processed = self.prepare_features(df, insurance_type, is_training=False)
            
            # Get feature columns (excluding target columns)
            feature_cols = [col for col in df_processed.columns if col not in ['risk_score', 'premium']]
            X = df_processed[feature_cols]
            
            # Make predictions
            risk_model = self.models[f"{insurance_type}_{model_type}_risk"]
            premium_model = self.models[f"{insurance_type}_{model_type}_premium"]
            
            risk_score = float(risk_model.predict(X)[0])
            premium = float(premium_model.predict(X)[0])
            
            # Ensure reasonable ranges
            risk_score = max(1.0, min(10.0, risk_score))
            premium = max(1000, premium)
            
            return risk_score, premium, None
            
        except Exception as e:
            return None, None, f"Prediction error: {str(e)}"

# Global instance
ml_calculator = MLRiskCalculator()

def calculate_auto_risk_ml(vehicle_age, driver_age, accident_history, mileage, **kwargs):
    """ML-based auto insurance risk calculation"""
    features = {
        'vehicle_age': vehicle_age,
        'driver_age': driver_age,
        'accident_history': accident_history,
        'mileage': mileage,
        'vehicle_value': kwargs.get('vehicle_value', 800000),
        'location_risk': kwargs.get('location_risk', 'Medium'),
        'gender': kwargs.get('gender', 'Male'),
        'marital_status': kwargs.get('marital_status', 'Single')
    }
    
    risk_score, premium, error = ml_calculator.predict_risk('auto', features)
    
    if error:
        # Fallback to basic calculation
        from .risk_calculator import calculate_auto_risk
        return calculate_auto_risk(vehicle_age, driver_age, accident_history, mileage)
    
    # Generate recommendation based on ML prediction
    if risk_score < 4:
        recommendation = """🤖 ML-Enhanced High Risk Assessment:
        • Advanced driver monitoring systems recommended
        • Usage-based insurance with telematics
        • Comprehensive safety training programs
        • Regular vehicle maintenance monitoring"""
    elif risk_score < 7:
        recommendation = """🤖 ML-Enhanced Moderate Risk Assessment:
        • Consider hybrid insurance models
        • Implement safety scoring systems
        • Periodic risk reassessment
        • Personalized premium adjustments"""
    else:
        recommendation = """🤖 ML-Enhanced Low Risk Assessment:
        • Optimal candidate for premium discounts
        • Long-term policy benefits
        • Advanced coverage options
        • Loyalty program eligibility"""
    
    return round(risk_score, 1), recommendation, int(premium)

def calculate_property_risk_ml(property_age, location_risk, construction_type, flood_zone, **kwargs):
    """ML-based property insurance risk calculation"""
    features = {
        'property_age': property_age,
        'property_value': kwargs.get('property_value', 3000000),
        'location_risk': location_risk,
        'construction_type': construction_type,
        'flood_zone': 1 if flood_zone else 0,
        'security_systems': kwargs.get('security_systems', 0),
        'fire_safety': kwargs.get('fire_safety', 1)
    }
    
    risk_score, premium, error = ml_calculator.predict_risk('property', features)
    
    if error:
        # Fallback to basic calculation
        from .risk_calculator import calculate_property_risk
        return calculate_property_risk(property_age, location_risk, construction_type, flood_zone)
    
    # Generate recommendation based on ML prediction
    if risk_score < 4:
        recommendation = """🤖 ML-Enhanced High Risk Property Assessment:
        • Smart home security systems integration
        • IoT-based monitoring for early detection
        • Climate change adaptation measures
        • Enhanced building materials recommendations"""
    elif risk_score < 7:
        recommendation = """🤖 ML-Enhanced Moderate Risk Property Assessment:
        • Regular property condition monitoring
        • Preventive maintenance scheduling
        • Risk mitigation system upgrades
        • Customized coverage adjustments"""
    else:
        recommendation = """🤖 ML-Enhanced Low Risk Property Assessment:
        • Premium property insurance rates
        • Advanced coverage options available
        • Green building certification benefits
        • Long-term protection strategies"""
    
    return round(risk_score, 1), recommendation, int(premium)

def calculate_health_risk_ml(age, bmi, smoking, exercise_frequency, chronic_conditions, family_history, **kwargs):
    """ML-based health insurance risk calculation"""
    exercise_map = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3, "Daily": 4}
    
    features = {
        'age': age,
        'bmi': bmi,
        'smoking': 1 if smoking else 0,
        'exercise_frequency': exercise_map.get(exercise_frequency, 2),
        'chronic_conditions': chronic_conditions,
        'family_history': 1 if family_history else 0,
        'occupation_risk': kwargs.get('occupation_risk', 'Medium'),
        'income': kwargs.get('income', 800000)
    }
    
    risk_score, premium, error = ml_calculator.predict_risk('health', features)
    
    if error:
        # Fallback to basic calculation
        from .risk_calculator import calculate_health_risk
        return calculate_health_risk(age, bmi, smoking, exercise_frequency, chronic_conditions, family_history)
    
    # Generate recommendation based on ML prediction
    if risk_score < 4:
        recommendation = """🤖 ML-Enhanced High Risk Health Assessment:
        • Personalized wellness programs with AI coaching
        • Wearable device integration for health monitoring
        • Telemedicine and remote patient monitoring
        • Predictive health analytics for early intervention"""
    elif risk_score < 7:
        recommendation = """🤖 ML-Enhanced Moderate Risk Health Assessment:
        • Health tracking app integration
        • Regular health screening reminders
        • Lifestyle modification support programs
        • Dynamic premium adjustment based on health improvements"""
    else:
        recommendation = """🤖 ML-Enhanced Low Risk Health Assessment:
        • Premium health insurance benefits
        • Advanced preventive care coverage
        • Wellness reward programs
        • Long-term health protection strategies"""
    
    return round(risk_score, 1), recommendation, int(premium)

def calculate_life_risk_ml(age, gender, occupation, lifestyle, coverage_amount, medical_exams, **kwargs):
    """ML-based life insurance risk calculation"""
    features = {
        'age': age,
        'gender': gender,
        'occupation': occupation,
        'lifestyle': lifestyle,
        'coverage_amount': coverage_amount,
        'medical_exams': 1 if medical_exams else 0,
        'smoking': kwargs.get('smoking', 0),
        'income': kwargs.get('income', 1000000)
    }
    
    risk_score, premium, error = ml_calculator.predict_risk('life', features)
    
    if error:
        # Fallback to basic calculation
        from .risk_calculator import calculate_life_risk
        return calculate_life_risk(age, gender, occupation, lifestyle, coverage_amount, medical_exams)
    
    # Calculate mortality rate estimate
    mortality_rate = round(0.1 + (age - 20) * 0.01 + (0.1 if gender == "Male" else 0), 2)
    
    # Generate recommendation based on ML prediction
    if risk_score < 4:
        recommendation = """🤖 ML-Enhanced High Risk Life Assessment:
        • Specialized underwriting with additional medical exams
        • Lifestyle modification programs with premium incentives
        • Regular health monitoring and check-ins
        • Flexible premium payment options"""
    elif risk_score < 7:
        recommendation = """🤖 ML-Enhanced Moderate Risk Life Assessment:
        • Standard life insurance with competitive rates
        • Optional rider benefits for enhanced protection
        • Health improvement tracking for premium discounts
        • Family protection planning services"""
    else:
        recommendation = """🤖 ML-Enhanced Low Risk Life Assessment:
        • Preferred plus life insurance rates
        • Maximum coverage options available
        • Long-term financial planning integration
        • Estate planning and wealth transfer strategies"""
    
    return round(risk_score, 1), recommendation, int(premium), mortality_rate

def calculate_cyber_risk_ml(num_employees, has_security_policy, past_incidents, uses_mfa, **kwargs):
    """ML-based cyber insurance risk calculation"""
    features = {
        'num_employees': num_employees,
        'has_security_policy': 1 if has_security_policy else 0,
        'past_incidents': past_incidents,
        'uses_mfa': 1 if uses_mfa else 0,
        'industry_risk': kwargs.get('industry_risk', 'Medium'),
        'revenue': kwargs.get('revenue', 10000000),
        'data_sensitivity': kwargs.get('data_sensitivity', 'Medium')
    }
    
    risk_score, premium, error = ml_calculator.predict_risk('cyber', features)
    
    if error:
        # Fallback to basic calculation
        from .risk_calculator import calculate_cyber_risk
        return calculate_cyber_risk(num_employees, has_security_policy, past_incidents, uses_mfa)
    
    # Generate recommendation based on ML prediction
    if risk_score < 4:
        recommendation = """🤖 ML-Enhanced High Cyber Risk Assessment:
        • Advanced threat detection with AI-powered security
        • 24/7 security operations center monitoring
        • Incident response team on retainer
        • Regular penetration testing and vulnerability assessments"""
    elif risk_score < 7:
        recommendation = """🤖 ML-Enhanced Moderate Cyber Risk Assessment:
        • Enhanced cybersecurity framework implementation
        • Employee security awareness training programs
        • Regular security audits and compliance checks
        • Cyber insurance with comprehensive coverage"""
    else:
        recommendation = """🤖 ML-Enhanced Low Cyber Risk Assessment:
        • Maintain excellent cybersecurity posture
        • Premium cyber insurance rates available
        • Advanced threat intelligence integration
        • Cyber resilience and business continuity planning"""
    
    return round(risk_score, 1), recommendation, int(premium)
