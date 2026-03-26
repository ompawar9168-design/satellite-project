import cv2
import numpy as np
import base64


def base64_to_gray_image(image_base64):
    image_bytes = base64.b64decode(image_base64)
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError("Failed to decode grayscale image")

    return image


def estimate_total_area_sqkm(lat, lng, offset=0.01):
    # Very rough hackathon-safe estimate for bbox area
    # 1 degree latitude ~ 111 km
    lat_km = 2 * offset * 111.0

    # longitude shrinks with latitude
    lng_km = 2 * offset * 111.0 * np.cos(np.radians(lat))

    return round(lat_km * lng_km, 2)


def calculate_changed_area_sqkm(change_percent, total_area_sqkm):
    return round((change_percent / 100.0) * total_area_sqkm, 2)


def calculate_annual_rate(old_value, new_value, years_gap=4):
    return round((new_value - old_value) / years_gap, 2)


def get_zone_masks(shape):
    h, w = shape
    half_h = h // 2
    half_w = w // 2

    masks = {
        "north": np.zeros((h, w), dtype=np.uint8),
        "south": np.zeros((h, w), dtype=np.uint8),
        "east": np.zeros((h, w), dtype=np.uint8),
        "west": np.zeros((h, w), dtype=np.uint8),
    }

    masks["north"][:half_h, :] = 1
    masks["south"][half_h:, :] = 1
    masks["west"][:, :half_w] = 1
    masks["east"][:, half_w:] = 1

    return masks


def calculate_zonewise_change(threshold_map_base64):
    threshold_img = base64_to_gray_image(threshold_map_base64)
    binary = (threshold_img > 0).astype(np.uint8)

    total_pixels = binary.shape[0] * binary.shape[1]
    zone_masks = get_zone_masks(binary.shape)

    result = {}

    for zone_name, zone_mask in zone_masks.items():
        zone_pixels = int(np.count_nonzero(zone_mask))
        changed_zone_pixels = int(np.count_nonzero(binary * zone_mask))

        zone_change_percent = round((changed_zone_pixels / zone_pixels) * 100, 2) if zone_pixels else 0
        result[zone_name] = zone_change_percent

    overall_changed_pixels = int(np.count_nonzero(binary))
    overall_change_percent = round((overall_changed_pixels / total_pixels) * 100, 2) if total_pixels else 0

    return {
        "overall_change_percent_from_mask": overall_change_percent,
        "zones": result
    }


def build_advanced_stats(lat, lng, change_percent, threshold_map_base64, old_classification, new_classification):
    total_area_sqkm = estimate_total_area_sqkm(lat, lng)
    changed_area_sqkm = calculate_changed_area_sqkm(change_percent, total_area_sqkm)

    urban_growth_rate = calculate_annual_rate(
        old_classification.get("urban_percent", 0),
        new_classification.get("urban_percent", 0),
    )

    vegetation_change_rate = calculate_annual_rate(
        old_classification.get("vegetation_percent", 0),
        new_classification.get("vegetation_percent", 0),
    )

    water_change_rate = calculate_annual_rate(
        old_classification.get("water_percent", 0),
        new_classification.get("water_percent", 0),
    )

    zone_data = calculate_zonewise_change(threshold_map_base64)

    return {
        "total_area_sqkm": total_area_sqkm,
        "changed_area_sqkm": changed_area_sqkm,
        "annual_urban_growth_rate": urban_growth_rate,
        "annual_vegetation_change_rate": vegetation_change_rate,
        "annual_water_change_rate": water_change_rate,
        "zonewise_change": zone_data["zones"],
        "overall_change_percent_from_mask": zone_data["overall_change_percent_from_mask"],
    }