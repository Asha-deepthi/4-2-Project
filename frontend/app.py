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
st.sidebar.markdown("""
- 🍛 Food recognition  
- 📊 Glycemic Load estimation  
- 📈 Post-meal glucose prediction  
- 💡 Personalized recommendations  
""")

st.sidebar.info(
    "📌 **Research prototype** – not a medical device."
)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">🍽️ AI Glycemic Load & Post-Meal Glucose Prediction</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Upload a meal image and enter recent glucose values to predict post-meal glucose trends</div>',
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
        st.image(image, width=180)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RIGHT: USER INPUTS ----------------
with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🩸 Enter Recent Glucose Values")

    g1 = st.number_input(
        "Previous glucose value (mg/dL)",
        min_value=60,
        max_value=300,
        value=100
    )

    g2 = st.number_input(
        "Previous glucose value (mg/dL)",
        min_value=60,
        max_value=300,
        value=105
    )

    g3 = st.number_input(
        "Previous glucose value (mg/dL)",
        min_value=60,
        max_value=300,
        value=110
    )

    analyze = st.button("🚀 Start Analysis", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ANALYSIS ----------------
if uploaded_image and analyze:

    with st.spinner("Analyzing meal using backend AI service..."):

        backend_url = "http://127.0.0.1:8000/analyze-meal"

        files = {
            "file": (
                uploaded_image.name,
                uploaded_image.getvalue(),
                uploaded_image.type
            )
        }

        params = {
            "g1": g1,
            "g2": g2,
            "g3": g3
        }

        try:
            response = requests.post(
                backend_url,
                files=files,
                params=params
            )
            response.raise_for_status()
            result = response.json()

        except requests.exceptions.RequestException:
            st.error("❌ Backend connection failed")
            st.stop()

    # ---------------- RESULTS ----------------
    st.markdown("## 📋 Analysis Results")

    # Detected Foods
    st.markdown("### 🍛 Detected Food Items")
    for food in result["foods"]:
        st.write(
            f"✔ **{food['name']}** "
            f"({int(food['confidence'] * 100)}% confidence)"
        )

    # Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Glycemic Load", result["glycemic_load"])

    with col2:
        st.metric(
        "Predicted Peak Glucose",
        f"{result['predicted_peak_glucose']} mg/dL"
    )


    # ---------------- GLUCOSE CURVE ----------------
    st.markdown("### 📈 Predicted Post-Meal Glucose Curve")

    glucose_curve = result["predicted_glucose_curve"]
    time = np.arange(15, 15 * (len(glucose_curve) + 1), 15)

    fig, ax = plt.subplots()
    ax.plot(time, glucose_curve, linewidth=2)
    ax.axhline(180, linestyle="--", color="red", label="High Threshold")
    ax.set_xlabel("Time after meal (minutes)")
    ax.set_ylabel("Glucose (mg/dL)")
    ax.legend()

    st.pyplot(fig)

    # ---------------- RECOMMENDATION ----------------
    st.markdown("### 💡 Personalized Recommendation")
    st.success(result["recommendation"])

# ---------------- FOOTER ----------------
st.markdown(
    '<div class="footer">⚠️ Research prototype for academic use only. Not a medical device.</div>',
    unsafe_allow_html=True
)
