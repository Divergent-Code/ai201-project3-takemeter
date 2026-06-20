---
{
  "id": "file_m8n9pwpp",
  "filetype": "document",
  "filename": "README",
  "created_at": "2026-06-20T19:24:40.112Z",
  "updated_at": "2026-06-20T19:24:41.605Z",
  "meta": {
    "location": "/",
    "tags": [],
    "categories": [],
    "description": "",
    "source": "markdown"
  }
}
---
# TakeMeter — Classifying Discourse Quality in Horror Communities

A fine-tuned text classifier that sorts horror-community posts by **discourse quality**: is a take an *argued analysis*, a *felt reaction*, or a *bare hot take*? Built on `distilbert-base-uncased`, fine-tuned on 217 hand-reviewed Reddit posts, and benchmarked against a Claude Haiku (`claude-haiku-4-5-20251001`) zero-shot baseline.

> Companion docs: design reasoning and edge-case rules live in `planning.md`. This README is the standalone final report.

---

## 1. Community

Horror film & literature subreddits — primarily **r/horror**, **r/HorrorLit**, **r/HorrorReviewed**, **r/HorrorMovies**, with a wider net across r/Scream, r/stephenking, r/folkhorror, r/cosmichorror, r/slashers, r/HorrorGaming, r/AskHorror, and others.

**Why this community:** Horror is an unusually opinion-dense fandom. The *same* film — say *Hereditary* — surfaces as a careful thematic argument, a raw "I couldn't sleep" reaction, and a flat unsupported ranking. That natural variation in *how* people talk about the same works is exactly what a discourse-quality classifier needs, and the community already polices the distinction informally ("that's not analysis, that's just an opinion").

## 2. Label Taxonomy

Three mutually-exclusive labels. The unit of classification is a **take** — a post that expresses a stance, judgment, or response to a work. (Pure questions, bare news, and logistics posts are *not takes* and were excluded; see §3.)

| Label | Definition | Example |
|---|---|---|
| **critical_analysis** | A structured argument about a work's themes, craft, pacing, subtext, or lore, backed by specific examples or reasoning. Argues/analyzes rather than asserts. | "The Descent isn't just about monsters; the cave is a physical manifestation of Sarah's grief after the crash — every tightening passage mirrors how the film withholds her recovery." |
| **visceral_reaction** | An immediate emotional or physical response (fear, disgust, awe, boredom). Focus is the personal felt experience, not *why* the work succeeds. | "Just watched Event Horizon for the first time — where has this movie been my whole life??? So fun and gory, great cast." |
| **hot_take** | A bold, confident, often contrarian opinion stated as fact, with little/no supporting evidence. Asserts a debatable value judgment rather than arguing it. | "Drag Me To Hell is the most underrated horror film of the 2000s, full stop." |

Second example per label:

- **critical_analysis:** "Scream 6 works better than 5 because it finally lets the legacy characters age into the franchise's anxieties instead of just referencing them — the bodega scene reframes the killer's M.O. around public space."
- **visceral_reaction:** "A Short Stay in Hell is a brutal read. It left me with a deep, lingering sense of existential dread I still haven't shaken."
- **hot_take:** "Unpopular opinion: every NoSleep creepypasta-turned-novel I've read has been disappointing."

The boundary that matters most: **is the claim *argued* or merely *asserted*?** That line separates `critical_analysis` from `hot_take` and is where we expect the model to struggle most.

## 3. Dataset

- **Source:** Posts and self-text scraped from the subreddits above via `old.reddit.com`(Playwright; see `scrape_reddit.py` and `scrape_stage.py`). Both `top` (multiple time windows) and `controversial` sorts were used — `controversial` deliberately surfaces the bold/unpopular opinions that feed the `hot_take` class.
- **Size:** **217 labeled examples**, single CSV (`dataset.csv`), columns `text, label, notes`. The Colab notebook splits it 70/15/15 → \~152 train / \~33 val / \~33 test.

**Label distribution (count per label):**

| Label | Count | Share |
|---|---|---|
| critical_analysis | 86 | 39.6% |
| visceral_reaction | 68 | 31.3% |
| hot_take | 63 | 29.0% |
| **Total** | **217** | — |

No label exceeds 70%; the smallest class is 29%.

**Labeling process.** Each post was read and assigned exactly one label using the §2 definitions and the decision rules in `planning.md` §3. Annotation was **LLM-assisted and human-reviewed**: an LLM proposed a label (or `none`) with a one-line justification, and every proposal was checked against the definitions before acceptance. Posts that fit no quality label (pure "help me find this movie" questions, bare news, cosplay shares, polls) were labeled `none` and **dropped** rather than forced into a bucket. Pre-labeling artifacts are retained for transparency: `remap.json` (re-annotation of the original collection) and `staging_labeled.json` (the wider scrape). See §8.

**Three genuinely difficult examples and how they were decided:**

1. *"Hereditary is a masterpiece because the clicking sound Charlie makes is the most terrifying sound in cinema, I couldn't sleep for days."* — Names a specific filmic element (→ analysis) but the payload is the emotional aftermath (→ reaction). **Decision:** the element only justifies a personal feeling, it isn't tied to a broader mechanic → **visceral_reaction**.
2. A post titled *"Hot take: Scream 7 is the best sequel"* that then gives three specific, defensible reasons. **Decision:** ignore the self-label; the body supplies real evidence → **critical_analysis**. (This case produced the explicit "ignore the title" rule.)
3. *"This book is garbage, I lost interest immediately."* — value judgment (→ hot_take) vs. felt state (→ reaction). **Decision:** "garbage" is a debatable quality claim and dominates the post → **hot_take**; tie-break goes to whichever of the two is more prominent.

## 4. Fine-Tuning

- **Base model:** `distilbert-base-uncased` (HuggingFace).
- **Platform:** Google Colab, free **T4 GPU**, using the provided starter notebook (`Copy of ai201_project3_takemeter_starter_clean.ipynb`). The notebook's `LABEL_MAP` and `SYSTEM_PROMPT` are pre-filled for this 3-label taxonomy.
- **Training setup:** *(defaults unless noted)* 3 epochs, learning rate 2e-5, batch size 16, `distilbert-base-uncased` sequence-classification head with 3 output labels.

**Key hyperparameter decision — epochs.**

> *After running Section 3, fill this in with what you observed.* Suggested framing: with only \~152 training examples, more epochs risks memorizing rather than learning the argued-vs-asserted boundary. Report whether you kept 3 epochs or adjusted, and cite the validation-loss trend (e.g. "val loss flattened/rose after epoch N, so I kept/reduced epochs").

## 5. Baseline (Claude Haiku zero-shot)

- **Model:** `claude-haiku-4-5-20251001` via Anthropic API, no task-specific training.
- **Prompt:** the §2 label definitions + one example per label, instructing the model to output only the label name (see notebook Section 5). Each test post is classified independently; unparseable responses are flagged by the notebook.
- **How results were collected:** run on the **same locked test split** as the fine-tuned model, before fine-tuning, so the comparison is apples-to-apples.

## 6. Evaluation Report

> ⚠️ **To complete after running the Colab notebook (Sections 3–5).** Download `evaluation_results.json` and `confusion_matrix.png`, commit them, and fill the tables below from the notebook output.

### Overall accuracy

| Model | Test accuracy |
| :--- | :--- |
| Claude Haiku `claude-haiku-4-5-20251001` (zero-shot) | *TODO* |
| Fine-tuned DistilBERT | *TODO* |

### Per-class metrics (fine-tuned model)

| Label | Precision | Recall | F1 |
| :--- | :--- | :--- | :--- |
| critical_analysis | *TODO* | *TODO* | *TODO* |
| visceral_reaction | *TODO* | *TODO* | *TODO* |
| hot_take | *TODO* | *TODO* | *TODO* |

### Confusion matrix

> Paste `confusion_matrix.png` here and state which off-diagonal cell dominates. Hypothesis to test: `critical_analysis ↔ hot_take` is the heaviest confusion, because the only difference between them is whether the claim is *argued* or merely *asserted* — a distinction that hinges on content the model may not weigh heavily.

![Confusion matrix](confusion_matrix.png)

### Three wrong predictions, analyzed

> Pick 3 misclassified test examples from the notebook. For each, go past "it got it wrong": name the true vs. predicted label, then explain *why* using the guiding lens — is it the argued-vs-asserted boundary, a short/low-info post, sarcasm, or a topic that signals one label while the structure signals another? Note whether it's a labeling issue or a data/boundary issue.

1. *TODO*
2. *TODO*
3. *TODO*

### Sample classifications (fine-tuned model)

> Run 3–5 posts through the model and record predicted label + confidence. For at least one correct one, explain why the prediction is reasonable.

| Post (truncated) | Predicted | Confidence | Note |
| :--- | :--- | :--- | :--- |
| *TODO* | *TODO* | *TODO* | *TODO* |

### Reflection: what the model learned vs. what I intended

> *Write after seeing results.* The intent was a classifier that keys on *whether a claim is supported*. A likely gap: the model may instead key on **surface features** — exclamation marks and first-person emotion words → `visceral_reaction`; superlatives ("best", "overrated") → `hot_take`; length and paragraph structure → `critical_analysis`— rather than actually assessing argument quality. Use the confusion matrix and the 3 errors to argue which specific proxy the model latched onto.

## 7. Spec Reflection

**One way the spec helped:** The spec's insistence that labels be *mutually exclusive* and *grounded in community norms* (and the 2–4 label limit) is what forced the project's biggest correction — collapsing an initial 7-label content-type scheme down to 3 discourse-quality labels. Following that constraint surfaced that most of the original data weren't "takes" at all.

**One way the implementation diverged:** The spec frames data collection as "\~1–2 hours of manual copy-paste, don't let it become a coding project." In practice, scraping with Playwright was necessary to cast a wide enough net across many subreddits to backfill the thin `hot_take` and `critical_analysis` classes after \~58% of collected posts had to be dropped as `none`. The annotation itself stayed manual-review; only the *collection* was automated.

## 8. AI Usage

1. **Re-annotation / label remapping (annotation assistance — disclosed).** I directed an LLM to re-label the entire dataset from the old 7-label scheme into the 3 quality labels, given the §2 definitions and §3 rules, outputting a label-or-`none` plus a one-line reason per post (`remap.json`, `staging_labeled.json`). I reviewed every proposal against the definitions, kept `none` rows out of the dataset, and accepted the balance only after confirming no class was forced. **What I overrode:** posts the LLM wanted to file as `critical_analysis` purely because they were long got demoted to `hot_take` when the length wasn't actually backed by argument.
2. **Label stress-testing.** I had an LLM generate boundary posts between each label pair to probe my definitions. The `hot_take`-vs-`critical_analysis` cases it produced (a confident claim with one cherry-picked stat) drove the explicit "ignore the self-label, judge the body" rule now in `planning.md` §3.

> *After evaluation, add a third instance:* failure-pattern analysis — paste the misclassified examples to an LLM, have it propose error patterns, and verify each by re-reading the errors yourself.

## Repo contents

| File | What it is |
| :--- | :--- |
| `dataset.csv` | 217 labeled examples (final, 3 labels) |
| `planning.md` | Design doc: labels, edge-case rules, metrics, AI tool plan |
| `Copy of ai201_..._starter_clean.ipynb` | Colab fine-tuning notebook (label map + system prompt pre-filled) |
| `scrape_reddit.py`, `scrape_stage.py` | Reddit collection scripts |
| `remap.json`, `staging_labeled.json` | LLM pre-labeling artifacts (transparency) |
| `dataset_7label_backup.csv` | Original 7-label dataset, before the taxonomy revision |
| `evaluation_results.json`, `confusion_matrix.png` | *To add from Colab* |
