import json
import urllib.request
from datetime import datetime, timedelta
import os

# Naver API Credentials
# FIXME: Replace with your actual Client ID and Secret
CLIENT_ID = os.environ.get("NAVER_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

def collect_keyword_trend(output_file="fan_hotpack_trend.json"):
    if CLIENT_ID == "YOUR_CLIENT_ID" or CLIENT_SECRET == "YOUR_CLIENT_SECRET":
        print("Error: Please set NAVER_CLIENT_ID and NAVER_CLIENT_SECRET in environment variables or edit the script.")
        return

    url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"

    # Date Range: Last 1 year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    body = {
        "startDate": start_date.strftime('%Y-%m-%d'),
        "endDate": end_date.strftime('%Y-%m-%d'),
        "timeUnit": "date",
        "category": "50000003",  # Digital/Home Appliance
        "keyword": [
            {"name": "선풍기", "param": ["선풍기"]},
            {"name": "핫팩", "param": ["핫팩"]}
        ],
        "device": "", 
        "gender": "",
        "ages": []
    }

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
    request.add_header("Content-Type", "application/json")

    try:
        print(f"Fetching data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
        response = urllib.request.urlopen(request, data=json.dumps(body).encode("utf-8"))
        res_data = json.loads(response.read().decode("utf-8"))
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(res_data, f, indent=2, ensure_ascii=False)
        print(f"Success! Data saved to {output_file}")
        return res_data

    except Exception as e:
        print(f"API Call Failed: {e}")

if __name__ == "__main__":
    collect_keyword_trend()
