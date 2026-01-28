import os
import numpy as np
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "glucose_lstm.h5")

# Load model ONLY for inference
model = load_model(MODEL_PATH, compile=False)

def predict_glucose_curve(
    recent_glucose,   # list of 3 values
    glycemic_load,
    steps=12          # 3 hours → 12 steps of 15 min
):
    """
    Predict post-meal glucose curve.
    """

    predictions = []
    window = recent_glucose.copy()

    for _ in range(steps):
        x = np.array([
            [
                [window[0], glycemic_load],
                [window[1], glycemic_load],
                [window[2], glycemic_load],
            ]
        ])

        next_glucose = model.predict(x, verbose=0)[0][0]
        predictions.append(next_glucose)

        window = [window[1], window[2], next_glucose]

    return predictions
