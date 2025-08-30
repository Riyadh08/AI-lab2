import numpy as np

# ---------------- Membership Functions ---------------- #
def triangular(x, a, b, c):
    """
    Vectorized triangular membership function.
    x can be a scalar or a NumPy array.
    """
    x = np.array(x, dtype=float)
    y = np.zeros_like(x)

    # Rising edge
    idx = (x > a) & (x < b)
    y[idx] = (x[idx] - a) / (b - a)

    # Peak
    idx = (x == b)
    y[idx] = 1.0

    # Falling edge
    idx = (x > b) & (x < c)
    y[idx] = (c - x[idx]) / (c - b)

    # Outside the triangle (already 0)
    return np.clip(y, 0, 1)


# ---------------- Fuzzy Sets ---------------- #
def temperature_membership(temp):
    return {
        "Low": triangular(temp, 0, 0, 50),
        "Medium": triangular(temp, 25, 50, 75),
        "High": triangular(temp, 50, 100, 100)
    }

def humidity_membership(humid):
    return {
        "Low": triangular(humid, 0, 0, 50),
        "Medium": triangular(humid, 25, 50, 75),
        "High": triangular(humid, 50, 100, 100)
    }

def fan_speed_membership(x):
    return {
        "Low": triangular(x, 0, 0, 50),
        "Medium": triangular(x, 25, 50, 75),
        "High": triangular(x, 50, 100, 100)
    }

# ---------------- Rule Evaluation ---------------- #
def apply_rules(temp, humid):
    """
    Fuzzy rules:
    1. IF Temp is Low AND Humidity is Low THEN Fan is Low
    2. IF Temp is Low AND Humidity is Medium THEN Fan is Low
    3. IF Temp is Low AND Humidity is High THEN Fan is Medium
    4. IF Temp is Medium AND Humidity is Low THEN Fan is Low
    5. IF Temp is Medium AND Humidity is Medium THEN Fan is Medium
    6. IF Temp is Medium AND Humidity is High THEN Fan is High
    7. IF Temp is High THEN Fan is High
    """
    rules = []

    rules.append(("Low", min(temp["Low"], humid["Low"])))
    rules.append(("Low", min(temp["Low"], humid["Medium"])))
    rules.append(("Medium", min(temp["Low"], humid["High"])))
    rules.append(("Low", min(temp["Medium"], humid["Low"])))
    rules.append(("Medium", min(temp["Medium"], humid["Medium"])))
    rules.append(("High", min(temp["Medium"], humid["High"])))
    rules.append(("High", temp["High"]))  # Temp high dominates

    return rules

# ---------------- Defuzzification ---------------- #
def defuzzify(rules, resolution=1000):
    x = np.linspace(0, 100, resolution)
    agg = np.zeros_like(x)

    for label, strength in rules:
        mf = fan_speed_membership(x)[label]
        agg = np.maximum(agg, np.minimum(strength, mf))  # Mamdani aggregation

    numerator = np.sum(x * agg)
    denominator = np.sum(agg)
    return numerator / denominator if denominator != 0 else 0

# ---------------- Main Example ---------------- #
if __name__ == "__main__":
    temps = [23, 45, 56, 78]
    humids = [56, 45, 78, 78]

    for t, h in zip(temps, humids):
        temp = temperature_membership(t)
        humid = humidity_membership(h)
        rules = apply_rules(temp, humid)
        fan_speed = defuzzify(rules)
        print(f"Temperature: {t}, Humidity: {h} --> Fan Speed: {fan_speed:.2f}")
