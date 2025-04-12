
# Take Home Assignment - Backend (Katekima)

## 📁 Struktur Folder

```
.
├── README.md
├── Assignment 1/           # Implementasi LFSR menggunakan Python
└── Assignment 2/           # Sistem API Django untuk manajemen stok gudang
```

---

## 🧠 Assignment 1: Linear Feedback Shift Register (LFSR)

### 🔍 Deskripsi
Implementasi LFSR sederhana dan umum yang bisa dikonfigurasi. Tugas ini melatih pemahaman tentang stream cipher pada sistem kriptografi.

### 📌 Fitur
- **Basic LFSR:**
  - Inisialisasi state awal (misalnya `0110`)
  - Menampilkan state dan stream bit sebanyak 20 kali
- **General LFSR:**
  - Register size dinamis
  - Tap sequence dapat diatur (XOR index)
  - Reset dan update state
  - Output stream bit yang sesuai dengan konfigurasi

---

## 🏬 Assignment 2: Stock Warehouse REST API

### 🔍 Deskripsi
Aplikasi Django REST API untuk sistem gudang yang mencakup modul Items, Purchases, Sells, dan laporan perubahan stok.

### 🧱 Modul & Endpoint

#### 1. Items
- `GET /items/` – List semua item
- `GET /items/{code}` – Detail item
- `POST /items/` – Tambah item
- `PUT /items/{code}` – Update item
- `DELETE /items/{code}` – Soft delete item

#### 2. Purchases
- `GET /purchase/` – Semua pembelian
- `POST /purchase/` – Tambah pembelian (header)
- `POST /purchase/{code}/details/` – Tambah detail pembelian (update stok dan saldo)

#### 3. Sells
- `GET /sell/` – Semua penjualan
- `POST /sell/` – Tambah penjualan (header)
- `POST /sell/{code}/details/` – Tambah detail penjualan (kurangi stok & saldo sesuai FIFO)

#### 4. Reporting
- `GET /report/{item_code}/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` – Laporan perubahan stok dalam rentang waktu

### 🛠️ Tech Stack
- python
- Django
- Django REST Framework
- SQLite

---

## 📝 Catatan
- Semua operasi delete menggunakan metode **soft delete** (mengubah `is_deleted`).
- Laporan stok menghitung berdasarkan FIFO, mengikuti urutan pembelian saat melakukan penjualan.