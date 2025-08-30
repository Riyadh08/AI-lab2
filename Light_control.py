# 1. Define triangular membership function
def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif x == b:
        return 1
    elif x < b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)

# 2. Input values
ambient_input = 60      # Ambient Light in Lux
preference_input = 45   # User preference (0-100)

# 3. Fuzzify Ambient Light
ambient_dark = triangular(ambient_input, 0, 0, 50)
ambient_dim = triangular(ambient_input, 40, 95, 150)
ambient_bright = triangular(ambient_input, 100, 300, 500)

# 4. Fuzzify User Preference
pref_dim = triangular(preference_input, 0, 0, 30)
pref_low = triangular(preference_input, 20, 35, 50)
pref_medium = triangular(preference_input, 40, 55, 70)
pref_high = triangular(preference_input, 60, 75, 90)
pref_bright = triangular(preference_input, 80, 90, 100)

# 5. Apply fuzzy rules using min() for AND
# Rule1: Dark & Dim -> Dim
rule1 = min(ambient_dark, pref_dim)
# Rule2: Dark & Low -> Low
rule2 = min(ambient_dark, pref_low)
# Rule3: Dim & Low -> Dim
rule3 = min(ambient_dim, pref_low)
# Rule4: Dim & Medium -> Medium
rule4 = min(ambient_dim, pref_medium)
# Rule5: Bright & Bright -> Bright
rule5 = min(ambient_bright, pref_bright)

# 6. Defuzzify using weighted average
# Assign brightness values: Dim=10, Low=30, Medium=50, High=70, Bright=90
numerator = rule1*10 + rule2*30 + rule3*10 + rule4*50 + rule5*90
denominator = rule1 + rule2 + rule3 + rule4 + rule5

brightness_output = numerator / denominator if denominator != 0 else 0

print(f"Crisp Brightness Level: {brightness_output:.2f}")
