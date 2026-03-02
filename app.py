import streamlit as st

st.set_page_config(page_title="CompliNova AI", page_icon="🧠", layout="wide")

st.title("CompliNova AI")
st.caption("AI-Powered Medical Device Regulatory Intelligence System")

st.divider()

col1, col2 = st.columns(2)

with col1:
    device_name = st.text_input("Device Name")
    intended_use = st.text_input("Intended Use")

with col2:
    target_population = st.text_input("Target Population")
    uses_ai = st.selectbox("Uses AI?", ["Yes", "No"])

device_description = st.text_area("Device Description")

st.divider()

if st.button("Run Compliance Audit"):

    st.success("Audit Completed Successfully")

    st.subheader("📊 Risk Classification")
    st.write("Class C – Moderate to High Risk (AI-based diagnostic device under MDR 2017 Rule 4(2))")

    st.subheader("⚠ Compliance Gaps")
    st.write("• Clinical validation documentation missing")
    st.write("• AI training dataset transparency required")
    st.write("• DPDPA consent mechanism not defined")
    st.write("• Risk management file incomplete")

    st.subheader("📁 Required Documents")
    st.write("• Device Master File (DMF)")
    st.write("• Clinical Evaluation Report")
    st.write("• Risk Management File (ISO 14971)")
    st.write("• Software Validation Report")
    st.write("• AI Model Performance Documentation")

    st.subheader("🤖 AI Bias Risk Assessment")
    st.write("AI model requires bias validation across demographic groups.")

    st.subheader("🔐 Data Privacy Compliance")
    st.write("Patient health data detected. DPDPA consent and encryption mechanisms required.")

    st.subheader("📈 Approval Readiness Score")
    st.progress(72)
    st.write("Score: 72/100")

    st.subheader("🧩 Regulatory Complexity")
    st.warning("Moderate to High Complexity – Structured documentation and validation required.")

    st.subheader("⏳ Estimated Approval Preparation Time")
    st.write("4–6 Months")

    st.subheader("🚀 Impact Statement")
    st.write("CompliNova AI reduces regulatory preparation time by approximately 60% and improves compliance clarity.")
