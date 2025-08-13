import streamlit as st
import pandas as pd
from utils.risk_calculator import calculate_health_risk

st.set_page_config(page_title="Health Insurance Assessment", page_icon="🏥", layout="wide")

# Custom CSS for health theme
st.markdown("""
<style>
.health-header {
    background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}

.health-section {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #ff6b6b;
    margin: 1rem 0;
}

.health-info {
    background: #e8f5e8;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #c3e6c3;
    margin: 1rem 0;
}

.risk-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

.bmi-indicator {
    padding: 0.5rem;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
    margin: 0.5rem 0;
}

.bmi-normal { background-color: #d4edda; color: #155724; }
.bmi-overweight { background-color: #fff3cd; color: #856404; }
.bmi-obese { background-color: #f8d7da; color: #721c24; }
.bmi-underweight { background-color: #cce7ff; color: #004085; }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="health-header">
    <h1>🏥 Health Insurance Risk Assessment</h1>
    <p>Comprehensive health evaluation for personalized insurance recommendations</p>
</div>
""", unsafe_allow_html=True)

# Health statistics for India
st.markdown("""
<div class="health-info">
    <h4>📊 Health Insurance Facts for India</h4>
    <p>Only <strong>28%</strong> of Indians have health insurance. Average medical inflation is <strong>12-15%</strong> annually. 
    Critical illness affects <strong>1 in 3</strong> people. Get adequate coverage to protect your family's financial health.</p>
</div>
""", unsafe_allow_html=True)

# Progress indicator
progress_cols = st.columns(5)
with progress_cols[0]:
    st.markdown("✅ **Personal Info**")
with progress_cols[1]:
    st.markdown("⚖️ **Physical Health**")
with progress_cols[2]:
    st.markdown("🏃 **Lifestyle**")
with progress_cols[3]:
    st.markdown("🧬 **Medical History**")
with progress_cols[4]:
    st.markdown("📊 **Assessment**")

st.markdown("---")

with st.form("health_form"):
    # Personal Information
    st.markdown("""
    <div class="health-section">
        <h3>👤 Personal Information</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input(
            "Age", 
            min_value=18, 
            max_value=100, 
            value=35,
            help="Age of the person to be insured"
        )
        
        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"],
            help="Gender affects certain health risk calculations"
        )
        
        occupation = st.selectbox(
            "Occupation Type",
            ["Desk Job/IT Professional", "Field Work", "Healthcare Worker", "Manual Labor", "Business/Sales", "Student", "Retired", "Other"],
            help="Occupation-related health risks"
        )
    
    with col2:
        height = st.number_input(
            "Height (cm)", 
            min_value=100, 
            max_value=250, 
            value=170,
            help="Height in centimeters"
        )
        
        weight = st.number_input(
            "Weight (kg)", 
            min_value=30, 
            max_value=200, 
            value=70,
            help="Current weight in kilograms"
        )
        
        # Calculate BMI automatically
        bmi = weight / ((height/100) ** 2) if height > 0 else 0
        
        bmi_category = ""
        bmi_class = ""
        if bmi < 18.5:
            bmi_category = "Underweight"
            bmi_class = "bmi-underweight"
        elif bmi < 25:
            bmi_category = "Normal"
            bmi_class = "bmi-normal"
        elif bmi < 30:
            bmi_category = "Overweight"
            bmi_class = "bmi-overweight"
        else:
            bmi_category = "Obese"
            bmi_class = "bmi-obese"
        
        st.markdown(f"""
        <div class="bmi-indicator {bmi_class}">
            BMI: {bmi:.1f} ({bmi_category})
        </div>
        """, unsafe_allow_html=True)

    # Lifestyle Factors
    st.markdown("""
    <div class="health-section">
        <h3>🏃 Lifestyle & Habits</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        smoking = st.selectbox(
            "Smoking Habit",
            ["Never smoked", "Former smoker (quit >2 years)", "Former smoker (quit <2 years)", "Occasional smoker", "Regular smoker"],
            help="Smoking history and current status"
        )
        
        alcohol = st.selectbox(
            "Alcohol Consumption",
            ["Never", "Occasionally (social)", "Moderate (2-3 times/week)", "Regular (daily)", "Heavy drinking"],
            help="Alcohol consumption pattern"
        )
        
        exercise_frequency = st.selectbox(
            "Exercise Frequency", 
            ["Never", "Rarely (monthly)", "Sometimes (weekly)", "Often (3-4 times/week)", "Daily"],
            help="Regular physical activity frequency"
        )
    
    with col4:
        diet_type = st.selectbox(
            "Diet Type",
            ["Balanced diet", "Vegetarian", "Vegan", "High protein", "Junk food heavy", "Irregular eating"],
            help="Primary dietary pattern"
        )
        
        sleep_hours = st.selectbox(
            "Average Sleep (hours/night)",
            ["< 5 hours", "5-6 hours", "6-7 hours", "7-8 hours", "8+ hours"],
            help="Average nightly sleep duration"
        )
        
        stress_level = st.selectbox(
            "Stress Level",
            ["Very Low", "Low", "Moderate", "High", "Very High"],
            help="Overall stress level in daily life"
        )

    # Medical History
    st.markdown("""
    <div class="health-section">
        <h3>🧬 Medical History</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        chronic_conditions = st.multiselect(
            "Existing Medical Conditions",
            ["None", "Diabetes", "Hypertension", "Heart Disease", "Asthma", "Arthritis", "Thyroid", "High Cholesterol", "Other"],
            help="Current chronic medical conditions"
        )
        
        medications = st.selectbox(
            "Regular Medications",
            ["None", "1-2 medications", "3-5 medications", "5+ medications"],
            help="Number of regular prescription medications"
        )
        
        last_checkup = st.selectbox(
            "Last Health Checkup",
            ["Within 6 months", "6-12 months ago", "1-2 years ago", "More than 2 years", "Never"],
            help="When was your last comprehensive health checkup"
        )
    
    with col6:
        family_history = st.multiselect(
            "Family Medical History",
            ["None", "Heart Disease", "Cancer", "Diabetes", "Stroke", "High Blood Pressure", "Mental Health Issues", "Genetic Disorders"],
            help="Family history of major illnesses"
        )
        
        previous_surgeries = st.selectbox(
            "Previous Surgeries",
            ["None", "Minor surgery", "Major surgery", "Multiple surgeries"],
            help="History of surgical procedures"
        )
        
        hospitalization = st.selectbox(
            "Hospitalizations (Last 5 years)",
            ["None", "1 time", "2-3 times", "4+ times"],
            help="Number of hospital admissions"
        )

    # Current Coverage
    st.markdown("""
    <div class="health-section">
        <h3>💼 Current Insurance Coverage</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col7, col8 = st.columns(2)
    
    with col7:
        current_coverage = st.selectbox(
            "Existing Health Insurance",
            ["None", "Corporate/Group insurance", "Individual policy < ₹5L", "Individual policy ₹5-10L", "Individual policy > ₹10L"],
            help="Current health insurance coverage"
        )
        
        coverage_amount = st.selectbox(
            "Desired Coverage Amount",
            ["₹5 Lakhs", "₹10 Lakhs", "₹15 Lakhs", "₹25 Lakhs", "₹50 Lakhs", "₹1 Crore+"],
            help="Desired insurance coverage amount"
        )
    
    with col8:
        family_members = st.number_input(
            "Family Members to Cover", 
            min_value=1, 
            max_value=10, 
            value=1,
            help="Number of family members for coverage"
        )
        
        preferred_hospitals = st.selectbox(
            "Preferred Hospital Network",
            ["Any network hospital", "Tier 1 city hospitals", "Premium hospitals only", "Specific hospital chain"],
            help="Hospital network preference"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_submit = st.columns([1, 2, 1])
    with col_submit[1]:
        submitted = st.form_submit_button(
            "🔍 Calculate Health Insurance Premium", 
            use_container_width=True,
            type="primary"
        )

if submitted:
    # Enhanced risk calculation
    smoking_binary = "Regular smoker" in smoking or "Occasional smoker" in smoking
    chronic_count = len([c for c in chronic_conditions if c != "None"])
    family_history_binary = len([f for f in family_history if f != "None"]) > 0
    
    risk_score, recommendation, premium_estimate = calculate_health_risk(
        age, 
        bmi, 
        smoking_binary, 
        exercise_frequency, 
        chronic_count, 
        family_history_binary
    )
    
    # Advanced premium calculation
    base_premium = premium_estimate
    
    # Age-based adjustment
    if age > 60:
        base_premium *= 2.0
    elif age > 45:
        base_premium *= 1.5
    elif age > 35:
        base_premium *= 1.2
    
    # Lifestyle adjustments
    if "Regular smoker" in smoking:
        base_premium *= 1.5
    elif "Occasional smoker" in smoking:
        base_premium *= 1.3
    
    if "Heavy drinking" in alcohol:
        base_premium *= 1.3
    elif "Regular" in alcohol:
        base_premium *= 1.1
    
    # Exercise discount
    if "Daily" in exercise_frequency:
        base_premium *= 0.9
    elif "Often" in exercise_frequency:
        base_premium *= 0.95
    
    # Coverage amount adjustment
    coverage_multiplier = {
        "₹5 Lakhs": 1.0, "₹10 Lakhs": 1.8, "₹15 Lakhs": 2.5,
        "₹25 Lakhs": 3.8, "₹50 Lakhs": 7.0, "₹1 Crore+": 12.0
    }
    base_premium *= coverage_multiplier.get(coverage_amount, 1.0)
    
    # Family members adjustment
    if family_members > 1:
        base_premium *= (1 + (family_members - 1) * 0.7)  # 70% for each additional member
    
    final_premium = int(base_premium)
    
    # Display results
    st.success("🎯 Health Insurance Assessment Complete!", icon="✅")
    
    # Results dashboard
    st.markdown("### 📊 Health Risk Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        health_status = "High Risk" if risk_score >= 7 else "Moderate Risk" if risk_score >= 4 else "Low Risk"
        st.metric(
            label="Health Risk",
            value=health_status,
            delta=f"Score: {risk_score}/10"
        )
    
    with col2:
        st.metric(
            label="Monthly Premium",
            value=f"₹{final_premium:,.0f}",
            delta=f"For {coverage_amount} coverage"
        )
    
    with col3:
        st.metric(
            label="Annual Premium",
            value=f"₹{final_premium*12:,.0f}",
            delta=f"Family of {family_members}"
        )
    
    with col4:
        wellness_score = max(10, 100 - (risk_score * 10) - (chronic_count * 5))
        st.metric(
            label="Wellness Score",
            value=f"{wellness_score}%",
            delta="Health rating"
        )
    
    # Health insights
    st.markdown("### 🩺 Health Insights & Risk Factors")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.markdown("**🔍 Risk Factors Identified:**")
        risk_factors = []
        
        if bmi >= 30:
            risk_factors.append("High BMI (Obesity)")
        elif bmi >= 25:
            risk_factors.append("Elevated BMI (Overweight)")
        
        if age > 50:
            risk_factors.append("Advanced age factor")
        
        if smoking_binary:
            risk_factors.append("Smoking habit")
        
        if chronic_count > 0:
            risk_factors.append(f"{chronic_count} chronic condition(s)")
        
        if family_history_binary:
            risk_factors.append("Family medical history")
        
        if "Never" in exercise_frequency or "Rarely" in exercise_frequency:
            risk_factors.append("Sedentary lifestyle")
        
        if not risk_factors:
            risk_factors.append("No major risk factors identified")
        
        for factor in risk_factors:
            st.write(f"• {factor}")
    
    with insights_col2:
        st.markdown("**💡 Health Improvement Suggestions:**")
        
        suggestions = []
        
        if bmi >= 25:
            suggestions.append("Consider weight management program")
        
        if "Never" in exercise_frequency:
            suggestions.append("Start regular physical activity (30 min/day)")
        
        if smoking_binary:
            suggestions.append("Smoking cessation program recommended")
        
        if "High" in stress_level:
            suggestions.append("Stress management techniques")
        
        if "< 5 hours" in sleep_hours or "5-6 hours" in sleep_hours:
            suggestions.append("Improve sleep hygiene (7-8 hours)")
        
        if "More than 2 years" in last_checkup or "Never" in last_checkup:
            suggestions.append("Schedule comprehensive health checkup")
        
        for suggestion in suggestions[:6]:  # Show top 6 suggestions
            st.write(f"• {suggestion}")
    
    # Insurance recommendations
    st.markdown("### 💊 Personalized Insurance Recommendations")
    
    recommendations_list = []
    
    if age > 45:
        recommendations_list.append("Consider critical illness cover for age-related risks")
    
    if chronic_count > 0:
        recommendations_list.append("Ensure pre-existing disease coverage after waiting period")
    
    if family_history_binary:
        recommendations_list.append("Genetic counseling and early screening recommendations")
    
    if family_members > 1:
        recommendations_list.append("Family floater policy may be more cost-effective")
    
    recommendations_list.append(f"Annual health checkup covered under {coverage_amount} plan")
    recommendations_list.append("Consider top-up plan for higher coverage at lower cost")
    
    for i, rec in enumerate(recommendations_list, 1):
        st.info(f"**{i}.** {rec}", icon="💡")
    
    # Top health insurance providers
    st.markdown("### 🏥 Top Health Insurance Providers in India")
    
    insurers_data = [
        ["Star Health Insurance", f"₹{final_premium*0.9:,.0f} - ₹{final_premium*1.1:,.0f}", "4.3⭐", "Health Specialist", "No Room Rent Limit"],
        ["HDFC ERGO Health", f"₹{final_premium*0.85:,.0f} - ₹{final_premium*1.05:,.0f}", "4.5⭐", "Wide Network", "Quick Claim Settlement"],
        ["ICICI Lombard Health", f"₹{final_premium*0.95:,.0f} - ₹{final_premium*1.15:,.0f}", "4.4⭐", "Digital First", "24x7 Support"],
        ["Bajaj Allianz Health", f"₹{final_premium*1.0:,.0f} - ₹{final_premium*1.2:,.0f}", "4.2⭐", "Comprehensive Cover", "Health Coaching"],
        ["New India Mediclaim", f"₹{final_premium*0.8:,.0f} - ₹{final_premium*1.0:,.0f}", "4.1⭐", "Government Backed", "Affordable Premium"],
        ["Max Bupa Health", f"₹{final_premium*1.05:,.0f} - ₹{final_premium*1.25:,.0f}", "4.4⭐", "Premium Care", "International Coverage"]
    ]
    
    df = pd.DataFrame(insurers_data, columns=["Insurance Provider", "Premium Range", "Rating", "Specialty", "Key Feature"])
    st.dataframe(df, use_container_width=True)
    
    # Save to session state
    st.session_state["health_risk"] = {
        "age": age,
        "bmi": bmi,
        "smoking": smoking,
        "exercise_frequency": exercise_frequency,
        "chronic_conditions": chronic_conditions,
        "family_history": family_history,
        "coverage_amount": coverage_amount,
        "family_members": family_members,
        "risk_score": risk_score,
        "premium_estimate": final_premium,
        "health_status": health_status,
        "wellness_score": wellness_score
    }
