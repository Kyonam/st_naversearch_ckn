import json
import urllib.request
import os

def load_env_local(filepath=".env.local"):
    env = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    env[key] = value
    return env

def test_category(cid, secret, cat_id):
    url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"
    body = {
        "startDate": "2025-03-04",
        "endDate": "2026-03-03",
        "timeUnit": "date",
        "category": cat_id,
        "keyword": [{"name": "핫팩", "param": ["핫팩"]}],
        "device": "", "gender": "", "ages": []
    }
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", cid)
    request.add_header("X-Naver-Client-Secret", secret)
    request.add_header("Content-Type", "application/json")
    try:
        response = urllib.request.urlopen(request, data=json.dumps(body).encode("utf-8"))
        data = json.loads(response.read().decode("utf-8"))
        count = len(data['results'][0]['data']) if data['results'] and data['results'][0]['data'] else 0
        print(f"Category {cat_id}: {count} days of data found.")
    except Exception as e:
        print(f"Category {cat_id}: Error {e}")

if __name__ == "__main__":
    env = load_env_local()
    cid = env.get("ClIENT_ID") or env.get("CLIENT_ID")
    secret = env.get("ClIENT_SECRET") or env.get("CLIENT_SECRET")
    
    # Test common categories
    categories = ["50000005", "50000007", "50000002", "50000000", "50000008"]
    for cat in categories:
        test_category(cid, secret, cat)
