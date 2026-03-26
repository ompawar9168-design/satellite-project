def determine_main_problem(class_comparison):
    urban_change = class_comparison.get("urban_growth_percent", 0)
    vegetation_change = class_comparison.get("vegetation_change_percent", 0)
    water_change = class_comparison.get("water_change_percent", 0)

    issues = []

    if urban_change > 0:
        issues.append(("Urban Expansion", abs(urban_change)))

    if vegetation_change < 0:
        issues.append(("Vegetation Loss", abs(vegetation_change)))

    if water_change < 0:
        issues.append(("Water Loss", abs(water_change)))

    if not issues:
        return "Stable Land Pattern", None

    issues.sort(key=lambda x: x[1], reverse=True)

    main_problem = issues[0][0]
    secondary_problem = issues[1][0] if len(issues) > 1 else None

    return main_problem, secondary_problem


def determine_severity(change_percent, class_comparison):
    urban_change = abs(class_comparison.get("urban_growth_percent", 0))
    vegetation_change = abs(class_comparison.get("vegetation_change_percent", 0))
    water_change = abs(class_comparison.get("water_change_percent", 0))

    score = max(change_percent, urban_change, vegetation_change, water_change)

    if score >= 15:
        return "High"
    elif score >= 7:
        return "Medium"
    else:
        return "Low"


def generate_problem_summary(class_comparison, change_percent, transition_stats, advanced_stats):
    main_problem, secondary_problem = determine_main_problem(class_comparison)
    severity = determine_severity(change_percent, class_comparison)

    return {
        "urban_change": round(class_comparison.get("urban_growth_percent", 0), 2),
        "vegetation_change": round(class_comparison.get("vegetation_change_percent", 0), 2),
        "water_change": round(class_comparison.get("water_change_percent", 0), 2),
        "other_change": round(class_comparison.get("other_change_percent", 0), 2),
        "overall_change": round(change_percent, 2),
        "main_problem": main_problem,
        "secondary_problem": secondary_problem,
        "severity": severity,
        "top_transition": max(
            transition_stats,
            key=transition_stats.get
        ) if transition_stats else None,
        "changed_area_sqkm": advanced_stats.get("changed_area_sqkm", 0),
    }