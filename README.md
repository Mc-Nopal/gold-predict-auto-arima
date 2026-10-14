# 🪙 Gold Predict with Auto ARIMA & Streamlit

> Aplikasi web interaktif berbasis Python untuk melakukan analisis data historis dan peramalan (_forecasting_) harga emas masa depan menggunakan algoritma **Auto ARIMA**, lengkap dengan konversi otomatis mata uang dan satuan berat.

---

## 🚀 Fitur Utama

- **Antarmuka Modern (Streamlit):** Dibangun dengan desain layout yang bersih, responsif, dan berpusat di tengah layar.
- **Data Historis Efisien (`yfinance`):** Mengambil data historis harga emas dunia dan kurs mata uang secara langsung tanpa memerlukan API Key atau risiko kuota habis (_rate-limit_).
- **Peramalan Cerdas (Auto ARIMA):** Menggunakan pustaka `pmdarima` untuk secara otomatis mencari parameter optimal ($p, d, q$) guna memprediksi tren harga emas.
- **Konversi Otomatis:** Mengubah satuan internasional dari _Troy Ounce_ ($oz$) ke Harga per Gram ($gram$) serta konversi mata uang pilihan (**USD** / **IDR**).
- **Indikator Tren & Akurasi:** Dilengkapi dengan perhitungan tingkat akurasi model berbasis MAPE serta indikator kenaikan/penurunan harga secara visual.

---

## 🛠️ Tech Stack

- **Python** (Bahasa Pemrograman Utama)
- **Streamlit** (Framework Web UI)
- **Pandas & NumPy** (Pengolahan & Manipulasi Data)
- **yfinance** (Sumber Data Pasar Keuangan)
- **pmdarima / Statsmodels** (Model Statistik Time-Series / Auto ARIMA)

---

## 📂 Struktur Direktori Proyek

```text
gold-predict-arima/
│
├── main.py            # File utama antarmuka Streamlit (UI)
├── function.py        # Logika pengambilan data yfinance & model Auto ARIMA
├── requirements.txt   # Daftar dependensi / library proyek
└── .gitignore         # Konfigurasi file/folder yang diabaikan oleh Git
```

## ⚙️ Cara Instalasi dan Menjalankan (Lokal)

1. Clone repository

```
   git clone https://github.com/Mc-Nopal/gold-predict-arima.git
   cd gold-predict-arima
```

2. Buat dan Aktifkan Virtual Environment (Opsional tapi Disarankan):

```
   python -m venv venv
```

- Windows:

```
venv\Scripts\activate
```

- macOS/Linux:

```
source venv/bin/activate
```

3. Install Semua Dependencies:

```
pip install -r requirements.txt
```

4. Jalankan Aplikasi Streamlit:

```
streamlit run main.py
```

5. Buka tautan http://localhost:8501 yang muncul di terminal melalui web browser.

📈 Cara Penggunaan

1. Tentukan Banyak Data Historis (Hari) menggunakan slider (rentang 50 hingga 100 hari ke belakang).
2. Tentukan Banyak Hari Prediksi yang diinginkan ke depan (1 s.d. 30 hari).
3. Pilih Mata Uang Konversi (USD atau IDR).
4. Klik tombol "Jalankan Prediksi 🚀".
5. Lihat hasil metrik akurasi, kartu tren kenaikan/penurunan, diagram grafik interaktif, serta tabel detail angka prediksi.

👤 Author
Naufal — github.com/Mc-Nopal

✨ Jika proyek ini bermanfaat, jangan lupa berikan ⭐ pada repository ini!
