import praw
from textblob import TextBlob

# Step 1: Connect to Reddit API
reddit = praw.Reddit(
    client_id="XK0lWyVnNbeo7eJuVPAvSQ",
    client_secret="y9wOANl5vvqxvpvmGOefQb6XYUmlIA",  # <- Complete this exactly from your screen
    user_agent="user_persona_app by chakru"
)

# Step 2: Ask for Reddit username
username = input("Enter Reddit username (not full URL): ")
user = reddit.redditor(username)

# Step 3: Get user posts and comments
comments = []
posts = []

try:
    for comment in user.comments.new(limit=20):
        comments.append(comment.body)

    for submission in user.submissions.new(limit=10):
        posts.append(submission.title + "\n" + (submission.selftext or ""))
except Exception as e:
    print("Error:", e)
    exit()

# Step 4: Analyze using TextBlob
def analyze_text(texts):
    combined = " ".join(texts)
    blob = TextBlob(combined)
    return {
        "keywords": blob.noun_phrases[:10],
        "sentiment": blob.sentiment.polarity
    }

comment_analysis = analyze_text(comments)
post_analysis = analyze_text(posts)

# Step 5: Build persona text
persona = f"""
Reddit User Persona for: {username}

Top Comment Keywords: {comment_analysis['keywords']}
Comment Sentiment Score: {comment_analysis['sentiment']}

Top Post Keywords: {post_analysis['keywords']}
Post Sentiment Score: {post_analysis['sentiment']}

Likely Interests: {comment_analysis['keywords'] + post_analysis['keywords']}
Tone: {"Positive" if (comment_analysis['sentiment'] + post_analysis['sentiment'])/2 > 0 else "Negative or Neutral"}

Sample Comment Used:
{comments[0] if comments else "No comment found"}

Sample Post Used:
{posts[0] if posts else "No post found"}
"""

# Step 6: Save to file
with open(f"{username}_persona.txt", "w", encoding='utf-8') as f:
    f.write(persona)

print("✅ User persona saved to text file!")

