# proyek-analisis-data
Olist E-Commerce Data Analysis Dashboard using Streamlit (RFM, Geospatial, and Delivery Performance Analysis)

## Brazilian E-Commerce Data Analysis Project

### Deskripsi
Proyek ini merupakan analisis data dataset Olist E-Commerce dengan fokus pada Segmentasi Pelanggan (RFM Analysis), Distribusi Geospasial, serta hubungan antara Kualitas Produk dan Performa Logistik. Dashboard ini dibuat untuk memberikan insight strategis bagi tim bisnis dalam meningkatkan retensi pelanggan.

### Struktur Direktori
- **/dashboard**: Berisi file aplikasi Streamlit (`dashboard.py`) dan data yang telah dibersihkan (`main_data.csv`).
- **/data**: Berisi dataset mentah (raw data) dalam format CSV.
- **notebook.ipynb**: File proses analisis data mulai dari Wrangling, EDA, hingga Visualisasi.
- **requirements.txt**: Daftar library Python yang dibutuhkan.

### Cara Menjalankan Dashboard
#### 1. Persiapan Lingkungan (Local)
Pastikan Anda memiliki Python terinstal, lalu buat virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Untuk Windows: venv\Scripts\activate
```

#### 2. Instalasi Library
Instal semua dependensi yang diperlukan:
```bash
pip install -r requirements.txt
```

#### 3. Menjalankan Aplikasi
Masuk ke direktori utama proyek dan jalankan perintah berikut:
```bash
streamlit run dashboard/dashboard.py
```

## Penulis
Nalitha Eka Naswadyna
