# ⚖️ Mīzān: Sistem Analisis Impulsivitas Berbasis AI
<!-- # ⚖️ Mīzān: Your AI Financial Guardian -->

**Mīzān** (ميزان) adalah sebuah sistem aplikasi web cerdas dan interaktif yang dirancang untuk menjadi asisten keuangan pribadi Anda. Dengan memanfaatkan **Sistem Inferensi Fuzzy (FIS) Mamdani**, aplikasi ini tidak hanya mengklasifikasikan tingkat impulsivitas sebuah transaksi belanja, tetapi juga memberdayakan pengguna dengan menyediakan **umpan balik, visualisasi data, dan dasbor analisis riwayat** untuk membantu mereka memahami serta meningkatkan kebiasaan belanja mereka.

Proyek ini menggabungkan teori kecerdasan buatan dengan pengalaman pengguna yang intuitif untuk memberikan wawasan finansial yang praktis dan dapat ditindaklanjuti, membantu pengguna mencapai "mizan" atau keseimbangan dalam keuangan mereka.

## ✨ Fitur Utama

- **Analisis Tingkat Impulsif:** Memberikan penilaian (*Tidak Impulsif*, *Cukup Impulsif*, *Sangat Impulsif*) untuk sebuah transaksi berdasarkan:
    - **Rasio Pengeluaran:** Perbandingan antara pengeluaran aktual dan budget ideal.
    - **Frekuensi Belanja:** Seberapa sering transaksi tersebut dilakukan dalam sebulan.
    - **Kategori Barang:** Apakah barang tersebut kebutuhan primer atau keinginan tersier.
- **Visualisasi Logika AI:** Pengguna dapat melihat grafik fungsi keanggotaan (membership functions) secara interaktif untuk memahami bagaimana AI "berpikir" dan mengambil keputusan untuk setiap prediksi.
- **Evaluasi Performa Model:** Menjalankan pengujian model AI terhadap dataset `budget.csv` untuk mengukur performa secara objektif menggunakan metrik klasifikasi standar:
    - Akurasi
    - Mean Absolute Error (MAE)
    - Confusion Matrix
    - Distribusi Error
- **Dasbor Analisis Riwayat:** Menyajikan ringkasan visual dari semua transaksi yang telah disimpan oleh pengguna, termasuk:
    - KPI (Key Performance Indicators) finansial (total pengeluaran, total budget).
    - Grafik *Pie Chart* untuk distribusi pengeluaran berdasarkan kategori (Primer vs. Tersier).
    - Grafik *Bar Chart* untuk distribusi tingkat impulsivitas dari transaksi yang disimpan.
- **Penyimpanan Lokal:** Riwayat transaksi disimpan di `localStorage` browser, memungkinkan data tetap ada bahkan setelah halaman di-refresh.

## 🛠️ Teknologi yang Digunakan

- **Backend:**
    - **Python 3**
    - **Flask:** Sebagai web framework.
    - **scikit-fuzzy:** Untuk implementasi logika fuzzy (FIS Mamdani).
    - **NumPy & Pandas:** Untuk komputasi numerik dan manipulasi data.
    - **Matplotlib:** Untuk membuat visualisasi performa model dan fungsi keanggotaan.
- **Frontend:**
    - **HTML5**
    - **CSS3** (Vanilla CSS)
    - **JavaScript** (Vanilla JS)
    - **Font Awesome:** Untuk ikon.

## 🚀 Cara Menjalankan Proyek

Pastikan Anda sudah memiliki **Python 3** terinstal di sistem Anda.

1.  **Clone Repositori Ini**
    ```bash
    git clone [https://github.com/zaidanahnaf/Mīzān.git](https://github.com/zaidanahnaf/Mīzān.git)
    cd Mīzān
    ```

2.  **Buat dan Aktifkan Virtual Environment**
    Ini sangat direkomendasikan untuk menjaga dependensi proyek tetap terisolasi.
    ```bash
    # Membuat venv
    python -m venv venv

    # Mengaktifkan venv (Windows - PowerShell)
    .\venv\Scripts\activate

    # Mengaktifkan venv (macOS/Linux)
    source venv/bin/activate
    ```
    Anda akan melihat `(venv)` di awal baris terminal jika berhasil.

3.  **Instal Semua Pustaka yang Dibutuhkan**
    Jalankan perintah berikut untuk menginstal semua pustaka yang ada di file `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi Flask**
    Setelah semua instalasi selesai, jalankan aplikasi utama.
    ```bash
    python app.py
    ```

5.  **Buka Aplikasi di Browser**
    Buka browser web Anda dan kunjungi alamat berikut:
    [**http://127.0.0.1:5000**](http://127.0.0.1:5000)

Aplikasi **Mīzān** Anda kini siap digunakan!

## API Endpoints

Aplikasi ini memiliki beberapa API endpoint yang bisa diakses:

- `POST /api/predict`: Menerima data formulir dan mengembalikan hasil prediksi impulsivitas.
- `POST /api/visualize_memberships`: Menerima data input dan mengembalikan gambar plot fungsi keanggotaan.
- `GET /api/evaluate_model`: Menjalankan evaluasi model menggunakan `budget.csv` dan mengembalikan metrik beserta plot performa.

---