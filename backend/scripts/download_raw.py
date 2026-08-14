import urllib.request
import os
import json

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/canonical", exist_ok=True)

url = "https://raw.githubusercontent.com/ayush-that/codejeet/master/public/data/questions.json"
print("Downloading raw dataset...")
try:
    with urllib.request.urlopen(url) as response:
        data = response.read()
        with open("data/raw/codejeet_questions.json", "wb") as f:
            f.write(data)
        print("Download complete.")
        
        parsed = json.loads(data)
        print("Type:", type(parsed))
        if isinstance(parsed, list):
            print("Length:", len(parsed))
            if len(parsed) > 0:
                print("First item:", json.dumps(parsed[0], indent=2))
        elif isinstance(parsed, dict):
            print("Keys:", list(parsed.keys()))
            first_key = list(parsed.keys())[0]
            print("First item:", json.dumps(parsed[first_key], indent=2))
except Exception as e:
    print(f"Error: {e}")
