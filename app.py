import streamlit as st
import requests
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Glycemic Load & Glucose Predictor",
    layout="centered"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🍽️ AI-Based Glycemic Load & Glucose Prediction")
st.write(
    "Upload a meal image to estimate **Glycemic Load (GL)** "
    "and predict **post-meal blood glucose levels**."
)

st.divider()

# -----------------------------
# IMAGE UPLOAD
# -----------------------------
uploaded_image = st.file_uploader(
    "📷 Upload Meal Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Meal Image", use_column_width=True)

    st.divider()

    # -----------------------------
    # ANALYZE BUTTON
    # -----------------------------
    if st.button("🔍 Analyze Meal"):

        with st.spinner("Analyzing meal..."):

            # -----------------------------------
            # TEMPORARY MOCK RESPONSE (Backend later)
            # -----------------------------------
            response_data = {
                "detected_foods": [
                    {"name": "White Rice", "confidence": 0.92},
                    {"name": "Dal", "confidence": 0.88}
                ],
                "glycemic_load": 38,
                "predicted_glucose": 185,
                "recommendation": "🚶 Walk for 15 minutes to reduce glucose spike"
            }

        # -----------------------------
        # FOOD DETECTION RESULT
        # -----------------------------
        st.subheader("🍛 Detected Food Items")
        for food in response_data["detected_foods"]:
            st.write(
                f"- **{food['name']}** "
                f"(Confidence: {int(food['confidence'] * 100)}%)"
            )

        st.divider()

        # -----------------------------
        # GL RESULT
        # -----------------------------
        st.subheader("📊 Glycemic Load (GL)")
        st.metric(
            label="Estimated Meal GL",
            value=response_data["glycemic_load"]
        )

        st.write(
            "ℹ️ Glycemic Load reflects how much this meal "
            "is expected to raise blood sugar."
        )

        st.divider()

        # -----------------------------
        # GLUCOSE PREDICTION GRAPH
        # -----------------------------
        st.subheader("📈 Predicted Blood Glucose Trend")

        # Dummy glucose curve for demo
        time = np.arange(0, 180, 15)
        glucose_curve = 100 + np.sin(time / 60) * 40 + 45

        fig, ax = plt.subplots()
        ax.plot(time, glucose_curve, marker="o")
        ax.axhline(180, color="red", linestyle="--", label="High Threshold")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel("Glucose (mg/dL)")
        ax.set_title("Post-Meal Glucose Prediction")
        ax.legend()

        st.pyplot(fig)

        st.write(
            f"🔺 **Predicted Peak Glucose:** "
            f"{response_data['predicted_glucose']} mg/dL"
        )

        st.divider()

        # -----------------------------
        # RECOMMENDATION
        # -----------------------------
        st.subheader("💡 Personalized Recommendation")
        st.success(response_data["recommendation"])

        st.caption(
            "⚠️ This system is a research prototype and not a medical device."
        )
