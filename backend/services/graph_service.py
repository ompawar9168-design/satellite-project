def generate_graph_data(old_classification, new_classification, prediction_2028, zonewise_change):
    comparison_bar_chart = [
        {
            "name": "Urban",
            "before": old_classification.get("urban_percent", 0),
            "after": new_classification.get("urban_percent", 0),
        },
        {
            "name": "Vegetation",
            "before": old_classification.get("vegetation_percent", 0),
            "after": new_classification.get("vegetation_percent", 0),
        },
        {
            "name": "Water",
            "before": old_classification.get("water_percent", 0),
            "after": new_classification.get("water_percent", 0),
        },
        {
            "name": "Other",
            "before": old_classification.get("other_percent", 0),
            "after": new_classification.get("other_percent", 0),
        },
    ]

    pie_chart_2024 = [
        {"name": "Urban", "value": new_classification.get("urban_percent", 0)},
        {"name": "Vegetation", "value": new_classification.get("vegetation_percent", 0)},
        {"name": "Water", "value": new_classification.get("water_percent", 0)},
        {"name": "Other", "value": new_classification.get("other_percent", 0)},
    ]

    change_chart = [
        {
            "name": "Urban",
            "change": round(
                new_classification.get("urban_percent", 0) -
                old_classification.get("urban_percent", 0), 2
            ),
        },
        {
            "name": "Vegetation",
            "change": round(
                new_classification.get("vegetation_percent", 0) -
                old_classification.get("vegetation_percent", 0), 2
            ),
        },
        {
            "name": "Water",
            "change": round(
                new_classification.get("water_percent", 0) -
                old_classification.get("water_percent", 0), 2
            ),
        },
        {
            "name": "Other",
            "change": round(
                new_classification.get("other_percent", 0) -
                old_classification.get("other_percent", 0), 2
            ),
        },
    ]

    trend_chart = [
        {
            "year": "2020",
            "urban": old_classification.get("urban_percent", 0),
            "vegetation": old_classification.get("vegetation_percent", 0),
            "water": old_classification.get("water_percent", 0),
            "other": old_classification.get("other_percent", 0),
        },
        {
            "year": "2024",
            "urban": new_classification.get("urban_percent", 0),
            "vegetation": new_classification.get("vegetation_percent", 0),
            "water": new_classification.get("water_percent", 0),
            "other": new_classification.get("other_percent", 0),
        },
        {
            "year": "2028",
            "urban": prediction_2028.get("urban_percent", 0),
            "vegetation": prediction_2028.get("vegetation_percent", 0),
            "water": prediction_2028.get("water_percent", 0),
            "other": prediction_2028.get("other_percent", 0),
        },
    ]

    zone_chart = [
        {"zone": "North", "change": zonewise_change.get("north", 0)},
        {"zone": "South", "change": zonewise_change.get("south", 0)},
        {"zone": "East", "change": zonewise_change.get("east", 0)},
        {"zone": "West", "change": zonewise_change.get("west", 0)},
    ]

    risk_chart = [
        {
            "type": "Urban Expansion Risk",
            "value": max(
                0,
                round(
                    new_classification.get("urban_percent", 0) -
                    old_classification.get("urban_percent", 0), 2
                )
            ),
        },
        {
            "type": "Vegetation Loss Risk",
            "value": max(
                0,
                round(
                    old_classification.get("vegetation_percent", 0) -
                    new_classification.get("vegetation_percent", 0), 2
                )
            ),
        },
        {
            "type": "Water Loss Risk",
            "value": max(
                0,
                round(
                    old_classification.get("water_percent", 0) -
                    new_classification.get("water_percent", 0), 2
                )
            ),
        },
    ]

    return {
        "bar_chart": comparison_bar_chart,
        "pie_chart_2024": pie_chart_2024,
        "change_chart": change_chart,
        "trend_chart": trend_chart,
        "zone_chart": zone_chart,
        "risk_chart": risk_chart,
    }