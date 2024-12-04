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

    return response

if __name__ == "__main__":
    response = fetch_data(day=1)
    print(response.text)