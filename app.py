"""
RiskShieldAI™ Insurance Risk & Fraud Assessment Platform
Main Application Entry Point
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
import numpy as np

# Configure page settings
st.set_page_config(
    page_title="RiskShieldAI™ Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function"""
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">🛡️ RiskShieldAI™</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #7f8c8d;">Insurance Risk & Fraud Assessment Platform</h2>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.markdown("## 📊 Navigation")
    st.sidebar.markdown("---")
    
    # Platform overview
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🚗 Auto Insurance</h3>
            <p>Vehicle and driver risk assessment with real-time analytics</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🏠 Property Insurance</h3>
            <p>Property risk evaluation including environmental factors</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🔒 Cyber Insurance</h3>
            <p>Digital risk assessment and cybersecurity posture analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🏥 Health Insurance</h3>
            <p>Health risk profiling and wellness assessment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="metric-card">
            <h3>👨‍👩‍👧‍👦 Life Insurance</h3>
            <p>Mortality risk assessment and coverage planning</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Platform features
    st.markdown("## 🔧 Platform Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🔍 Risk Assessment
        - **Multi-Type Coverage**: Auto, Property, and Cyber insurance
        - **Real-Time Analysis**: Instant risk scoring and recommendations
        - **Advanced Analytics**: Machine learning-powered insights
        - **Customizable Parameters**: Flexible assessment criteria
        """)
        
        st.markdown("""
        ### 🤖 AI-Powered Fraud Detection
        - **Pattern Recognition**: Advanced anomaly detection
        - **Real-Time Monitoring**: Continuous fraud surveillance
        - **Predictive Modeling**: ML-based fraud prediction
        - **Alert Management**: Automated risk notifications
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Risk Analytics Dashboard
        - **Business Intelligence**: Comprehensive reporting
        - **Predictive Analytics**: Forecasting and trends
        - **Portfolio Analysis**: Risk distribution insights
        - **Performance Metrics**: KPI tracking and monitoring
        """)
        
        st.markdown("""
        ### 📄 SmartAuditAI™ Document Intelligence
        - **Automated Processing**: OCR and NLP capabilities
        - **Document Verification**: Authenticity checking
        - **Content Analysis**: Intelligent text extraction
        - **Fraud Detection**: Document-based risk assessment
        """)
    
    # Real dashboard metrics based on actual assessments
    st.markdown("## 📈 Platform Overview")
    
    # Get real data from session state
    auto_data = st.session_state.get("auto_risk", {})
    property_data = st.session_state.get("property_risk", {})
    cyber_data = st.session_state.get("cyber_risk", {})
    health_data = st.session_state.get("health_risk", {})
    life_data = st.session_state.get("life_risk", {})
    
    # Count completed assessments
    assessments = [auto_data, property_data, cyber_data, health_data, life_data]
    completed_assessments = len([a for a in assessments if a])
    
    # Calculate average risk score from completed assessments
    risk_scores = []
    total_premiums = 0
    fraud_indicators = 0
    
    for assessment in assessments:
        if assessment and 'risk_score' in assessment:
            risk_scores.append(assessment['risk_score'])
        if assessment and 'premium_estimate' in assessment:
            total_premiums += assessment['premium_estimate']
    
    avg_risk_score = sum(risk_scores) / len(risk_scores) if risk_scores else 0
    
    # Check for potential fraud indicators
    if auto_data and auto_data.get('accident_history', 0) > 2:
        fraud_indicators += 1
    if cyber_data and cyber_data.get('past_incidents', 0) > 3:
        fraud_indicators += 1
    if health_data and len(health_data.get('chronic_conditions', [])) > 3:
        fraud_indicators += 1
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Completed Assessments",
            value=str(completed_assessments),
            delta=f"out of 5 types"
        )
    
    with col2:
        st.metric(
            label="Fraud Indicators",
            value=str(fraud_indicators),
            delta="Risk factors detected" if fraud_indicators > 0 else "Clean profile"
        )
    
    with col3:
        if avg_risk_score > 0:
            st.metric(
                label="Average Risk Score",
                value=f"{avg_risk_score:.1f}/10",
                delta="Your profile"
            )
        else:
            st.metric(
                label="Risk Score",
                value="Not calculated",
                delta="Complete assessments"
            )
    
    with col4:
        if total_premiums > 0:
            st.metric(
                label="Total Annual Premium",
                value=f"₹{total_premiums:,.0f}",
                delta="All policies"
            )
        else:
            st.metric(
                label="Premium Estimate",
                value="Not available",
                delta="Complete assessments"
            )
    
    with col5:
        completion_rate = (completed_assessments / 5) * 100
        st.metric(
            label="Profile Completion",
            value=f"{completion_rate:.0f}%",
            delta=f"{5-completed_assessments} remaining"
        )
    
    # Real charts based on user data
    col1, col2 = st.columns(2)
    
    with col1:
        if completed_assessments > 0:
            # Risk distribution chart with real data
            insurance_types = []
            user_risk_scores = []
            
            if auto_data and 'risk_score' in auto_data:
                insurance_types.append('Auto')
                user_risk_scores.append(auto_data['risk_score'])
            
            if property_data and 'risk_score' in property_data:
                insurance_types.append('Property')
                user_risk_scores.append(property_data['risk_score'])
            
            if cyber_data and 'risk_score' in cyber_data:
                insurance_types.append('Cyber')
                user_risk_scores.append(cyber_data['risk_score'])
            
            if health_data and 'risk_score' in health_data:
                insurance_types.append('Health')
                user_risk_scores.append(health_data['risk_score'])
            
            if life_data and 'risk_score' in life_data:
                insurance_types.append('Life')
                user_risk_scores.append(life_data['risk_score'])
            
            if insurance_types:
                risk_data = pd.DataFrame({
                    'Insurance Type': insurance_types,
                    'Your Risk Score': user_risk_scores
                })
                
                fig = px.bar(risk_data, x='Insurance Type', y='Your Risk Score', 
                            title='Your Risk Score by Insurance Type',
                            color='Your Risk Score', 
                            color_continuous_scale='RdYlGn_r',
                            range_y=[0, 10])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Complete risk assessments to see your personalized risk analysis chart")
        else:
            st.info("📊 Complete insurance assessments to see your personalized dashboard")
    
    with col2:
        if completed_assessments > 0:
            # Premium comparison chart
            insurance_types = []
            premiums = []
            
            if auto_data and 'premium_estimate' in auto_data:
                insurance_types.append('Auto')
                premiums.append(auto_data['premium_estimate'])
            
            if property_data and 'premium_estimate' in property_data:
                insurance_types.append('Property')
                premiums.append(property_data['premium_estimate'])
            
            if cyber_data and 'premium_estimate' in cyber_data:
                insurance_types.append('Cyber')
                premiums.append(cyber_data['premium_estimate'])
            
            if health_data and 'premium_estimate' in health_data:
                insurance_types.append('Health')
                premiums.append(health_data['premium_estimate'] * 12)  # Convert monthly to annual
            
            if life_data and 'premium_estimate' in life_data:
                insurance_types.append('Life')
                premiums.append(life_data['premium_estimate'])
            
            if insurance_types:
                premium_data = pd.DataFrame({
                    'Insurance Type': insurance_types,
                    'Annual Premium (₹)': premiums
                })
                
                fig = px.pie(premium_data, values='Annual Premium (₹)', names='Insurance Type',
                            title='Your Premium Distribution by Insurance Type')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Complete assessments to see your premium breakdown")
        else:
            st.info("💰 Complete insurance assessments to see your premium analysis")
    
    # Assessment status section
    if completed_assessments > 0:
        st.markdown("## 📋 Assessment Status")
        
        status_col1, status_col2 = st.columns(2)
        
        with status_col1:
            st.markdown("### ✅ Completed Assessments")
            if auto_data:
                risk_level = "High" if auto_data.get('risk_score', 0) <= 4 else "Medium" if auto_data.get('risk_score', 0) <= 7 else "Low"
                st.success(f"🚗 Auto Insurance - Risk: {risk_level} - Premium: ₹{auto_data.get('premium_estimate', 0):,.0f}")
            
            if property_data:
                risk_level = "High" if property_data.get('risk_score', 0) <= 4 else "Medium" if property_data.get('risk_score', 0) <= 7 else "Low"
                st.success(f"🏠 Property Insurance - Risk: {risk_level} - Premium: ₹{property_data.get('premium_estimate', 0):,.0f}")
            
            if cyber_data:
                risk_level = "High" if cyber_data.get('risk_score', 0) <= 4 else "Medium" if cyber_data.get('risk_score', 0) <= 7 else "Low"
                st.success(f"🔒 Cyber Insurance - Risk: {risk_level} - Premium: ₹{cyber_data.get('premium_estimate', 0):,.0f}")
            
            if health_data:
                risk_level = "High" if health_data.get('risk_score', 0) >= 7 else "Medium" if health_data.get('risk_score', 0) >= 4 else "Low"
                st.success(f"🏥 Health Insurance - Risk: {risk_level} - Premium: ₹{health_data.get('premium_estimate', 0)*12:,.0f}/year")
            
            if life_data:
                risk_level = "High" if life_data.get('risk_score', 0) >= 7 else "Medium" if life_data.get('risk_score', 0) >= 4 else "Low"
                st.success(f"👨‍👩‍👧‍👦 Life Insurance - Risk: {risk_level} - Premium: ₹{life_data.get('premium_estimate', 0):,.0f}")
        
        with status_col2:
            st.markdown("### ⏳ Pending Assessments")
            remaining = []
            if not auto_data:
                remaining.append("🚗 Auto Insurance")
            if not property_data:
                remaining.append("🏠 Property Insurance")
            if not cyber_data:
                remaining.append("🔒 Cyber Insurance")
            if not health_data:
                remaining.append("🏥 Health Insurance")
            if not life_data:
                remaining.append("👨‍👩‍👧‍👦 Life Insurance")
            
            if remaining:
                for item in remaining:
                    st.warning(f"{item} - Not completed")
            else:
                st.success("🎉 All assessments completed!")
    
    # Getting started section
    st.markdown("## 🚀 Getting Started")
    
    st.markdown("""
    Welcome to RiskShieldAI™! Here's how to get started:
    
    1. **Select an Assessment Type**: Choose from Auto, Property, or Cyber Insurance in the sidebar
    2. **Input Assessment Data**: Fill in the required information for risk analysis
    3. **Review Risk Scores**: Get instant risk assessments and recommendations
    4. **Analyze Results**: Use our analytics dashboard for deeper insights
    5. **Document Processing**: Upload documents for AI-powered verification
    
    ### 📋 Quick Actions
    """)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🚗 Auto Assessment", use_container_width=True):
            st.switch_page("pages/1_Auto_Insurance.py")
    
    with col2:
        if st.button("🏠 Property Assessment", use_container_width=True):
            st.switch_page("pages/2_Property_Insurance.py")
    
    with col3:
        if st.button("🔒 Cyber Assessment", use_container_width=True):
            st.switch_page("pages/3_Cyber_Insurance.py")
    
    with col4:
        if st.button("🏥 Health Assessment", use_container_width=True):
            st.switch_page("pages/4_Health_Insurance.py")
    
    with col5:
        if st.button("👨‍👩‍👧‍👦 Life Assessment", use_container_width=True):
            st.switch_page("pages/5_Life_Insurance.py")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d;">
        <p>RiskShieldAI™ Platform | Powered by Advanced AI & Machine Learning</p>
        <p>© 2024 RiskShieldAI™. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
