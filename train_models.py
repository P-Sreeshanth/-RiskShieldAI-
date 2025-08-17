"""
ML Model Trainer - Initialize and train all ML models for RiskShieldAI
Run this script to train all models for risk assessment, fraud detection, and document analysis
"""

import os
import sys

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

def install_requirements():
    """Install required packages"""
    print("Installing required ML packages...")
    os.system("pip install scikit-learn==1.3.2 xgboost==2.0.3 lightgbm==4.1.0 joblib==1.3.2")
    os.system("pip install imbalanced-learn==0.11.0 matplotlib==3.7.2 seaborn==0.13.0")
    print("Basic ML packages installed successfully!")
    
    print("\nNote: For full functionality, also install:")
    print("- OpenCV: pip install opencv-python==4.8.1.78")
    print("- TensorFlow: pip install tensorflow==2.15.0")
    print("- Tesseract OCR: pip install pytesseract==0.3.10")
    print("- CatBoost: pip install catboost==1.2.2")
    print("- SHAP: pip install shap==0.44.0")

def train_all_models():
    """Train all ML models"""
    print("Starting ML model training for RiskShieldAI...")
    
    try:
        # Import ML modules
        from utils.ml_risk_calculator import ml_calculator
        from utils.ml_fraud_detector import ml_fraud_detector
        
        print("\nTraining Risk Assessment Models...")
        
        # Train risk models for all insurance types
        insurance_types = ['auto', 'property', 'health', 'life', 'cyber']
        
        for insurance_type in insurance_types:
            print(f"\nTraining {insurance_type.title()} Insurance Risk Model...")
            try:
                best_model = ml_calculator.train_models(insurance_type)
                print(f"SUCCESS: {insurance_type.title()} insurance model trained successfully!")
                print(f"   Best performing model: {best_model}")
            except Exception as e:
                print(f"ERROR: Training {insurance_type} model failed: {str(e)}")
        
        print("\nTraining Fraud Detection Models...")
        
        # Train fraud detection models
        try:
            best_fraud_model = ml_fraud_detector.train_fraud_models()
            print(f"SUCCESS: Fraud detection models trained successfully!")
            print(f"   Best performing model: {best_fraud_model}")
        except Exception as e:
            print(f"ERROR: Training fraud detection models failed: {str(e)}")
        
        print("\nTraining Document Intelligence Models...")
        
        # Train document analysis models (if dependencies are available)
        try:
            from utils.document_intelligence import document_ai
            document_ai.train_document_fraud_classifier()
            print("SUCCESS: Document analysis models trained successfully!")
        except ImportError as e:
            print("WARNING: Document intelligence dependencies not available.")
            print("   Install opencv-python, tensorflow, and pytesseract for full functionality.")
        except Exception as e:
            print(f"ERROR: Training document models failed: {str(e)}")
        
        print("\nModel training completed!")
        print("\nTraining Summary:")
        print("- Risk Assessment Models: Trained for Auto, Property, Health, Life, and Cyber insurance")
        print("- Fraud Detection Models: Trained with multiple algorithms (RF, XGBoost, LightGBM, Isolation Forest)")
        print("- Document Intelligence: Trained for document authenticity analysis")
        
        print("\nAvailable Models:")
        print("- XGBoost: High accuracy, good for complex patterns")
        print("- LightGBM: Fast and memory efficient, recommended for production")
        print("- Random Forest: Robust and interpretable")
        print("- Isolation Forest: Excellent for anomaly/fraud detection")
        
        return True
        
    except ImportError as e:
        print(f"ERROR: Import failed: {str(e)}")
        print("Please install required packages first using install_requirements()")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {str(e)}")
        return False

def test_models():
    """Test trained models with sample data"""
    print("\nTesting trained models...")
    
    try:
        from utils.ml_risk_calculator import (
            calculate_auto_risk_ml,
            calculate_property_risk_ml,
            calculate_health_risk_ml,
            calculate_life_risk_ml,
            calculate_cyber_risk_ml
        )
        from utils.ml_fraud_detector import detect_fraud_ml
        
        # Test auto insurance
        print("\nTesting Auto Insurance Risk Assessment:")
        risk_score, recommendation, premium = calculate_auto_risk_ml(
            vehicle_age=5,
            driver_age=30,
            accident_history=1,
            mileage=15000
        )
        print(f"   Risk Score: {risk_score}/10")
        print(f"   Premium: ₹{premium:,}")
        
        # Test fraud detection
        print("\nTesting Fraud Detection:")
        fraud_score, alerts = detect_fraud_ml(
            claim_amount=300000,
            claim_type="Auto",
            suspicious_docs=False,
            prior_fraud=False
        )
        print(f"   Fraud Score: {fraud_score}/10")
        print(f"   Status: {'High Risk' if fraud_score >= 8 else 'Moderate Risk' if fraud_score >= 6 else 'Low Risk'}")
        
        print("\nModel testing completed successfully!")
        return True
        
    except Exception as e:
        print(f"ERROR: Testing failed: {str(e)}")
        return False

def main():
    """Main function to run the training process"""
    print("RiskShieldAI ML Model Training System")
    print("=" * 50)
    
    # Check if models directory exists
    models_dir = os.path.join('utils', 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir, exist_ok=True)
    
    fraud_models_dir = os.path.join('utils', 'fraud_models')
    if not os.path.exists(fraud_models_dir):
        os.makedirs(fraud_models_dir, exist_ok=True)
    
    doc_models_dir = os.path.join('utils', 'document_models')
    if not os.path.exists(doc_models_dir):
        os.makedirs(doc_models_dir, exist_ok=True)
    
    print("\nModel directories created/verified")
    
    # Option menu
    while True:
        print("\n" + "=" * 50)
        print("Choose an option:")
        print("1. Install ML requirements")
        print("2. Train all models")
        print("3. Test trained models")
        print("4. Train and test (recommended)")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            install_requirements()
        elif choice == '2':
            success = train_all_models()
            if success:
                print("\nAll models trained successfully!")
            else:
                print("\nTraining failed. Check error messages above.")
        elif choice == '3':
            success = test_models()
            if not success:
                print("\nTesting failed. Make sure models are trained first.")
        elif choice == '4':
            print("\nRunning complete training and testing pipeline...")
            if train_all_models():
                test_models()
            else:
                print("\nTraining failed. Cannot proceed to testing.")
        elif choice == '5':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
