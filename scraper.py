import requests
from bs4 import BeautifulSoup
import sys
import re
import csv

if len(sys.argv) < 3:
    print("Usage: python scraper.py <url> <type>")
    print("type: links | emails")
    sys.exit()

url = sys.argv[1]
mode = sys.argv[2]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
    sys.exit()

soup = BeautifulSoup(response.text, "html.parser")

results = set()

if mode == "links":
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            results.add(href)

elif mode == "emails":
    text = soup.get_text()
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    results.update(emails)

else:
    print("Unknown mode")
    sys.exit()

with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["result"])
    for r in results:
        writer.writerow([r])

print(f"Saved {len(results)} results to results.csv")
