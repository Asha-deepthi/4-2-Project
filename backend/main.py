from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from food_detection.yolo_detector import detect_food_items
from gl_calculation import calculate_glycemic_load
from glucose_prediction.lstm_model import predict_glucose_curve

# --------------------------------------------------
# App Initialization
# --------------------------------------------------
app = FastAPI(
    title="AI Glycemic Load & Post-Meal Glucose Prediction API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Food name normalization mapping
# (YOLO output → Nutrition DB labels)
# --------------------------------------------------
FOOD_NAME_MAPPING = {
    "rice": "white_rice",
    "idli": "idli",
    "dosa": "dosa",
    "sambar": "sambar",
    "dal": "dal"
}

# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------
@app.get("/")
def root():
    return {"status": "Backend running successfully"}

# --------------------------------------------------
# Analyze Meal Endpoint
# --------------------------------------------------
@app.post("/analyze-meal")
async def analyze_meal(
    file: UploadFile = File(...),

    # User-provided recent glucose values (mg/dL)
    g1: float = 100,   # 30 min before meal
    g2: float = 105,   # 15 min before meal
    g3: float = 110    # just before meal
):
    """
    End-to-end pipeline:
    Image → Food detection → Glycemic Load →
    (User glucose + GL) → LSTM →
    Post-meal glucose curve
    """

    # ----------------------------------------------
    # 1. Read image bytes
    # ----------------------------------------------
    image_bytes = await file.read()

    # ----------------------------------------------
    # 2. Detect food items using YOLOv8
    # ----------------------------------------------
    detected_foods = detect_food_items(image_bytes)

    if not detected_foods:
        return {
            "foods": [],
            "glycemic_load": 0,
            "glucose_curve": [],
            "recommendation": "No food detected. Please upload a clearer image."
        }

    # ----------------------------------------------
    # 3. Normalize food names
    # ----------------------------------------------
    normalized_foods = []
    for food in detected_foods:
        mapped_name = FOOD_NAME_MAPPING.get(food["name"], food["name"])
        normalized_foods.append({
            "name": mapped_name,
            "confidence": float(food["confidence"])
        })

    # ----------------------------------------------
    # 4. Remove duplicate detections
    # ----------------------------------------------
    unique_foods = {}
    for food in normalized_foods:
        name = food["name"]
        confidence = food["confidence"]

        if name not in unique_foods or confidence > unique_foods[name]["confidence"]:
            unique_foods[name] = food

    final_foods = list(unique_foods.values())

    # ----------------------------------------------
    # 5. Glycemic Load Calculation
    # ----------------------------------------------
    PORTION_GRAMS = 200  # assumed portion (prototype)
    total_gl = 0.0

    for food in final_foods:
        gl_value = calculate_glycemic_load(
            food_name=food["name"],
            portion_grams=PORTION_GRAMS
        )
        if gl_value is not None:
            total_gl += gl_value

    total_gl = float(round(total_gl, 2))

    # ----------------------------------------------
    # 6. LSTM-based Post-Meal Glucose Prediction
    # ----------------------------------------------
    recent_glucose = [g1, g2, g3]

    glucose_curve = predict_glucose_curve(
        recent_glucose=recent_glucose,
        glycemic_load=total_gl,
        steps=12  # 3 hours → 12 × 15 min
    )

    predicted_peak = float(round(max(glucose_curve), 1)) if glucose_curve else None

    # ----------------------------------------------
    # 7. Recommendation Logic
    # ----------------------------------------------
    if predicted_peak and predicted_peak >= 180:
        recommendation = "Walk for 15–20 minutes to reduce glucose spike"
    elif predicted_peak and predicted_peak < 70:
        recommendation = "Consume a small carbohydrate snack"
    else:
        recommendation = "Glucose level expected to remain stable"

    # ----------------------------------------------
    # 8. Final Response
    # ----------------------------------------------
    response = {
    "foods": [
        {
            "name": str(food["name"]),
            "confidence": float(food["confidence"])
        }
        for food in final_foods
    ],
    "glycemic_load": float(total_gl),
    "predicted_peak_glucose": float(predicted_peak) if predicted_peak is not None else None,
    "predicted_glucose_curve": [float(g) for g in glucose_curve],
    "recommendation": str(recommendation)
}


    return response
