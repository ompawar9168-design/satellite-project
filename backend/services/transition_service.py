import cv2
import numpy as np
import base64


def base64_to_label_map(image_base64):
    image_bytes = base64.b64decode(image_base64)
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError("Failed to decode label map")

    return image


def calculate_transition_stats(old_label_b64, new_label_b64):
    old_map = base64_to_label_map(old_label_b64)
    new_map = base64_to_label_map(new_label_b64)

    new_map = cv2.resize(new_map, (old_map.shape[1], old_map.shape[0]), interpolation=cv2.INTER_NEAREST)

    total_pixels = old_map.shape[0] * old_map.shape[1]

    def pct(mask):
        return round((np.count_nonzero(mask) / total_pixels) * 100, 2)

    vegetation_to_urban = pct((old_map == 1) & (new_map == 3))
    water_to_urban = pct((old_map == 2) & (new_map == 3))
    water_to_other = pct((old_map == 2) & (new_map == 4))
    other_to_urban = pct((old_map == 4) & (new_map == 3))
    vegetation_to_other = pct((old_map == 1) & (new_map == 4))
    no_change = pct(old_map == new_map)

    return {
        "vegetation_to_urban": vegetation_to_urban,
        "water_to_urban": water_to_urban,
        "water_to_other": water_to_other,
        "other_to_urban": other_to_urban,
        "vegetation_to_other": vegetation_to_other,
        "no_change": no_change,
    }