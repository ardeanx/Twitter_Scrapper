import sqlite3
from datetime import datetime

DB_PATH = 'instance/main.db' # PATH ke database → Ini pake SQLite

def init_db(): # Inisiasi Fungsi model
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tweet_text TEXT,
            tweet_image TEXT,
            username TEXT,
            tweet_count INTEGER,
            hashtags TEXT,
            mentions TEXT,
            emojis TEXT,
            posting_date TEXT,
            scrape_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_tweet(data): # Fungsi untuk memasukkan data ke database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Cek apakah tweet sudah ada berdasarkan tweet_text
    c.execute('SELECT id FROM tweets WHERE tweet_text = ?', (data['tweet_text'],))
    exists = c.fetchone()
    if exists:
        conn.close()
        return
    c.execute('''
        INSERT INTO tweets (tweet_text, tweet_image, username, tweet_count, hashtags, mentions, emojis, posting_date, scrape_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['tweet_text'],
        data['tweet_image'],
        data['username'],
        data['tweet_count'],
        data['hashtags'],
        data['mentions'],
        data.get('emojis', ""),
        data.get('posting_date', ""),  # data posting_date
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

def get_all_tweets():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM tweets ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def clear_tweets():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM tweets')
    conn.commit()
    conn.close()
