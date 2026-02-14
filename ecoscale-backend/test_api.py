import requests
import json

API = "http://127.0.0.1:8000/api/optimize"

payload = {
    "appType": "web",
    "trafficRps": 500,
    "cpuCores": 8,
    "memoryGb": 16,
    "priority": "balanced"
}

def main():
    print("POST", API)
    r = requests.post(API, json=payload, timeout=5)
    try:
        r.raise_for_status()
    except Exception as e:
        print("Request failed:", e)
        print("Status code:", r.status_code)
        print(r.text)
        return

    data = r.json()
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
