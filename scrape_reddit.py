from playwright.sync_api import sync_playwright
import csv
import json
import time

def run():
    print("Launching real browser to bypass Reddit's 403 block...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        posts = set()
        
        # Hitting the JSON endpoints directly through the browser context!
        endpoints = [
            "https://old.reddit.com/r/horror/top.json?t=all&limit=100",
            "https://old.reddit.com/r/horror/top.json?t=year&limit=100",
            "https://old.reddit.com/r/horror/hot.json?limit=100",
            "https://old.reddit.com/r/horror/controversial.json?t=all&limit=100"
        ]
        
        for base_url in endpoints:
            after = None
            for i in range(5):  # 5 pages of 100 = 500 posts per endpoint
                url = base_url
                if after:
                    url += f"&after={after}"
                    
                print(f"Fetching JSON from {url}...")
                page.goto(url)
                time.sleep(2)
                
                try:
                    content = page.evaluate("document.body.innerText")
                    data = json.loads(content)
                    
                    children = data.get("data", {}).get("children", [])
                    for child in children:
                        post_data = child.get("data", {})
                        title = post_data.get("title", "")
                        body = post_data.get("selftext", "")
                        
                        text = f"{title} - {body}".replace('\n', ' ').replace('\r', ' ').strip()
                        
                        if len(text) > 100:
                            posts.add(text)
                            
                    after = data.get("data", {}).get("after")
                    print(f"Total collected: {len(posts)}")
                    
                    if not after or len(posts) >= 250:
                        break
                        
                except Exception as e:
                    print(f"Failed to parse JSON: {e}")
                    break
                    
            if len(posts) >= 250:
                print("\nReached target of 250 posts! Stopping scraper.")
                break
                
        browser.close()
        
        csv_path = 'dataset.csv'
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['text', 'label', 'notes'])
            for post in list(posts)[:250]:
                writer.writerow([post, '', ''])
                
        print(f"\nSuccessfully saved {min(len(posts), 250)} posts to {csv_path}!")
        print("Open this file in Excel or Google Sheets to begin your manual labeling.")

if __name__ == "__main__":
    run()
