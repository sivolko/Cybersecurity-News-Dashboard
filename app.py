import streamlit as st
import feedparser
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from collections import Counter
import re

# Function to fetch and parse RSS feeds
def fetch_feed(url):
    return feedparser.parse(url)

# Default list of RSS feed URLs
default_rss_feeds = {
    'Bleeping Computer': 'https://social.cyware.com/allnews/feed',
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews',
    # Add more default RSS feed URLs here
}

# Streamlit app
st.title('Cybersecurity News Dashboard')

# RSS Feed Management
st.sidebar.title('Manage RSS Feeds')
rss_feeds = st.sidebar.text_area('Enter RSS feed URLs (one per line)', '\n'.join(default_rss_feeds.values()))
rss_feeds = rss_feeds.split('\n')
rss_feed_names = [f'Feed {i+1}' for i in range(len(rss_feeds))]

# Fetch and combine all feeds
all_entries = []
for i, url in enumerate(rss_feeds):
    feed = fetch_feed(url)
    for entry in feed.entries:
        entry['source'] = rss_feed_names[i]
    all_entries.extend(feed.entries)

# Convert entries to DataFrame
data = {
    'Title': [entry.title for entry in all_entries],
    'Link': [entry.link for entry in all_entries],
    'Date': [entry.published for entry in all_entries],
    'Summary': [entry.summary for entry in all_entries],
    'Source': [entry.source for entry in all_entries]
}
df = pd.DataFrame(data)

# Convert Date column to datetime and handle errors
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Sentiment Analysis
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

df['Sentiment'] = df['Summary'].apply(get_sentiment)

# Keyword Extraction
def extract_keywords(text):
    words = re.findall(r'\w+', text.lower())
    return [word for word in words if len(word) > 3]

df['Keywords'] = df['Summary'].apply(extract_keywords)

# Trending Topics
all_keywords = [keyword for keywords in df['Keywords'] for keyword in keywords]
trending_topics = Counter(all_keywords).most_common(10)

# Pagination
items_per_page = 10
total_pages = max((len(df) - 1) // items_per_page + 1, 1)
page = st.slider('Page', 1, total_pages, 1)

start_idx = (page - 1) * items_per_page
end_idx = start_idx + items_per_page
paginated_df = df.iloc[start_idx:end_idx]

# Display news articles in a side-by-side block layout
for i in range(0, len(paginated_df), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(paginated_df):
            with cols[j]:
                row = paginated_df.iloc[i + j]
                st.subheader(row['Title'])
                st.write(row['Summary'])
                st.markdown(f"[Read more]({row['Link']})")
                st.write(f"Published on: {row['Date']}")
                st.write(f"Sentiment: {'Positive' if row['Sentiment'] > 0 else 'Negative' if row['Sentiment'] < 0 else 'Neutral'}")
                st.markdown("---")

# Visualization: Number of articles per source
source_counts = df['Source'].value_counts()
fig, ax = plt.subplots()
source_counts.plot(kind='bar', ax=ax)
ax.set_title('Number of Articles per Source')
ax.set_xlabel('Source')
ax.set_ylabel('Number of Articles')
st.pyplot(fig)

# Visualization: Trending Topics
fig, ax = plt.subplots()
topics, counts = zip(*trending_topics)
ax.bar(topics, counts)
ax.set_title('Trending Topics')
ax.set_xlabel('Topic')
ax.set_ylabel('Count')
st.pyplot(fig)

# Add some custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #2e2e2e;
        color: white;
    }
    .stTextInput {
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
        color: black;
    }
    .stButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }
    .stMarkdown h2 {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
