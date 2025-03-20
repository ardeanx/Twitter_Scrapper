# Twitter Scraper

Proyek ini adalah alat Twitter Scraper yang mengambil data tweet dari akun Twitter target (misalnya, @collegemfs) tanpa menggunakan API resmi. Proyek ini menggunakan Selenium untuk mengeksekusi JavaScript pada halaman Twitter, menyimpan data yang di-scrape ke dalam SQLite, dan menyediakan antarmuka web menggunakan Flask. Selain itu, alat ini juga mendukung ekspor data ke file CSV serta memiliki opsi untuk membersihkan (clear) database dengan pengarsipan data sebelumnya.

## Fitur

- **Scraping Tweet secara Otomatis**

Menggunakan Selenium untuk mengambil tweet, gambar, emoji, hashtag, mention, dan tanggal posting tweet.

- **Penyimpanan Data ke SQLite**

Data tweet disimpan ke dalam database SQLite. Data lama tidak dihapus saat scraping baru dilakukan, dengan pengecekan duplikasi berdasarkan konten tweet.

- **Ekspor CSV**

Data tweet dapat diekspor ke file CSV dengan format yang terstruktur.

- **Antarmuka Web Sederhana**

Dibuat menggunakan Flask dan menampilkan data tweet dalam bentuk tabel. Terdapat tombol:

    - New Scrape: Memicu proses scraping baru.
    - Refresh Data: Memuat ulang data dari database.
    - Download CSV: Mengunduh file CSV.
    - Delete Database: Mengarsipkan data lama ke file CSV dan menghapus data dari database.


- **Pengarsipan Data Sebelum Clear Database**

Sebelum membersihkan database, data lama diarsipkan ke file CSV dengan penamaan berbasis timestamp.


# Persyaratan

- Python 3.10 (atau versi kompatibel lainnya)
- Flask
- Selenium
- webdriver_manager
- pandas
- SQLite (terintegrasi dengan Python melalui modul sqlite3)
- Chrome WebDriver

> (webdriver_manager akan mengelola ChromeDriver secara otomatis)

# Instalasi & Setup

1. **Clone Repository**

```bash
git clone https://github.com/username/twitter-scraper.git
cd twitter-scraper
```

2. **Buat Virtual Environment dan Install Dependency**

Buat virtual environment:

```bash
python -m venv venv
```
Aktifkan virtual environment

- **Windows:**

```bash
venv\Scripts\activate
```

- **macOS/Linux:**

```bash
source venv/bin/activate
```

Install semua dependency:

```bash
pip install -r requirements.txt
```

3. **Struktur File & Folder**

Pastikan struktur folder proyek sesuai:

```php
twitter-scraper/
├── instance/
│    └── main.db           # Database SQLite (akan dibuat otomatis)
├── templates/
│    ├── index.html        # Tampilan utama antarmuka web
│    └── clear_db_confirm.html  # Halaman konfirmasi clear database
├── static/               # (Opsional) untuk file favicon atau aset lainnya
│    └── favicon.ico
├── app.py                # Aplikasi Flask
├── main_selenium.py      # Fungsi scraping menggunakan Selenium
├── models.py             # Operasi database SQLite
├── requirements.txt      # Daftar dependency
└── README.md             # Dokumentasi proyek
```

# Cara menjalankan

1. **Inisialisasi Database**

Pastikan database telah diinisiasi. Ini biasanya dilakukan secara otomatis saat aplikasi Flask dijalankan, karena fungsi `init_db()` dipanggil di `app.py`.

2. **Jalankan Aplikasi Flask**

Dari root folder, jalankan:

```bash
python app.py
```

3. **Akses Antarmuka Web**

Buka browser dan arahkan ke [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

4. **Fungsi Endpoint**

- **New Scrape**

Tekan tombol "New Scrape" untuk memicu proses scraping. Data yang baru diambil akan disimpan ke database jika tidak terduplikasi.

- **Refresh Data:**

Tekan tombol "Refresh Data" untuk memuat ulang data dari database.

- **Download CSV:**

Tekan tombol "Download CSV" untuk mengunduh file CSV yang berisi data tweet.

- **Delete Database:**

Tekan tombol `Delete Database` untuk membuka halaman konfirmasi. Jika dikonfirmasi, data lama akan diarsipkan ke file CSV dengan nama berbasis timestamp, lalu database dibersihkan.

# Konfigurasi Penyesuaian

- **Scraping dengan Selenium:**

Fungsi `scrape_twitter()` di `main.py` telah dikonfigurasi untuk menggunakan opsi headless pada Chrome. Anda dapat menyesuaikan waktu tunggu `(time.sleep())` atau batas scroll (`max_scrolls`) sesuai dengan kebutuhan untuk mendapatkan jumlah tweet yang diinginkan.

- **Pencegahan Duplikasi:**

Fungsi `insert_tweet()` di `models.py` melakukan pengecekan berdasarkan tweet_text sebelum menyimpan data baru ke database.

- **Penambahan Parameter Posting Date:**

Data tweet yang di-scrape sekarang mencakup tanggal posting, yang diambil dari elemen `<time>` pada halaman tweet. Parameter ini juga ditampilkan di antarmuka web dan disimpan di database.

# Troubleshooting

1 **Duplikasi Data:**

Jika terjadi duplikasi, periksa fungsi pengecekan di `models.insert_tweet()` dan pastikan nilai tweet_text unik.

2 **Scraping Gagal / Data Kosong:**

Jika hasil scraping tidak sesuai, periksa:
  - Struktur HTML Twitter (yang mungkin telah berubah).
  - Waktu tunggu (time.sleep) yang cukup untuk memuat halaman.
  - Pastikan ChromeDriver terinstall dengan benar melalui webdriver_manager.

3  **Error Dependency:**

Jika terjadi masalah kompatibilitas antara numpy dan pandas, coba perbarui kedua paket tersebut atau reinstall sesuai versi yang kompatibel.

# Penutup

Dokumentasi ini diharapkan dapat membantu Anda memahami dan menjalankan proyek Twitter Scraper dengan baik. Jangan ragu untuk menyesuaikan dan mengembangkan fitur-fitur tambahan sesuai kebutuhan.

- Email: ardeanbimasaputra@gmail.com
- Instagram: [@ardeanbimasaputra](https://instagram.com/ardeanbimasaputra)