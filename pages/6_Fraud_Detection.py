import streamlit as st
from utils.fraud_detector import detect_fraud

st.set_page_config(page_title="Fraud Detection", page_icon="🕵️")
st.markdown("<h1 style='color:#d35400;'>🕵️ Fraud Detection System</h1>", unsafe_allow_html=True)

st.markdown("Enter claim details for fraud analysis.")
st.markdown("<span style='color:#555;'>Enter claim details for fraud analysis. All fields are required.</span>", unsafe_allow_html=True)

with st.form("fraud_form"):
    claim_amount = st.number_input("Claim Amount ($)", min_value=0, value=1000)
    claim_amount = st.number_input("Claim Amount (₹)", min_value=0, value=50000, help="Total claim amount in Indian Rupees.")
    claim_type = st.selectbox("Claim Type", ["Auto", "Property", "Cyber"])
    claim_type = st.selectbox("Claim Type", ["Auto", "Property", "Cyber"], help="Type of insurance claim.")
    suspicious_docs = st.checkbox("Suspicious Documents?")
    suspicious_docs = st.checkbox("Suspicious Documents?", help="Are any documents flagged as suspicious?")
    prior_fraud = st.checkbox("Prior Fraud History?")
    prior_fraud = st.checkbox("Prior Fraud History?", help="Has the claimant been involved in fraud before?")
    submitted = st.form_submit_button("Analyze Fraud Risk")

if submitted:
    errors = []
    if claim_amount < 0:
        errors.append("Claim amount cannot be negative.")
    if errors:
        for e in errors:
            st.error(e)
    else:
        fraud_score, alerts = detect_fraud(claim_amount, claim_type, suspicious_docs, prior_fraud)
        st.metric("Fraud Score", f"{fraud_score}/10")
        st.warning(alerts)
        st.session_state["fraud_detection"] = {
            "claim_amount": claim_amount,
            "claim_type": claim_type,
            "suspicious_docs": suspicious_docs,
            "prior_fraud": prior_fraud,
            "fraud_score": fraud_score,
            "alerts": alerts
        }
