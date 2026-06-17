import urllib.request
import json
import csv
import time

urls = [
    "https://www.reddit.com/r/horror/hot.json?limit=100",
    "https://www.reddit.com/r/horror/top.json?limit=100&t=month",
    "https://www.reddit.com/r/horror/controversial.json?limit=100&t=month"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (Takemeter script)'
}

posts = []
seen = set()

print("Fetching posts from r/horror...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
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
