import requests
import time

from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
env_path = os.path.join(BASE_DIR, ".env")

load_dotenv(env_path)

def fetch_jobs():
    all_jobs = []

    queries = [
        "etl developer",
        "data engineer",
        "python developer",
        ".NET developer",
        "ELT developer"
    ]

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for query in queries:
        print(f"Fetching jobs for: {query}")

        for page in range(1, 11):  # 10 pages per query
            url = f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"

            params = {
                "app_id": os.getenv("APP_ID"),
                "app_key": os.getenv("APP_KEY"),
                "results_per_page": 50,
                "what": query
            }
           
            try:
                response = requests.get(url, params=params, headers=headers)

                # 🔍 Debug info
                print(f"Status Code: {response.status_code}")

                if response.status_code != 200:
                    print(f"❌ Failed for query={query}, page={page}")
                    print(response.text[:200])  # show error
                    break

                data = response.json()
                jobs = data.get("results", [])

                if not jobs:
                    print(f"No jobs found for query={query}, page={page}")
                    break

                all_jobs.extend(jobs)

                time.sleep(1)  # ✅ avoid API ban

            except Exception as e:
                print(f"Error for query={query}, page={page}: {e}")
                break

    print(f"Total jobs fetched: {len(all_jobs)}")
    return all_jobs