"""
Fraud Detector Utility - Enhanced for Indian Market
"""

def detect_fraud(claim_amount, claim_type, suspicious_docs, prior_fraud):
    score = 5
    alerts = []
    
    # Adjust thresholds for Indian market (INR)
    if claim_amount > 500000:  # ₹5 lakh threshold
        score += 2
        alerts.append("High claim amount detected (>₹5 lakhs).")
    elif claim_amount > 200000:  # ₹2 lakh threshold
        score += 1
        alerts.append("Moderate claim amount (>₹2 lakhs) - requires review.")
    
    if suspicious_docs:
        score += 2
        alerts.append("Suspicious documents flagged for verification.")
    
    if prior_fraud:
        score += 1
        alerts.append("Prior fraud history found in records.")
    
    if claim_type == "Cyber":
        score += 1
        alerts.append("Cyber claim: inherently higher risk category.")
    elif claim_type == "Auto" and claim_amount > 300000:
        score += 1
        alerts.append("High-value auto claim requires additional verification.")
    elif claim_type == "Property" and claim_amount > 1000000:
        score += 1
        alerts.append("High-value property claim - consider site inspection.")
    
    score = min(10, score)
    
    if score >= 8:
        alerts.append("🚨 POTENTIAL FRAUD DETECTED! Immediate review and investigation recommended.")
        alerts.append("Actions: Assign to fraud investigation team, request additional documentation.")
    elif score >= 6:
        alerts.append("⚠️ MODERATE FRAUD RISK. Enhanced review and verification required.")
        alerts.append("Actions: Secondary review, verify claim details, contact claimant.")
    else:
        alerts.append("✅ LOW FRAUD RISK. Standard processing can proceed.")
        alerts.append("Actions: Normal claim processing workflow.")
    
    # Add specific recommendations based on claim type
    if claim_type == "Auto":
        alerts.append("Auto-specific checks: Vehicle registration, accident report, repair estimates.")
    elif claim_type == "Property":
        alerts.append("Property-specific checks: Property ownership, damage assessment, repair quotes.")
    elif claim_type == "Cyber":
        alerts.append("Cyber-specific checks: Incident report, forensic analysis, business impact assessment.")
    elif claim_type == "Health":
        alerts.append("Health-specific checks: Medical reports, hospital bills, treatment verification.")
    elif claim_type == "Life":
        alerts.append("Life-specific checks: Death certificate, medical history, beneficiary verification.")
    
    return score, "\n".join(alerts)
