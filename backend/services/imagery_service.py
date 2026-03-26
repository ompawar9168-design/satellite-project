def build_esri_image_url(lat, lng, size=512):
    min_lon = lng - 0.01
    min_lat = lat - 0.01
    max_lon = lng + 0.01
    max_lat = lat + 0.01

    return (
        "https://services.arcgisonline.com/ArcGIS/rest/services/"
        "World_Imagery/MapServer/export"
        f"?bbox={min_lon},{min_lat},{max_lon},{max_lat}"
        "&bboxSR=4326"
        f"&size={size},{size}"
        "&imageSR=4326"
        "&format=png"
        "&f=image"
    )


def get_real_imagery_result(lat, lng, old_year, new_year):
    return {
        "old_year": old_year,
        "new_year": new_year,
        "old_image_url": build_esri_image_url(lat, lng),
        "new_image_url": build_esri_image_url(lat, lng),
    }