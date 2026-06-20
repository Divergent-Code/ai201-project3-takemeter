# TakeMeter Planning: Horror Discourse Quality

## 1. Community

**Community:** Horror film & literature subreddits — primarily `r/horror`, `r/HorrorLit`,
`r/HorrorReviewed`, `r/HorrorMovies`, plus a wider net of horror-adjacent subs
(`r/Scream`, `r/stephenking`, `r/folkhorror`, `r/cosmichorror`, `r/slashers`,
`r/HorrorGaming`, `r/AskHorror`, and others).

**Reasoning:** Horror is an unusually opinion-dense fandom. Fans don't just say they
liked something — they argue about whether a film's dread is *earned* or cheap, gush
about a book that genuinely scared them, and float bold contrarian rankings ("X is the
most overrated horror film of the decade"). That variety is exactly what a
discourse-quality classifier needs: the same topic (say, *Hereditary*) shows up as a
careful thematic argument, as a raw "I couldn't sleep" reaction, and as a flat
unsupported hot take. The community itself implicitly polices this — comments like
"that's not analysis, that's just an opinion" are common — so the distinctions are
*grounded in how the community already talks about its own discourse.*

## 2. Labels

The taxonomy is **3 mutually-exclusive discourse-quality labels**. The unit of
classification is a *take* — a post that expresses a stance, judgment, or response to a
work. (Pure info-seeking questions, bare news announcements, and logistics posts are
not takes and are excluded from the dataset; see §4.)

### `critical_analysis`
The post makes a structured argument about a work's themes, craft, pacing, subtext, or
lore, backed by specific examples or reasoning. **The point is to argue or analyze, not
just to assert or to react.**
- *Example 1:* "The Descent isn't just about monsters; the cave is a physical
  manifestation of Sarah's grief and claustrophobic trauma after the car crash — every
  tightening passage mirrors how the film withholds her recovery."
- *Example 2:* "Scream 6 works better than 5 because it finally lets the legacy
  characters age into the franchise's anxieties instead of just referencing them — the
  bodega scene reframes the killer's M.O. around public space, which the earlier films
  never did."

### `visceral_reaction`
An immediate emotional or physical response to a work — fear, disgust, awe, excitement,
boredom. **The focus is the personal felt experience**, not an analysis of *why* the
work mechanically succeeds, and not a debatable value claim.
- *Example 1:* "Just watched Event Horizon for the first time — where has this movie
  been my whole life??? So fun and gory, great cast. I love '90s movies, there's just a
  vibe."
- *Example 2:* "A Short Stay in Hell is a brutal read. It left me with a deep, lingering
  sense of existential dread I still haven't shaken."

### `hot_take`
A bold, confident, often contrarian opinion stated as fact, with little to no
supporting evidence. **The post asserts a debatable value judgment rather than arguing
it** (which would be `critical_analysis`) **or simply emoting** (which would be
`visceral_reaction`).
- *Example 1:* "Drag Me To Hell is the most underrated horror film of the 2000s, full
  stop."
- *Example 2:* "Unpopular opinion: every NoSleep creepypasta-turned-novel I've read has
  been disappointing."

## 3. Hard Edge Cases

The whole taxonomy lives or dies on three boundaries. Each has an explicit decision rule.

- **`critical_analysis` vs. `visceral_reaction`** — *"Hereditary is a masterpiece
  because the clicking sound Charlie makes is the most terrifying sound in cinema, I
  couldn't sleep for days."* It names a specific filmic element (sound design) but the
  payload is the emotional aftermath.
  **Rule:** If the post connects the specific element to a broader theme or cinematic
  mechanic (*why* it works), it's `critical_analysis`. If the element merely justifies a
  personal emotional response, it's `visceral_reaction`. → `visceral_reaction`.

- **`hot_take` vs. `critical_analysis`** — a post titled "Hot take: Scream 7 is the best
  sequel" that then supplies three specific, defensible reasons.
  **Rule:** Ignore the self-label. If the post supplies genuine, specific evidence that
  would support the claim with the opinion framing removed, it's `critical_analysis`. If
  the evidence is absent, vague, or decorative, it's `hot_take`. → depends on the body,
  not the title.

- **`hot_take` vs. `visceral_reaction`** — *"This book is garbage, I lost interest
  immediately."* Is it a value judgment (`hot_take`) or a felt reaction
  (`visceral_reaction`)?
  **Rule:** If the core is a *debatable claim about the work's quality* ("garbage,"
  "overrated," "the best"), it's `hot_take`. If the core is the *writer's internal state*
  ("it bored me," "it disgusted me"), it's `visceral_reaction`. Tie-break toward the more
  prominent of the two.

**Out-of-taxonomy ("none"):** Pure "help me find this movie" questions, bare news/casting
announcements with no opinion or emotion, polls, cosplay shares, and meta/logistics posts
are *not takes* and are dropped during annotation rather than forced into a bucket. This
was the single biggest data decision in the project (see §4).

## 4. Data Collection Plan

- **Source:** Posts and self-text from the horror subreddits listed in §1, scraped from
  `old.reddit.com` with Playwright (`scrape_reddit.py`, `scrape_stage.py`). Both `top`
  (multiple time windows) and `controversial` sorts were used — `controversial` is
  deliberately included because it surfaces the bold/unpopular opinions that feed the
  `hot_take` class.
- **Target:** ≥ 200 labeled *takes* across the 3 labels, aiming for rough balance
  (~33% each) and no class below ~25%.
- **Underrepresentation plan:** The initial collection skewed toward content-type posts
  (questions, news), so a large fraction was dropped as "none." When a quality class ran
  thin, we cast a wider net across more subreddits and used the `controversial` sort
  rather than re-labeling poor-fit posts into the class — keeping the data honest matters
  more than hitting a round number with noise.

## 5. Evaluation Metrics

- **Overall accuracy** — first-glance read of how well the model categorizes, and the
  headline number for the fine-tuned-vs-baseline comparison.
- **Per-class precision / recall / F1** — accuracy alone hides class-specific failure.
  With three subjective classes, the model could look fine overall while completely
  failing one boundary. Per-class F1 is the metric that exposes that; we care most about
  the F1 of `critical_analysis` and `hot_take`, the pair most likely to be confused.
- **Confusion matrix** — to read the *direction* of errors. The key question is whether
  `critical_analysis` and `hot_take` bleed into each other (the boundary is "is the claim
  argued or just asserted?"), which a single F1 number can't show.

## 6. Definition of Success

Concrete threshold: the fine-tuned model should reach **≥ 70% overall accuracy** on the
held-out test set **and beat the Claude Haiku (`claude-haiku-4-5-20251001`) zero-shot baseline by a
clear margin** (not within noise), with **per-class F1 ≥ 0.60 on all three labels** —
critically including `critical_analysis`, the smallest and hardest class. A model that
hits 70% overall but scores ~0 F1 on `critical_analysis` is *not* a success: it would
just be a `hot_take`/`visceral_reaction` detector. "Good enough for deployment" as a
community-forum filter means it can reliably separate an *argued* take from an *asserted*
one — that distinction is the whole point of the tool.

## 7. AI Tool Plan

**A. Label stress-testing.** Before committing to the 3-label scheme, the definitions and
edge-case rules were given to an LLM with instructions to generate boundary posts between
each label pair. Posts that couldn't be cleanly classified drove the explicit decision
rules in §3 (especially the "ignore the self-label" rule for `hot_take` vs.
`critical_analysis`).

**B. Annotation assistance (disclosed).** The dataset was re-annotated from an earlier
7-label content-type scheme into this 3-label quality scheme with LLM assistance: each
post was passed to an LLM with the §2 definitions and §3 rules, which proposed a label
(or "none") plus a one-line justification. **Every** proposed label was reviewed against
the definitions before being accepted, and "none" rows were dropped rather than kept.
This is disclosed in the README's AI Usage section. The pre-labeling artifacts
(`remap.json`, `staging_labeled.json`) are retained for transparency.

**C. Failure-pattern analysis.** After evaluation, the list of misclassified test
examples will be given to an LLM to surface candidate error patterns (e.g., "short posts
default to `hot_take`," or "`critical_analysis` ↔ `hot_take` confusion on review-style
posts"). Each proposed pattern will be verified by re-reading the actual errors before it
goes in the evaluation report — the LLM surfaces candidates, it does not get the final
word.

---

### Update log
- **Taxonomy revised from 7 content-type labels to 3 discourse-quality labels.** The
  original scheme (`critical_analysis`, `visceral_reaction`, `hot_take`, `discussion`,
  `question`, `recommendation`, `news_and_rumors`) exceeded the 2–4 label requirement and
  mixed a *quality* axis with a *content-type* axis, hurting mutual exclusivity. Honest
  re-annotation showed only the three quality labels capture *discourse quality*; the
  content-type rows were either remapped to a quality label or dropped as "none." Wider
  scraping then backfilled the quality classes to ≥ 200 examples.
