import cv2
import numpy as np
import base64


def base64_to_color_image(image_base64):
    image_bytes = base64.b64decode(image_base64)
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Failed to decode color image")

    return image


def image_to_base64(image):
    success, buffer = cv2.imencode(".png", image)
    if not success:
        raise ValueError("Failed to encode image")

    return base64.b64encode(buffer).decode("utf-8")


def generate_change_map(old_image_base64, new_image_base64):
    old_img = base64_to_color_image(old_image_base64)
    new_img = base64_to_color_image(new_image_base64)

    new_img = cv2.resize(new_img, (old_img.shape[1], old_img.shape[0]))

    old_gray = cv2.cvtColor(old_img, cv2.COLOR_BGR2GRAY)
    new_gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)

    old_gray = cv2.equalizeHist(old_gray)
    new_gray = cv2.equalizeHist(new_gray)

    old_blur = cv2.GaussianBlur(old_gray, (7, 7), 0)
    new_blur = cv2.GaussianBlur(new_gray, (7, 7), 0)

    diff = cv2.absdiff(old_blur, new_blur)

    _, thresh = cv2.threshold(diff, 35, 255, cv2.THRESH_BINARY)

    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(thresh, connectivity=8)
    cleaned = np.zeros_like(thresh)

    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area > 500:
            cleaned[labels == i] = 255

    changed_pixels = np.count_nonzero(cleaned)
    total_pixels = cleaned.shape[0] * cleaned.shape[1]
    change_percent = round((changed_pixels / total_pixels) * 100, 2)

    heatmap = cv2.applyColorMap(cleaned, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(new_img, 0.8, heatmap, 0.4, 0)

    return {
        "change_percent": change_percent,
        "change_map_base64": image_to_base64(overlay),
        "threshold_map_base64": image_to_base64(cleaned),
    }