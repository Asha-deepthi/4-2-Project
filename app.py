import streamlit as st
import requests
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Glycemic Intelligence",
    page_icon="🍽️",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #2C3E50;
    }
    .sub-title {
        font-size: 18px;
        color: #5D6D7E;
    }
    .card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    .metric-box {
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        background-color: #F4F6F7;
    }
    .footer {
        text-align: center;
        color: gray;
        font-size: 12px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 AI Glycemic Intelligence")
st.sidebar.write("An AI-driven system for:")
st.sidebar.markdown("""
- 🍛 Food recognition  
- 📊 Glycemic Load estimation  
- 📈 Blood glucose forecasting  
- 💡 Personalized recommendations  
""")

st.sidebar.info(
    "📌 **Note:** This is a research prototype, not a medical device."
)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">🍽️ AI Glycemic Load & Glucose Prediction</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Upload a meal image to estimate glycemic load and predict post-meal blood glucose trends</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- MAIN LAYOUT ----------------
left_col, right_col = st.columns([1, 1])

# ---------------- LEFT: IMAGE UPLOAD ----------------
with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📷 Upload Meal Image")
    uploaded_image = st.file_uploader(
        "Choose an image of your meal",
        type=["jpg", "jpeg", "png"]
    )
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RIGHT: ANALYSIS BUTTON ----------------
with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔍 Analyze Meal")
    st.write(
        "The system will detect food items, calculate glycemic load, "
        "forecast blood glucose, and provide recommendations."
    )
    analyze = st.button("🚀 Start Analysis", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- MOCK RESPONSE (replace with backend later) ----------------
if uploaded_image and analyze:

    with st.spinner("Analyzing meal using AI models..."):
        response = {
            "foods": [
                {"name": "White Rice", "confidence": 0.92},
                {"name": "Dal", "confidence": 0.88}
            ],
            "gl": 38,
            "predicted_glucose": 185,
            "recommendation": "🚶 Walk for 15 minutes to reduce glucose spike"
        }

    # ---------------- RESULTS SECTION ----------------
    st.markdown("## 📋 Analysis Results")

    # -------- Detected Foods --------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🍛 Detected Food Items")
    for food in response["foods"]:
        st.write(
            f"✔ **{food['name']}** "
            f"({int(food['confidence']*100)}% confidence)"
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # -------- Metrics --------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("Glycemic Load (GL)", response["gl"])
        st.write("Impact of meal on blood sugar")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("Predicted Peak Glucose", f"{response['predicted_glucose']} mg/dL")
        st.write("Expected post-meal glucose peak")
        st.markdown('</div>', unsafe_allow_html=True)

    # -------- Glucose Graph --------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 Predicted Blood Glucose Trend")

    time = np.arange(0, 180, 15)
    glucose = 100 + np.sin(time / 60) * 40 + 45

    fig, ax = plt.subplots()
    ax.plot(time, glucose, linewidth=2)
    ax.axhline(180, linestyle="--", color="red", label="High Threshold")
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Glucose (mg/dL)")
    ax.legend()

    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

    # -------- Recommendation --------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💡 Personalized Recommendation")
    st.success(response["recommendation"])
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(
    '<div class="footer">⚠️ Research prototype for academic use only. Not a medical device.</div>',
    unsafe_allow_html=True
)
