from playwright.sync_api import sync_playwright
import csv
import time

def run():
    print("Launching real browser to bypass Reddit's 403 block...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Bypass the 18+ NSFW warning gate that blocks feeds!
        context.add_cookies([
            {"name": "over18", "value": "1", "domain": ".reddit.com", "path": "/"},
            {"name": "over18", "value": "1", "domain": "old.reddit.com", "path": "/"}
        ])
        
        page = context.new_page()
        
        posts = set()
        
        urls = [
            "https://old.reddit.com/r/horror/top/?sort=top&t=all",
            "https://old.reddit.com/r/horror/top/?sort=top&t=year",
            "https://old.reddit.com/r/horror/new/",
            "https://old.reddit.com/r/horror/hot/",
            "https://old.reddit.com/r/horror/controversial/?sort=controversial&t=all"
        ]
        
        for url in urls:
            print(f"\nNavigating to {url}...")
            page.goto(url)
            
            for i in range(12):  # Scrape up to 12 pages per feed
                print(f"Scraping page {i+1}...")
                time.sleep(1.5)
                
                # Check for NSFW warning button just in case cookie isn't enough
                try:
                    nsfw_btn = page.locator("button[name='over18'][value='yes']")
                    if nsfw_btn.count() > 0:
                        nsfw_btn.first.click()
                        time.sleep(1)
                except:
                    pass
                
                # Expand all text posts
                expandos = page.locator("div.expando-button.selftext")
                for j in range(expandos.count()):
                    try:
                        expandos.nth(j).click()
                        time.sleep(0.3)
                    except:
                        pass
                
                entries = page.locator("div.entry")
                for j in range(entries.count()):
                    entry = entries.nth(j)
                    try:
                        title = entry.locator("a.title").inner_text()
                        body = ""
                        if entry.locator("div.usertext-body").count() > 0:
                            body = entry.locator("div.usertext-body").inner_text()
                        
                        text = f"{title} - {body}".replace('\n', ' ').replace('\r', ' ').strip()
                        
                        if len(text) > 100:
                            posts.add(text)
                    except Exception:
                        continue
                        
                print(f"Total collected so far: {len(posts)}")
                
                if len(posts) >= 250:
                    break
                
                next_btn = page.locator("span.next-button a")
                if next_btn.count() > 0:
                    next_url = next_btn.first.get_attribute("href")
                    page.goto(next_url)
                else:
                    print("No 'next' button found, moving to next feed.")
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
