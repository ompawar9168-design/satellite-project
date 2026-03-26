import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SENTINEL_CLIENT_ID")
CLIENT_SECRET = os.getenv("SENTINEL_CLIENT_SECRET")


def get_access_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("Sentinel credentials missing in .env file")

    url = "https://services.sentinel-hub.com/oauth/token"

    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET),
        timeout=30
    )
    response.raise_for_status()
    return response.json()["access_token"]


def create_bbox(lat, lng, offset=0.01):
    return [
        lng - offset,
        lat - offset,
        lng + offset,
        lat + offset
    ]


def _post_process_request(payload):
    token = get_access_token()

    url = "https://services.sentinel-hub.com/api/v1/process"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    return base64.b64encode(response.content).decode("utf-8")


def _base_input_payload(lat, lng, year):
    bbox = create_bbox(lat, lng)

    return {
        "input": {
            "bounds": {
                "bbox": bbox
            },
            "data": [
                {
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": {
                            "from": f"{year}-03-01T00:00:00Z",
                            "to": f"{year}-04-30T23:59:59Z"
                        },
                        "maxCloudCoverage": 10,
                        "mosaickingOrder": "leastCC"
                    }
                }
            ]
        },
        "output": {
            "width": 768,
            "height": 768,
            "responses": [
                {
                    "identifier": "default",
                    "format": {
                        "type": "image/png"
                    }
                }
            ]
        }
    }


def get_true_color_image(lat, lng, year):
    payload = _base_input_payload(lat, lng, year)
    payload["evalscript"] = """
    //VERSION=3
    function setup() {
      return {
        input: ["B04", "B03", "B02"],
        output: { bands: 3 }
      };
    }

    function evaluatePixel(sample) {
      return [
        Math.min(1, 3 * sample.B04),
        Math.min(1, 3 * sample.B03),
        Math.min(1, 3 * sample.B02)
      ];
    }
    """
    return _post_process_request(payload)


def get_ndvi_image(lat, lng, year):
    payload = _base_input_payload(lat, lng, year)
    payload["evalscript"] = """
    //VERSION=3
    function setup() {
      return {
        input: ["B08", "B04"],
        output: { bands: 1 }
      };
    }

    function evaluatePixel(sample) {
      let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04 + 0.0001);
      let scaled = (ndvi + 1.0) / 2.0;
      return [Math.max(0, Math.min(1, scaled))];
    }
    """
    return _post_process_request(payload)


def get_ndwi_image(lat, lng, year):
    payload = _base_input_payload(lat, lng, year)
    payload["evalscript"] = """
    //VERSION=3
    function setup() {
      return {
        input: ["B03", "B08"],
        output: { bands: 1 }
      };
    }

    function evaluatePixel(sample) {
      let ndwi = (sample.B03 - sample.B08) / (sample.B03 + sample.B08 + 0.0001);
      let scaled = (ndwi + 1.0) / 2.0;
      return [Math.max(0, Math.min(1, scaled))];
    }
    """
    return _post_process_request(payload)


def get_ndbi_image(lat, lng, year):
    payload = _base_input_payload(lat, lng, year)
    payload["evalscript"] = """
    //VERSION=3
    function setup() {
      return {
        input: ["B11", "B08"],
        output: { bands: 1 }
      };
    }

    function evaluatePixel(sample) {
      let ndbi = (sample.B11 - sample.B08) / (sample.B11 + sample.B08 + 0.0001);
      let scaled = (ndbi + 1.0) / 2.0;
      return [Math.max(0, Math.min(1, scaled))];
    }
    """
    return _post_process_request(payload)


def get_spectral_stack(lat, lng, year):
    return {
        "true_color": get_true_color_image(lat, lng, year),
        "ndvi": get_ndvi_image(lat, lng, year),
        "ndwi": get_ndwi_image(lat, lng, year),
        "ndbi": get_ndbi_image(lat, lng, year),
    }