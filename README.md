# 🎨 Color Picker AI

Website berbasis AI yang mengekstrak warna dominan dari sebuah gambar menggunakan algoritma **K-Means Clustering**. Dibangun dengan Python dan Streamlit.

> Tugas Praktikum Artificial Intelligence

---

## 📋 Deskripsi

Color Picker AI adalah aplikasi web yang menerima input berupa gambar (JPG/JPEG/PNG) dan menghasilkan palet warna paling dominan dari gambar tersebut. Aplikasi ini menggunakan algoritma **unsupervised machine learning** yaitu K-Means Clustering untuk mengelompokkan pixel-pixel pada gambar menjadi beberapa cluster, di mana pusat tiap cluster (centroid) merepresentasikan satu warna dominan.

## ✨ Fitur

- 📤 Upload gambar (JPG, JPEG, PNG)
- 🎨 Ekstraksi 3–10 warna dominan (jumlah dapat diatur via slider)
- 🔢 Tampilan kode warna dalam format **HEX** dan **RGB**
- 🏷️ **Nama warna** otomatis (e.g. Coral, Lavender, Slategray)
- 📊 Persentase tiap warna terhadap keseluruhan gambar
- 🌈 UI dengan tema light pastel + animasi gradient & particles
- 🎴 Kartu warna dengan efek 3D tilt & hover

---

## 🧠 Algoritma AI yang Digunakan

### K-Means Clustering

K-Means adalah algoritma *unsupervised learning* yang mengelompokkan data ke dalam K cluster berdasarkan kemiripan. Dalam konteks ekstraksi warna:

1. **Representasi data**: Setiap pixel gambar dikonversi menjadi titik di ruang 3 dimensi (R, G, B).
2. **Inisialisasi**: K centroid awal dipilih (K = jumlah warna yang dicari).
3. **Iterasi**:
   - Setiap pixel dimasukkan ke cluster dengan centroid terdekat (jarak Euclidean).
   - Centroid diperbarui menjadi rata-rata pixel dalam cluster.
4. **Konvergensi**: Iterasi berhenti ketika centroid tidak berubah signifikan.
5. **Hasil**: K centroid akhir = K warna dominan.

### Mengapa K-Means?

- ✅ Sederhana, cepat, dan efektif untuk data warna RGB
- ✅ Tidak memerlukan data label (cocok untuk gambar sembarang)
- ✅ Hasil yang konsisten dengan `random_state` yang sama

---

## 🛠️ Teknologi

| Komponen | Library | Fungsi |
|----------|---------|--------|
| Framework Web | Streamlit | Membuat UI website |
| Pengolahan Gambar | Pillow (PIL) | Baca & resize gambar |
| Komputasi Array | NumPy | Manipulasi pixel sebagai array |
| Machine Learning | scikit-learn | Implementasi K-Means |
| Penamaan Warna | webcolors | Konversi RGB ke nama CSS terdekat |

---

## 🚀 Cara Menjalankan Lokal

### Prasyarat
- Python 3.8 atau lebih baru
- pip

### Instalasi

1. **Clone repository**
```bash
   git clone https://github.com/USERNAME/color-picker-ai.git
   cd color-picker-ai
```

2. **Buat virtual environment** (opsional tapi disarankan)
```bash
   python -m venv venv
   venv\Scripts\activate     # Windows
   source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Jalankan aplikasi**
```bash
   streamlit run app.py
```

5. **Buka browser** di `http://localhost:8501`

---

## 🌐 Demo Online

Aplikasi sudah di-deploy dan dapat diakses melalui:

🔗 **[LINK_AKAN_DIISI_SETELAH_DEPLOY]**

---

## 📂 Struktur Project
color-picker-ai/
│
├── app.py              # Kode utama aplikasi Streamlit
├── requirements.txt    # Daftar dependencies
├── README.md           # Dokumentasi
└── .gitignore          # File yang diabaikan Git
---

## 📖 Cara Menggunakan

1. Buka website
2. Atur jumlah warna dominan via slider (default: 5, range: 3–10)
3. Upload gambar dari komputer (drag & drop atau klik area upload)
4. Tunggu beberapa detik — sistem akan memproses dengan K-Means
5. Lihat hasil: kartu warna dengan nama, HEX, RGB, dan persentase

---

## 👤 Penulis

**Vivian Azarine**  
Praktikum Artificial Intelligence — Semester 4

---

## 📄 Lisensi

Project ini dibuat untuk keperluan akademik (tugas praktikum).