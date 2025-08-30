import numpy as np

# ---------------- Membership Functions ---------------- #
#Parameters: a, b, c, d define the trapezoid shape
def trapezoidal(x, a, b, c, d):
 
    x = np.array(x, dtype=float)
    y = np.zeros_like(x)

    # Rising edge
    if b != a:
        y = np.where((x >= a) & (x <= b), (x - a) / (b - a), y)
    else:  # vertical left edge
        y = np.where(x <= a, 1.0, y)

    # Top (flat region)
    y = np.where((x >= b) & (x <= c), 1.0, y)

    # Falling edge
    if d != c:
        y = np.where((x >= c) & (x <= d), (d - x) / (d - c), y)
    else:  # vertical right edge
        y = np.where(x >= d, 1.0, y)

    return np.clip(y, 0, 1)

# ---------------- Fuzzy Sets ---------------- #

def ambient_light_membership(x):
    return {
        "Dark": trapezoidal(x, 0, 0, 40, 50),
        "Dim": trapezoidal(x, 40, 50, 150, 150),
        "Bright": trapezoidal(x, 100, 150, 500, 500)
    }

def user_pref_membership(x):
    return {
        "Dim": trapezoidal(x, 0, 0, 20, 30),
        "Low": trapezoidal(x, 20, 30, 50, 50),
        "Medium": trapezoidal(x, 40, 50, 70, 70),
        "High": trapezoidal(x, 60, 70, 90, 90),
        "Bright": trapezoidal(x, 80, 90, 100, 100)
    }

def brightness_output_membership(x):
    return {
        "Dim": trapezoidal(x, 0, 0, 20, 30),
        "Low": trapezoidal(x, 20, 30, 40, 50),
        "Medium": trapezoidal(x, 40, 50, 60, 70),
        "High": trapezoidal(x, 60, 70, 80, 90),
        "Bright": trapezoidal(x, 80, 90, 100, 100)
    }


# ---------------- Rule Evaluation ---------------- #

def apply_rules(ambient, user):
    """
    Apply the given fuzzy rules.
    Rules:
    1. IF Ambient=Dark AND Pref=Dim THEN Brightness=Dim
    2. IF Ambient=Dark AND Pref=Low THEN Brightness=Low
    3. IF Ambient=Dim AND Pref=Low THEN Brightness=Dim
    4. IF Ambient=Dim AND Pref=Medium THEN Brightness=Medium
    5. IF Ambient=Bright AND Pref=Bright THEN Brightness=Bright
    """

    rules = []

    # Rule 1
    rules.append(("Dim", min(ambient["Dark"], user["Dim"])))
    # Rule 2
    rules.append(("Low", min(ambient["Dark"], user["Low"])))
    # Rule 3
    rules.append(("Dim", min(ambient["Dim"], user["Low"])))
    # Rule 4
    rules.append(("Medium", min(ambient["Dim"], user["Medium"])))
    # Rule 5
    rules.append(("Bright", min(ambient["Bright"], user["Bright"])))

    return rules

# ---------------- Defuzzification ---------------- #

def defuzzify(rules, resolution=1000):
    """ Mamdani inference + Center of Gravity """
    x = np.linspace(0, 100, resolution)
    agg = np.zeros_like(x)

    for output_label, strength in rules:
        mf = brightness_output_membership(x)[output_label]
        agg = np.maximum(agg, np.minimum(strength, mf))  # Aggregation

    # Center of Gravity
    numerator = np.sum(x * agg)
    denominator = np.sum(agg)
    if denominator == 0:
        return 0
    return numerator / denominator

# ---------------- Main Example ---------------- #

if __name__ == "__main__":
    ambient_input = 45   # Lux
    user_input = 25      # User preference (0-100)

    # Fuzzification
    ambient = ambient_light_membership(ambient_input)
    user = user_pref_membership(user_input)

    # Rule Evaluation
    rules = apply_rules(ambient, user)

    # Defuzzification
    brightness = defuzzify(rules)

    print("Ambient Light Input:", ambient_input, "Lux")
    print("User Preference Input:", user_input)
    print("Final Brightness Level (0-100):", round(brightness, 2))
