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

response = requests.get(url)
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

print("Saved results to results.csv")
