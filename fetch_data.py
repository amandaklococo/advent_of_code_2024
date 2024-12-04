import requests
from dotenv import load_dotenv
import os

def fetch_data(day):

    load_dotenv()
    secret_key = os.getenv("ADVENT_KEY")

    url = f"https://adventofcode.com/2024/day/{day}/input"

    headers = {
        "Cookie": secret_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.text

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

    return data

if __name__ == "__main__":
    data = fetch_data(day=2)
    print(data)