# Co-Authored-By: VEGA <vega@noreply.local>
# Co-Authored-By: Hayden <hayden@noreply.local>

import csv

# Map of prefix text to the manually annotated category
manual_mappings = {
    "Just received this commissioned painting": "discussion",
    "Which part 2 would you ladies and gents want?": "discussion",
    "Alyce Kills, Contracted, Almost Mercy": "discussion",
    "Just watched Event Horizon for the first time": "visceral_reaction",
    "Saw a clip of a movie can’t figure out": "question",
    "Just watched tusk and I don’t know": "visceral_reaction",
    "The Autopsy of Jane Doe is a Sneakily Good": "recommendation",
    "Watching this classic today, of course": "visceral_reaction",
    "Help me find a horror movie (2005–2015)": "question",
    "My thoughts on the Backrooms Movie": "critical_analysis",
    "What’s a horror remake you’ll defend": "discussion",
    "No one cared to dress up this year": "discussion",
    "I believe this was one of the first": "discussion",
    "I’m wondering if someone can help identify": "question",
    "Oddity - im confused - When darcy": "question",
    "Why wasn’t HIM talked about more": "discussion",
    "One year ago today, LongLegs was released": "discussion",
    "Did you ever say no to a movie": "discussion",
    "Looking for Title of Film - I remember": "question",
    "The movie Drag Me To Hell is highly": "hot_take",
    "Daveigh Chase - She passed away": "news_and_rumors",
    "Can't remember name of bizarre, obscure": "question",
    "Have you all seen \"The Void\"": "discussion",
    "Jacobs Ladder (1990) one of the best": "critical_analysis",
    "What’s a horror movie that absolutely terrified": "discussion",
    "Why is this so controversial?": "hot_take",
    "This is one of those movies that you notice": "discussion",
    "Blind-watched The Void last night": "discussion",
    "Thoughts on Strange Darling?": "discussion",
    "The Exorcist STILL wrecks me": "visceral_reaction",
    "Obsession was something I’ve never seen": "visceral_reaction",
    "Sinners, 28 Years Later or Weapons": "discussion",
    "Is it worth watching all the Scream movies": "question",
    "Presence (Movie) - SPOILER AHEAD": "critical_analysis",
    "What do you think of Wolf Creek?": "discussion",
    "Thoughts on the underseen but brilliant": "discussion",
    "In honor of the 50th anniversary": "discussion",
    "Lloyd Kaufman is celebrating": "news_and_rumors",
    "Help me find this movie - A couple": "question",
    "help me find the title of this movie": "question",
    "I know some people didn't like the twist": "discussion",
    "I enjoyed this way more than I thought": "visceral_reaction",
    "Help! - I’m trying for the life": "question",
    "Just watched You're Next and I didn’t": "discussion",
    "My Horror Film Subway Map 2025": "discussion",
    "Thoughts on Event Horizon (1997) I'm": "discussion",
    "Looking for a movie i watched as a kid": "question",
    "Recently got my supervisor into the film": "discussion",
    "Anytime I’m having a day": "discussion",
    "Anytime I’m having a bad day": "discussion",
    "Should I follow through on watching": "question",
    "Looking for a very specific movie. help": "question",
    "if everything seen in horror was actually real": "discussion",
    "[Crosspost] Hi /r/movies! I'm Olivia": "news_and_rumors",
    "It’s been a long time since a movie": "visceral_reaction",
    "Anyone know this movie? - I saw": "question",
    "Help me find a movie - I saw a clip": "question",
    "Looking again for the 1974 Black Christmas": "question",
    "This s+#t! What a fresh take on": "visceral_reaction",
    "Horror movie titles help please": "question",
    "Truly shocked by how good this movie": "critical_analysis",
    "Getting ready for Halloween 🎃": "discussion",
    "I decided to watch Alien 1979 for the": "visceral_reaction",
    "Obsession vs Backrooms - I just": "critical_analysis",
    "My favorite sub. What other iconic": "discussion",
    "Evil Dead Rise, first one I have ever": "visceral_reaction",
    "What are must watch horror movies ?": "discussion",
    "What are your thoughts on The Silence": "hot_take",
    "Obsession - Just watched *Obsession*": "critical_analysis",
    "Sarah Michelle Gellar, horror queen": "news_and_rumors",
    "Go in blind for this one guys": "recommendation",
    "If Obsession had A24’s budget": "discussion",
    "Need help finding a Movie with a woman": "question",
    "This looks like a nice, fun movie!": "discussion",
    "Looking for a movie.....": "question",
    "DUMPLINGS (2004) | One of the rare": "recommendation",
    "So Leatherface used to be one of the": "discussion",
    "Happy 10th anniversary to my favorite": "discussion",
    "What’s the best horror movie franchise?": "discussion",
    "I’m unsure if it would count as horror": "hot_take",
    "NIGHTBREED (1990) This is in my top": "discussion",
    "Weekly recommendations thread.": "recommendation",
    "Who’s your favourite final girl from": "discussion",
    "Need help finding a movie, hotel room": "question",
    "Can anyone identify this old horror": "question",
    "Watched the theatrical cut for the first": "hot_take",
    "My 15 year old daughter is a massive": "discussion",
    "“Dr Sleep” was incredible": "discussion",
    "Frenzy Moon - Someone out there": "visceral_reaction",
    "HAS ANYONE WATCHED WEAPONS?": "question",
    "Has anyone seen Good Boy?": "discussion",
    "How old were you when you watched your": "discussion",
    "Obsession - Been wanting to watch": "visceral_reaction",
    "I'm an amputee and I usually make": "discussion",
    "Came across this news article of Stephen": "discussion",
    "Is 'Misery' (1990) actually worth": "discussion",
    "Need help finding a movie that has a scene": "question",
    "Trying to find this movie!! - Looking": "question",
    "Has anyone seen the movie \"Creep\"?": "discussion",
    "I “dress up” my porch goose tattoo": "discussion",
    "Amazing creature actors Bolaji": "discussion",
    "I've been watching hundreds of horror": "visceral_reaction",
    "David Howard Thornton and young": "news_and_rumors",
    "I met Joe Dante at the Horrorhound": "discussion",
    "This year I did something I always wanted": "discussion",
    "If you're liking new gothic horror movies": "recommendation",
    "I draw pop culture as vintage comics": "discussion",
    "People always talking about perfect couple": "discussion",
    "Bordello of blood extremely underrated": "hot_take",
    "Horror movie with a wheelchair-bound": "question",
    "¿Me ayudarían a encontrar esta película?": "question",
    "Is Mandy the quintessential Nick Cage": "critical_analysis",
    "I looked over and saw this man looking": "visceral_reaction",
    "Joe Hill is \"sprinting madly for my": "news_and_rumors",
    "The /r/HorrorLit Book Club has selected": "news_and_rumors",
    "Commonly Requested Book Recs: The Spreadsheet": "recommendation",
    "What line made you want to quit": "discussion",
    "NYC’s first-ever horror bookshop": "news_and_rumors",
    "I'll be one year sober at midnight": "question",
    "My wife gifted me a creepy custom": "discussion",
    "TOP HORROR RECOMMENDATIONS IN ORDER": "recommendation",
    "R.I.P. Anne Rice": "news_and_rumors",
    "Who else wishes they could read the X-Files": "discussion",
    "Whats the most disturbing, vile book": "visceral_reaction",
    "Remember to patronize your local": "discussion",
    "A book finally scared me.": "visceral_reaction",
    "CLIVE BARKER: \"Guys! I’m here!": "news_and_rumors",
    "Request for this sub to go 'dark'": "news_and_rumors",
    "Hi, I created a Goodreads list": "recommendation",
    "I didn’t realise how many people never": "discussion",
    "Books that feel evil - I want": "question",
    "Novels about weird places that": "question",
    "Books with Christian God as the horror?": "question",
    "Can we talk about the elephant in": "discussion",
    "I hate this group...": "discussion",
    "A Short Stay in Hell is a brutal": "visceral_reaction",
    "Bury Your Gays wins 2025 Locus": "news_and_rumors",
    "\"Lolita\" is not a love story": "critical_analysis",
    "What book is so disturbing, you would": "discussion",
    "What’s your absolute favourite horror": "discussion",
    "Did Goosebumps kick off your interest": "discussion",
    "A look at R. L. Stine's daily": "news_and_rumors",
    "Looking for the scariest, and I mean": "question",
    "If you could recommend just ONE horror": "recommendation",
    "I love Darcy Coates, but she does not": "critical_analysis",
    "Just finished \"We Used To Live Here\"": "visceral_reaction",
    "R. L. Stine's (the author of Goosebumps)": "hot_take",
    "Who else is using the": "discussion",
    "Sometimes I can’t tell the difference": "discussion",
    "What is the most horrifying nonfiction": "discussion",
    "You know what I love? That creeping": "discussion",
    "Hidden Pictures is ringing alarm": "discussion"
}

rows = []
modified_count = 0
with open('dataset.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)
    for row in reader:
        text = row[0]
        # Only modify if it doesn't already have a label
        if len(row) <= 1 or not row[1]:
            matched = False
            for prefix, label in manual_mappings.items():
                if prefix in text or prefix.lower() in text.lower():
                    # Grow row if needed
                    while len(row) < 3:
                        row.append('')
                    row[1] = label
                    matched = True
                    modified_count += 1
                    break
        rows.append(row)

with open('dataset.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Applied manual labels to {modified_count} rows.")
