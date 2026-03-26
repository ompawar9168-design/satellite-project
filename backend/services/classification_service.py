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


def image_to_base64(image):
    success, buffer = cv2.imencode(".png", image)
    if not success:
        raise ValueError("Failed to encode image")

    return base64.b64encode(buffer).decode("utf-8")


def decode_index(gray_image):
    normalized = gray_image.astype(np.float32) / 255.0
    return (normalized * 2.0) - 1.0


def classify_land_cover_from_indices(ndvi_b64, ndwi_b64, ndbi_b64):
    ndvi_img = base64_to_gray_image(ndvi_b64)
    ndwi_img = base64_to_gray_image(ndwi_b64)
    ndbi_img = base64_to_gray_image(ndbi_b64)

    ndwi_img = cv2.resize(ndwi_img, (ndvi_img.shape[1], ndvi_img.shape[0]))
    ndbi_img = cv2.resize(ndbi_img, (ndvi_img.shape[1], ndvi_img.shape[0]))

    ndvi = decode_index(ndvi_img)
    ndwi = decode_index(ndwi_img)
    ndbi = decode_index(ndbi_img)

    vegetation_mask = ndvi > 0.30
    water_mask = ndwi > 0.20
    urban_mask = ndbi > 0.20

    water_mask = water_mask & (~vegetation_mask)
    urban_mask = urban_mask & (~vegetation_mask) & (~water_mask)

    classification = np.zeros(ndvi.shape, dtype=np.uint8)
    classification[vegetation_mask] = 1
    classification[water_mask] = 2
    classification[urban_mask] = 3
    classification[classification == 0] = 4  # Other

    kernel = np.ones((3, 3), np.uint8)
    classification = cv2.morphologyEx(classification, cv2.MORPH_OPEN, kernel)

    vegetation_count = int(np.count_nonzero(classification == 1))
    water_count = int(np.count_nonzero(classification == 2))
    urban_count = int(np.count_nonzero(classification == 3))
    other_count = int(np.count_nonzero(classification == 4))

    total_pixels = classification.shape[0] * classification.shape[1]

    vegetation_percent = round((vegetation_count / total_pixels) * 100, 2)
    water_percent = round((water_count / total_pixels) * 100, 2)
    urban_percent = round((urban_count / total_pixels) * 100, 2)
    other_percent = round((other_count / total_pixels) * 100, 2)

    classified_map = np.zeros((classification.shape[0], classification.shape[1], 3), dtype=np.uint8)

    # BGR
    classified_map[classification == 1] = [0, 180, 0]       # Vegetation
    classified_map[classification == 2] = [255, 120, 0]     # Water
    classified_map[classification == 3] = [210, 210, 210]   # Urban
    classified_map[classification == 4] = [80, 220, 230]    # Other

    return {
        "vegetation_percent": vegetation_percent,
        "water_percent": water_percent,
        "urban_percent": urban_percent,
        "other_percent": other_percent,
        "classified_map_base64": image_to_base64(classified_map),
        "label_map_base64": image_to_base64(classification),
    }


def compare_classification(old_result, new_result):
    return {
        "urban_growth_percent": round(new_result["urban_percent"] - old_result["urban_percent"], 2),
        "vegetation_change_percent": round(new_result["vegetation_percent"] - old_result["vegetation_percent"], 2),
        "water_change_percent": round(new_result["water_percent"] - old_result["water_percent"], 2),
        "other_change_percent": round(new_result["other_percent"] - old_result["other_percent"], 2),
    }