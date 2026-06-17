from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        
        page.goto("https://old.reddit.com/r/horror/hot/")
        print("Page title:", page.title())
        
        btn = page.locator("span.next-button a")
        print("Next btn count:", btn.count())
        
        if btn.count() > 0:
            print("Next href:", btn.first.get_attribute("href"))
        else:
            print("Body HTML snippet:", page.inner_html("body")[:500])

if __name__ == "__main__":
    test()
