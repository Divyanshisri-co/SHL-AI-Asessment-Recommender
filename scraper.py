import requests
import json
import os

DATA_URL = "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json"
OUTPUT_FILE = "data/shl_catalog.json"


def infer_test_type(item):
    keys = " ".join(item.get("keys", [])).lower()

    if "personality" in keys or "behavior" in keys:
        return "P"

    if "ability" in keys or "aptitude" in keys:
        return "K"

    if "situational" in keys:
        return "B"

    return "K"


def extract_skills(text):
    keywords = [
        "java",
        "python",
        "leadership",
        "communication",
        "numerical",
        "verbal",
        "coding",
        "sales",
        "customer service",
        "problem solving",
        "stakeholder",
        "personality",
        "cognitive"
    ]

    found = []

    lower_text = text.lower()

    for kw in keywords:
        if kw in lower_text:
            found.append(kw)

    return found


def download_catalog():
    os.makedirs("data", exist_ok=True)

    print("Downloading SHL catalog...")

    response = requests.get(DATA_URL, timeout=60)
    response.raise_for_status()

    raw_text = response.text
    raw_text = raw_text.replace("\x00", "")

    raw_data = json.loads(raw_text, strict=False)

    catalog = []

    for item in raw_data:
        name = str(item.get("name", "")).strip()
        url = str(item.get("link", "")).strip()
        description = str(item.get("description", "")).strip()

        if not name or not url:
            continue

        searchable = f"{name} {description}"

        catalog.append({
            "name": name,
            "url": url,
            "description": description,
            "test_type": infer_test_type(item),
            "skills": extract_skills(searchable)
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(catalog)} assessments")


if __name__ == "__main__":
    download_catalog()