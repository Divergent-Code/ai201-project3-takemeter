from playwright.sync_api import sync_playwright
import csv
import time
import os

def run():
    print("Launching real browser to bypass Reddit's 403 block...")
    
    csv_path = 'dataset.csv'
    existing_data = {}
    
    # Load existing data to prevent overwriting
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                next(reader) # skip header
                for row in reader:
                    if row and len(row) >= 1:
                        text = row[0]
                        label = row[1] if len(row) > 1 else ''
                        notes = row[2] if len(row) > 2 else ''
                        existing_data[text] = (label, notes)
            except StopIteration:
                pass

    print(f"Loaded {len(existing_data)} existing posts from {csv_path}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Bypass the 18+ NSFW warning gate
        context.add_cookies([
            {"name": "over18", "value": "1", "domain": ".reddit.com", "path": "/"},
            {"name": "over18", "value": "1", "domain": "old.reddit.com", "path": "/"}
        ])
        
        page = context.new_page()
        
        new_posts = set()
        
        # Use more subreddits, but fewer pages each to avoid rate limits
        urls = [
            "https://old.reddit.com/r/horrorlit/top/?sort=top&t=all",
            "https://old.reddit.com/r/horrorlit/top/?sort=top&t=year",
            "https://old.reddit.com/r/stephenking/top/?sort=top&t=all",
            "https://old.reddit.com/r/stephenking/top/?sort=top&t=year",
            "https://old.reddit.com/r/Scream/top/?sort=top&t=all",
            "https://old.reddit.com/r/HalloweenMovies/top/?sort=top&t=all",
            "https://old.reddit.com/r/deadmeatjames/top/?sort=top&t=all",
            "https://old.reddit.com/r/HorrorGaming/top/?sort=top&t=all",
            "https://old.reddit.com/r/HorrorMovies/top/?sort=top&t=month"
        ]
        
        total_collected = len(existing_data)
        
        for url in urls:
            if total_collected >= 250:
                break
                
            print(f"\nNavigating to {url}...")
            page.goto(url)
            
            for i in range(5):  # Only 5 pages per feed to avoid getting IP blocked!
                print(f"Scraping page {i+1}...")
                time.sleep(2.0)
                
                try:
                    nsfw_btn = page.locator("button[name='over18'][value='yes']")
                    if nsfw_btn.count() > 0:
                        nsfw_btn.first.click()
                        time.sleep(1)
                except:
                    pass
                
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
                        
                        if len(text) > 100 and text not in existing_data and text not in new_posts:
                            new_posts.add(text)
                            total_collected += 1
                    except Exception:
                        continue
                        
                print(f"Total collected so far: {total_collected}")
                
                if total_collected >= 250:
                    break
                
                next_btn = page.locator("span.next-button a")
                if next_btn.count() > 0:
                    next_url = next_btn.first.get_attribute("href")
                    page.goto(next_url)
                else:
                    print("No 'next' button found, moving to next feed.")
                    break
            
        browser.close()
        
        # Combine old and new data
        for post in new_posts:
            existing_data[post] = ('', '')
            
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['text', 'label', 'notes'])
            
            # Write up to 250 posts
            count = 0
            for text, (label, notes) in existing_data.items():
                if count >= 250:
                    break
                writer.writerow([text, label, notes])
                count += 1
                
        print(f"\nSuccessfully saved {count} posts to {csv_path}!")

if __name__ == "__main__":
    run()
