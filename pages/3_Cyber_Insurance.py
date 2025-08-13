import streamlit as st
import pandas as pd
from utils.risk_calculator import calculate_cyber_risk

st.set_page_config(page_title="Cyber Insurance Assessment", page_icon="🔒", layout="wide")

# Custom CSS for cybersecurity theme
st.markdown("""
<style>
.cyber-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}

.security-section {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #667eea;
    margin: 1rem 0;
}

.cyber-alert {
    background: #fff3cd;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #ffeaa7;
    margin: 1rem 0;
}

.form-container {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

.metric-cyber {
    background: linear-gradient(135deg, #4834d4 0%, #686de0 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin: 0.5rem 0;
}

.threat-card {
    background: #ffe6e6;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #ff6b6b;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="cyber-header">
    <h1>🔒 Cyber Insurance Risk Assessment</h1>
    <p>Comprehensive cybersecurity evaluation for digital age protection</p>
</div>
""", unsafe_allow_html=True)

# Cyber threat awareness
st.markdown("""
<div class="cyber-alert">
    <h4>⚠️ Cyber Threats in India - 2024 Statistics</h4>
    <p>India faces <strong>1.1 million cyber attacks daily</strong>. Ransomware attacks increased by <strong>218%</strong> in 2023. 
    Small businesses are <strong>3x more likely</strong> to be targeted. Protect your organization with comprehensive cyber insurance.</p>
</div>
""", unsafe_allow_html=True)

# Progress steps
progress_cols = st.columns(5)
with progress_cols[0]:
    st.markdown("✅ **Organization Info**")
with progress_cols[1]:
    st.markdown("🔐 **Security Posture**")
with progress_cols[2]:
    st.markdown("🛡️ **Risk Factors**")
with progress_cols[3]:
    st.markdown("📊 **Assessment**")
with progress_cols[4]:
    st.markdown("💼 **Coverage**")

st.markdown("---")

with st.form("cyber_form"):
    # Organization Information
    st.markdown("""
    <div class="security-section">
        <h3>🏢 Organization Information</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        business_type = st.selectbox(
            "Business Type",
            ["IT Services", "E-commerce", "Financial Services", "Healthcare", "Manufacturing", "Education", "Government", "Retail", "Other"],
            help="Type of business organization"
        )
        
        num_employees = st.number_input(
            "Number of Employees", 
            min_value=1, 
            max_value=10000, 
            value=50,
            help="Total number of employees in organization"
        )
        
        annual_revenue = st.selectbox(
            "Annual Revenue (₹ Crores)",
            ["< 1 Crore", "1-5 Crores", "5-25 Crores", "25-100 Crores", "> 100 Crores"],
            help="Annual business revenue"
        )
    
    with col2:
        data_sensitivity = st.selectbox(
            "Data Sensitivity Level",
            ["Low (Basic business data)", "Medium (Customer data)", "High (Financial/Medical data)", "Critical (Government/Defense)"],
            help="Level of sensitive data handled"
        )
        
        customer_data_volume = st.selectbox(
            "Customer Data Volume",
            ["< 1,000 records", "1,000 - 10,000 records", "10,000 - 100,000 records", "> 100,000 records"],
            help="Volume of customer data stored"
        )
        
        compliance_requirements = st.multiselect(
            "Compliance Requirements",
            ["GDPR", "PCI DSS", "HIPAA", "SOX", "ISO 27001", "RBI Guidelines", "SEBI Regulations", "None"],
            help="Regulatory compliance requirements"
        )

    # Security Infrastructure
    st.markdown("""
    <div class="security-section">
        <h3>🔐 Security Infrastructure</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        has_security_policy = st.checkbox("Formal Cybersecurity Policy", help="Written and implemented security policies")
        uses_mfa = st.checkbox("Multi-Factor Authentication", help="MFA enabled for critical systems")
        has_firewall = st.checkbox("Enterprise Firewall", help="Network firewall protection")
        has_antivirus = st.checkbox("Endpoint Security/Antivirus", help="Comprehensive endpoint protection")
        has_backup = st.checkbox("Regular Data Backups", help="Automated backup systems")
    
    with col4:
        security_training = st.selectbox(
            "Employee Security Training",
            ["None", "Annual Training", "Quarterly Training", "Monthly Training", "Continuous Training"],
            help="Frequency of cybersecurity awareness training"
        )
        
        incident_response = st.selectbox(
            "Incident Response Plan",
            ["No plan", "Basic plan", "Documented plan", "Tested plan", "Certified plan"],
            help="Cybersecurity incident response preparedness"
        )
        
        security_budget = st.selectbox(
            "Security Budget (% of Revenue)",
            ["< 1%", "1-3%", "3-5%", "5-10%", "> 10%"],
            help="Annual cybersecurity investment"
        )

    # Risk Assessment
    st.markdown("""
    <div class="security-section">
        <h3>🛡️ Risk Assessment</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        past_incidents = st.number_input(
            "Past Cyber Incidents (Last 3 years)", 
            min_value=0, 
            max_value=20, 
            value=0,
            help="Number of cyber security incidents experienced"
        )
        
        remote_work = st.selectbox(
            "Remote Work Policy",
            ["No remote work", "Limited remote work", "Hybrid model", "Fully remote", "BYOD policy"],
            help="Remote work arrangements"
        )
        
        cloud_usage = st.selectbox(
            "Cloud Infrastructure",
            ["No cloud services", "Basic cloud usage", "Hybrid cloud", "Multi-cloud", "Cloud-first strategy"],
            help="Cloud services utilization"
        )
    
    with col6:
        third_party_vendors = st.number_input(
            "Third-party Vendor Integrations", 
            min_value=0, 
            max_value=100, 
            value=5,
            help="Number of external vendor integrations"
        )
        
        payment_processing = st.checkbox("Online Payment Processing", help="Handles online financial transactions")
        mobile_apps = st.checkbox("Mobile Applications", help="Organization has mobile apps")
        iot_devices = st.checkbox("IoT/Connected Devices", help="Uses Internet of Things devices")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_submit = st.columns([1, 2, 1])
    with col_submit[1]:
        submitted = st.form_submit_button(
            "🔍 Calculate Cyber Risk Assessment", 
            use_container_width=True,
            type="primary"
        )

if submitted:
    # Enhanced risk calculation
    risk_score, recommendation, premium_estimate = calculate_cyber_risk(
        num_employees, 
        has_security_policy, 
        past_incidents, 
        uses_mfa
    )
    
    # Advanced premium calculation based on additional factors
    base_premium = premium_estimate
    
    # Business type risk multiplier
    business_risk = {
        "Financial Services": 1.5, "Healthcare": 1.4, "E-commerce": 1.3,
        "IT Services": 1.2, "Government": 1.4, "Education": 1.1,
        "Manufacturing": 1.0, "Retail": 1.1, "Other": 1.0
    }
    base_premium *= business_risk.get(business_type, 1.0)
    
    # Revenue-based adjustment
    revenue_multiplier = {
        "< 1 Crore": 0.7, "1-5 Crores": 1.0, "5-25 Crores": 1.3,
        "25-100 Crores": 1.6, "> 100 Crores": 2.0
    }
    base_premium *= revenue_multiplier.get(annual_revenue, 1.0)
    
    # Security posture discount
    security_score = 0
    security_score += 1 if has_security_policy else 0
    security_score += 1 if uses_mfa else 0
    security_score += 1 if has_firewall else 0
    security_score += 1 if has_antivirus else 0
    security_score += 1 if has_backup else 0
    
    security_discount = security_score * 0.03  # 3% per security measure
    base_premium *= (1 - min(security_discount, 0.20))  # Max 20% discount
    
    # Past incidents penalty
    if past_incidents > 0:
        base_premium *= (1 + past_incidents * 0.15)  # 15% increase per incident
    
    final_premium = int(base_premium)
    
    # Calculate risk level
    total_risk_factors = past_incidents + (0 if has_security_policy else 2) + (0 if uses_mfa else 1)
    adjusted_risk_score = max(1, min(10, risk_score - total_risk_factors))
    
    # Display results
    st.success("🎯 Cyber Risk Assessment Complete!", icon="✅")
    
    # Results dashboard
    st.markdown("### 📊 Cybersecurity Risk Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        risk_level = "Critical" if adjusted_risk_score <= 3 else "High" if adjusted_risk_score <= 5 else "Medium" if adjusted_risk_score <= 7 else "Low"
        st.metric(
            label="Risk Level",
            value=risk_level,
            delta=f"Score: {adjusted_risk_score}/10"
        )
    
    with col2:
        st.metric(
            label="Annual Premium",
            value=f"₹{final_premium:,.0f}",
            delta=f"For {num_employees} employees"
        )
    
    with col3:
        coverage_amount = final_premium * 50  # 50x premium as coverage
        st.metric(
            label="Coverage Amount",
            value=f"₹{coverage_amount:,.0f}",
            delta="Maximum claim"
        )
    
    with col4:
        security_rating = min(100, security_score * 20)
        st.metric(
            label="Security Rating",
            value=f"{security_rating}%",
            delta=f"{security_score}/5 measures"
        )
    
    # Threat analysis
    st.markdown("### ⚠️ Threat Analysis")
    
    threat_col1, threat_col2 = st.columns(2)
    
    with threat_col1:
        st.markdown("""
        <div class="threat-card">
            <h4>🎯 Primary Threats for Your Business</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if business_type == "Financial Services":
            threats = ["Ransomware attacks", "Data breaches", "Insider threats", "API vulnerabilities"]
        elif business_type == "E-commerce":
            threats = ["Payment fraud", "Customer data theft", "DDoS attacks", "Supply chain attacks"]
        elif business_type == "Healthcare":
            threats = ["Medical record theft", "Ransomware", "IoT vulnerabilities", "Insider threats"]
        else:
            threats = ["Phishing attacks", "Malware infections", "Data breaches", "Business disruption"]
        
        for threat in threats:
            st.write(f"• {threat}")
    
    with threat_col2:
        st.markdown("""
        <div class="threat-card">
            <h4>📈 Attack Likelihood Factors</h4>
        </div>
        """, unsafe_allow_html=True)
        
        factors = []
        if past_incidents > 0:
            factors.append(f"Previous incidents: {past_incidents} (High risk)")
        if not has_security_policy:
            factors.append("No security policy (Medium risk)")
        if not uses_mfa:
            factors.append("No MFA (Medium risk)")
        if "remote work" in remote_work.lower() and "no" not in remote_work.lower():
            factors.append("Remote work (Low-Medium risk)")
        if not factors:
            factors.append("Good security posture (Low risk)")
        
        for factor in factors:
            st.write(f"• {factor}")
    
    # Recommendations
    st.markdown("### 💡 Cybersecurity Recommendations")
    
    recommendations = []
    
    if not has_security_policy:
        recommendations.append("Develop and implement a comprehensive cybersecurity policy")
    if not uses_mfa:
        recommendations.append("Enable Multi-Factor Authentication for all critical systems")
    if not has_firewall:
        recommendations.append("Deploy enterprise-grade firewall protection")
    if security_training == "None":
        recommendations.append("Implement regular cybersecurity awareness training for employees")
    if incident_response in ["No plan", "Basic plan"]:
        recommendations.append("Develop and test incident response procedures")
    if past_incidents > 0:
        recommendations.append("Conduct security audit to identify and remediate vulnerabilities")
    
    for i, rec in enumerate(recommendations[:6], 1):  # Show top 6 recommendations
        st.info(f"**{i}.** {rec}", icon="💡")
    
    # Insurance providers
    st.markdown("### 🏢 Top Cyber Insurance Providers in India")
    
    insurers_data = [
        ["HDFC ERGO Cyber Sachet", f"₹{final_premium*0.85:,.0f} - ₹{final_premium*1.1:,.0f}", "4.5⭐", "SME Focused", "₹1-50 Cr Coverage"],
        ["ICICI Lombard CyberSafe", f"₹{final_premium*0.9:,.0f} - ₹{final_premium*1.15:,.0f}", "4.4⭐", "24x7 Support", "Incident Response"],
        ["Bajaj Allianz CyberEdge", f"₹{final_premium*0.95:,.0f} - ₹{final_premium*1.2:,.0f}", "4.3⭐", "Comprehensive Cover", "Legal Support"],
        ["Tata AIG Cyber Secure", f"₹{final_premium*0.88:,.0f} - ₹{final_premium*1.1:,.0f}", "4.4⭐", "Risk Assessment", "Prevention Focus"],
        ["New India Cyber Protect", f"₹{final_premium*0.8:,.0f} - ₹{final_premium*1.05:,.0f}", "4.1⭐", "Government Backing", "Affordable Rates"],
        ["Oriental Cyber Shield", f"₹{final_premium*0.85:,.0f} - ₹{final_premium*1.08:,.0f}", "4.2⭐", "PSU Trust", "Quick Claims"]
    ]
    
    df = pd.DataFrame(insurers_data, columns=["Insurance Product", "Premium Range", "Rating", "Key Feature", "Coverage"])
    st.dataframe(df, use_container_width=True)
    
    # Coverage details
    st.markdown("### 📋 Recommended Coverage Components")
    
    coverage_col1, coverage_col2 = st.columns(2)
    
    with coverage_col1:
        st.markdown("""
        **🛡️ First-Party Coverage**
        - Business Interruption: ₹{:,.0f}
        - Data Recovery: ₹{:,.0f}
        - Cyber Extortion: ₹{:,.0f}
        - System Restoration: ₹{:,.0f}
        """.format(coverage_amount*0.3, coverage_amount*0.2, coverage_amount*0.15, coverage_amount*0.1))
    
    with coverage_col2:
        st.markdown("""
        **⚖️ Third-Party Coverage**
        - Data Liability: ₹{:,.0f}
        - Regulatory Fines: ₹{:,.0f}
        - Legal Defense: ₹{:,.0f}
        - Credit Monitoring: ₹{:,.0f}
        """.format(coverage_amount*0.4, coverage_amount*0.2, coverage_amount*0.15, coverage_amount*0.1))
    
    # Save to session state
    st.session_state["cyber_risk"] = {
        "business_type": business_type,
        "num_employees": num_employees,
        "has_security_policy": has_security_policy,
        "uses_mfa": uses_mfa,
        "past_incidents": past_incidents,
        "security_score": security_score,
        "risk_score": adjusted_risk_score,
        "premium_estimate": final_premium,
        "coverage_amount": coverage_amount,
        "risk_level": risk_level
    }
