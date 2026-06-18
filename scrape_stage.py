"""Wide-net staging scraper for TakeMeter.

Collects NEW horror posts into staging_posts.csv (text only, unlabeled) for a
3-label discourse-quality taxonomy: critical_analysis / visceral_reaction / hot_take.

It does NOT touch dataset.csv. Posts already present in dataset_7label_backup.csv
or base_quality.csv are skipped so we don't re-collect anything previously labeled.
We cast a wide net across many horror subreddits and include the `controversial`
sort, which surfaces bold/unpopular opinions (good for the thin hot_take class).
"""
from playwright.sync_api import sync_playwright
import csv
import os
import time

STAGING = "staging_posts.csv"
TARGET = 400          # raw posts to stage (we filter/label down afterward)
PAGES_PER_FEED = 6    # keep modest to avoid IP blocks
MIN_LEN = 120         # skip ultra-short titles with no substance


def load_seen():
    """Texts we've already collected/labeled — never re-stage these."""
    seen = set()
    for path in ("dataset_7label_backup.csv", "base_quality.csv", STAGING):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                reader = csv.reader(f)
                try:
                    next(reader)  # header
                except StopIteration:
                    continue
                for row in reader:
                    if row:
                        seen.add(row[0])
    return seen


def feed_urls():
    # Reaction/analysis-heavy subs sorted top (best quality takes) +
    # controversial (surfaces hot takes / unpopular opinions).
    subs = [
        "horror", "horrorlit", "HorrorReviewed", "HorrorMovies", "TrueFilm",
        "horrorbookclub", "Scream", "folkhorror", "cosmichorror",
        "slashers", "stephenking", "HalloweenMovies", "monstermovies", "IndieHorror",
        "AskHorror", "HorrorGaming", "residentevil", "silenthill", "classichorror",
        "horroratmosphere", "horror_film", "moviecritic",
    ]
    urls = []
    for s in subs:
        # Multiple time windows + controversial sort surface fresh, opinionated posts.
        urls.append(f"https://old.reddit.com/r/{s}/top/?sort=top&t=all")
        urls.append(f"https://old.reddit.com/r/{s}/top/?sort=top&t=month")
        urls.append(f"https://old.reddit.com/r/{s}/controversial/?sort=controversial&t=all")
        urls.append(f"https://old.reddit.com/r/{s}/controversial/?sort=controversial&t=year")
    return urls


def run():
    seen = load_seen()
    print(f"Loaded {len(seen)} already-collected posts to skip.")
    new_posts = []
    new_set = set()

    header_needed = not os.path.exists(STAGING)

    def flush(batch):
        nonlocal header_needed
        if not batch:
            return
        with open(STAGING, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if header_needed:
                w.writerow(["text"])
                header_needed = False
            for t in batch:
                w.writerow([t])

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        context.add_cookies([
            {"name": "over18", "value": "1", "domain": ".reddit.com", "path": "/"},
            {"name": "over18", "value": "1", "domain": "old.reddit.com", "path": "/"},
        ])
        page = context.new_page()

        for url in feed_urls():
            if len(new_posts) >= TARGET:
                break
            print(f"\nNavigating: {url}")
            feed_batch = []
            try:
                page.goto(url, timeout=30000)
            except Exception as e:
                print(f"  goto failed: {e}")
                continue

            for i in range(PAGES_PER_FEED):
                if len(new_posts) >= TARGET:
                    break
                time.sleep(2.0)
                try:
                    btn = page.locator("button[name='over18'][value='yes']")
                    if btn.count() > 0:
                        btn.first.click()
                        time.sleep(1)
                except Exception:
                    pass

                expandos = page.locator("div.expando-button.selftext")
                for j in range(expandos.count()):
                    try:
                        expandos.nth(j).click()
                        time.sleep(0.2)
                    except Exception:
                        pass

                entries = page.locator("div.entry")
                for j in range(entries.count()):
                    entry = entries.nth(j)
                    try:
                        title = entry.locator("a.title").inner_text()
                        body = ""
                        if entry.locator("div.usertext-body").count() > 0:
                            body = entry.locator("div.usertext-body").inner_text()
                        text = f"{title} - {body}".replace("\n", " ").replace("\r", " ").strip()
                        if len(text) > MIN_LEN and text not in seen and text not in new_set:
                            new_set.add(text)
                            new_posts.append(text)
                            feed_batch.append(text)
                    except Exception:
                        continue
                print(f"  page {i+1}: staged total {len(new_posts)}")

                nxt = page.locator("span.next-button a")
                if nxt.count() > 0:
                    try:
                        page.goto(nxt.first.get_attribute("href"), timeout=30000)
                    except Exception:
                        break
                else:
                    break

            flush(feed_batch)  # persist after each feed so a kill doesn't lose progress

        browser.close()
    print(f"\nStaged {len(new_posts)} new posts this run -> {STAGING}")


if __name__ == "__main__":
    run()
