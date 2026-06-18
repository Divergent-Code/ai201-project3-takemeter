---
{
  "id": "file_1vnbr3bm",
  "filetype": "document",
  "filename": "AGENTS",
  "created_at": "2026-06-18T04:42:44.390Z",
  "updated_at": "2026-06-18T04:42:44.390Z",
  "meta": {
    "location": "/",
    "tags": [],
    "categories": [],
    "description": "",
    "source": "markdown"
  }
}
---
# TakeMeter — AI201 Project 3

## Project overview

TakeMeter is an academic text-classification project for the AI201 course (Project 3). The goal is to collect horror-related Reddit posts, label them into discourse categories, fine-tune a small transformer classifier, and compare it against a zero-shot Groq LLM baseline.

The project lives in a single flat directory. There is no package structure, no test suite, and no formal build system. The main workflow is:

1. **Collect** posts from horror subreddits using `scrape_reddit.py`.
2. **Label** them, either manually or with helper scripts (`auto_label.py`, `apply_labels.py`).
3. **Clean** the CSV with `clean_csv.py`.
4. **Train & evaluate** in the provided Colab starter notebook (`Copy of ai201_project3_takemeter_starter_clean.ipynb`), which fine-tunes `distilbert-base-uncased` and runs a Groq zero-shot baseline.

Project planning and label definitions are recorded in `planning.md`.

## Technology stack

- **Language:** Python 3.14.3
- **Virtual environment:** `.venv/` (created with `venv`, `include-system-site-packages = false`)
- **Installed packages (in `.venv`):**
  - `playwright==1.60.0` — browser automation for Reddit scraping
  - `requests==2.34.2` — HTTP utility
  - Standard transitive dependencies (`certifi`, `charset-normalizer`, `greenlet`, `idna`, `pyee`, `typing_extensions`, `urllib3`)
- **Notebook environment:** Google Colab with a T4 GPU runtime (expected by the starter notebook)
- **ML libraries (installed inside Colab, not locally):** `transformers`, `datasets`, `torch`, `sklearn`, `pandas`, `numpy`, `matplotlib`, `groq`, `python-dotenv`
- **Browser target:** Chromium via Playwright, using `old.reddit.com` to reduce blocking

## Project structure

```
.
├── .venv/                                          # Local Python virtual environment
├── .gitignore                                      # Python/IDE/OS ignores
├── planning.md                                     # Label definitions, data plan, success criteria
├── dataset.csv                                     # Annotated dataset (text, label, notes)
├── scrape_reddit.py                                # Playwright scraper for horror subreddits
├── auto_label.py                                   # Heuristic auto-labeler for the 3-class taxonomy
├── apply_labels.py                                 # Hard-coded per-row label overrides
├── clean_csv.py                                    # Regex cleanup of trailing whitespace in dataset.csv
├── debug_reddit.py                                 # Minimal Playwright sanity check for old.reddit.com
└── Copy of ai201_project3_takemeter_starter_clean.ipynb
                                                    # Colab notebook: DistilBERT fine-tuning + Groq baseline
```

There are no sub-packages, modules, `pyproject.toml`, `requirements.txt`, `setup.py`, test files, or CI/CD configuration. The starter notebook assumes you upload `dataset.csv` manually into Colab.

## Build and run commands

Activate the local environment before running any scraper or helper script:

```bash
# Windows (Git Bash / bash)
source .venv/Scripts/activate

# Run the scraper
python scrape_reddit.py

# Apply heuristic labels (overwrites dataset.csv)
python auto_label.py

# Apply hard-coded overrides (overwrites dataset.csv)
python apply_labels.py

# Clean CSV whitespace
python clean_csv.py

# Sanity-check Reddit access
python debug_reddit.py
```

The notebook is designed for Google Colab:

1. Open `Copy of ai201_project3_takemeter_starter_clean.ipynb` in Colab.
2. Set runtime to **T4 GPU** (`Runtime → Change runtime type → T4 GPU`).
3. Upload `dataset.csv` when the notebook prompts for it.
4. Fill in the `LABEL_MAP` and `SYSTEM_PROMPT` TODO sections with your actual labels.
5. Run all cells.

## Code organization

- **`scrape_reddit.py`** — Top-level script. Launches Chromium headless, navigates a list of horror subreddits on `old.reddit.com`, expands self-text posts, extracts `title + body`, deduplicates against existing `dataset.csv`, and writes up to 250 rows. It sets an `over18=1` cookie to bypass Reddit's NSFW gate.
- **`auto_label.py`** — Rule-based labeler for the original 3-class taxonomy (`critical_analysis`, `hot_take`, `visceral_reaction`) using keyword scoring. It overwrites `dataset.csv` and injects three hard-coded notes at rows 12, 45, and 103.
- **`apply_labels.py`** — Applies a static dictionary of row-number-to-label overrides. The labels in this file use a broader taxonomy (`critical_analysis`, `news_and_rumors`, `discussion`, `recommendation`, `question`, `hot_take`) that differs from `planning.md`. It directly overwrites `dataset.csv`.
- **`clean_csv.py`** — Small regex cleanup script that removes trailing spaces before commas and at end-of-line in `dataset.csv`.
- **`debug_reddit.py`** — Minimal Playwright probe that prints the page title and next-button presence for `old.reddit.com/r/horror/hot/`.
- **Notebook** — Contains the full training/evaluation pipeline in six sections: load dataset, prepare data, fine-tune DistilBERT, evaluate fine-tuned model, run Groq baseline, and compare/export results.

## Dataset

- **File:** `dataset.csv`
- **Columns:** `text`, ` label`, ` notes` (note the leading spaces in the header as currently written)
- **Current size:** 176 rows (including header)
- **Current label distribution:**
  - `discussion`: 46
  - `question`: 35
  - (empty): 39
  - `recommendation`: 17
  - `news_and_rumors`: 13
  - `visceral_reaction`: 11
  - `hot_take`: 9
  - `critical_analysis`: 6

The project originally defined three labels in `planning.md` (`critical_analysis`, `visceral_reaction`, `hot_take`), but the current dataset has been partially annotated with additional labels (`discussion`, `question`, `recommendation`, `news_and_rumors`). Before training, reconcile the label set and update `LABEL_MAP` in the notebook accordingly. Empty labels must be filled or dropped; the notebook drops rows whose labels are missing from `LABEL_MAP`.

## Development conventions

- Scripts are written as flat, self-contained files intended to be run directly (`if __name__ == "__main__": ...`).
- CSV is both the data store and the intermediate format; every helper script reads and overwrites `dataset.csv`.
- There is no formatter, linter, or type checker configured.
- The project uses `print()` for progress and status logging.
- API keys (Groq) are expected to live in Colab Secrets, never in source files.

## Testing

There are no automated tests. Manual verification steps:

1. Run `python debug_reddit.py` to confirm Playwright can reach Reddit.
2. Inspect `dataset.csv` after scraping/labeling to verify expected row counts and labels.
3. In Colab, confirm the notebook prints `"✅ All labels match your LABEL_MAP"` before training.
4. Review `confusion_matrix.png` and the misclassified examples printed by the notebook.

## Security considerations

- **Do not commit API keys.** The Groq key is meant to be read from Colab Secrets (`userdata.get("GROQ_API_KEY")`).
- The scraper includes `over18=1` cookies and browses subreddits that may contain NSFW content. Ensure this matches your organization's acceptable-use policy.
- Reddit scraping may violate Reddit's Terms of Service and can result in IP/rate limiting. The script already limits itself to 5 pages per feed and stops at 250 posts.
- `dataset.csv` contains public Reddit text, but still avoid including PII or usernames in committed data.
- The `.gitignore` already excludes `.venv/`, `.env`, IDE directories, and Python cache files.

## Common gotchas

- `dataset.csv` headers currently have leading spaces (`text`, ` label`, ` notes`). If you switch to pandas in the notebook, either strip the column names or rename them explicitly.
- `auto_label.py` and `apply_labels.py` both overwrite `dataset.csv` in place. Run them in the intended order and keep backups if you need to preserve manual annotations.
- The notebook's `LABEL_MAP` TODO must be edited to match the actual labels present in `dataset.csv`; the example map is illustrative and will fail validation otherwise.
- The broader label set introduced by `apply_labels.py` does not match the three-class taxonomy in `planning.md`. Decide on a single taxonomy before fine-tuning.
