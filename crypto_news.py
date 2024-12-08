import tkinter as tk
from tkinter import scrolledtext
import feedparser
from datetime import datetime
import time

# Function to fetch news from RSS feeds
def get_crypto_news():
    urls = [
        'https://cointelegraph.com/rss',
        'https://blog.coinjar.com/rss/',
        'https://wundertrading.com/buy-crypto/en/rss',
        'https://tsakf.org/feed/rss',
        'https://www.marcowutzer.com/blog/rss/',
        'https://multicoin.capital/rss.xml',
        'https://coinidol.com/rss2/',
        'https://bitrss.com/rss.xml',
        'https://www.bitdegree.org/crypto/news/rss',
        'https://blog-eu.bitflyer.com/rss/',
        'https://bitpay.com/blog/rss/',
        'https://u.today/rss',
        'https://blockchain.news/rss',
        'https://komodoplatform.com/en/blog/rss/',
        'https://bravenewcoin.com/rss/insights',
        'https://www.bitrates.com/feed/rss',
        'https://blog.bake.io/rss/',
        'https://plezna.com/rss/',
        'https://blog.localcoinswap.com/rss/',
        'https://vestorportal.com/rss/',
        'https://cryptodefix.com/rss?type=&tag='
    ]
    
    news_list = []
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            published_time = entry.get('published_parsed', None)
            time_difference = get_time_difference(published_time) if published_time else None
            news_list.append({'title': title, 'link': link, 'time_difference': time_difference})
    
    # Sorting news by time difference (None values go to the end)
    news_list.sort(key=lambda x: x['time_difference'] if x['time_difference'] is not None else datetime.max - datetime.now())
    
    return news_list

# Function to calculate the time difference from when the news was published
def get_time_difference(published_time):
    now = datetime.now()
    published_datetime = datetime.fromtimestamp(time.mktime(published_time))
    time_difference = now - published_datetime
    return time_difference

# Function to format the time difference in a human-readable way
def format_time_difference(time_difference):
    if time_difference is None:
        return "unknown time"
    
    days = time_difference.days
    seconds = time_difference.seconds

    if days > 0:
        return f"{days} days ago"
    elif seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minutes ago"
    else:
        hours = seconds // 3600
        return f"{hours} hours ago"

# Function to display the news in the GUI
def show_news():
    news_textbox.delete(1.0, tk.END)  # Clear previous news
    articles = get_crypto_news()  # Fetch new news articles
    for article in articles:
        title = article['title']
        link = article['link']
        time_difference = article['time_difference']
        formatted_time_difference = format_time_difference(time_difference)

        # Insert news title, time difference, and link into the text box
        news_textbox.insert(tk.END, f"Title: {title}\n")
        news_textbox.insert(tk.END, f"Time: {formatted_time_difference}\n")
        news_textbox.insert(tk.END, f"Link: {link}\n")
        news_textbox.insert(tk.END, "-"*50 + "\n")

# Creating the GUI window
window = tk.Tk()
window.title("Crypto News")

# Creating the scrollable text box to display the news
news_textbox = scrolledtext.ScrolledText(window, width=100, height=30)
news_textbox.pack(padx=10, pady=10)

# Creating the button to refresh the news
refresh_button = tk.Button(window, text="Refresh News", command=show_news)
refresh_button.pack(pady=10)

# Load the news initially
show_news()

# Start the GUI event loop
window.mainloop()
