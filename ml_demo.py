"""
ML Demo Script - Showcase RiskShieldAI ML Capabilities
Run this script to see ML models in action with sample data
"""

import sys
import os
import time

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"TARGET: {title}")
    print("="*60)

def print_result(title, result):
    """Print formatted result"""
    print(f"\nRESULT {title}:")
    if isinstance(result, tuple):
        for i, item in enumerate(result):
            print(f"   {i+1}. {item}")
    else:
        print(f"   {result}")

def demo_risk_assessment():
    """Demonstrate ML-based risk assessment"""
    print_header("ML-Enhanced Risk Assessment Demo")
    
    try:
        from ml_risk_calculator import (
            calculate_auto_risk_ml,
            calculate_property_risk_ml,
            calculate_health_risk_ml,
            calculate_life_risk_ml,
            calculate_cyber_risk_ml
        )
        
        print("\nAuto Insurance Risk Assessment:")
        print("   Customer: 30-year-old with 5-year-old car, 1 accident, 15,000 km/year")
        
        risk_score, recommendation, premium = calculate_auto_risk_ml(
            vehicle_age=5,
            driver_age=30,
            accident_history=1,
            mileage=15000
        )
        
        print(f"   Risk Score: {risk_score}/10")
        print(f"   Estimated Premium: ₹{premium:,}")
        print(f"   Risk Level: {'High' if risk_score < 4 else 'Moderate' if risk_score < 7 else 'Low'}")
        
        print("\nProperty Insurance Risk Assessment:")
        print("   Property: 15-year-old house in medium-risk area, concrete construction")
        
        risk_score, recommendation, premium = calculate_property_risk_ml(
            property_age=15,
            location_risk="Medium",
            construction_type="Concrete",
            flood_zone=False
        )
        
        print(f"   Risk Score: {risk_score}/10")
        print(f"   Estimated Premium: ₹{premium:,}")
        print(f"   Risk Level: {'High' if risk_score < 4 else 'Moderate' if risk_score < 7 else 'Low'}")
        
        print("\nHealth Insurance Risk Assessment:")
        print("   Individual: 45-year-old, BMI 28, non-smoker, exercises sometimes")
        
        risk_score, recommendation, premium = calculate_health_risk_ml(
            age=45,
            bmi=28,
            smoking=False,
            exercise_frequency="Sometimes",
            chronic_conditions=0,
            family_history=False
        )
        
        print(f"   Risk Score: {risk_score}/10")
        print(f"   Estimated Premium: ₹{premium:,}")
        print(f"   Risk Level: {'High' if risk_score < 4 else 'Moderate' if risk_score < 7 else 'Low'}")
        
        print("\nCyber Insurance Risk Assessment:")
        print("   Company: 50 employees, has security policy, uses MFA, no past incidents")
        
        risk_score, recommendation, premium = calculate_cyber_risk_ml(
            num_employees=50,
            has_security_policy=True,
            past_incidents=0,
            uses_mfa=True
        )
        
        print(f"   Risk Score: {risk_score}/10")
        print(f"   Estimated Premium: ₹{premium:,}")
        print(f"   Risk Level: {'High' if risk_score < 4 else 'Moderate' if risk_score < 7 else 'Low'}")
        
        print("\nML Risk Assessment Demo Completed Successfully!")
        
    except ImportError:
        print("Error: ML models not available. Please run 'python train_models.py' first.")
    except Exception as e:
        print(f"Error: {str(e)}")

def demo_fraud_detection():
    """Demonstrate ML-based fraud detection"""
    print_header("ML-Enhanced Fraud Detection Demo")
    
    try:
        from ml_fraud_detector import detect_fraud_ml, batch_fraud_screening
        
        print("\nSingle Claim Fraud Analysis:")
        print("   Claim: ₹3,00,000 auto insurance claim, no suspicious docs, no prior fraud")
        
        fraud_score, alerts = detect_fraud_ml(
            claim_amount=300000,
            claim_type="Auto",
            suspicious_docs=False,
            prior_fraud=False,
            claimant_age=35,
            policy_duration=24
        )
        
        print(f"   Fraud Score: {fraud_score}/10")
        print(f"   Status: {'HIGH RISK' if fraud_score >= 8 else 'MODERATE RISK' if fraud_score >= 6 else 'LOW RISK'}")
        print("   Analysis Summary:")
        alert_lines = alerts.split('\n')[:5]  # Show first 5 lines
        for line in alert_lines:
            if line.strip():
                print(f"      {line}")
        
        print("\nHigh-Risk Claim Analysis:")
        print("   Claim: ₹8,00,000 property claim, suspicious docs, prior fraud history")
        
        fraud_score, alerts = detect_fraud_ml(
            claim_amount=800000,
            claim_type="Property",
            suspicious_docs=True,
            prior_fraud=True,
            claimant_age=40,
            policy_duration=6  # Short policy duration
        )
        
        print(f"   Fraud Score: {fraud_score}/10")
        print(f"   Status: {'HIGH RISK' if fraud_score >= 8 else 'MODERATE RISK' if fraud_score >= 6 else 'LOW RISK'}")
        
        print("\nBatch Fraud Screening Demo:")
        print("   Analyzing 3 claims simultaneously...")
        
        claims = [
            {
                'claim_amount': 150000,
                'claim_type': 'Auto',
                'suspicious_docs': False,
                'prior_fraud': False,
                'claimant_age': 28
            },
            {
                'claim_amount': 500000,
                'claim_type': 'Property',
                'suspicious_docs': True,
                'prior_fraud': False,
                'claimant_age': 45
            },
            {
                'claim_amount': 1000000,
                'claim_type': 'Cyber',
                'suspicious_docs': False,
                'prior_fraud': True,
                'claimant_age': 38
            }
        ]
        
        results = batch_fraud_screening(claims)
        
        for i, result in enumerate(results):
            print(f"   Claim {i+1}: Fraud Score {result['fraud_score']}/10 - {result['risk_level']} Risk")
        
        print("\nML Fraud Detection Demo Completed Successfully!")
        
    except ImportError:
        print("Error: ML models not available. Please run 'python train_models.py' first.")
    except Exception as e:
        print(f"Error: {str(e)}")

def demo_model_comparison():
    """Compare different ML models"""
    print_header("ML Model Performance Comparison")
    
    try:
        from ml_risk_calculator import ml_calculator
        
        print("\nComparing Different ML Models for Auto Insurance:")
        
        sample_features = {
            'vehicle_age': 7,
            'driver_age': 35,
            'accident_history': 2,
            'mileage': 20000,
            'vehicle_value': 600000,
            'location_risk': 'High',
            'gender': 'Male',
            'marital_status': 'Married'
        }
        
        models = ['lightgbm', 'xgboost', 'random_forest', 'catboost']
        
        for model in models:
            try:
                start_time = time.time()
                risk_score, premium, error = ml_calculator.predict_risk('auto', sample_features, model_type=model)
                inference_time = (time.time() - start_time) * 1000
                
                if error:
                    print(f"   {model.upper()}: Error - {error}")
                else:
                    print(f"   {model.upper()}: Risk Score {risk_score:.1f}/10, Premium ₹{premium:,} ({inference_time:.1f}ms)")
                    
            except Exception as e:
                print(f"   {model.upper()}: Not available - {str(e)}")
        
        print("\n📈 Model Characteristics:")
        print("   • LightGBM: Fastest inference, good accuracy, memory efficient")
        print("   • XGBoost: High accuracy, robust to overfitting")
        print("   • Random Forest: Good interpretability, handles outliers well")
        print("   • CatBoost: Excellent with categorical features, minimal preprocessing")
        
        print("\nModel Comparison Demo Completed!")
        
    except ImportError:
        print("Error: ML models not available. Please run 'python train_models.py' first.")
    except Exception as e:
        print(f"Error: {str(e)}")

def demo_document_intelligence():
    """Demonstrate document analysis capabilities"""
    print_header("Document Intelligence Demo (SmartAuditAI)")
    
    try:
        from document_intelligence import document_ai
        
        print("\nDocument Analysis Capabilities:")
        print("   • OCR Text Extraction using Tesseract")
        print("   • Image Quality Assessment")
        print("   • Document Authenticity Verification")
        print("   • Fraud Pattern Detection")
        print("   • Security Features Detection")
        
        print("\nSimulated Document Analysis:")
        print("   Creating synthetic document analysis results...")
        
        # Simulate document analysis since we don't have actual images
        synthetic_result = {
            'authenticity_score': 7,
            'fraud_probability': 0.25,
            'analysis_results': [
                "✓ Good OCR confidence (87.5%)",
                "✓ Adequate text content detected",
                "! Missing expected watermark",
                "✓ Consistent font formatting",
                "✓ LOW FRAUD RISK - Document appears authentic"
            ],
            'recommendations': [
                "Proceed with standard verification",
                "Consider watermark verification for high-value claims"
            ]
        }
        
        print(f"   Authenticity Score: {synthetic_result['authenticity_score']}/10")
        print(f"   Fraud Probability: {synthetic_result['fraud_probability']:.1%}")
        print("   Analysis Results:")
        for result in synthetic_result['analysis_results']:
            print(f"      {result}")
        
        print("   Recommendations:")
        for rec in synthetic_result['recommendations']:
            print(f"      • {rec}")
        
        print("\nDocument Intelligence Features:")
        print("   • Tesseract OCR for text extraction")
        print("   • MobileNetV2 CNN for image analysis")
        print("   • Multi-factor authenticity scoring")
        print("   • Batch document processing")
        print("   • Real-time fraud detection")
        
        print("\nDocument Intelligence Demo Completed!")
        
    except ImportError:
        print("Error: Document intelligence dependencies not available.")
        print("   Install: pip install opencv-python tensorflow pytesseract")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    """Main demo function"""
    print("RiskShieldAI ML Capabilities Demo")
    print("="*60)
    print("Demonstrating advanced machine learning features for insurance analytics")
    
    while True:
        print("\n" + "="*60)
        print("Choose a demo:")
        print("1. Risk Assessment with ML Models")
        print("2. Fraud Detection with ML Models")
        print("3. ML Model Performance Comparison")
        print("4. Document Intelligence (SmartAuditAI)")
        print("5. Run All Demos")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            demo_risk_assessment()
        elif choice == '2':
            demo_fraud_detection()
        elif choice == '3':
            demo_model_comparison()
        elif choice == '4':
            demo_document_intelligence()
        elif choice == '5':
            print("\nRunning Complete ML Demo Suite...")
            demo_risk_assessment()
            demo_fraud_detection()
            demo_model_comparison()
            demo_document_intelligence()
            print("\nComplete Demo Suite Finished!")
        elif choice == '6':
            print("\nThank you for exploring RiskShieldAI ML capabilities!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
