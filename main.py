from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_twitter(): #Inisiasi Fungsi 
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://twitter.com/collegemfs") # Buka Target yang mau di Scrape
    
    time.sleep(5)  # Tunggu halaman loading

    tweets_data = []
    tweet_set = set()
    scroll_attempts = 0
    max_scrolls = 50  # Percobaan maksimal untuk scroll halaman. 50 brarti 50x scroll kbawah
    
    while len(tweets_data) < 100 and scroll_attempts < max_scrolls: # Pembangun fungsi → Maks 100 Data
        tweets = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
        for tweet in tweets:
            try:
                # Ambil username
                username_elem = tweet.find_element(By.XPATH, './/div[@data-testid="User-Name"]//a')
                username = username_elem.get_attribute("href")
                username = "@" + username.split("/")[-1]

                # Ambil konten tweet
                content_element = tweet.find_element(By.XPATH, './/div[@lang]')
                content = content_element.text  

                # Ambil emoji (dari <img alt="😊">) → Tapi kyanya tara jadi ini 🤔
                emoji_elements = content_element.find_elements(By.XPATH, './/img[@alt]')
                emojis = [emoji.get_attribute("alt") for emoji in emoji_elements]

                # Ambil gambar di dalam tweet
                image_elements = tweet.find_elements(By.XPATH, './/div[@data-testid="tweetPhoto"]//img')
                images = [img.get_attribute("src") for img in image_elements]

                # Ambil tanggal postingan (dari tag <time>)
                try:
                    time_elem = tweet.find_element(By.TAG_NAME, "time")
                    posting_date = time_elem.get_attribute("datetime")
                except Exception:
                    posting_date = ""

                # Ambil hashtag dan mention dari teks
                hashtags = [word for word in content.split() if word.startswith("#")]
                mentions = [word for word in content.split() if word.startswith("@")]

                # Cegah duplikasi tweet berdasarkan konten
                if content not in tweet_set:
                    tweet_set.add(content)
                    tweets_data.append({
                        "tweet_text": content,
                        "tweet_image": ", ".join(images),
                        "username": username,
                        "tweet_count": len(tweets),
                        "hashtags": ", ".join(hashtags),
                        "mentions": ", ".join(mentions),
                        "emojis": ", ".join(emojis),
                        "posting_date": posting_date
                    })
            except Exception:
                continue

        # Scroll halaman untuk memuat tweet berikutnya
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        scroll_attempts += 1

    driver.quit()
    
    df = pd.DataFrame(tweets_data)
    df.to_csv("tweets.csv", index=False)
    return tweets_data

if __name__ == "__main__":
    data = scrape_twitter()
    print("Jumlah tweet yang berhasil di-scrape:", len(data))
    for tweet in data[:3]:
        print(tweet)
