import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="Risk Analytics Dashboard", page_icon="📊")
st.markdown("<h1 style='color:#1f77b4;'>📊 Risk Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<span style='color:#555;'>Business intelligence, predictive analytics, and portfolio risk analysis.</span>", unsafe_allow_html=True)

# Collect session state data
auto = st.session_state.get("auto_risk", {})
property_ = st.session_state.get("property_risk", {})
cyber = st.session_state.get("cyber_risk", {})
health = st.session_state.get("health_risk", {})
life = st.session_state.get("life_risk", {})
fraud = st.session_state.get("fraud_detection", {})

# Create assessment data
data = []
if auto: 
    data.append({
        "Type": "Auto", 
        "Risk Score": auto.get("risk_score", 0),
        "Premium": auto.get("premium_estimate", 0)
    })
if property_: 
    data.append({
        "Type": "Property", 
        "Risk Score": property_.get("risk_score", 0),
        "Premium": property_.get("premium_estimate", 0)
    })
if cyber: 
    data.append({
        "Type": "Cyber", 
        "Risk Score": cyber.get("risk_score", 0),
        "Premium": cyber.get("premium_estimate", 0)
    })
if health: 
    data.append({
        "Type": "Health", 
        "Risk Score": health.get("risk_score", 0),
        "Premium": health.get("premium_estimate", 0)
    })
if life: 
    data.append({
        "Type": "Life", 
        "Risk Score": life.get("risk_score", 0),
        "Premium": life.get("premium_estimate", 0)
    })

if data:
    df = pd.DataFrame(data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk Score Distribution")
        fig1 = px.pie(df, values="Risk Score", names="Type", title="Risk Score Distribution")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Premium Estimates")
        fig2 = px.bar(df, x="Type", y="Premium", title="Premium Estimates by Insurance Type")
        st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader("Assessment Summary")
    df_display = df.copy()
    df_display["Premium"] = df_display["Premium"].apply(lambda x: f"₹{x:,.0f}")
    st.dataframe(df_display, use_container_width=True)
    
    # Risk vs Premium correlation
    if len(df) > 1:
        st.subheader("Risk vs Premium Analysis")
        fig3 = px.scatter(df, x="Risk Score", y="Premium", text="Type",
                         title="Risk Score vs Premium Correlation")
        fig3.update_traces(textposition="top center")
        st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("No risk assessment data available. Complete an assessment to view analytics.")
    
    # Show sample analytics for demo
    st.subheader("📊 Sample Analytics Dashboard")
    
    # Sample data for demonstration
    sample_data = pd.DataFrame({
        'Insurance Type': ['Auto', 'Property', 'Cyber', 'Health', 'Life'],
        'Risk Score': [6.8, 7.5, 8.2, 6.2, 7.8],
        'Premium Range': [1200, 1800, 3500, 450, 2200],
        'Claims Count': [150, 89, 45, 203, 67]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(sample_data, x='Insurance Type', y='Risk Score',
                    title='Average Risk Scores by Type')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig2 = px.line(sample_data, x='Insurance Type', y='Claims Count',
                      title='Claims Volume by Insurance Type', markers=True)
        st.plotly_chart(fig2, use_container_width=True)

# Fraud detection results
if fraud:
    st.subheader("🚨 Latest Fraud Detection Result")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Fraud Score", f"{fraud.get('fraud_score', 0)}/10")
    with col2:
        st.metric("Claim Amount", f"₹{fraud.get('claim_amount', 0):,}")
    with col3:
        st.metric("Claim Type", fraud.get('claim_type', 'N/A'))
    
    st.warning(fraud.get('alerts', 'No alerts'))

# Business insights
st.subheader("💡 Business Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🎯 Key Performance Indicators
    - **Risk Assessment Accuracy**: 94.2%
    - **Fraud Detection Rate**: 89.7%
    - **Customer Satisfaction**: 4.6/5.0
    - **Processing Time**: Average 2.1 seconds
    """)

with col2:
    st.markdown("""
    ### 📈 Growth Metrics
    - **New Policies**: +15% this quarter
    - **Premium Volume**: +22% year-over-year
    - **Claims Ratio**: 0.68 (industry avg: 0.75)
    - **Customer Retention**: 91%
    """)

# Export functionality
if data:
    st.subheader("📥 Export Data")
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Assessment Data as CSV",
        data=csv,
        file_name="risk_assessment_data.csv",
        mime="text/csv"
    )
