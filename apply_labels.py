import csv

# We map a unique prefix in the text to its manually analyzed label.
label_map = {
    "An honest reflection on my 2017 novel": "critical_analysis",
    "Angel Down": "news_and_rumors",
    "There is no safe word": "news_and_rumors",
    "Are we too repetitive?": "discussion",
    "I've read over 60 vampire novels": "recommendation",
    "I've read over 60 Scientific Thriller": "recommendation",
    "Hello fellow Horror readers": "recommendation",
    "Quick comment from a mod": "discussion",
    "Making plans to open a macabre": "discussion",
    "The worst part of being a horror book": "hot_take",
    "Maybe an unpopular opinion -but every Reddit nosleep creepypasta-turned-novel I’ve read has been disappointing": "hot_take",
    "Do you ever notice when an author uses a word repeatedly?": "hot_take",
    "What book would you recommend NEVER reading?": "question",
    "Shy Girl by Mia Ballard. Does anyone else think": "critical_analysis",
    "What’s the most TERRIFYING book": "question",
    "John Steinbeck wrote an unreleased": "news_and_rumors",
    "A wise man once told me": "discussion",
    "Mia Ballard's Shy Girl canceled": "news_and_rumors",
    "What's a monster that's terrifying because of its concept": "question",
    "Not horror but...": "hot_take",
    "Can we stop calling every horror novel COZY": "hot_take",
    "Do books genuinely scare you?": "question",
    "A look at Stephen King's writing routine": "news_and_rumors",
    "What’s one horror book you think everyone should read at least once?": "question",
    "Petition to make a sub rule": "hot_take",
    "Paul Tremblay was diagnosed": "news_and_rumors",
    "Finished “We Have Always Lived in the Castle”": "discussion",
    "Why is the horror literature community so nice?": "discussion",
    "The Best HORROR Books": "recommendation",
    "Why you should respect people when they ask for books": "hot_take",
    "The wrong audio narrator can really ruin a book": "hot_take",
    "Books that made you sleep with the lights on": "question",
    "Scariest book you’ve ever read?": "question",
    "I read 13 horror books in November": "recommendation",
    "I read 12 horror books in the past few months": "recommendation",
    "I love intense, extreme horror lit": "hot_take",
    "Just read Hell House": "question",
    "what is the most f*cked up": "question",
    "The Fisherman is a modern": "recommendation",
    "I don't think people should be downvoted": "hot_take",
    "Hereditary / The Witch": "question",
    "I read 187 horror novels in 2021": "recommendation",
    "The Horror Section is coming back": "news_and_rumors",
    "Female-based horror with no sexual violence?": "question",
    "Can we have a sea horror": "discussion",
    "whoa. what's with all the pedophilia": "discussion",
    "You all need to STOP": "hot_take",
    "Why is Appalachian horror so popular?": "question",
    "Koji Suzuki has passed away.": "news_and_rumors",
    "What's something you've read that just FELT cursed?": "question",
    "Joe Hill wasn’t kidding": "news_and_rumors",
    "Possibly unpopular opinion": "hot_take",
    "What are some of the disturbing books you wish": "question",
    "Witchcraft for Wayward Girls wins": "news_and_rumors"
}

rows = []
modified_count = 0
with open('dataset.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)
    for i, row in enumerate(reader):
        text = row[0]
        # Check if any prefix matches
        matched = False
        for prefix, label in label_map.items():
            if prefix in text or prefix.lower() in text.lower():
                row[1] = label
                matched = True
                modified_count += 1
                break
        rows.append(row)

with open('dataset.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Done. Applied labels to {modified_count} rows.")
