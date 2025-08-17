"""
ML-Based Fraud Detector - Enhanced with Machine Learning Models
Supports Isolation Forest, Local Outlier Factor, XGBoost, Random Forest
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import xgboost as xgb
import lightgbm as lgb
try:
    from imblearn.over_sampling import SMOTE
    SMOTE_AVAILABLE = True
except ImportError:
    SMOTE_AVAILABLE = False
    print("Warning: imbalanced-learn not available. SMOTE will be skipped.")
import warnings
warnings.filterwarnings('ignore')

class MLFraudDetector:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.model_path = os.path.join(os.path.dirname(__file__), 'fraud_models')
        os.makedirs(self.model_path, exist_ok=True)
        
    def create_synthetic_fraud_data(self, n_samples=10000, fraud_rate=0.05):
        """Create synthetic fraud detection training data"""
        np.random.seed(42)
        
        n_fraud = int(n_samples * fraud_rate)
        n_normal = n_samples - n_fraud
        
        # Normal claims
        normal_data = {
            'claim_amount': np.random.lognormal(10, 1.5, n_normal),  # Log-normal distribution
            'claim_type': np.random.choice(['Auto', 'Property', 'Health', 'Life', 'Cyber'], n_normal),
            'claimant_age': np.random.randint(18, 80, n_normal),
            'policy_duration': np.random.randint(1, 120, n_normal),  # months
            'num_previous_claims': np.random.poisson(0.5, n_normal),
            'claim_settlement_time': np.random.normal(15, 5, n_normal),  # days
            'documentation_completeness': np.random.normal(0.9, 0.1, n_normal),
            'witness_availability': np.random.choice([0, 1], n_normal, p=[0.3, 0.7]),
            'claim_complexity': np.random.choice(['Low', 'Medium', 'High'], n_normal, p=[0.6, 0.3, 0.1]),
            'geographical_risk': np.random.choice(['Low', 'Medium', 'High'], n_normal, p=[0.5, 0.4, 0.1]),
            'time_between_incident_and_claim': np.random.exponential(2, n_normal),  # days
            'is_fraud': np.zeros(n_normal)
        }
        
        # Fraudulent claims (different patterns)
        fraud_data = {
            'claim_amount': np.random.lognormal(12, 2, n_fraud),  # Higher amounts
            'claim_type': np.random.choice(['Auto', 'Property', 'Health', 'Life', 'Cyber'], n_fraud),
            'claimant_age': np.random.randint(25, 65, n_fraud),  # Different age distribution
            'policy_duration': np.random.randint(1, 24, n_fraud),  # Shorter policy duration
            'num_previous_claims': np.random.poisson(2, n_fraud),  # More previous claims
            'claim_settlement_time': np.random.normal(25, 10, n_fraud),  # Longer settlement time
            'documentation_completeness': np.random.normal(0.6, 0.2, n_fraud),  # Poor documentation
            'witness_availability': np.random.choice([0, 1], n_fraud, p=[0.8, 0.2]),  # Fewer witnesses
            'claim_complexity': np.random.choice(['Low', 'Medium', 'High'], n_fraud, p=[0.2, 0.3, 0.5]),
            'geographical_risk': np.random.choice(['Low', 'Medium', 'High'], n_fraud, p=[0.2, 0.3, 0.5]),
            'time_between_incident_and_claim': np.random.exponential(8, n_fraud),  # Longer delay
            'is_fraud': np.ones(n_fraud)
        }
        
        # Combine data
        all_data = {}
        for key in normal_data.keys():
            all_data[key] = np.concatenate([normal_data[key], fraud_data[key]])
        
        df = pd.DataFrame(all_data)
        
        # Add derived features
        df['claim_amount_log'] = np.log1p(df['claim_amount'])
        df['claim_to_policy_ratio'] = df['claim_amount'] / (df['policy_duration'] * 1000)
        df['avg_claim_per_month'] = df['num_previous_claims'] / np.maximum(df['policy_duration'], 1)
        df['documentation_quality_score'] = df['documentation_completeness'] * df['witness_availability']
        
        # Shuffle the data
        df = df.sample(frac=1).reset_index(drop=True)
        
        return df
    
    def prepare_features_fraud(self, df, is_training=True):
        """Prepare features for fraud detection models"""
        df_processed = df.copy()
        
        # Encode categorical variables
        categorical_cols = ['claim_type', 'claim_complexity', 'geographical_risk']
        
        for col in categorical_cols:
            if col in df_processed.columns:
                encoder_key = f"fraud_{col}_encoder"
                
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
                            most_frequent = self.encoders[encoder_key].classes_[0]
                            df_processed[col] = df_processed[col].replace(list(new_vals), most_frequent)
                        
                        df_processed[col] = self.encoders[encoder_key].transform(df_processed[col])
        
        # Scale numerical features
        numerical_cols = df_processed.select_dtypes(include=[np.number]).columns
        numerical_cols = [col for col in numerical_cols if col not in ['is_fraud']]
        
        if is_training:
            scaler = StandardScaler()
            df_processed[numerical_cols] = scaler.fit_transform(df_processed[numerical_cols])
            self.scalers['fraud_scaler'] = scaler
        else:
            if 'fraud_scaler' in self.scalers:
                df_processed[numerical_cols] = self.scalers['fraud_scaler'].transform(df_processed[numerical_cols])
        
        return df_processed
    
    def train_fraud_models(self):
        """Train fraud detection models"""
        print("Training fraud detection models...")
        
        # Generate training data
        df = self.create_synthetic_fraud_data(n_samples=15000, fraud_rate=0.08)
        
        # Prepare features
        df_processed = self.prepare_features_fraud(df, is_training=True)
        
        # Separate features and target
        feature_cols = [col for col in df_processed.columns if col != 'is_fraud']
        X = df_processed[feature_cols]
        y = df_processed['is_fraud']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Handle class imbalance with SMOTE (if available)
        if SMOTE_AVAILABLE:
            smote = SMOTE(random_state=42)
            X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
        else:
            # Use original data if SMOTE not available
            X_train_balanced, y_train_balanced = X_train, y_train
            print("Using unbalanced data (SMOTE not available)")
        
        # Train multiple models
        models_config = {
            'isolation_forest': IsolationForest(contamination=0.1, random_state=42),
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'xgboost': xgb.XGBClassifier(n_estimators=100, random_state=42),
            'lightgbm': lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1)
        }
        
        best_model = None
        best_auc = 0
        
        for model_name, model in models_config.items():
            try:
                if model_name == 'isolation_forest':
                    # Isolation Forest is unsupervised
                    model.fit(X_train)
                    y_pred = model.predict(X_test)
                    y_pred = (y_pred == -1).astype(int)  # Convert to binary
                    auc_score = roc_auc_score(y_test, y_pred)
                else:
                    # Supervised models
                    model.fit(X_train_balanced, y_train_balanced)
                    y_pred_proba = model.predict_proba(X_test)[:, 1]
                    auc_score = roc_auc_score(y_test, y_pred_proba)
                
                print(f"{model_name}: AUC Score: {auc_score:.4f}")
                
                if auc_score > best_auc:
                    best_auc = auc_score
                    best_model = model_name
                
                # Save model
                self.models[f"fraud_{model_name}"] = model
                joblib.dump(model, os.path.join(self.model_path, f"fraud_{model_name}.pkl"))
                
            except Exception as e:
                print(f"Error training {model_name}: {str(e)}")
        
        # Save encoders and scalers
        joblib.dump(self.encoders, os.path.join(self.model_path, "fraud_encoders.pkl"))
        joblib.dump(self.scalers, os.path.join(self.model_path, "fraud_scalers.pkl"))
        
        print(f"Best fraud detection model: {best_model} (AUC: {best_auc:.4f})")
        return best_model
    
    def load_fraud_models(self, model_type='lightgbm'):
        """Load trained fraud detection models"""
        try:
            model_path = os.path.join(self.model_path, f"fraud_{model_type}.pkl")
            encoders_path = os.path.join(self.model_path, "fraud_encoders.pkl")
            scalers_path = os.path.join(self.model_path, "fraud_scalers.pkl")
            
            if all(os.path.exists(path) for path in [model_path, encoders_path, scalers_path]):
                self.models[f"fraud_{model_type}"] = joblib.load(model_path)
                self.encoders.update(joblib.load(encoders_path))
                self.scalers.update(joblib.load(scalers_path))
                return True
            else:
                print("Fraud models not found. Training new models...")
                self.train_fraud_models()
                return True
        except Exception as e:
            print(f"Error loading fraud models: {str(e)}")
            return False
    
    def detect_fraud_ml(self, claim_data, model_type='lightgbm'):
        """Detect fraud using ML models"""
        try:
            # Ensure models are loaded
            if not self.load_fraud_models(model_type):
                return None, ["Error loading fraud detection models"]
            
            # Create DataFrame from claim data
            df = pd.DataFrame([claim_data])
            
            # Add derived features
            if 'claim_amount' in df.columns:
                df['claim_amount_log'] = np.log1p(df['claim_amount'])
            if 'claim_amount' in df.columns and 'policy_duration' in df.columns:
                df['claim_to_policy_ratio'] = df['claim_amount'] / (df['policy_duration'] * 1000)
            if 'num_previous_claims' in df.columns and 'policy_duration' in df.columns:
                df['avg_claim_per_month'] = df['num_previous_claims'] / np.maximum(df['policy_duration'], 1)
            if 'documentation_completeness' in df.columns and 'witness_availability' in df.columns:
                df['documentation_quality_score'] = df['documentation_completeness'] * df['witness_availability']
            
            # Prepare features
            df_processed = self.prepare_features_fraud(df, is_training=False)
            
            # Make prediction
            model = self.models[f"fraud_{model_type}"]
            
            if model_type == 'isolation_forest':
                prediction = model.predict(df_processed)[0]
                fraud_probability = 0.8 if prediction == -1 else 0.2
                is_fraud = prediction == -1
            else:
                fraud_probability = float(model.predict_proba(df_processed)[0, 1])
                is_fraud = fraud_probability > 0.5
            
            # Calculate fraud score (1-10 scale)
            fraud_score = int(1 + fraud_probability * 9)
            
            return fraud_score, fraud_probability, is_fraud, None
            
        except Exception as e:
            return None, None, None, f"Fraud detection error: {str(e)}"

# Global instance
ml_fraud_detector = MLFraudDetector()

def detect_fraud_ml(claim_amount, claim_type, suspicious_docs, prior_fraud, **kwargs):
    """ML-based fraud detection with enhanced features"""
    
    # Prepare claim data with additional features
    claim_data = {
        'claim_amount': claim_amount,
        'claim_type': claim_type,
        'claimant_age': kwargs.get('claimant_age', 40),
        'policy_duration': kwargs.get('policy_duration', 24),  # months
        'num_previous_claims': 1 if prior_fraud else kwargs.get('num_previous_claims', 0),
        'claim_settlement_time': kwargs.get('claim_settlement_time', 15),  # days
        'documentation_completeness': 0.3 if suspicious_docs else kwargs.get('documentation_completeness', 0.9),
        'witness_availability': kwargs.get('witness_availability', 1),
        'claim_complexity': kwargs.get('claim_complexity', 'Medium'),
        'geographical_risk': kwargs.get('geographical_risk', 'Medium'),
        'time_between_incident_and_claim': kwargs.get('time_between_incident_and_claim', 2)
    }
    
    # Use ML model for fraud detection
    result = ml_fraud_detector.detect_fraud_ml(claim_data, model_type='lightgbm')
    
    if len(result) == 4 and result[3] is None:
        fraud_score, fraud_probability, is_fraud, _ = result
    else:
        # Fallback to basic fraud detection
        from .fraud_detector import detect_fraud
        return detect_fraud(claim_amount, claim_type, suspicious_docs, prior_fraud)
    
    # Generate alerts based on ML prediction
    alerts = []
    alerts.append(f"🤖 ML Fraud Score: {fraud_score}/10 (Probability: {fraud_probability:.2%})")
    
    # Risk-based alerts
    if fraud_score >= 8:
        alerts.append("🚨 HIGH FRAUD RISK DETECTED! Immediate investigation required.")
        alerts.append("🔍 ML Analysis: Multiple fraud indicators detected in claim pattern.")
        alerts.append("📋 Actions: Assign to specialist fraud team, conduct thorough investigation.")
        
        if claim_type == "Auto":
            alerts.append("🚗 Auto-specific ML checks: Accident reconstruction analysis, vehicle history verification.")
        elif claim_type == "Property":
            alerts.append("🏠 Property-specific ML checks: Damage pattern analysis, property history investigation.")
        elif claim_type == "Health":
            alerts.append("🏥 Health-specific ML checks: Medical record verification, provider network analysis.")
        elif claim_type == "Cyber":
            alerts.append("💻 Cyber-specific ML checks: Digital forensics, incident timeline analysis.")
        elif claim_type == "Life":
            alerts.append("📋 Life-specific ML checks: Medical examiner review, beneficiary investigation.")
            
    elif fraud_score >= 6:
        alerts.append("⚠️ MODERATE FRAUD RISK. Enhanced verification required.")
        alerts.append("🔍 ML Analysis: Some anomalies detected in claim characteristics.")
        alerts.append("📋 Actions: Secondary review, additional documentation request.")
        
        if claim_type == "Auto":
            alerts.append("🚗 Auto ML insights: Verify accident details, check repair estimates.")
        elif claim_type == "Property":
            alerts.append("🏠 Property ML insights: Validate damage assessment, confirm property ownership.")
        elif claim_type == "Health":
            alerts.append("🏥 Health ML insights: Cross-check medical records, verify treatment necessity.")
        elif claim_type == "Cyber":
            alerts.append("💻 Cyber ML insights: Validate security incident, assess business impact.")
        elif claim_type == "Life":
            alerts.append("📋 Life ML insights: Verify death certificate, confirm policy details.")
            
    elif fraud_score >= 4:
        alerts.append("✅ LOW-MODERATE FRAUD RISK. Standard processing with monitoring.")
        alerts.append("🔍 ML Analysis: Normal claim pattern with minor anomalies.")
        alerts.append("📋 Actions: Standard verification, routine processing.")
    else:
        alerts.append("✅ LOW FRAUD RISK. Normal claim processing.")
        alerts.append("🔍 ML Analysis: Claim characteristics align with normal patterns.")
        alerts.append("📋 Actions: Fast-track processing available.")
    
    # Add ML-specific insights
    alerts.append(f"\n🧠 ML Insights:")
    alerts.append(f"• Fraud probability: {fraud_probability:.1%}")
    alerts.append(f"• Risk factors analyzed: {len(claim_data)} features")
    alerts.append(f"• Model confidence: {'High' if abs(fraud_probability - 0.5) > 0.3 else 'Medium'}")
    
    # Add recommendations based on specific risk factors
    if claim_amount > 500000:
        alerts.append("💰 High claim amount detected - Enhanced financial verification recommended.")
    
    if suspicious_docs:
        alerts.append("📄 Document authenticity concerns - OCR and forensic analysis suggested.")
    
    if prior_fraud:
        alerts.append("⚠️ Prior fraud history - Elevated monitoring and verification required.")
    
    return fraud_score, "\n".join(alerts)

def detect_anomaly_patterns(claims_data):
    """Detect anomaly patterns in multiple claims using Isolation Forest"""
    try:
        if not ml_fraud_detector.load_fraud_models('isolation_forest'):
            return []
        
        # Prepare claims data
        df = pd.DataFrame(claims_data)
        df_processed = ml_fraud_detector.prepare_features_fraud(df, is_training=False)
        
        # Use Isolation Forest for anomaly detection
        model = ml_fraud_detector.models['fraud_isolation_forest']
        anomaly_scores = model.decision_function(df_processed)
        anomalies = model.predict(df_processed)
        
        # Find anomalous claims
        anomalous_claims = []
        for i, (score, is_anomaly) in enumerate(zip(anomaly_scores, anomalies)):
            if is_anomaly == -1:  # Anomaly detected
                anomalous_claims.append({
                    'claim_index': i,
                    'anomaly_score': float(score),
                    'risk_level': 'High' if score < -0.5 else 'Medium'
                })
        
        return anomalous_claims
        
    except Exception as e:
        print(f"Anomaly detection error: {str(e)}")
        return []

def batch_fraud_screening(claims_list):
    """Screen multiple claims for fraud using ML models"""
    results = []
    
    for i, claim in enumerate(claims_list):
        try:
            score, alerts = detect_fraud_ml(**claim)
            results.append({
                'claim_id': i,
                'fraud_score': score,
                'risk_level': 'High' if score >= 8 else 'Medium' if score >= 6 else 'Low',
                'alerts': alerts
            })
        except Exception as e:
            results.append({
                'claim_id': i,
                'fraud_score': None,
                'risk_level': 'Error',
                'alerts': f"Processing error: {str(e)}"
            })
    
    return results
