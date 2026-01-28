import numpy as np

def generate_glucose_curve(
    baseline_glucose,
    glycemic_load,
    timesteps=13  # 0 to 180 min, every 15 min
):
    """
    Generate a synthetic post-meal glucose curve.
    """

    time = np.arange(timesteps)
    peak_time = np.random.randint(4, 6)  # 60–90 min
    peak_rise = glycemic_load * np.random.uniform(0.9, 1.3)

    glucose = []

    for t in time:
        if t <= peak_time:
            value = baseline_glucose + (peak_rise * (t / peak_time))
        else:
            decay = np.exp(-(t - peak_time) / 3)
            value = baseline_glucose + peak_rise * decay

        glucose.append(value)

    return np.array(glucose)


def create_training_data(num_samples=1000):
    X, y = [], []

    for _ in range(num_samples):
        baseline = np.random.uniform(90, 140)
        gl = np.random.uniform(10, 60)

        curve = generate_glucose_curve(baseline, gl)

        for i in range(len(curve) - 3):
            seq = [
                [curve[i], gl],
                [curve[i + 1], gl],
                [curve[i + 2], gl]
            ]
            X.append(seq)
            y.append(curve[i + 3])

    return np.array(X), np.array(y)
