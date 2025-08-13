import streamlit as st
import pandas as pd
from utils.risk_calculator import calculate_property_risk

st.set_page_config(page_title="Property Insurance Assessment", page_icon="🏠", layout="wide")

# Custom CSS for better UI
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #2c3e50 0%, #3498db 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}

.section-header {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #3498db;
    margin: 1rem 0;
}

.info-box {
    background: #e8f4fd;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #bde0ff;
    margin: 1rem 0;
}

.form-section {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

.stSelectbox > div > div {
    background-color: #ffffff;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
}

.stNumberInput > div > div > input {
    background-color: #ffffff;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🏠 Property Insurance Risk Assessment</h1>
    <p>Comprehensive evaluation for your property protection needs</p>
</div>
""", unsafe_allow_html=True)

# Information section
st.markdown("""
<div class="info-box">
    <h4>📋 What We Evaluate</h4>
    <p>Our AI-powered assessment considers property age, location risks, construction materials, and environmental factors to provide accurate insurance recommendations tailored for Indian property market.</p>
</div>
""", unsafe_allow_html=True)

# Progress indicator
progress_cols = st.columns(4)
with progress_cols[0]:
    st.markdown("✅ **Property Details**")
with progress_cols[1]:
    st.markdown("🏗️ **Construction Info**")
with progress_cols[2]:
    st.markdown("🌍 **Risk Factors**")
with progress_cols[3]:
    st.markdown("📊 **Assessment**")

st.markdown("---")

with st.form("property_form"):
    # Property Information Section
    st.markdown("""
    <div class="section-header">
        <h3>🏠 Property Information</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        property_age = st.number_input(
            "Property Age (years)", 
            min_value=0, 
            max_value=100, 
            value=10,
            help="Age of the property in years"
        )
        
        property_value = st.number_input(
            "Property Value (₹ Lakhs)", 
            min_value=5, 
            max_value=1000, 
            value=50,
            help="Current market value of your property"
        )
    
    with col2:
        property_type = st.selectbox(
            "Property Type", 
            ["Apartment", "Independent House", "Villa", "Row House", "Penthouse"],
            help="Type of residential property"
        )
        
        carpet_area = st.number_input(
            "Carpet Area (sq ft)", 
            min_value=200, 
            max_value=10000, 
            value=1000,
            help="Carpet area of the property"
        )

    # Construction Details Section
    st.markdown("""
    <div class="section-header">
        <h3>🏗️ Construction Details</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        construction_type = st.selectbox(
            "Construction Type", 
            ["RCC (Reinforced Concrete)", "Brick & Mortar", "Steel Frame", "Wood Frame", "Other"],
            help="Primary construction material"
        )
        
        floor_level = st.selectbox(
            "Floor Level", 
            ["Ground Floor", "1st-3rd Floor", "4th-7th Floor", "8th Floor & Above"],
            help="Floor on which property is located"
        )
    
    with col4:
        electrical_system = st.selectbox(
            "Electrical System Age", 
            ["Less than 5 years", "5-10 years", "10-20 years", "More than 20 years"],
            help="Age of electrical wiring and systems"
        )
        
        security_features = st.multiselect(
            "Security Features",
            ["CCTV Surveillance", "Security Guard", "Intercom System", "Fire Extinguisher", "Smoke Detector", "Burglar Alarm"],
            help="Available security features"
        )

    # Location & Risk Factors Section
    st.markdown("""
    <div class="section-header">
        <h3>🌍 Location & Risk Factors</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        location_risk = st.selectbox(
            "Location Risk Level", 
            ["Low Risk (Tier 1 Cities - Safe Areas)", "Medium Risk (Tier 2 Cities)", "High Risk (Flood/Earthquake Prone)"],
            help="Risk level based on geographical location"
        )
        
        nearby_facilities = st.multiselect(
            "Nearby Facilities",
            ["Fire Station (< 2km)", "Hospital (< 1km)", "Police Station (< 2km)", "Main Road Access", "Public Transport"],
            help="Emergency services and connectivity"
        )
    
    with col6:
        flood_zone = st.checkbox("Located in Flood Prone Area?", help="Is the property in a flood-prone zone?")
        earthquake_zone = st.checkbox("High Earthquake Risk Zone?", help="Is the property in seismic zone IV or V?")
        industrial_area = st.checkbox("Near Industrial Area?", help="Located within 5km of industrial zone?")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_submit = st.columns([1, 2, 1])
    with col_submit[1]:
        submitted = st.form_submit_button(
            "🔍 Calculate Property Insurance Risk", 
            use_container_width=True,
            type="primary"
        )

if submitted:
    # Enhanced risk calculation with additional parameters
    risk_score, recommendation, premium_estimate = calculate_property_risk(
        property_age, 
        location_risk.split(" ")[0], 
        construction_type, 
        flood_zone
    )
    
    # Adjust premium based on additional factors
    base_premium = premium_estimate
    
    # Property value adjustment
    if property_value > 100:
        base_premium *= 1.3
    elif property_value > 75:
        base_premium *= 1.2
    elif property_value > 50:
        base_premium *= 1.1
    
    # Security features discount
    security_discount = len(security_features) * 0.02  # 2% per feature
    base_premium *= (1 - min(security_discount, 0.15))  # Max 15% discount
    
    # Floor level adjustment
    if "Ground Floor" in floor_level:
        base_premium *= 1.1  # Higher risk
    elif "8th Floor" in floor_level:
        base_premium *= 1.05  # Slightly higher risk
    
    final_premium = int(base_premium)
    
    # Display results with enhanced UI
    st.success("🎯 Property Risk Assessment Complete!", icon="✅")
    
    # Results dashboard
    st.markdown("### 📊 Assessment Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Risk Score",
            value=f"{risk_score}/10",
            delta=f"Risk Level: {'Low' if risk_score >= 7 else 'Medium' if risk_score >= 4 else 'High'}"
        )
    
    with col2:
        st.metric(
            label="Annual Premium",
            value=f"₹{final_premium:,.0f}",
            delta=f"For ₹{property_value}L property"
        )
    
    with col3:
        coverage_percent = min(95, 70 + len(security_features) * 2)
        st.metric(
            label="Coverage %",
            value=f"{coverage_percent}%",
            delta="Of property value"
        )
    
    with col4:
        claim_ratio = max(5, 15 - len(security_features))
        st.metric(
            label="Claim Ratio",
            value=f"{claim_ratio}%",
            delta="Industry average"
        )
    
    # Detailed recommendations
    st.markdown("### 💡 Personalized Recommendations")
    
    recommendations = [
        f"Based on your {property_type.lower()} with {construction_type.lower()}, we recommend comprehensive coverage",
        f"Property age ({property_age} years) suggests {'standard' if property_age < 20 else 'enhanced'} maintenance coverage",
        f"Security features present: {len(security_features)} - Eligible for safety discount",
        f"Location risk level: {location_risk.split(' ')[0]} - Premium adjusted accordingly"
    ]
    
    if flood_zone:
        recommendations.append("⚠️ Flood zone property - Add natural disaster coverage")
    if earthquake_zone:
        recommendations.append("⚠️ Earthquake risk zone - Structural damage coverage recommended")
    if len(security_features) < 3:
        recommendations.append("🔒 Consider adding more security features for premium discounts")
    
    for i, rec in enumerate(recommendations, 1):
        st.info(f"**{i}.** {rec}", icon="💡")
    
    # Top insurers for property insurance
    st.markdown("### 🏢 Top Property Insurance Providers in India")
    
    insurers_data = [
        ["HDFC ERGO General", f"₹{final_premium*0.9:,.0f} - ₹{final_premium*1.1:,.0f}", "4.6⭐", "Quick Claim Settlement", "Online & Offline"],
        ["ICICI Lombard", f"₹{final_premium*0.85:,.0f} - ₹{final_premium*1.05:,.0f}", "4.4⭐", "24x7 Customer Support", "Digital First"],
        ["Bajaj Allianz", f"₹{final_premium*0.95:,.0f} - ₹{final_premium*1.15:,.0f}", "4.5⭐", "Wide Network", "Comprehensive Coverage"],
        ["New India Assurance", f"₹{final_premium*0.8:,.0f} - ₹{final_premium*1.0:,.0f}", "4.2⭐", "Government Backed", "Trusted Brand"],
        ["Tata AIG", f"₹{final_premium*0.9:,.0f} - ₹{final_premium*1.1:,.0f}", "4.3⭐", "Smart Claims Process", "Innovation Focus"],
        ["Oriental Insurance", f"₹{final_premium*0.85:,.0f} - ₹{final_premium*1.05:,.0f}", "4.1⭐", "Affordable Premiums", "PSU Reliability"]
    ]
    
    df = pd.DataFrame(insurers_data, columns=["Insurance Provider", "Premium Range", "Rating", "Key Strength", "Service Type"])
    st.dataframe(df, use_container_width=True)
    
    # Coverage breakdown
    st.markdown("### 📋 Recommended Coverage Breakdown")
    
    coverage_col1, coverage_col2 = st.columns(2)
    
    with coverage_col1:
        st.markdown("""
        **🏠 Structure Coverage**
        - Building & Fixtures: ₹{:,.0f}
        - Electrical Fittings: ₹{:,.0f}
        - Plumbing: ₹{:,.0f}
        """.format(property_value*50000, property_value*8000, property_value*5000))
    
    with coverage_col2:
        st.markdown("""
        **🛋️ Contents Coverage**
        - Household Items: ₹{:,.0f}
        - Electronics: ₹{:,.0f}
        - Jewelry & Valuables: ₹{:,.0f}
        """.format(property_value*15000, property_value*10000, property_value*5000))
    
    # Save to session state
    st.session_state["property_risk"] = {
        "property_age": property_age,
        "property_value": property_value,
        "property_type": property_type,
        "location_risk": location_risk,
        "construction_type": construction_type,
        "flood_zone": flood_zone,
        "security_features": security_features,
        "risk_score": risk_score,
        "premium_estimate": final_premium,
        "coverage_percent": coverage_percent
    }
