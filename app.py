from flask import Flask, render_template, redirect, url_for, send_file, request
import models
from main import scrape_twitter  # pastikan ini mengacu ke fungsi scraping terbaru
import csv
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    tweets = models.get_all_tweets()
    return render_template('index.html', tweets=tweets)

# Endpoint Scrape → Endpoint ini maksudnya routing sistem untuk cek + event apakah sudah di tekan/berjalan atau belum
@app.route('/scrape', methods=['POST'])
def new_scrape():
    data = scrape_twitter()
    for tweet in data:
        models.insert_tweet({
            'tweet_text': tweet["tweet_text"],
            'tweet_image': tweet["tweet_image"],
            'username': tweet["username"],
            'tweet_count': tweet["tweet_count"],
            'hashtags': tweet["hashtags"],
            'mentions': tweet["mentions"],
            'emojis': tweet["emojis"],
            'posting_date': tweet["posting_date"]
        })
    return redirect(url_for('index'))

# Endpoint download
@app.route('/download', methods=['GET'])
def download_csv():
    tweets = models.get_all_tweets()
    csv_file = 'tweets.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Tweet Text', 'Tweet Image', 'Username', 'Tweet Count', 'Hashtags', 'Mentions', 'Emojis', 'Posting Date', 'Scrape Time'])
        for row in tweets:
            writer.writerow(row)
    return send_file(csv_file, as_attachment=True)

# Endpoint clear_db
@app.route('/clear_db', methods=['GET', 'POST'])
def clear_db():
    if request.method == 'POST':
        tweets = models.get_all_tweets()
        if tweets:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_filename = f"tweets_archive_{timestamp}.csv"
            with open(archive_filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Tweet Text', 'Tweet Image', 'Username', 'Tweet Count', 'Hashtags', 'Mentions', 'Emojis', 'Posting Date', 'Scrape Time'])
                for row in tweets:
                    writer.writerow(row)
        models.clear_tweets()
        return redirect(url_for('index'))
    return render_template('clear_db_confirm.html')

if __name__ == '__main__':
    models.init_db()
    app.run(debug=True)