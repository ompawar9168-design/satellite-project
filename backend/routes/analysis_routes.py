from flask import Blueprint, request, jsonify
from services.sentinel_service import get_spectral_stack
from services.change_service import generate_change_map
from services.classification_service import classify_land_cover_from_indices, compare_classification
from services.insight_service import generate_insights
from services.prediction_service import calculate_prediction, generate_prediction_insights
from services.stats_service import build_advanced_stats
from services.graph_service import generate_graph_data
from services.transition_service import calculate_transition_stats
from services.problem_service import generate_problem_summary

analysis_bp = Blueprint("analysis_bp", __name__)


@analysis_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "success",
        "message": "API is healthy"
    }), 200


@analysis_bp.route("/run-analysis", methods=["POST"])
def run_analysis():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No request body received"
            }), 400

        selected_position = data.get("selectedPosition", {})
        old_year = data.get("oldYear")
        new_year = data.get("NewYear") or data.get("newYear")

        lat = selected_position.get("lat")
        lng = selected_position.get("lng")

        if lat is None or lng is None:
            return jsonify({
                "status": "error",
                "message": "Latitude and longitude are required"
            }), 400

        if not old_year or not new_year:
            return jsonify({
                "status": "error",
                "message": "oldYear and newYear are required"
            }), 400

        old_stack = get_spectral_stack(lat, lng, old_year)
        new_stack = get_spectral_stack(lat, lng, new_year)

        change_result = generate_change_map(
            old_stack["true_color"],
            new_stack["true_color"]
        )

        old_classification = classify_land_cover_from_indices(
            old_stack["ndvi"],
            old_stack["ndwi"],
            old_stack["ndbi"]
        )

        new_classification = classify_land_cover_from_indices(
            new_stack["ndvi"],
            new_stack["ndwi"],
            new_stack["ndbi"]
        )

        class_comparison = compare_classification(
            old_classification,
            new_classification
        )

        transition_stats = calculate_transition_stats(
            old_classification["label_map_base64"],
            new_classification["label_map_base64"]
        )

        insights = generate_insights(
            old_classification,
            new_classification,
            change_result["change_percent"]
        )

        prediction_2028 = calculate_prediction(
            old_classification,
            new_classification
        )

        prediction_insights = generate_prediction_insights(prediction_2028)

        advanced_stats = build_advanced_stats(
            lat=lat,
            lng=lng,
            change_percent=change_result["change_percent"],
            threshold_map_base64=change_result["threshold_map_base64"],
            old_classification=old_classification,
            new_classification=new_classification,
        )

        graph_data = generate_graph_data(
            old_classification=old_classification,
            new_classification=new_classification,
            prediction_2028=prediction_2028,
            zonewise_change=advanced_stats.get("zonewise_change", {})
        )

        problem_summary = generate_problem_summary(
            class_comparison=class_comparison,
            change_percent=change_result["change_percent"],
            transition_stats=transition_stats,
            advanced_stats=advanced_stats
        )

        return jsonify({
            "status": "success",
            "message": "Analysis completed successfully",
            "result": {
                "old_image": old_stack["true_color"],
                "new_image": new_stack["true_color"],
                "change_percent": change_result["change_percent"],
                "change_map_base64": change_result["change_map_base64"],
                "threshold_map_base64": change_result["threshold_map_base64"],
                "old_classification": old_classification,
                "new_classification": new_classification,
                "class_comparison": class_comparison,
                "transition_stats": transition_stats,
                "insights": insights,
                "prediction_2028": prediction_2028,
                "prediction_insights": prediction_insights,
                "advanced_stats": advanced_stats,
                "graphs": graph_data,
                "problem_summary": problem_summary,
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500