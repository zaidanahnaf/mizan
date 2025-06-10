# ⚙️ Panduan Setup & Instalasi Proyek Mīzān

Dokumen ini berisi panduan teknis langkah demi langkah untuk melakukan instalasi dan setup proyek Mīzān di lingkungan pengembangan lokal.

## 1. Prasyarat

Pastikan perangkat Anda telah terinstal perangkat lunak berikut:

- **Python**: Versi 3.9 atau yang lebih baru.
- **pip**: Packet installer untuk Python (biasanya sudah terinstal bersama Python).
- **Git**: Untuk meng-clone repositori.

## 2. Langkah-langkah Instalasi

Ikuti langkah-langkah berikut secara berurutan di dalam terminal atau command prompt Anda.

#### Langkah A: Clone Repositori
Buka terminal, arahkan ke direktori tempat Anda ingin menyimpan proyek, lalu jalankan perintah berikut:
```bash
git clone [https://github.com/zaidanahnaf/Mīzān.git](https://github.com/zaidanahnaf/Mīzān.git)
cd Mīzān
```

#### Langkah B: Buat dan Aktifkan Virtual Environment
Sangat penting untuk membuat lingkungan terisolasi agar tidak mengganggu instalasi Python utama di sistem Anda.

```bash
# 1. Buat folder virtual environment bernama 'venv'
python -m venv venv

# 2. Aktifkan environment tersebut
# Untuk Windows (PowerShell):
.\venv\Scripts\activate

# Untuk macOS/Linux:
source venv/bin/activate
```
**Verifikasi:** Setelah aktivasi berhasil, Anda akan melihat `(venv)` di awal baris terminal Anda.

#### Langkah C: Instal Semua Dependensi
Gunakan file `requirements.txt` untuk menginstal semua pustaka Python yang dibutuhkan oleh proyek dengan satu perintah.
```bash
pip install -r requirements.txt
```
Tunggu hingga proses download dan instalasi semua pustaka (seperti Flask, scikit-fuzzy, pandas, dll.) selesai.

#### Langkah D: Jalankan Aplikasi
Setelah semua dependensi terinstal, Anda siap menjalankan server Flask.
```bash
python app.py
```
**Verifikasi:** Anda akan melihat output di terminal yang menandakan server berjalan, biasanya diakhiri dengan baris seperti ini:
```
* Running on [http://127.0.0.1:5000](http://127.0.0.1:5000)
```

#### Langkah E: Buka di Browser
Buka browser web Anda (Chrome, Firefox, dll.) dan kunjungi alamat `http://127.0.0.1:5000`. Aplikasi Mīzān Anda seharusnya sudah berjalan.

## 3. Panduan Troubleshooting (Mengatasi Masalah Umum)

Berikut adalah beberapa masalah umum yang mungkin terjadi saat proses setup beserta solusinya.

#### Masalah 1: `ModuleNotFoundError: No module named 'numpy'` (atau pustaka lain)
- **Penyebab:** Anda menjalankan `python app.py` tanpa mengaktifkan virtual environment `(venv)` terlebih dahulu, atau proses `pip install -r requirements.txt` belum dijalankan.
- **Solusi:** Pastikan Anda melihat `(venv)` di terminal Anda. Jika tidak, jalankan perintah aktivasi (Langkah B). Setelah itu, jalankan kembali `pip install -r requirements.txt`.

#### Masalah 2: Error "running scripts is disabled on this system" di PowerShell
- **Penyebab:** Kebijakan eksekusi (Execution Policy) di PowerShell Windows secara default memblokir skrip.
- **Solusi:** Jalankan perintah ini di PowerShell untuk mengizinkan eksekusi skrip hanya pada sesi terminal saat ini (ini aman).
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
  ```
  Setelah itu, coba aktifkan kembali venv dengan `.\venv\Scripts\activate`.

#### Masalah 3: Error `Can't find a usable init.tcl`
- **Penyebab:** Pustaka `matplotlib` mencoba menggunakan backend grafis `TkAgg` yang instalasinya mungkin rusak di sistem Anda.
- **Solusi:** Proyek ini sudah diatur untuk menggunakan backend `Agg` yang tidak memerlukan GUI. Pastikan dua baris kode ini ada di bagian paling atas file `visualization.py` dan `evaluator.py`, **sebelum** `import matplotlib.pyplot as plt`.
  ```python
  import matplotlib
  matplotlib.use('Agg')
  ```

## 4. Struktur Proyek

Berikut adalah penjelasan singkat mengenai file-file utama dalam proyek ini:

- `app.py`: Server utama Flask. Mengatur semua rute (routing) dan API endpoint.
- `fuzzy_system.py`: Inti dari kecerdasan buatan. Berisi definisi sistem fuzzy, fungsi keanggotaan, dan aturan (rules).
- `evaluator.py`: Kelas untuk melakukan evaluasi performa model terhadap dataset.
- `visualization.py`: Fungsi untuk membuat visualisasi grafik fungsi keanggotaan.
- `budget.csv`: Dataset yang digunakan untuk menguji akurasi model.
- `requirements.txt`: Daftar semua dependensi pustaka Python.
- `/templates`: Folder berisi semua file HTML.
- `/static`: Folder berisi semua file statis seperti CSS dan JavaScript.