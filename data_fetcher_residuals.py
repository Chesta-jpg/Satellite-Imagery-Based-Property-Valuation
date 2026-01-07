# ============================================================
# Robust Mapbox Satellite Image Fetcher (with Retry & Resume)
# ============================================================

import os
import time
import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

print("SCRIPT STARTED")

# =========================
# CONFIG
# =========================
MAPBOX_TOKEN = "pk.eyJ1IjoiY2hlc3RhdGl3YXJpMSIsImEiOiJjbWp1aTk4NjgwOHVtM2RzOTN3MHQ0dXplIn0.PFMPvGBiYFdiq1tsv_2i0Q"
ZOOM = 18
IMAGE_SIZE = "224x224"
SLEEP_TIME = 0.25        # slower = safer
TIMEOUT = 15

# =========================
# PATHS
# =========================
TRAIN_DATA_PATH = "data/train.xlsx"
RESIDUAL_ID_PATH = "high_residual_ids.csv"
IMAGE_SAVE_DIR = "satellite_images/residual_train"

# =========================
# LOAD DATA
# =========================
train_df = pd.read_excel(TRAIN_DATA_PATH)
residual_ids = pd.read_csv(RESIDUAL_ID_PATH)["id"].tolist()

print("Total residual samples:", len(residual_ids))
os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

# =========================
# REQUEST SESSION WITH RETRIES
# =========================
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)
session.mount("https://", HTTPAdapter(max_retries=retries))

# =========================
# FETCH IMAGES (RESUME SAFE)
# =========================
for idx in residual_ids:

    save_path = os.path.join(IMAGE_SAVE_DIR, f"{idx}.png")

    # ✅ Skip already downloaded images
    if os.path.exists(save_path):
        continue

    try:
        row = train_df.loc[idx]
        lat, lon = row["lat"], row["long"]

        url = (
            f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/"
            f"{lon},{lat},{ZOOM}/"
            f"{IMAGE_SIZE}"
            f"?access_token={MAPBOX_TOKEN}"
        )

        print(f"Fetching index {idx}")
        response = session.get(url, timeout=TIMEOUT)

        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"Saved {idx}.png")
        else:
            print(f"Failed {idx} | Status {response.status_code}")

        time.sleep(SLEEP_TIME)

    except Exception as e:
        print(f"Error at index {idx}: {e}")
        print("Sleeping 5 seconds and continuing...")
        time.sleep(5)
        continue

print("SCRIPT FINISHED SUCCESSFULLY")