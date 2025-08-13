import streamlit as st

st.set_page_config(page_title="Insurance Recommendations", page_icon="💡")
st.markdown("<h1 style='color:#27ae60;'>💡 Smart Insurance Recommendations</h1>", unsafe_allow_html=True)
st.markdown("<span style='color:#555;'>Get personalized insurance advice and suggestions for better coverage.</span>", unsafe_allow_html=True)

# Check if user has completed assessments
auto = st.session_state.get("auto_risk", {})
property_ = st.session_state.get("property_risk", {})
cyber = st.session_state.get("cyber_risk", {})
health = st.session_state.get("health_risk", {})
life = st.session_state.get("life_risk", {})

# Calculate total premium for use throughout the page
total_premium = (
    auto.get("premium_estimate", 0) +
    property_.get("premium_estimate", 0) +
    cyber.get("premium_estimate", 0) +
    health.get("premium_estimate", 0) +
    life.get("premium_estimate", 0)
)

st.markdown("## 🎯 Personalized Recommendations")

if any([auto, property_, cyber, health, life]):
    st.success("Based on your risk assessments, here are our recommendations:")
    
    # Auto Insurance Recommendations
    if auto:
        st.markdown("### 🚗 Auto Insurance Optimization")
        risk_score = auto.get("risk_score", 0)
        
        if risk_score <= 4:
            st.error("**High Risk Profile - Immediate Actions Needed:**")
            st.markdown("""
            **Top Priority Actions:**
            - Enroll in defensive driving course (₹5,000-15,000) → Save 10-15% on premium
            - Install GPS tracking system (₹8,000-20,000) → Save 5-10% on premium
            - Consider higher deductible (₹10,000 vs ₹5,000) → Save 15-25% on premium
            
            **Best Insurers for High-Risk Profiles:**
            1. **ICICI Lombard** - Flexible underwriting, good claim settlement
            2. **Bajaj Allianz** - Competitive rates for high-risk drivers
            3. **HDFC ERGO** - Comprehensive coverage options
            
            **Recommended Add-ons:**
            - Personal Accident Cover (₹200-500/year)
            - Zero Depreciation Cover (15-20% of premium)
            - Engine Protection Cover (₹1,500-3,000/year)
            """)
        
        elif risk_score <= 7:
            st.warning("**Moderate Risk - Room for Improvement:**")
            st.markdown("""
            **Optimization Strategies:**
            - Compare quotes from 4-5 insurers annually
            - Maintain claim-free record for NCB (up to 50% discount)
            - Bundle with home insurance for additional 5-10% discount
            
            **Recommended Insurers:**
            1. **TATA AIG** - Good customer service, fair pricing
            2. **New India Assurance** - Government backing, wide network
            3. **Oriental Insurance** - Competitive rates, reliable service
            
            **Cost-Effective Add-ons:**
            - Roadside Assistance (₹500-1,000/year)
            - Return to Invoice Cover (3-5% of premium)
            """)
        
        else:
            st.success("**Low Risk - Premium Rates Available:**")
            st.markdown("""
            **Premium Benefits You Qualify For:**
            - Maximum NCB discount (50% off base premium)
            - Preferred customer rates with most insurers
            - Online purchase discounts (additional 10-15% off)
            
            **Top Insurers for Low-Risk Drivers:**
            1. **IFFCO Tokio** - Excellent rates for safe drivers
            2. **SBI General** - Competitive pricing, good network
            3. **Reliance General** - Digital-first approach, quick settlements
            
            **Value-Added Features:**
            - Lifetime renewability guarantee
            - Worldwide coverage for international travel
            - Vintage car coverage options
            """)
    
    # Health Insurance Recommendations
    if health:
        st.markdown("### 🏥 Health Insurance Strategy")
        risk_score = health.get("risk_score", 0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Government Schemes to Consider:**")
            st.markdown("""
            - **Ayushman Bharat** - Up to ₹5 lakh coverage (for eligible families)
            - **ESIC Medical Coverage** - For salaried employees
            - **CGHS** - For central government employees
            - **State Health Schemes** - Check your state's offerings
            """)
        
        with col2:
            st.markdown("**Private Insurance Recommendations:**")
            if risk_score <= 4:
                st.markdown("""
                **High-Risk Health Profile:**
                - **Star Health** - Specializes in health insurance
                - **Max Bupa** - Good coverage for pre-existing conditions
                - **Apollo Munich** - Comprehensive health solutions
                
                **Essential Features:**
                - Pre-existing disease cover (after waiting period)
                - Critical illness rider (₹500-2,000/year)
                - Maternity benefits (if applicable)
                """)
            else:
                st.markdown("""
                **Good Health Profile:**
                - **HDFC ERGO** - Wellness benefits and rewards
                - **ICICI Lombard** - Comprehensive coverage options
                - **Bajaj Allianz** - Good claim settlement ratio
                
                **Value-Added Benefits:**
                - Annual health checkups (covered)
                - Wellness program discounts
                - Alternative treatment coverage
                """)
    
    # Display summary recommendations
    st.markdown("## 📊 Overall Insurance Portfolio Strategy")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Annual Premium", f"₹{total_premium:,}")
    
    with col2:
        potential_savings = int(total_premium * 0.15)  # Assume 15% potential savings
        st.metric("Potential Annual Savings", f"₹{potential_savings:,}")
    
    with col3:
        coverage_types = len([x for x in [auto, property_, cyber, health, life] if x])
        st.metric("Coverage Types", f"{coverage_types}/5")

else:
    st.info("Complete risk assessments to receive personalized insurance recommendations.")
    st.markdown("### 🎯 General Insurance Guidance")

# General recommendations for all users
st.markdown("## 🔍 How to Get Better Insurance")

tab1, tab2, tab3, tab4 = st.tabs(["💰 Save Money", "📋 Better Coverage", "🏆 Top Insurers", "📱 Digital Tools"])

with tab1:
    st.markdown("""
    ### Money-Saving Strategies
    
    **1. Compare and Switch Annually**
    - Use comparison websites: PolicyBazaar, Coverfox, InsuranceDekho
    - Save 20-30% by switching to competitive insurers
    - Check for online purchase discounts (10-15% additional savings)
    
    **2. Bundle Insurance Policies**
    - Combine auto + home insurance: Save 5-10%
    - Family health insurance vs individual: Save 15-25%
    - Life + health insurance combos: Additional benefits
    
    **3. Maintain Good Records**
    - No-claim bonus (NCB): Up to 50% discount on auto insurance
    - Claim-free health insurance: Premium discounts and loyalty benefits
    - Good credit score: Better rates on life insurance
    
    **4. Choose Higher Deductibles**
    - Auto insurance: ₹10,000 vs ₹5,000 deductible → Save 15-25%
    - Health insurance: ₹25,000 vs ₹10,000 deductible → Save 20-30%
    
    **5. Utilize Tax Benefits**
    - Health insurance premiums: Deduction up to ₹25,000-₹50,000 under 80D
    - Life insurance premiums: Deduction up to ₹1.5 lakh under 80C
    - Calculate tax-adjusted cost for true premium comparison
    """)

with tab2:
    st.markdown("""
    ### Getting Better Coverage
    
    **1. Essential Add-ons Worth Buying**
    
    **Auto Insurance:**
    - Zero Depreciation Cover (for cars less than 5 years old)
    - Engine Protection Cover (especially in flood-prone areas)
    - Personal Accident Cover for driver/passengers
    - Return to Invoice Cover (for expensive cars)
    
    **Health Insurance:**
    - Critical illness rider (₹500-2,000/year for ₹10 lakh cover)
    - Personal accident cover (₹200-500/year)
    - OPD coverage (for regular medical expenses)
    - Maternity coverage (if planning family)
    
    **Life Insurance:**
    - Accidental death benefit (doubles the sum assured)
    - Premium waiver on disability
    - Critical illness rider
    - Term insurance with return of premium (if budget allows)
    
    **2. Coverage Amount Guidelines**
    - Health Insurance: 10-15x your annual income
    - Life Insurance: 15-20x your annual income
    - Auto Insurance: Full IDV (Insured Declared Value)
    - Property Insurance: Current replacement cost, not purchase price
    """)

with tab3:
    st.markdown("""
    ### Top Insurance Companies in India
    
    **🏆 Best Overall Performers (Based on Claim Settlement Ratio & Customer Satisfaction)**
    
    **Life Insurance:**
    1. **LIC** - 98.74% claim settlement ratio, largest network
    2. **HDFC Life** - 98.66%, excellent digital services
    3. **SBI Life** - 97.50%, good for traditional products
    4. **ICICI Prudential** - 98.30%, innovative products
    5. **Max Life** - 99.34%, highest claim settlement ratio
    
    **Health Insurance:**
    1. **Star Health** - Specialized health insurer, 94.1% settlement ratio
    2. **HDFC ERGO** - 92.8%, comprehensive wellness programs
    3. **ICICI Lombard** - 89.6%, good digital interface
    4. **Bajaj Allianz** - 86.4%, wide hospital network
    5. **New India Assurance** - Government backing, reliable
    
    **Auto Insurance:**
    1. **IFFCO Tokio** - 97.2% claim settlement, competitive rates
    2. **SBI General** - 95.8%, extensive network
    3. **HDFC ERGO** - 94.5%, quick claim processing
    4. **ICICI Lombard** - 93.2%, good customer service
    5. **Bajaj Allianz** - 91.8%, comprehensive coverage options
    
    **Property/Home Insurance:**
    1. **HDFC ERGO** - Comprehensive home insurance solutions
    2. **ICICI Lombard** - Good coverage options, competitive pricing
    3. **Bajaj Allianz** - Flexible policy terms
    4. **TATA AIG** - Excellent customer service
    5. **New India Assurance** - Traditional, reliable coverage
    """)

with tab4:
    st.markdown("""
    ### Digital Tools & Resources
    
    **📱 Essential Apps & Websites**
    
    **Comparison Platforms:**
    - **PolicyBazaar** - Comprehensive comparison across all insurance types
    - **Coverfox** - Good for health and motor insurance
    - **InsuranceDekho** - User-friendly interface, good customer support
    - **Paisa Policy** - Emerging platform with competitive rates
    
    **Insurer Apps:**
    - **HDFC ERGO Mobile App** - Claim filing, policy management
    - **ICICI Lombard iLombarD** - Digital claims, quick settlements
    - **Bajaj Allianz Caringly Yours** - Health insurance management
    - **SBI General** - Comprehensive policy services
    
    **Government Resources:**
    - **IRDAI Website** (irdai.gov.in) - Verify insurer credentials, file complaints
    - **Insurance Ombudsman** - Complaint resolution
    - **Ayushman Bharat Portal** - Check eligibility for government health scheme
    
    **Financial Tools:**
    - **Term Insurance Calculator** - Determine adequate life coverage
    - **Health Insurance Calculator** - Assess required health coverage
    - **EMI Calculator** - Plan insurance premium payments
    - **Tax Calculator** - Optimize insurance for tax benefits
    
    **Tips for Using Digital Platforms:**
    1. Always verify information on official insurer websites
    2. Read policy documents carefully before purchasing
    3. Keep digital copies of all insurance documents
    4. Use mobile apps for quick claim reporting and tracking
    5. Set premium payment reminders to avoid policy lapse
    """)

# Action items section
st.markdown("## ✅ Next Steps")

action_items = []
if not auto and not property_ and not cyber and not health and not life:
    action_items.append("Complete risk assessments for personalized recommendations")

if total_premium > 0:
    action_items.extend([
        f"Review current premiums (Total: ₹{total_premium:,}) for optimization opportunities",
        "Compare quotes from at least 3 insurers before renewal",
        "Consider bundling policies for additional discounts"
    ])

action_items.extend([
    "Set annual insurance review calendar reminder",
    "Organize all insurance documents digitally",
    "Verify all nominee details are up to date",
    "Check for any unclaimed insurance benefits"
])

for i, item in enumerate(action_items, 1):
    st.markdown(f"{i}. {item}")

# Contact information
st.markdown("---")
st.markdown("""
### 📞 Need Help?

**Insurance Advisory Services:**
- **IRDAI Helpline**: 155255 (Toll-free)
- **Consumer Helpline**: 1800-11-4000
- **Insurance Ombudsman**: For complaint resolution

**Disclaimer**: These recommendations are based on general risk assessment algorithms and market research. 
Please consult with qualified insurance advisors for personalized advice and verify all information with respective insurers before making decisions.
""")
