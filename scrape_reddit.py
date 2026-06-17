from playwright.sync_api import sync_playwright
import csv
import time

def run():
    print("Launching real browser to bypass Reddit's 403 block...")
    with sync_playwright() as p:
        # Use a real browser to bypass API blocks
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        posts = set()
        
        # old.reddit is much easier to scrape visually
        url = "https://old.reddit.com/r/horror/top/?sort=top&t=month"
        page.goto(url)
        
        for i in range(10):  # Scrape up to 10 pages to ensure we get enough text
            print(f"Scraping page {i+1}...")
            time.sleep(2)
            
            # Expand all text posts on the page to read their bodies
            expandos = page.locator("div.expando-button.selftext")
            for j in range(expandos.count()):
                try:
                    expandos.nth(j).click()
                    time.sleep(0.5)
                except:
                    pass
            
            # Grab titles and the expanded text bodies
            entries = page.locator("div.entry")
            for j in range(entries.count()):
                entry = entries.nth(j)
                try:
                    title = entry.locator("a.title").inner_text()
                    body = ""
                    if entry.locator("div.usertext-body").count() > 0:
                        body = entry.locator("div.usertext-body").inner_text()
                    
                    text = f"{title} - {body}".replace('\n', ' ').replace('\r', ' ').strip()
                    
                    # Only keep meaty posts (ignore short image/link titles)
                    if len(text) > 100:
                        posts.add(text)
                except Exception:
                    continue
                    
            print(f"Total collected so far: {len(posts)}")
            
            # Click the 'next' button
            next_btn = page.locator("span.next-button a")
            if next_btn.count() > 0:
                next_url = next_btn.get_attribute("href")
                page.goto(next_url)
            else:
                break
                
        browser.close()
        
        csv_path = 'dataset.csv'
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['text', 'label', 'notes'])
            for post in list(posts)[:250]: # Save top 250
                writer.writerow([post, '', ''])
                
        print(f"\nSuccessfully saved {min(len(posts), 250)} posts to {csv_path}!")
        print("Open this file in Excel or Google Sheets to begin your manual labeling.")

if __name__ == "__main__":
    run()
