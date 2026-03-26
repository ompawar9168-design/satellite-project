def calculate_prediction(old_classification, new_classification):
    years_gap = 4   # 2020 -> 2024
    future_gap = 4  # 2024 -> 2028

    classes = ["urban_percent", "vegetation_percent", "water_percent", "other_percent"]

    prediction = {}

    for cls in classes:
        old_val = old_classification.get(cls, 0)
        new_val = new_classification.get(cls, 0)

        annual_change = (new_val - old_val) / years_gap
        future_val = new_val + (annual_change * future_gap)

        future_val = max(0, min(100, future_val))
        prediction[cls] = round(future_val, 2)

    return {
        "urban_percent": prediction["urban_percent"],
        "vegetation_percent": prediction["vegetation_percent"],
        "water_percent": prediction["water_percent"],
        "other_percent": prediction["other_percent"],
    }


def generate_prediction_insights(prediction_2028):
    insights = []

    urban = prediction_2028.get("urban_percent", 0)
    vegetation = prediction_2028.get("vegetation_percent", 0)
    water = prediction_2028.get("water_percent", 0)

    if urban > 35:
        insights.append("⚠️ Rapid urban expansion expected by 2028")

    if vegetation < 30:
        insights.append("🌳 Vegetation cover may fall to a risk level by 2028")

    if water < 1:
        insights.append("💧 Water body coverage may become critically low by 2028")

    if not insights:
        insights.append("✅ No major environmental risk predicted by 2028")

    return insights