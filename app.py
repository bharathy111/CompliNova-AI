import streamlit as st
import ollama
import json
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="CompliNova AI", page_icon="🧠", layout="wide")

# ---------- UI Styling ----------
st.markdown("""
<style>
.big-title {
    font-size:42px !important;
    font-weight:800;
    color:#3B82F6;
}
.subtitle {
    font-size:16px;
    color:#94A3B8;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">CompliNova AI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Medical Device Regulatory Intelligence System</p>', unsafe_allow_html=True)
st.divider()

# ---------- User Inputs ----------
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

    with st.spinner("Analyzing regulatory compliance..."):

        prompt = f"""
You are CompliNova AI, an expert Indian Medical Device Regulatory Intelligence System.

Analyze this device:

Device Name: {device_name}
Intended Use: {intended_use}
Target Population: {target_population}
Uses AI: {uses_ai}
Device Description: {device_description}

Perform:
1. Risk Classification (Class A/B/C/D)
2. Relevant CDSCO clauses
3. Compliance gaps
4. Required documents
5. Clinical validation requirement
6. AI bias risk (if AI used)
7. Data privacy compliance (DPDPA)
8. Estimated approval preparation time (months)
9. Approval readiness score (40-95)
10. Regulatory complexity index (Low/Moderate/High)
11. Rural deployment suitability score (0-100)
12. Model confidence score (60-95)
13. Executive summary
14. Impact statement

Return STRICTLY valid JSON in this format:

{{
  "Executive_Summary": "",
  "Risk_Classification": {{
    "Class": "",
    "Justification": "",
    "Relevant_CDSCO_Clauses": []
  }},
  "Compliance_Gaps": [],
  "Required_Documents": [],
  "Clinical_Validation_Required": "",
  "AI_Bias_Risk_Assessment": "",
  "Data_Privacy_Compliance": "",
  "Estimated_Approval_Preparation_Time_Months": "",
  "Approval_Readiness_Score": "",
  "Regulatory_Complexity_Index": "",
  "Rural_Deployment_Suitability_Score": "",
  "Model_Confidence_Score": "",
  "Impact_Statement": ""
}}

Return ONLY JSON. No explanations. No markdown.
"""

        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": "You are a CDSCO regulatory expert."},
                {"role": "user", "content": prompt}
            ],
            options={"temperature": 0.1}
        )

        output = response["message"]["content"]

    # --------- Safe JSON Extraction ----------
    json_match = re.search(r"\{.*\}", output, re.DOTALL)

    if json_match:
        clean_json = json_match.group(0)
        try:
            data = json.loads(clean_json)
        except:
            st.error("Model returned malformed JSON. Try again.")
            st.stop()
    else:
        st.error("Model did not return valid JSON. Try again.")
        st.stop()

    st.success("Audit Completed Successfully")

    # ---------- Executive Summary ----------
    st.subheader("📌 Executive Summary")
    st.write(data["Executive_Summary"])

    # ---------- Risk ----------
    st.subheader("📊 Risk Classification")
    st.write("Class:", data["Risk_Classification"]["Class"])
    st.write(data["Risk_Classification"]["Justification"])
    st.write("Relevant Clauses:", ", ".join(data["Risk_Classification"]["Relevant_CDSCO_Clauses"]))

    # ---------- Compliance Gaps ----------
    st.subheader("⚠ Compliance Gaps")
    for gap in data["Compliance_Gaps"]:
        st.write("•", gap)

    # ---------- Documents ----------
    st.subheader("📁 Required Documents")
    for doc in data["Required_Documents"]:
        st.write("•", doc)

    # ---------- Clinical ----------
    st.subheader("🧪 Clinical Validation")
    st.write(data["Clinical_Validation_Required"])

    # ---------- AI Bias ----------
    st.subheader("🤖 AI Bias Risk")
    st.write(data["AI_Bias_Risk_Assessment"])

    # ---------- Privacy ----------
    st.subheader("🔐 Data Privacy Compliance")
    st.write(data["Data_Privacy_Compliance"])

    # ---------- Metrics ----------
    st.subheader("📈 Regulatory Metrics")

    colA, colB, colC = st.columns(3)

    readiness = int(data["Approval_Readiness_Score"])
    rural = int(data["Rural_Deployment_Suitability_Score"])
    confidence = int(data["Model_Confidence_Score"])

    with colA:
        st.metric("Approval Readiness", f"{readiness}/100")
        st.progress(readiness)

    with colB:
        st.metric("Rural Suitability", f"{rural}/100")
        st.progress(rural)

    with colC:
        st.metric("Model Confidence", f"{confidence}/100")
        st.progress(confidence)

    # ---------- Complexity ----------
    st.subheader("🧩 Regulatory Complexity")
    complexity = data["Regulatory_Complexity_Index"]

    if complexity == "High":
        st.error("High Complexity – Extensive Clinical Trials Required")
    elif complexity == "Moderate":
        st.warning("Moderate Complexity – Structured Compliance Needed")
    else:
        st.success("Low Complexity – Streamlined Path")

    # ---------- Time ----------
    st.subheader("⏳ Estimated Approval Preparation Time")
    st.write(data["Estimated_Approval_Preparation_Time_Months"], "Months")

    # ---------- Impact ----------
    st.subheader("🚀 Impact Statement")
    st.write(data["Impact_Statement"])

    # ---------- PDF Export ----------
    if st.button("Download Audit Report as PDF"):
        doc = SimpleDocTemplate("CompliNova_Report.pdf")
        styles = getSampleStyleSheet()
        elements = []

        for key, value in data.items():
            elements.append(Paragraph(f"<b>{key}</b>", styles["Heading2"]))
            elements.append(Spacer(1, 12))
            elements.append(Paragraph(str(value), styles["Normal"]))
            elements.append(Spacer(1, 24))

        doc.build(elements)

        with open("CompliNova_Report.pdf", "rb") as f:
            st.download_button("Click to Download PDF", f, file_name="CompliNova_Report.pdf")