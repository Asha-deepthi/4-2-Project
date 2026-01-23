from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from gl_calculation import calculate_glycemic_load

# ---------------------------------------
# Create FastAPI app
# ---------------------------------------
app = FastAPI(
    title="AI Glycemic Load Backend",
    description="Backend API for food analysis and glucose prediction",
    version="1.0"
)

# ---------------------------------------
# Enable CORS (frontend access)
# ---------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------
# Root endpoint (health check)
# ---------------------------------------
@app.get("/")
def root():
    return {"status": "Backend is running successfully"}

# ---------------------------------------
# Analyze Meal Endpoint (DUMMY LOGIC)
# ---------------------------------------
@app.post("/analyze-meal")
async def analyze_meal(file: UploadFile = File(...)):
    """
    This endpoint receives a food image and returns
    dummy analysis results.
    """

    # NOTE: We are NOT processing the image yet
    # This is just a skeleton response

    detected_foods = [
        {"name": "white_rice", "confidence": 0.92},
        {"name": "dal", "confidence": 0.88}
    ]

    portion_grams = 200  # assumed portion

    total_gl = 0
    for food in detected_foods:
        gl = calculate_glycemic_load(food["name"], portion_grams)
        if gl:
            total_gl += gl

    response = {
        "foods": detected_foods,
        "glycemic_load": round(total_gl, 2),
        "predicted_glucose": 185,  # dummy for now
        "recommendation": "Walk for 15 minutes to reduce glucose spike"
    }

    return response
