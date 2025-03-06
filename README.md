---

# ⚡ Analisis Losses dan Tegangan pada Jaringan Distribusi

Aplikasi ini digunakan untuk menganalisis losses dan profil tegangan pada jaringan distribusi di wilayah UP3 Semarang. Pengguna dapat memilih daerah yang diinginkan untuk melihat hasil perhitungan analisis tegangan dan losses, serta melakukan simulasi pengurangan losses dalam periode bulanan.

## Deskripsi Aplikasi

Aplikasi ini menyediakan beberapa fitur utama:

1. **Analisis Tegangan**: Menampilkan tegangan akhir pada node-node dalam jaringan distribusi, serta parameter jaringan seperti matriks admitansi (Ybus) dan beban di setiap node.
2. **Analisis Losses**: Menampilkan perbandingan losses (kWh) sebelum dan setelah optimasi, serta persentase losses terhadap daya yang dikirim.
3. **Simulasi Pengurangan Losses Bulanan**: Menampilkan proyeksi pengurangan losses dalam periode bulanan berdasarkan pengurangan 15% per bulan.

## Fitur Aplikasi

- **Pilih Daerah**: Pengguna dapat memilih salah satu dari tiga daerah: 
  - **UP3 Semarang**
  - **Boja**
  - **Semarang Timur**

- **Tab Hasil Perhitungan**: Menampilkan tegangan akhir pada jaringan distribusi dan parameter jaringan yang relevan.
- **Tab Analisis Losses**: Menampilkan grafik perbandingan losses dan persentase losses.
- **Tab Simulasi Bulanan**: Menampilkan simulasi pengurangan losses secara bertahap selama 12 bulan.

## Struktur Data

Aplikasi ini menggunakan data berikut untuk analisis:

- **Matriks Admitansi (Ybus)**: Matriks admitansi jaringan distribusi untuk masing-masing daerah.
- **P_load dan Q_load**: Beban aktif dan reaktif pada setiap node.
- **V_initial**: Tegangan awal pada setiap node.
- **Losses**: Nilai losses awal dan setelah optimasi untuk setiap daerah.

## Cara Penggunaan

1. Install dependensi dengan menggunakan `pip`:
   ```bash
   pip install streamlit numpy pandas matplotlib
   ```

2. Jalankan aplikasi dengan perintah:
   ```bash
   streamlit run app.py
   ```

3. Pilih daerah dari sidebar untuk melihat hasil analisis dan simulasi.

## Informasi Daerah

### 1. **UP3 Semarang**
   - Wilayah pelayanan distribusi listrik di Kota Semarang.
   - Beban node: 0 kW, 180 kW (Node 1, Node 2).

### 2. **Boja**
   - Kecamatan di Kabupaten Kendal dengan beban industri.
   - Beban node: 0 kW, 250 kW (Node 1, Node 2).

### 3. **Semarang Timur**
   - Wilayah padat penduduk dengan kebutuhan komersial tinggi.
   - Beban node: 0 kW, 200 kW (Node 1, Node 2).

## Dependencies

- **Streamlit**: Untuk membuat aplikasi web interaktif.
- **NumPy**: Untuk perhitungan numerik.
- **Pandas**: Untuk pengolahan data dan tabel.
- **Matplotlib**: Untuk membuat grafik visualisasi.

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, silakan fork repository ini dan buat pull request dengan perubahan atau perbaikan yang diusulkan.

## Lisensi

Proyek ini menggunakan lisensi MIT - lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.

---
