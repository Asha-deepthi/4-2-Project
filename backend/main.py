from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

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

    response = {
        "foods": [
            {"name": "White Rice", "confidence": 0.92},
            {"name": "Dal", "confidence": 0.88}
        ],
        "glycemic_load": 38,
        "predicted_glucose": 185,
        "recommendation": "Walk for 15 minutes to reduce glucose spike"
    }

    return response
