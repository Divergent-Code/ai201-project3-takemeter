import requests
import json
import csv
import time

urls = [
    "https://www.reddit.com/r/horror/hot.json?limit=100",
    "https://www.reddit.com/r/horror/top.json?limit=100&t=month",
    "https://www.reddit.com/r/horror/controversial.json?limit=100&t=month"
]

# We use a very realistic browser header and session to avoid Reddit's 403 blocker
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

posts = []
seen = set()

print("Fetching posts from r/horror...")
session = requests.Session()

for url in urls:
    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for child in data['data']['children']:
                post = child['data']
                if post['id'] not in seen:
                    seen.add(post['id'])
                    # Combine title and body
                    text = post.get('title', '') + " - " + post.get('selftext', '')
                    # Clean up newlines for the CSV
                    text = text.replace('\n', ' ').replace('\r', ' ').strip()
                    
                    # We only want text posts that have a bit of substance
                    if len(text) > 50 and "http" not in post.get('selftext', ''): 
                        posts.append(text)
            print(f"Fetched from {url}")
        else:
            print(f"Error fetching {url}: HTTP {response.status_code}")
            
        time.sleep(2) # be nice to Reddit API
    except Exception as e:
        print(f"Error fetching {url}: {e}")

# Save to CSV
csv_path = 'dataset.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['text', 'label', 'notes']) # Adding a notes column for hard edge cases
    for post in posts:
        writer.writerow([post, '', ''])

print(f"\nSuccessfully saved {len(posts)} posts to {csv_path}!")
print("Open this file in Excel or Google Sheets to begin your manual labeling.")
