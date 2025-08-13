import streamlit as st
import pandas as pd
from utils.risk_calculator import calculate_auto_risk

st.set_page_config(page_title="Auto Insurance Assessment", page_icon="🚗", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1e3c72, #2a5298);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.form-container {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
}
.result-container {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    border-left: 5px solid #28a745;
}
.info-box {
    background: #e7f3ff;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #2196F3;
    margin: 1rem 0;
}
.stButton > button {
    background: linear-gradient(90deg, #28a745, #20c997);
    color: white;
    border: none;
    padding: 0.75rem 2rem;
    border-radius: 25px;
    font-weight: bold;
    transition: all 0.3s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🚗 Auto Insurance Risk Assessment</h1>
    <p>Get instant quotes and personalized recommendations for your vehicle insurance</p>
</div>
""", unsafe_allow_html=True)

# Info section
with st.container():
    st.markdown("""
    <div class="info-box">
        <h4>📋 What You'll Need</h4>
        <p>Please have your vehicle registration, driving license, and recent insurance documents ready. 
        This assessment takes about 2 minutes and provides instant results.</p>
    </div>
    """, unsafe_allow_html=True)

# Form in container
with st.form("auto_insurance_form"):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    st.markdown("### 🚙 Vehicle Information")
    col1, col2 = st.columns(2)
    
    with col1:
        vehicle_age = st.selectbox(
            "Vehicle Age",
            options=list(range(0, 31)),
            index=5,
            help="Select how many years old your vehicle is"
        )
        
        vehicle_type = st.selectbox(
            "Vehicle Type",
            ["Hatchback", "Sedan", "SUV", "Luxury Car", "Commercial Vehicle"],
            help="Choose your vehicle category"
        )
    
    with col2:
        fuel_type = st.selectbox(
            "Fuel Type",
            ["Petrol", "Diesel", "CNG", "Electric", "Hybrid"],
            help="Select your vehicle's fuel type"
        )
        
        city_tier = st.selectbox(
            "City Tier",
            ["Tier 1 (Metro)", "Tier 2 (Major City)", "Tier 3 (Small City)", "Rural"],
            help="Where is the vehicle primarily used?"
        )
    
    st.markdown("### 👤 Driver Information")
    col3, col4 = st.columns(2)
    
    with col3:
        driver_age = st.slider(
            "Driver Age (in years)",
            min_value=18,
            max_value=80,
            value=30,
            help="Age of the primary driver"
        )
        
        driving_experience = st.slider(
            "Driving Experience (years)",
            min_value=0,
            max_value=50,
            value=5,
            help="Total years of driving experience"
        )
    
    with col4:
        accident_history = st.selectbox(
            "Accident History (last 5 years)",
            [0, 1, 2, 3, 4, 5],
            help="Number of accidents in the past 5 years"
        )
        
        violations = st.selectbox(
            "Traffic Violations (last 3 years)",
            [0, 1, 2, 3, 4, 5],
            help="Number of traffic rule violations"
        )
    
    st.markdown("### 🛣️ Usage Information")
    col5, col6 = st.columns(2)
    
    with col5:
        mileage = st.number_input(
            "Annual Mileage (km)",
            min_value=1000,
            max_value=100000,
            value=15000,
            step=1000,
            help="Approximate yearly distance driven"
        )
    
    with col6:
        usage_type = st.selectbox(
            "Primary Usage",
            ["Personal/Family", "Daily Commute", "Business/Commercial", "Weekend/Occasional"],
            help="How do you primarily use your vehicle?"
        )
    
    st.markdown("---")
    
    # Submit button with styling
    submitted = st.form_submit_button("🔍 Calculate Insurance Quote", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

if submitted:
    # Input validation with friendly messages
    errors = []
    if driver_age < 18:
        errors.append("🚫 Driver must be at least 18 years old to get insurance.")
    if mileage < 1000:
        errors.append("🚫 Annual mileage seems too low. Please check your input.")
    if driving_experience > (driver_age - 18):
        errors.append("🚫 Driving experience cannot exceed years since legal driving age.")
    
    if errors:
        st.error("Please correct the following issues:")
        for error in errors:
            st.write(error)
    else:
        # Show loading state
        with st.spinner("🔄 Calculating your personalized insurance quote..."):
            import time
            time.sleep(1)  # Simulate processing time
            
            # Calculate risk with enhanced factors
            base_vehicle_age = vehicle_age
            enhanced_mileage = mileage
            
            # Adjust for additional factors
            vehicle_multiplier = {"Hatchback": 1.0, "Sedan": 1.1, "SUV": 1.2, "Luxury Car": 1.5, "Commercial Vehicle": 1.3}
            city_multiplier = {"Tier 1 (Metro)": 1.3, "Tier 2 (Major City)": 1.1, "Tier 3 (Small City)": 1.0, "Rural": 0.9}
            
            # Calculate base risk
            risk_score, recommendation, base_premium = calculate_auto_risk(base_vehicle_age, driver_age, accident_history, enhanced_mileage)
            
            # Adjust premium for additional factors
            adjusted_premium = base_premium * vehicle_multiplier.get(vehicle_type, 1.0) * city_multiplier.get(city_tier, 1.0)
            
            if violations > 0:
                adjusted_premium *= (1 + violations * 0.1)
            
            adjusted_premium = int(adjusted_premium)
        
        # Results section with enhanced styling
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        
        st.markdown("## 📊 Your Insurance Assessment Results")
        
        # Metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            risk_color = "🟢" if risk_score >= 7 else "🟡" if risk_score >= 4 else "🔴"
            st.metric(
                label="Risk Score",
                value=f"{risk_score}/10 {risk_color}",
                help="Higher scores indicate lower risk"
            )
        
        with col2:
            st.metric(
                label="Annual Premium",
                value=f"₹{adjusted_premium:,}",
                delta=f"₹{adjusted_premium - base_premium:+,}" if adjusted_premium != base_premium else None,
                help="Estimated annual insurance premium"
            )
        
        with col3:
            risk_level = "Low Risk" if risk_score >= 7 else "Moderate Risk" if risk_score >= 4 else "High Risk"
            level_color = "success" if risk_score >= 7 else "warning" if risk_score >= 4 else "error"
            st.metric(
                label="Risk Category",
                value=risk_level,
                help="Your risk classification"
            )
        
        with col4:
            discount_eligible = "Yes" if risk_score >= 6 and accident_history == 0 else "Limited" if risk_score >= 4 else "No"
            st.metric(
                label="Discount Eligible",
                value=discount_eligible,
                help="Eligibility for premium discounts"
            )
        
        # Recommendation section
        st.markdown("### 💡 Personalized Recommendations")
        
        if risk_score >= 7:
            st.success("🎉 Excellent! You qualify for our best rates and maximum discounts.")
        elif risk_score >= 4:
            st.warning("⚠️ Good profile with room for improvement to get better rates.")
        else:
            st.error("🚨 High-risk profile. Consider safety measures to reduce premiums.")
        
        # Enhanced recommendations based on profile
        st.markdown("#### 📋 Ways to Optimize Your Premium:")
        
        tips = []
        if accident_history == 0:
            tips.append("✅ Keep your clean driving record for No Claim Bonus (up to 50% discount)")
        if violations > 0:
            tips.append(f"🚦 You have {violations} traffic violations. Maintain clean record to improve rates")
        if vehicle_age < 5:
            tips.append("🆕 Consider Zero Depreciation cover for your newer vehicle")
        if city_tier == "Tier 1 (Metro)":
            tips.append("🏙️ Metro city driving increases risk. Consider anti-theft devices for discounts")
        if mileage > 20000:
            tips.append("🛣️ High annual mileage detected. Consider usage-based insurance")
        
        for tip in tips:
            st.write(tip)
        
        st.info(recommendation)
        
        # Comparison table
        st.markdown("#### 🏆 Quick Insurer Comparison")
        
        import pandas as pd
        comparison_data = {
            "Insurer": ["HDFC ERGO", "ICICI Lombard", "Bajaj Allianz", "TATA AIG"],
            "Premium Range": [f"₹{adjusted_premium-2000:,} - ₹{adjusted_premium+1000:,}",
                            f"₹{adjusted_premium-1500:,} - ₹{adjusted_premium+1500:,}",
                            f"₹{adjusted_premium-1000:,} - ₹{adjusted_premium+2000:,}",
                            f"₹{adjusted_premium-500:,} - ₹{adjusted_premium+2500:,}"],
            "Rating": ["4.5/5", "4.3/5", "4.2/5", "4.0/5"],
            "Best For": ["Digital services", "Comprehensive coverage", "Competitive rates", "Customer service"]
        }
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)
        
        # Save to session state
        st.session_state["auto_risk"] = {
            "vehicle_age": vehicle_age,
            "vehicle_type": vehicle_type,
            "driver_age": driver_age,
            "accident_history": accident_history,
            "mileage": mileage,
            "risk_score": risk_score,
            "recommendation": recommendation,
            "premium_estimate": adjusted_premium,
            "city_tier": city_tier,
            "fuel_type": fuel_type
        }
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Next steps
        st.markdown("### 🎯 Next Steps")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("📞 Get Expert Consultation", use_container_width=True):
                st.info("Connect with our insurance experts for personalized advice!")
        
        with col_b:
            if st.button("📄 View Policy Details", use_container_width=True):
                st.info("Detailed policy terms and conditions will be shown here.")
        
        with col_c:
            if st.button("💾 Save Quote", use_container_width=True):
                st.success("Quote saved! Check your email for details.")
