import streamlit as st
import pandas as pd
from utils.risk_calculator import calculate_life_risk

st.set_page_config(page_title="Life Insurance Assessment", page_icon="👨‍👩‍👧‍👦", layout="wide")

# Custom CSS for life insurance theme
st.markdown("""
<style>
.life-header {
    background: linear-gradient(135deg, #8e44ad 0%, #3498db 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}

.life-section {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #8e44ad;
    margin: 1rem 0;
}

.protection-info {
    background: #e8f4fd;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #bde0ff;
    margin: 1rem 0;
}

.calculator-section {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

.needs-analysis {
    background: #fff8e1;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #ffcc02;
    margin: 1rem 0;
}

.family-card {
    background: #f3e5f5;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #9c27b0;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="life-header">
    <h1>👨‍👩‍👧‍👦 Life Insurance Risk Assessment</h1>
    <p>Comprehensive life protection planning for your family's financial security</p>
</div>
""", unsafe_allow_html=True)

# Life insurance importance
st.markdown("""
<div class="protection-info">
    <h4>🛡️ Why Life Insurance Matters</h4>
    <p>Only <strong>3.2%</strong> of Indians have life insurance coverage. Average coverage is just <strong>₹3.2 lakhs</strong> - 
    far below recommended <strong>10-15x annual income</strong>. Secure your family's future with adequate life protection.</p>
</div>
""", unsafe_allow_html=True)

# Progress indicator
progress_cols = st.columns(6)
with progress_cols[0]:
    st.markdown("✅ **Personal Details**")
with progress_cols[1]:
    st.markdown("👨‍👩‍👧‍👦 **Family Info**")
with progress_cols[2]:
    st.markdown("💼 **Financial Details**")
with progress_cols[3]:
    st.markdown("🏥 **Health & Lifestyle**")
with progress_cols[4]:
    st.markdown("📊 **Needs Analysis**")
with progress_cols[5]:
    st.markdown("💰 **Premium Calculation**")

st.markdown("---")

with st.form("life_form"):
    # Personal Information
    st.markdown("""
    <div class="life-section">
        <h3>👤 Personal Information</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input(
            "Age", 
            min_value=18, 
            max_value=80, 
            value=35,
            help="Age of the person to be insured"
        )
        
        gender = st.selectbox(
            "Gender", 
            ["Male", "Female", "Other"],
            help="Gender affects life expectancy calculations"
        )
        
        marital_status = st.selectbox(
            "Marital Status",
            ["Single", "Married", "Divorced", "Widowed"],
            help="Family status for dependency calculation"
        )
    
    with col2:
        education_level = st.selectbox(
            "Education Level",
            ["High School", "Graduate", "Post Graduate", "Professional Degree", "Doctorate"],
            help="Education level affects earning potential"
        )
        
        city_tier = st.selectbox(
            "City Type",
            ["Tier 1 City (Mumbai, Delhi, etc.)", "Tier 2 City", "Tier 3 City", "Rural Area"],
            help="Location affects cost of living and risk factors"
        )
        
        income_stability = st.selectbox(
            "Income Stability",
            ["Highly Stable (Government)", "Stable (Corporate)", "Moderate (Business)", "Variable (Freelance)"],
            help="Stability of income source"
        )

    # Family Information
    st.markdown("""
    <div class="life-section">
        <h3>👨‍👩‍👧‍👦 Family Information</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        dependents = st.number_input(
            "Number of Dependents", 
            min_value=0, 
            max_value=10, 
            value=2,
            help="Total family members dependent on your income"
        )
        
        children_ages = st.multiselect(
            "Children Age Groups",
            ["0-5 years", "6-12 years", "13-18 years", "19-25 years (College)", "25+ years"],
            help="Age groups of dependent children"
        )
        
        spouse_working = st.selectbox(
            "Spouse Employment",
            ["Not applicable", "Not working", "Part-time working", "Full-time working"],
            help="Spouse's employment status"
        )
    
    with col4:
        elderly_parents = st.checkbox("Supporting Elderly Parents", help="Financial support for parents")
        
        special_needs = st.checkbox("Special Needs Family Member", help="Family member with special care needs")
        
        future_goals = st.multiselect(
            "Major Future Expenses",
            ["Children's Education", "Children's Marriage", "Home Purchase", "Retirement Planning", "Business Investment", "Medical Emergencies"],
            help="Major financial goals requiring planning"
        )

    # Financial Information
    st.markdown("""
    <div class="life-section">
        <h3>💼 Financial Information</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        annual_income = st.number_input(
            "Annual Income (₹)", 
            min_value=100000, 
            max_value=100000000, 
            value=1000000,
            help="Total annual income in Indian Rupees"
        )
        
        monthly_expenses = st.number_input(
            "Monthly Family Expenses (₹)", 
            min_value=10000, 
            max_value=1000000, 
            value=50000,
            help="Total monthly household expenses"
        )
        
        existing_investments = st.number_input(
            "Existing Investments/Savings (₹)", 
            min_value=0, 
            max_value=100000000, 
            value=500000,
            help="Current savings and investments"
        )
    
    with col6:
        loans_outstanding = st.number_input(
            "Outstanding Loans (₹)", 
            min_value=0, 
            max_value=50000000, 
            value=0,
            help="Total outstanding loan amount"
        )
        
        current_life_cover = st.number_input(
            "Existing Life Insurance Cover (₹)", 
            min_value=0, 
            max_value=100000000, 
            value=0,
            help="Current life insurance coverage amount"
        )
        
        desired_coverage = st.selectbox(
            "Desired Coverage Multiple",
            ["5x Annual Income", "10x Annual Income", "15x Annual Income", "20x Annual Income", "Custom Amount"],
            help="Desired life insurance coverage as income multiple"
        )

    # Health & Lifestyle
    st.markdown("""
    <div class="life-section">
        <h3>🏥 Health & Lifestyle</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col7, col8 = st.columns(2)
    
    with col7:
        occupation = st.selectbox(
            "Occupation Category", 
            ["IT Professional", "Doctor/Healthcare", "Teacher/Professor", "Engineer", "Business Owner", "Government Employee", "Sales/Marketing", "Finance Professional", "Manual Labor", "Other"],
            help="Primary occupation category"
        )
        
        occupation_risk = st.selectbox(
            "Occupation Risk Level", 
            ["Low Risk (Office job)", "Medium Risk (Field work)", "High Risk (Hazardous work)"],
            help="Risk level associated with occupation"
        )
        
        work_travel = st.selectbox(
            "Work-related Travel",
            ["Minimal travel", "Domestic travel", "International travel", "Frequent travel"],
            help="Frequency and extent of work travel"
        )
    
    with col8:
        lifestyle = st.selectbox(
            "Lifestyle Assessment", 
            ["Very Healthy", "Healthy", "Average", "Risky", "High Risk"],
            help="Overall lifestyle and health assessment"
        )
        
        health_conditions = st.multiselect(
            "Health Conditions",
            ["None", "Diabetes", "Hypertension", "Heart Disease", "Asthma", "High Cholesterol", "Other Chronic Conditions"],
            help="Existing health conditions"
        )
        
        medical_exams = st.checkbox("Willing to Take Medical Exams?", help="Consent for medical examinations for better rates")

    # Calculate recommended coverage
    if desired_coverage == "Custom Amount":
        coverage_amount = st.number_input(
            "Custom Coverage Amount (₹)", 
            min_value=500000, 
            max_value=100000000, 
            value=5000000,
            help="Enter custom coverage amount"
        )
    else:
        multiplier = int(desired_coverage.split('x')[0])
        coverage_amount = annual_income * multiplier

    # Needs Analysis
    st.markdown("""
    <div class="needs-analysis">
        <h4>📊 Insurance Needs Analysis</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate different financial needs
    immediate_expenses = monthly_expenses * 12  # 1 year expenses
    education_fund = len([age for age in children_ages if age in ["0-5 years", "6-12 years", "13-18 years"]]) * 1500000  # ₹15L per child
    loan_coverage = loans_outstanding
    future_income_replacement = monthly_expenses * 12 * 10  # 10 years income replacement
    
    total_needs = immediate_expenses + education_fund + loan_coverage + future_income_replacement
    insurance_gap = max(0, total_needs - current_life_cover - existing_investments)
    
    needs_col1, needs_col2, needs_col3 = st.columns(3)
    
    with needs_col1:
        st.metric("Immediate Expenses", f"₹{immediate_expenses:,.0f}", "1 year expenses")
        st.metric("Education Fund", f"₹{education_fund:,.0f}", f"{len(children_ages)} children")
    
    with needs_col2:
        st.metric("Loan Coverage", f"₹{loan_coverage:,.0f}", "Outstanding debt")
        st.metric("Income Replacement", f"₹{future_income_replacement:,.0f}", "10 years")
    
    with needs_col3:
        st.metric("Total Financial Need", f"₹{total_needs:,.0f}", "Comprehensive requirement")
        st.metric("Insurance Gap", f"₹{insurance_gap:,.0f}", "Additional coverage needed")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_submit = st.columns([1, 2, 1])
    with col_submit[1]:
        submitted = st.form_submit_button(
            "🔍 Calculate Life Insurance Premium", 
            use_container_width=True,
            type="primary"
        )

if submitted:
    # Enhanced risk calculation
    risk_score, recommendation, premium_estimate, mortality_rate = calculate_life_risk(
        age, 
        gender, 
        occupation_risk, 
        lifestyle, 
        coverage_amount, 
        medical_exams
    )
    
    # Advanced premium calculation
    base_premium = premium_estimate
    
    # Age and gender adjustments
    if gender == "Female":
        base_premium *= 0.9  # Lower risk for females
    
    # Occupation risk adjustment
    occupation_multiplier = {"Low Risk (Office job)": 1.0, "Medium Risk (Field work)": 1.2, "High Risk (Hazardous work)": 1.5}
    base_premium *= occupation_multiplier.get(occupation_risk, 1.0)
    
    # Health conditions adjustment
    health_risk_count = len([h for h in health_conditions if h != "None"])
    if health_risk_count > 0:
        base_premium *= (1 + health_risk_count * 0.2)
    
    # Medical exam discount
    if medical_exams:
        base_premium *= 0.9
    
    # Lifestyle adjustment
    lifestyle_multiplier = {"Very Healthy": 0.85, "Healthy": 0.95, "Average": 1.0, "Risky": 1.3, "High Risk": 1.6}
    base_premium *= lifestyle_multiplier.get(lifestyle, 1.0)
    
    final_premium = int(base_premium)
    
    # Display results
    st.success("🎯 Life Insurance Assessment Complete!", icon="✅")
    
    # Results dashboard
    st.markdown("### 📊 Life Insurance Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Risk Score",
            value=f"{risk_score}/10",
            delta=f"Mortality Rate: {mortality_rate}%"
        )
    
    with col2:
        st.metric(
            label="Annual Premium",
            value=f"₹{final_premium:,.0f}",
            delta=f"For ₹{coverage_amount:,.0f} cover"
        )
    
    with col3:
        premium_percentage = (final_premium / annual_income) * 100
        st.metric(
            label="Premium % of Income",
            value=f"{premium_percentage:.1f}%",
            delta="Affordability ratio"
        )
    
    with col4:
        approval_status = "Pre-Approved" if risk_score <= 6 else "Medical Review Required" if risk_score <= 8 else "Detailed Assessment"
        st.metric(
            label="Approval Status",
            value=approval_status,
            delta="Application status"
        )
    
    # Coverage adequacy analysis
    st.markdown("### 📋 Coverage Adequacy Analysis")
    
    adequacy_col1, adequacy_col2 = st.columns(2)
    
    with adequacy_col1:
        st.markdown("**💰 Financial Protection Analysis:**")
        
        protection_ratio = (coverage_amount + existing_investments) / total_needs
        
        if protection_ratio >= 1.0:
            st.success(f"✅ Adequate Protection: {protection_ratio:.1f}x coverage ratio")
        elif protection_ratio >= 0.7:
            st.warning(f"⚠️ Moderate Protection: {protection_ratio:.1f}x coverage ratio")
        else:
            st.error(f"❌ Inadequate Protection: {protection_ratio:.1f}x coverage ratio")
        
        st.write(f"• Total Coverage: ₹{coverage_amount + existing_investments:,.0f}")
        st.write(f"• Financial Needs: ₹{total_needs:,.0f}")
        st.write(f"• Protection Gap: ₹{max(0, total_needs - coverage_amount - existing_investments):,.0f}")
    
    with adequacy_col2:
        st.markdown("**🎯 Recommended Actions:**")
        
        if premium_percentage > 15:
            st.write("• Consider term insurance for higher coverage at lower cost")
        if insurance_gap > coverage_amount * 0.5:
            st.write("• Increase coverage amount to bridge protection gap")
        if len(future_goals) > 2:
            st.write("• Consider separate education/retirement plans")
        if not medical_exams:
            st.write("• Opt for medical exams to get better premium rates")
        if health_risk_count > 0:
            st.write("• Focus on health improvement for future renewals")
        
        st.write("• Review coverage annually as income grows")

    # Insurance recommendations based on profile
    st.markdown("### 💡 Personalized Insurance Recommendations")
    
    recommendations_list = []
    
    if age < 30:
        recommendations_list.append("Consider term insurance with return of premium option")
    elif age > 50:
        recommendations_list.append("Whole life insurance for guaranteed coverage")
    
    if dependents > 2:
        recommendations_list.append("High coverage term plan to protect large family")
    
    if annual_income > 2000000:
        recommendations_list.append("Consider ULIP for investment + insurance combination")
    
    if len(children_ages) > 0:
        recommendations_list.append("Child education plans for future educational expenses")
    
    if elderly_parents:
        recommendations_list.append("Consider senior citizen health + life plans for parents")
    
    recommendations_list.append("Annual review of coverage with income growth")
    recommendations_list.append("Consider inflation protection with increasing cover option")
    
    for i, rec in enumerate(recommendations_list, 1):
        st.info(f"**{i}.** {rec}", icon="💡")
    
    # Top life insurance providers
    st.markdown("### 🏢 Top Life Insurance Providers in India")
    
    insurers_data = [
        ["LIC of India", f"₹{final_premium*0.85:,.0f} - ₹{final_premium*1.0:,.0f}", "4.2⭐", "Market Leader", "Guaranteed Claims"],
        ["HDFC Life", f"₹{final_premium*0.9:,.0f} - ₹{final_premium*1.1:,.0f}", "4.5⭐", "Digital Excellence", "Quick Processing"],
        ["ICICI Prudential", f"₹{final_premium*0.95:,.0f} - ₹{final_premium*1.15:,.0f}", "4.4⭐", "Product Innovation", "Online Services"],
        ["SBI Life", f"₹{final_premium*0.88:,.0f} - ₹{final_premium*1.08:,.0f}", "4.3⭐", "Bank Backing", "Wide Reach"],
        ["Max Life", f"₹{final_premium*1.0:,.0f} - ₹{final_premium*1.2:,.0f}", "4.4⭐", "Customer Service", "Flexible Plans"],
        ["Bajaj Allianz Life", f"₹{final_premium*0.92:,.0f} - ₹{final_premium*1.12:,.0f}", "4.3⭐", "Comprehensive Cover", "Health Benefits"]
    ]
    
    df = pd.DataFrame(insurers_data, columns=["Insurance Provider", "Premium Range", "Rating", "Strength", "Key Feature"])
    st.dataframe(df, use_container_width=True)
    
    # Product recommendations
    st.markdown("### 📦 Recommended Product Types")
    
    product_col1, product_col2 = st.columns(2)
    
    with product_col1:
        st.markdown("""
        **🎯 Primary Recommendation**
        - **Term Life Insurance**: ₹{:,.0f} coverage
        - Annual Premium: ₹{:,.0f}
        - Coverage Period: {} years
        - Death Benefit: ₹{:,.0f}
        """.format(coverage_amount, final_premium, 65-age, coverage_amount))
    
    with product_col2:
        st.markdown("""
        **🔄 Additional Options**
        - **Whole Life**: Lifetime coverage
        - **ULIP**: Investment + Insurance
        - **Money Back**: Periodic returns
        - **Child Plans**: Education funding
        """)
    
    # Save to session state
    st.session_state["life_risk"] = {
        "age": age,
        "gender": gender,
        "occupation": occupation,
        "lifestyle": lifestyle,
        "coverage_amount": coverage_amount,
        "annual_income": annual_income,
        "dependents": dependents,
        "medical_exams": medical_exams,
        "risk_score": risk_score,
        "premium_estimate": final_premium,
        "mortality_rate": mortality_rate,
        "total_needs": total_needs,
        "insurance_gap": insurance_gap,
        "protection_ratio": protection_ratio
    }
