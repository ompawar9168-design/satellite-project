def generate_insights(old_classification, new_classification, change_percent):
    insights = []

    urban_change = round(
        new_classification["urban_percent"] - old_classification["urban_percent"], 2
    )
    vegetation_change = round(
        new_classification["vegetation_percent"] - old_classification["vegetation_percent"], 2
    )
    water_change = round(
        new_classification["water_percent"] - old_classification["water_percent"], 2
    )

    if urban_change > 2:
        insights.append(f"🚧 Urban area increased by {urban_change}%")
    elif urban_change < -2:
        insights.append(f"🏙️ Urban area decreased by {abs(urban_change)}%")
    else:
        insights.append("🏙️ Urban area remained relatively stable")

    if vegetation_change < -2:
        insights.append(f"🌳 Vegetation reduced by {abs(vegetation_change)}%")
    elif vegetation_change > 2:
        insights.append(f"🌱 Vegetation increased by {vegetation_change}%")
    else:
        insights.append("🌿 Vegetation remained relatively stable")

    if water_change < -0.5:
        insights.append(f"💧 Water bodies reduced by {abs(water_change)}%")
    elif water_change > 0.5:
        insights.append(f"🌊 Water bodies increased by {water_change}%")
    else:
        insights.append("💦 Water bodies remained relatively stable")

    if change_percent > 15:
        insights.append("⚠️ High overall land-use change detected in this region")
    elif change_percent > 7:
        insights.append("📍 Moderate land-use change detected in this region")
    else:
        insights.append("✅ Low overall land-use change detected in this region")

    return insights