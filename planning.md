---
{
  "id": "file_u7k32mym",
  "filetype": "document",
  "filename": "planning",
  "created_at": "2026-06-18T04:43:14.431Z",
  "updated_at": "2026-06-18T04:43:14.431Z",
  "meta": {
    "location": "/",
    "tags": [],
    "categories": [],
    "description": "",
    "source": "markdown"
  }
}
---
# TakeMeter Planning: r/horror & r/HorrorLit

## 1. Community
**Community:** `r/horror` (Reddit) & `r/HorrorLit` (Reddit)
**Reasoning:** The horror film and literature community is highly text-heavy and diverse in its discourse. Fans don't just say they liked a piece of media; they dissect the themes, debate the lore, ask for recommendations, post news, or rave about how a work made them feel. This makes it a perfect fit for a classification task because distinguishing between structured critiques, emotional reactions, news, questions, and general discussions is a common and meaningful distinction within the community.

## 2. Labels
The taxonomy consists of 7 active labels tailored to the book- and movie-centric nature of the scraped subreddits:

1. `critical_analysis`: The post makes a structured argument about a work's themes, cinematography, pacing, or subtext, backed by specific examples.
   - *Example 1:* "The Descent isn't just about monsters; the cave setting is a physical manifestation of Sarah's grief and claustrophobic trauma following the car crash."
   - *Example 2:* "An honest reflection on my 2017 novel, Stolen Tongues... Stolen Tongues is vastly more popular than any of my other works - and it is also vastly lower in quality. It was never meant to be a novel... it was just a dinky reddit post on /r/NoSleep..."

2. `visceral_reaction`: An immediate emotional or physical response to a work, focusing purely on the personal experience of watching or reading it (fear, disgust, horror, excitement, boredom) rather than analyzing *why* it works mechanically.
   - *Example 1:* "Just watched Event Horizon for the first time - Where has this movie been my whole life??? So fun and gory. Great cast. I love 90’s movies there’s just a vibe..."
   - *Example 2:* "A Short Stay in Hell is a brutal read... it left me with a deep, lingering sense of existential dread."

3. `hot_take`: A bold, confident, and often contrarian/unpopular opinion stated as fact, with little to no supporting evidence or deeper analysis.
   - *Example 1:* "The movie Drag Me To Hell is highly underrated - Do people feel that Drag Me To Hell is highly underrated, or is it just me?"
   - *Example 2:* "Maybe an unpopular opinion -but every Reddit nosleep creepypasta-turned-novel I’ve read has been disappointing..."

4. `discussion`: General conversation, open-ended prompts, sharing fan art/costumes, general thoughts, or community polls about horror media without a specific question, review, or news announcement.
   - *Example 1:* "Just received this commissioned painting for one of the scariest shots (imo) in a horror movie. What’s your “scariest shot” in a horror film?"
   - *Example 2:* "No one cared to dress up this year at my work but me. Hopefully you all find enjoy my costume more than they did. I was born to be Leather Face -"

5. `question`: Posts seeking information, help identifying a forgotten title, advice on what to watch next, or querying the community about specific lore/plot details.
   - *Example 1:* "Help me find a horror movie (2005–2015) SWAT raid, suburban house, basement scene it might be an indie film..."
   - *Example 2:* "Oddity - im confused - When darcy is examining olins eye how is it that she was seeing things that olin never saw?"

6. `recommendation`: Specifically sharing lists of favorite books/movies, suggesting specific titles to the community, or starting threads dedicated to recommendations.
   - *Example 1:* "I've read over 60 vampire novels, here are my top 10 with small reviews..."
   - *Example 2:* "The Autopsy of Jane Doe is a Sneakily Good Movie... Please watch this movie if you haven't already."

7. `news_and_rumors`: Announcements, industry news, obituaries/tributes, casting updates, or release dates of horror media.
   - *Example 1:* "Daveigh Chase - She passed away today at 35. She played Samara in The Ring. May she rest peacefully 💕"
   - *Example 2:* "“Angel Down” by Daniel Kraus Wins 2026 Pulitzer for Fiction..."

## 3. Hard Edge Cases
- **Ambiguous Post:** *"Hereditary is a masterpiece because the clicking sound Charlie makes is the most terrifying sound in cinema history, I couldn't sleep for days."*
  - **Challenge:** It mentions a specific filmic element (sound design), which borders on `critical_analysis`, but primarily focuses on the emotional aftermath (couldn't sleep), bordering on `visceral_reaction`.
  - **Decision Rule:** If the post connects the specific element to a broader theme or cinematic mechanic, it’s `critical_analysis`. If it merely uses the element to justify a personal emotional response, it’s `visceral_reaction`. By this rule, the example post is labeled `visceral_reaction`.
- **Recommendation vs. Discussion:**
  - **Challenge:** A post asking "What are the best cosmic horror books?" contains a question but is designed to gather recommendations.
  - **Decision Rule:** Posts that explicitly seek a list of recommendations or request suggestions are labeled `question` (if asking) or `recommendation` (if providing). General queries about people's favorites that prompt open discussion are labeled `discussion`.

## 4. Data Collection Plan
- **Source:** Posts and top-level comments from `r/horror` and `r/HorrorLit`.
- **Quantity:** 206 examples total, manually annotated.
- **Distribution:** Distributed across the 7 labels to capture the full landscape of subreddit discourse.

## 5. Evaluation Metrics
- **Overall Accuracy:** To get a baseline read of how well the model categorizes overall.
- **Per-Class F1 Score:** Because accuracy can be misleading with a 7-class taxonomy where some classes might have higher representation (e.g., `discussion` vs. `critical_analysis`), the F1 score for each class will help verify that the model is learning the distinct features of each class.
- **Confusion Matrix:** To pinpoint exactly which boundaries the model struggles with (e.g., does it consistently misclassify `visceral_reaction` as `discussion`?).

## 6. Definition of Success
A successful model should comfortably beat the zero-shot baseline of a large LLM (e.g., Groq Llama 3). Specifically, we aim for an overall accuracy of > 70% on the test set, with a per-class F1 score of > 0.60 across the primary categories. If the model can reliably distinguish an unsupported `hot_take` from a supported `critical_analysis` and separate generic `discussion` from targeted `recommendation` or `news_and_rumors`, it would be genuinely useful for filtering and organizing community forums.
