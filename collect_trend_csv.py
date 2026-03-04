import json
import urllib.request
import csv
from datetime import datetime, timedelta
import os

# Load credentials from .env.local
def load_env_local(filepath=".env.local"):
    env = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    env[key] = value
    return env

def fetch_data(url, client_id, client_secret, body):
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    request.add_header("Content-Type", "application/json")
    
    response = urllib.request.urlopen(request, data=json.dumps(body).encode("utf-8"))
    return json.loads(response.read().decode("utf-8"))

def collect_and_save_csv():
    env = load_env_local()
    client_id = env.get("ClIENT_ID") or env.get("CLIENT_ID")
    client_secret = env.get("ClIENT_SECRET") or env.get("CLIENT_SECRET")

    if not client_id or not client_secret:
        print("Error: Client ID or Secret not found in .env.local")
        return

    url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"
    today = datetime.now()
    end_date_str = today.strftime('%Y-%m-%d')
    start_date_str = (today - timedelta(days=365)).strftime('%Y-%m-%d')

    # 1. Fan (Digital/Appliance: 50000003)
    body_fan = {
        "startDate": start_date_str,
        "endDate": end_date_str,
        "timeUnit": "date",
        "category": "50000003",
        "keyword": [{"name": "선풍기", "param": ["선풍기"]}],
        "device": "", "gender": "", "ages": []
    }

    # 2. Hot Pack (Sports/Leisure: 50000007)
    body_hot = {
        "startDate": start_date_str,
        "endDate": end_date_str,
        "timeUnit": "date",
        "category": "50000007",
        "keyword": [{"name": "핫팩", "param": ["핫팩"]}],
        "device": "", "gender": "", "ages": []
    }

    try:
        print("Fetching Fan data (50000003)...")
        res_fan = fetch_data(url, client_id, client_secret, body_fan)
        print("Fetching Hot Pack data (50000007)...")
        res_hot = fetch_data(url, client_id, client_secret, body_hot)

        csv_rows = [["date", "keyword_group", "ratio"]]
        
        # Add Fan data
        for result in res_fan.get("results", []):
            group_name = result.get("title")
            for entry in result.get("data", []):
                csv_rows.append([entry.get("period"), group_name, entry.get("ratio")])
        
        # Add Hot Pack data
        for result in res_hot.get("results", []):
            group_name = result.get("title")
            for entry in result.get("data", []):
                csv_rows.append([entry.get("period"), group_name, entry.get("ratio")])

        today_compact = today.strftime('%Y%m%d')
        filename = f"data/shopping_trend_fan_hotpack_{today_compact}.csv"
        
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerows(csv_rows)
            
        print(f"Successfully saved to: {filename}")
        print(f"Total rows collected: {len(csv_rows) - 1}")
        
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    collect_and_save_csv()
