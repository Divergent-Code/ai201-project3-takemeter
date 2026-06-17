# TakeMeter Planning: r/horror

## 1. Community
**Community:** `r/horror` (Reddit)
**Reasoning:** The horror community is incredibly text-heavy and diverse in its discourse. Fans don't just say they liked a movie; they dissect the themes, debate the lore, or just rave about how a movie made them feel. This makes it a perfect fit for a classification task because distinguishing between a well-supported critique, a purely emotional reaction, and an unsupported "hot take" is a common and meaningful distinction within the community.

## 2. Labels
1. `critical_analysis`: The post makes a structured argument about a film's themes, cinematography, pacing, or subtext, backed by specific examples from the movie.
   - *Example 1:* "The Descent isn't just about monsters; the cave setting is a physical manifestation of Sarah's grief and claustrophobic trauma following the car crash."
   - *Example 2:* "Longlegs uses negative space in the background of its wide shots to create a constant, looming sense of dread without relying on cheap jumpscares."
2. `visceral_reaction`: An immediate emotional or physical response to a film, focusing purely on the experience of watching it (fear, disgust, boredom) rather than analyzing *why* it works mechanically.
   - *Example 1:* "I just watched Skinamarink and I literally had to sleep with the lights on. The tension was unbearable."
   - *Example 2:* "Honestly, The Exorcist just wasn't scary to me. I found myself checking my phone halfway through."
3. `hot_take`: A bold, confident, and often contrarian opinion stated as fact, with little to no supporting evidence or deeper analysis.
   - *Example 1:* "Hereditary is the most overrated garbage of the last decade and anyone who thinks it's a masterpiece is pretending."
   - *Example 2:* "Rob Zombie's Halloween 2 is actually the best movie in the entire franchise, no contest."

## 3. Hard Edge Cases
**Ambiguous Post:** *"Hereditary is a masterpiece because the clicking sound Charlie makes is the most terrifying sound in cinema history, I couldn't sleep for days."*
**Challenge:** It mentions a specific filmic element (sound design), which borders on `critical_analysis`, but primarily focuses on the emotional aftermath (couldn't sleep), bordering on `visceral_reaction`.
**Decision Rule:** If the post connects the specific element to a broader theme or cinematic mechanic, it’s `critical_analysis`. If it merely uses the element to justify a personal emotional response, it’s `visceral_reaction`. By this rule, the example post is labeled `visceral_reaction`.

## 4. Data Collection Plan
**Source:** Posts and top-level comments from `r/horror`.
**Quantity:** At least 200 examples total, aiming for roughly an even split across the three labels (around 65-70 per label).
**Contingency:** If one label (e.g., `hot_take`) is underrepresented after collecting 200 examples, I will explicitly search the subreddit for "unpopular opinion", "overrated", or "hot take" threads to pad out that specific label's representation to ensure no label accounts for more than 70% of the dataset.

## 5. Evaluation Metrics
- **Overall Accuracy:** To get a baseline read of how well the model categorizes overall.
- **Per-Class F1 Score:** Because accuracy can be misleading if the classes become slightly imbalanced, the F1 score for each class will help verify that the model is actually learning the nuances of `critical_analysis` versus `visceral_reaction` rather than just predicting the most common class.
- **Confusion Matrix:** To pinpoint exactly *which* boundaries the model struggles with (e.g., does it consistently misclassify `visceral_reaction` as `hot_take`?).

## 6. Definition of Success
A successful model should comfortably beat the zero-shot baseline of Groq's LLM. Specifically, an overall accuracy of > 75% on the test set, with no single class having an F1 score below 0.65. If the model can reliably distinguish an unsupported `hot_take` from a supported `critical_analysis`, it would be genuinely useful for filtering low-effort posts in a community forum.

---

## AI Tool Plan
**A. Label stress-testing:** I will provide an AI tool (like Groq or Claude) with the label definitions and ask it to generate 5 "borderline" horror posts that are difficult to classify. If the definitions fail to handle them cleanly, I will refine the rules before manually annotating.
**B. Annotation assistance:** I will manually collect the 200 examples into a spreadsheet. To speed up the process, I may pass batches of them through an LLM prompt containing my definitions to pre-label them, but I will manually review and approve/correct *every single* assigned label to ensure high-quality training data.
**C. Failure analysis:** After fine-tuning, I will export the misclassified examples and feed them into an AI tool, asking it to identify common linguistic or structural patterns in the model's blind spots. I will verify these patterns myself before writing the final evaluation report.
