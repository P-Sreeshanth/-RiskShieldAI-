"""
Risk Calculator Utility - Enhanced for Demo Platform
"""

def calculate_auto_risk(vehicle_age, driver_age, accident_history, mileage):
    """Calculate auto insurance risk score and premium estimate"""
    score = 10 - (0.2 * vehicle_age + 0.1 * (100-driver_age)/10 + 0.5 * accident_history + 0.0001 * mileage)
    score = max(1, min(10, round(score, 1)))
    
    # Calculate premium estimate in INR
    base_premium = 15000  # Base premium in INR
    premium = base_premium + (10 - score) * 2000 + vehicle_age * 500 + accident_history * 5000
    
    if score < 4:
        recommendation = """High risk: Consider the following to get better insurance:
        • Take a defensive driving course (10-15% discount)
        • Install safety devices (GPS tracker, dashcam) - 5-10% discount
        • Choose higher deductible to reduce premium
        • Consider pay-as-you-drive insurance
        • Recommended insurers: ICICI Lombard, Bajaj Allianz, HDFC ERGO"""
    elif score < 7:
        recommendation = """Moderate risk: Suggestions for better coverage:
        • Compare quotes from multiple insurers
        • Consider comprehensive coverage with add-ons
        • Maintain good driving record for NCB benefits
        • Install anti-theft devices for discounts
        • Recommended insurers: TATA AIG, New India Assurance, Oriental Insurance"""
    else:
        recommendation = """Low risk: You qualify for preferred rates:
        • Excellent driving record - claim maximum NCB
        • Consider comprehensive coverage with zero depreciation
        • Look for loyalty discounts with existing insurers
        • Bundle with other insurance for additional savings
        • Recommended insurers: IFFCO Tokio, SBI General, Reliance General"""
    
    return score, recommendation, int(premium)

def calculate_property_risk(property_age, location_risk, construction_type, flood_zone):
    """Calculate property insurance risk score and premium estimate"""
    base = 10 - (0.1 * property_age)
    if location_risk == "High":
        base -= 2
    elif location_risk == "Medium":
        base -= 1
    if construction_type == "Wood":
        base -= 1
    if flood_zone:
        base -= 2
    score = max(1, min(10, round(base, 1)))
    
    # Calculate premium estimate in INR
    base_premium = 25000  # Base premium in INR
    risk_multiplier = {"Low": 1.0, "Medium": 1.3, "High": 1.8}
    construction_multiplier = {"Concrete": 0.9, "Brick": 1.0, "Wood": 1.4, "Other": 1.2}
    premium = base_premium * risk_multiplier.get(location_risk, 1.0) * construction_multiplier.get(construction_type, 1.0)
    if flood_zone:
        premium *= 1.5
    
    if score < 4:
        recommendation = """High risk: Essential protection strategies:
        • Get comprehensive home insurance with natural disaster coverage
        • Install security systems (CCTV, alarms) for 10-15% discount
        • Consider flood insurance as separate add-on
        • Upgrade electrical and plumbing systems
        • Recommended insurers: HDFC ERGO, ICICI Lombard, Bajaj Allianz
        • Consider: Fire insurance, earthquake cover, burglary protection"""
    elif score < 7:
        recommendation = """Moderate risk: Optimization suggestions:
        • Compare home insurance policies from multiple providers
        • Add valuable items coverage for electronics/jewelry
        • Consider home loan protection insurance
        • Install water leak detectors and smoke alarms
        • Recommended insurers: TATA AIG, New India Assurance, SBI General
        • Useful add-ons: Personal accident cover, temporary accommodation"""
    else:
        recommendation = """Low risk: Premium optimization opportunities:
        • Excellent property profile - negotiate better rates
        • Bundle home and auto insurance for discounts
        • Consider increasing deductible to lower premium
        • Maintain property well for continued low risk
        • Recommended insurers: IFFCO Tokio, Oriental Insurance, Reliance General
        • Consider: Home loan insurance, content insurance for valuables"""
    
    return score, recommendation, int(premium)

def calculate_cyber_risk(num_employees, has_security_policy, past_incidents, uses_mfa):
    """Calculate cyber insurance risk score and premium estimate"""
    base = 10 - (0.001 * num_employees + 0.5 * past_incidents)
    if not has_security_policy:
        base -= 2
    if not uses_mfa:
        base -= 1
    score = max(1, min(10, round(base, 1)))
    
    # Calculate premium estimate in INR
    base_premium = 50000 + (num_employees * 1000)  # Base premium in INR
    if not has_security_policy:
        base_premium *= 1.5
    if not uses_mfa:
        base_premium *= 1.3
    base_premium += past_incidents * 25000
    
    if score < 4:
        recommendation = """High risk: Immediate cybersecurity improvements needed:
        • Implement comprehensive cybersecurity policy
        • Enable multi-factor authentication across all systems
        • Conduct employee cybersecurity training
        • Install endpoint detection and response (EDR) solutions
        • Regular security audits and penetration testing
        • Recommended insurers: HDFC ERGO, Bajaj Allianz, ICICI Lombard
        • Essential coverages: Data breach response, business interruption, cyber extortion"""
    elif score < 7:
        recommendation = """Moderate risk: Enhance your cyber protection:
        • Review and update existing security policies
        • Implement advanced threat detection systems
        • Regular backup and disaster recovery testing
        • Cyber awareness training for all employees
        • Consider cyber liability insurance with higher limits
        • Recommended insurers: TATA AIG, New India Assurance, SBI General
        • Useful add-ons: Reputation management, regulatory fines coverage"""
    else:
        recommendation = """Low risk: Excellent cybersecurity posture:
        • Maintain current security standards
        • Consider premium cyber insurance for comprehensive protection
        • Continuous monitoring and threat intelligence
        • Regular compliance audits and certifications
        • Cyber insurance with worldwide coverage
        • Recommended insurers: IFFCO Tokio, Oriental Insurance, Reliance General
        • Advanced coverages: Supply chain liability, privacy liability, cloud security"""
    
    return score, recommendation, int(base_premium)

def calculate_health_risk(age, bmi, smoking, exercise_frequency, chronic_conditions, family_history):
    """Calculate health insurance risk score and premium estimate"""
    base = 10 - (age - 18) * 0.05  # Age factor
    
    # BMI factor
    if bmi < 18.5 or bmi > 30:
        base -= 1
    elif bmi > 25:
        base -= 0.5
    
    # Smoking factor
    if smoking:
        base -= 2
    
    # Exercise factor
    exercise_scores = {"Never": -1.5, "Rarely": -1, "Sometimes": 0, "Often": 0.5, "Daily": 1}
    base += exercise_scores.get(exercise_frequency, 0)
    
    # Chronic conditions
    base -= chronic_conditions * 0.8
    
    # Family history
    if family_history:
        base -= 1
    
    score = max(1, min(10, round(base, 1)))
    
    # Calculate premium estimate in INR
    base_premium = 8000  # Base premium in INR
    age_factor = max(1, age - 25) * 200
    bmi_factor = max(0, abs(bmi - 22.5) * 500)
    smoking_factor = 5000 if smoking else 0
    chronic_factor = chronic_conditions * 3000
    family_factor = 2000 if family_history else 0
    
    premium = base_premium + age_factor + bmi_factor + smoking_factor + chronic_factor + family_factor
    
    if score < 4:
        recommendation = """High risk: Health improvement and insurance strategies:
        • Join wellness programs for premium discounts (up to 30% off)
        • Consider health insurance with preventive care coverage
        • Quit smoking - many insurers offer cessation program discounts
        • Regular health checkups and maintain medical records
        • Look into government schemes: Ayushman Bharat, ESIC
        • Recommended insurers: Star Health, Max Bupa, Apollo Munich
        • Essential features: Pre-existing disease cover, maternity benefits, critical illness rider"""
    elif score < 7:
        recommendation = """Moderate risk: Optimize your health insurance:
        • Compare family floater vs individual policies
        • Add critical illness and accidental death riders
        • Maintain continuous coverage for waiting period benefits
        • Use preventive care benefits for annual checkups
        • Consider top-up or super top-up policies for higher coverage
        • Recommended insurers: HDFC ERGO, ICICI Lombard, Bajaj Allianz
        • Useful add-ons: OPD coverage, alternative treatment, mental health coverage"""
    else:
        recommendation = """Low risk: Excellent health profile advantages:
        • Qualify for preferred rates and comprehensive coverage
        • Consider high-value policies with global coverage
        • Take advantage of wellness program benefits and rewards
        • Long-term premium discounts for claim-free years
        • Family health insurance with lifetime renewability
        • Recommended insurers: TATA AIG, SBI General, New India Assurance
        • Premium features: International coverage, organ transplant, experimental treatments"""
    
    return score, recommendation, int(premium)

def calculate_life_risk(age, gender, occupation, lifestyle, coverage_amount, medical_exams):
    """Calculate life insurance risk score and premium estimate"""
    base = 10 - (age - 18) * 0.08  # Age is primary factor
    
    # Gender factor (actuarial tables)
    if gender == "Male":
        base -= 0.5
    
    # Occupation risk
    occupation_risk = {"Low Risk": 0, "Medium Risk": -1, "High Risk": -2}
    base += occupation_risk.get(occupation, 0)
    
    # Lifestyle factor
    lifestyle_risk = {"Healthy": 0.5, "Average": 0, "Risky": -1.5}
    base += lifestyle_risk.get(lifestyle, 0)
    
    # Medical exams bonus
    if medical_exams:
        base += 0.5
    
    score = max(1, min(10, round(base, 1)))
    
    # Calculate premium estimate (per ₹1000 coverage) in INR
    base_rate = 12  # Base rate per ₹1000 in INR
    age_multiplier = 1 + (age - 25) * 0.02
    gender_multiplier = 1.1 if gender == "Male" else 1.0
    occupation_multiplier = {"Low Risk": 1.0, "Medium Risk": 1.3, "High Risk": 2.0}
    lifestyle_multiplier = {"Healthy": 0.8, "Average": 1.0, "Risky": 1.5}
    
    rate = base_rate * age_multiplier * gender_multiplier
    rate *= occupation_multiplier.get(occupation, 1.0)
    rate *= lifestyle_multiplier.get(lifestyle, 1.0)
    
    if not medical_exams:
        rate *= 1.2
    
    annual_premium = (coverage_amount / 1000) * rate
    
    # Mortality rate estimate (simplified)
    mortality_rate = round(0.1 + (age - 20) * 0.01 + (0.1 if gender == "Male" else 0), 2)
    
    if score < 4:
        recommendation = """High risk: Specialized life insurance strategies:
        • Consider guaranteed acceptance life insurance (no medical exams)
        • Look into group life insurance through employer
        • Explore government life insurance schemes: LIC, Postal Life Insurance
        • Consider term insurance with return of premium
        • Recommended insurers: LIC, SBI Life, HDFC Life
        • Important riders: Accidental death, disability waiver, critical illness
        • Alternative: Employer group insurance, union-sponsored policies"""
    elif score < 7:
        recommendation = """Moderate risk: Balanced life insurance approach:
        • Compare term vs whole life insurance based on needs
        • Consider ULIP (Unit Linked Insurance Plans) for investment + insurance
        • Add riders for comprehensive protection
        • Explore online term insurance for competitive rates
        • Recommended insurers: ICICI Prudential, Bajaj Allianz, Max Life
        • Useful features: Premium waiver, income replacement, education fund
        • Consider: Increasing term cover, decreasing term cover based on liabilities"""
    else:
        recommendation = """Low risk: Premium life insurance opportunities:
        • Excellent profile - negotiate best rates with multiple insurers
        • Consider high-value term insurance with comprehensive riders
        • Explore investment-linked life insurance for wealth creation
        • Consider whole life insurance for estate planning
        • Recommended insurers: TATA AIA, Aditya Birla, Kotak Life
        • Premium features: Global coverage, flexible premiums, bonus additions
        • Advanced options: Variable life insurance, offshore life insurance"""
    
    return score, recommendation, int(annual_premium), mortality_rate
