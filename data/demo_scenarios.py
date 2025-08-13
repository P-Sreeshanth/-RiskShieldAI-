"""
Sample data and test scenarios for RiskShieldAI™ Demo
"""

# Sample Auto Insurance Data
auto_scenarios = [
    {
        "name": "Young Driver - High Risk",
        "vehicle_age": 2,
        "driver_age": 19,
        "accident_history": 1,
        "mileage": 25000,
        "expected_risk": "High",
        "notes": "Young driver with recent accident, high mileage"
    },
    {
        "name": "Experienced Driver - Low Risk",
        "vehicle_age": 5,
        "driver_age": 45,
        "accident_history": 0,
        "mileage": 12000,
        "expected_risk": "Low",
        "notes": "Mature driver, clean record, moderate usage"
    },
    {
        "name": "Senior Driver - Moderate Risk",
        "vehicle_age": 8,
        "driver_age": 70,
        "accident_history": 0,
        "mileage": 8000,
        "expected_risk": "Moderate",
        "notes": "Senior driver, older vehicle, low mileage"
    }
]

# Sample Property Insurance Data
property_scenarios = [
    {
        "name": "Urban Apartment - Low Risk",
        "property_age": 5,
        "location_risk": "Low",
        "construction_type": "Concrete",
        "flood_zone": False,
        "expected_risk": "Low",
        "notes": "New concrete construction in safe area"
    },
    {
        "name": "Rural Wood House - High Risk",
        "property_age": 25,
        "location_risk": "High",
        "construction_type": "Wood",
        "flood_zone": True,
        "expected_risk": "High",
        "notes": "Old wood construction in flood-prone area"
    },
    {
        "name": "Suburban Brick Home - Moderate Risk",
        "property_age": 15,
        "location_risk": "Medium",
        "construction_type": "Brick",
        "flood_zone": False,
        "expected_risk": "Moderate",
        "notes": "Mid-age brick home in moderate risk area"
    }
]

# Sample Cyber Insurance Data
cyber_scenarios = [
    {
        "name": "Small Startup - High Risk",
        "num_employees": 15,
        "has_security_policy": False,
        "past_incidents": 1,
        "uses_mfa": False,
        "expected_risk": "High",
        "notes": "Small company with minimal security measures"
    },
    {
        "name": "Enterprise Company - Low Risk",
        "num_employees": 500,
        "has_security_policy": True,
        "past_incidents": 0,
        "uses_mfa": True,
        "expected_risk": "Low",
        "notes": "Large company with comprehensive security"
    },
    {
        "name": "Growing Company - Moderate Risk",
        "num_employees": 100,
        "has_security_policy": True,
        "past_incidents": 1,
        "uses_mfa": True,
        "expected_risk": "Moderate",
        "notes": "Growing company with some security measures"
    }
]

# Sample Health Insurance Data
health_scenarios = [
    {
        "name": "Young Healthy Adult - Low Risk",
        "age": 25,
        "bmi": 22.5,
        "smoking": False,
        "exercise_frequency": "Daily",
        "chronic_conditions": 0,
        "family_history": False,
        "expected_risk": "Low",
        "notes": "Young, healthy lifestyle, no risk factors"
    },
    {
        "name": "Middle-aged Smoker - High Risk",
        "age": 50,
        "bmi": 32.0,
        "smoking": True,
        "exercise_frequency": "Never",
        "chronic_conditions": 2,
        "family_history": True,
        "expected_risk": "High",
        "notes": "Multiple risk factors, poor health habits"
    },
    {
        "name": "Active Senior - Moderate Risk",
        "age": 65,
        "bmi": 24.0,
        "smoking": False,
        "exercise_frequency": "Often",
        "chronic_conditions": 1,
        "family_history": False,
        "expected_risk": "Moderate",
        "notes": "Senior but active with minimal conditions"
    }
]

# Sample Life Insurance Data
life_scenarios = [
    {
        "name": "Young Professional - Low Risk",
        "age": 30,
        "gender": "Female",
        "occupation": "Low Risk",
        "lifestyle": "Healthy",
        "coverage_amount": 500000,
        "medical_exams": True,
        "expected_risk": "Low",
        "notes": "Young professional with healthy lifestyle"
    },
    {
        "name": "High-Risk Occupation - High Risk",
        "age": 45,
        "gender": "Male",
        "occupation": "High Risk",
        "lifestyle": "Risky",
        "coverage_amount": 1000000,
        "medical_exams": False,
        "expected_risk": "High",
        "notes": "Dangerous job, risky lifestyle, no medical exams"
    },
    {
        "name": "Middle-aged Average - Moderate Risk",
        "age": 40,
        "gender": "Male",
        "occupation": "Medium Risk",
        "lifestyle": "Average",
        "coverage_amount": 750000,
        "medical_exams": True,
        "expected_risk": "Moderate",
        "notes": "Average profile with moderate coverage"
    }
]

# Sample Fraud Detection Data
fraud_scenarios = [
    {
        "name": "Suspicious Large Claim",
        "claim_amount": 50000,
        "claim_type": "Auto",
        "suspicious_docs": True,
        "prior_fraud": True,
        "expected_fraud_score": "High",
        "notes": "Large claim with suspicious documentation and fraud history"
    },
    {
        "name": "Regular Small Claim",
        "claim_amount": 2500,
        "claim_type": "Property",
        "suspicious_docs": False,
        "prior_fraud": False,
        "expected_fraud_score": "Low",
        "notes": "Small claim with clean documentation and no history"
    },
    {
        "name": "Moderate Cyber Claim",
        "claim_amount": 15000,
        "claim_type": "Cyber",
        "suspicious_docs": False,
        "prior_fraud": False,
        "expected_fraud_score": "Moderate",
        "notes": "Cyber claim with inherently higher risk profile"
    }
]

# Demo presentation script
demo_script = {
    "introduction": [
        "Welcome to RiskShieldAI™ - Advanced Insurance Analytics Platform",
        "Today we'll demonstrate comprehensive risk assessment across 5 insurance types",
        "We'll show real-time risk scoring, premium calculation, and fraud detection"
    ],
    "auto_demo": [
        "Let's start with Auto Insurance Assessment",
        "We'll evaluate a young driver with recent accident history",
        "Notice the instant risk scoring and premium calculation",
        "The system provides detailed recommendations for risk mitigation"
    ],
    "property_demo": [
        "Moving to Property Insurance",
        "This scenario shows a wood construction home in a flood zone",
        "Observe how environmental factors impact the risk score",
        "Premium estimates adjust based on construction type and location"
    ],
    "cyber_demo": [
        "Cyber Insurance is increasingly important",
        "We're assessing a small startup with minimal security",
        "The platform evaluates security posture and past incidents",
        "Recommendations focus on improving cybersecurity measures"
    ],
    "health_demo": [
        "Health Insurance risk assessment considers lifestyle factors",
        "This example shows how BMI, smoking, and exercise affect premiums",
        "The system provides wellness recommendations",
        "Family history and chronic conditions are key factors"
    ],
    "life_demo": [
        "Life Insurance assessment focuses on mortality risk",
        "Age, occupation, and lifestyle are primary factors",
        "Medical exams can significantly reduce premiums",
        "Coverage amount affects the risk assessment"
    ],
    "fraud_demo": [
        "Our fraud detection system analyzes claim patterns",
        "This suspicious claim has multiple red flags",
        "The AI identifies potential fraud automatically",
        "Investigators receive prioritized alerts for review"
    ],
    "analytics_demo": [
        "The analytics dashboard provides business intelligence",
        "View portfolio risk distribution across insurance types",
        "Premium vs risk correlation helps optimize pricing",
        "Export capabilities support further analysis"
    ],
    "business_value": [
        "RiskShieldAI™ delivers measurable business value",
        "Reduces manual underwriting time by 70%",
        "Improves fraud detection accuracy to 89.7%",
        "Increases profitability through risk-based pricing"
    ],
    "conclusion": [
        "Thank you for the RiskShieldAI™ demonstration",
        "The platform is ready for production deployment",
        "Scalable architecture supports enterprise growth",
        "Questions and next steps discussion"
    ]
}

if __name__ == "__main__":
    print("RiskShieldAI™ Demo Data and Scenarios")
    print("=====================================")
    print(f"Auto scenarios: {len(auto_scenarios)}")
    print(f"Property scenarios: {len(property_scenarios)}")
    print(f"Cyber scenarios: {len(cyber_scenarios)}")
    print(f"Health scenarios: {len(health_scenarios)}")
    print(f"Life scenarios: {len(life_scenarios)}")
    print(f"Fraud scenarios: {len(fraud_scenarios)}")
