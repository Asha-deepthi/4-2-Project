# backend/glucose_prediction/train_lstm.py

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from synthetic_data import create_training_data

# Generate data
X, y = create_training_data(num_samples=3000)

# Build model
model = Sequential([
    LSTM(32, input_shape=(3, 2)),
    Dense(1)
])

model.compile(
    optimizer="adam",
    loss="mse"
)

model.summary()

# Train
model.fit(
    X, y,
    epochs=25,
    batch_size=32,
    validation_split=0.2
)

# Save model
model.save("backend/glucose_prediction/glucose_lstm.h5")
