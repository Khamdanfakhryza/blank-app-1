import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("⚡ Simulasi Pengurangan Losses dan Analisis Tegangan pada Jaringan Distribusi")
st.markdown("""
**Aplikasi ini mensimulasikan pengurangan losses (rugi-rugi daya) dan analisis tegangan pada jaringan distribusi listrik menggunakan metode Gauss-Seidel.**
""")

# --- Informasi Daerah ---
st.sidebar.title("Informasi Daerah")
st.sidebar.markdown("""
### **1. Boja**
Boja adalah sebuah kecamatan di Kabupaten Kendal, Jawa Tengah. Daerah ini termasuk dalam wilayah layanan **UP3 Semarang**, yang mengelola distribusi listrik di wilayah Semarang dan sekitarnya. 
Boja memiliki beban listrik yang cukup signifikan karena aktivitas industri dan rumah tangga.

### **2. Semarang Timur**
Semarang Timur adalah salah satu kecamatan di Kota Semarang yang termasuk dalam wilayah layanan **ULP (Unit Layanan Pelanggan) Semarang Timur**. 
Daerah ini memiliki jaringan distribusi listrik yang padat karena kepadatan penduduk dan aktivitas komersial.

### **3. UP3 Semarang**
UP3 (Unit Pelaksana Pelayanan Pelanggan) Semarang adalah unit operasional PLN yang bertanggung jawab atas distribusi listrik di wilayah Semarang, termasuk Boja dan Semarang Timur. 
UP3 Semarang berfokus pada optimasi jaringan untuk mengurangi losses dan meningkatkan keandalan pasokan listrik.
""")

# --- Input Data ---
st.header("📊 Input Data Jaringan")

# Data impedansi saluran (matriks admitansi Ybus)
st.subheader("Matriks Admitansi (Ybus)")
Ybus = np.array([[complex(12, -6), complex(-6, 3)],
                 [complex(-6, 3), complex(10, -4)]])
st.write(Ybus)

# Data beban
st.subheader("Beban pada Setiap Node (P dan Q)")
P_load = np.array([0, 250])  # kW
Q_load = np.array([0, 120])  # kVAR
st.write("P (kW):", P_load)
st.write("Q (kVAR):", Q_load)

# Tegangan awal
st.subheader("Tegangan Awal pada Setiap Node")
V = np.array([complex(1, 0), complex(0.98, 0.02)])
st.write("Tegangan Awal (pu):", V)

# --- Metode Gauss-Seidel ---
def gauss_seidel(Ybus, P_load, Q_load, V, tol=1e-6, max_iter=1000):
    """
    Menghitung tegangan pada setiap bus menggunakan metode Gauss-Seidel.
    """
    num_bus = len(V)
    for iteration in range(max_iter):
        V_new = np.copy(V)
        for i in range(1, num_bus):  # Mulai dari bus 1 (bus 0 adalah slack bus)
            sum_YV = sum(Ybus[i, j] * V_new[j] for j in range(num_bus) if j != i)
            V_new[i] = (P_load[i] - 1j * Q_load[i]) / np.conj(V_new[i]) - sum_YV
            V_new[i] /= Ybus[i, i]
        if np.allclose(V, V_new, atol=tol):
            st.write(f"Konvergensi tercapai dalam {iteration+1} iterasi.")
            break
        V = V_new
    else:
        st.write("Konvergensi tidak tercapai dalam jumlah iterasi maksimum.")
    return V

# Jalankan metode Gauss-Seidel
V_final = gauss_seidel(Ybus, P_load, Q_load, V)

# --- Hasil Perhitungan ---
st.header("📈 Hasil Perhitungan")

# Menampilkan tegangan akhir
st.subheader("Tegangan Akhir pada Setiap Node")
tegangan_df = pd.DataFrame({
    "Node": ["Node 1", "Node 2"],
    "Tegangan (pu)": np.abs(V_final),
    "Sudut (derajat)": np.angle(V_final, deg=True)
})
st.table(tegangan_df)

# --- Analisis Losses ---
st.header("📉 Analisis Losses")

# Data losses
initial_losses = 73083664  # kWh (rugi-rugi awal)
total_losses = 5193168     # kWh (rugi-rugi sebelum optimasi)
increased_losses = total_losses / 1.445  # Rugi-rugi setelah optimasi

# Menghitung persentase losses
persentase_losses = (total_losses / initial_losses) * 100

# Menampilkan hasil losses
st.subheader("Perbandingan Losses")
col1, col2, col3 = st.columns(3)
col1.metric("Losses Awal", f"{initial_losses:,} kWh")
col2.metric("Losses Sebelum Optimasi", f"{total_losses:,} kWh")
col3.metric("Losses Setelah Optimasi", f"{int(increased_losses):,} kWh")

# Grafik perbandingan losses
fig1, ax1 = plt.subplots()
ax1.bar(['Losses Awal', 'Losses Sebelum Optimasi', 'Losses Setelah Optimasi'],
        [initial_losses, total_losses, increased_losses],
        color=['red', 'orange', 'green'])
ax1.set_title('Pengurangan Losses dalam Jaringan ULP BOJA')
ax1.set_ylabel('Losses (kWh)')
for i, value in enumerate([initial_losses, total_losses, increased_losses]):
    ax1.text(i, value, f'{value:,.2f} kWh', ha='center', va='bottom')
st.pyplot(fig1)

# --- Simulasi Pengurangan Losses Bulanan ---
st.subheader("Simulasi Pengurangan Losses Bulanan")

# Data simulasi
months = ['May 24', 'June 24', 'July 24', 'August 24', 'September 24',
          'October 24', 'November 24', 'December 24', 'January 25',
          'February 25', 'March 25', 'April 25']

target_percentage = 4.0  # Target persentase losses
monthly_losses = [total_losses]
monthly_percentage_losses = [(total_losses / initial_losses) * 100]
current_losses = total_losses
current_percentage_losses = monthly_percentage_losses[0]

for month in months[1:]:
    if current_percentage_losses <= target_percentage:
        break
    reduction_percentage = (current_percentage_losses - target_percentage) / (len(months) - months.index(month))
    new_losses = current_losses * (1 - reduction_percentage / 100)
    current_losses = new_losses
    monthly_losses.append(new_losses)
    monthly_percentage_losses.append((new_losses / initial_losses) * 100)

# Grafik simulasi pengurangan losses
fig2, ax2 = plt.subplots()
ax2.plot(months, monthly_percentage_losses, marker='o', color='blue')
ax2.set_title('Simulasi Pengurangan Persentase Losses dari Mei 2024 hingga April 2025')
ax2.set_ylabel('Losses (%)')
ax2.set_xlabel('Bulan')
for i, (month, percentage) in enumerate(zip(months, monthly_percentage_losses)):
    ax2.text(i, percentage, f'{percentage:.2f}%', ha='center', va='bottom')
st.pyplot(fig2)

# --- Penutup ---
st.markdown("""
---
**Aplikasi ini dibuat untuk memvisualisasikan pengurangan losses dan analisis tegangan pada jaringan distribusi listrik di wilayah Boja, Semarang Timur, dan UP3 Semarang.**
Dengan memahami konsep losses dan metode Gauss-Seidel, kita dapat mengoptimalkan jaringan listrik untuk meningkatkan efisiensi.
""")
