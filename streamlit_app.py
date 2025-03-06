import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

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
            break
        V = V_new
    return V

# Menjalankan metode Gauss-Seidel
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
fig1 = go.Figure()
fig1.add_trace(go.Bar(x=['Losses Awal', 'Losses Sebelum Optimasi', 'Losses Setelah Optimasi'],
                      y=[initial_losses, total_losses, increased_losses],
                      marker_color=['red', 'orange', 'green']))
fig1.update_layout(title="Perbandingan Losses dalam Jaringan",
                   yaxis_title="Losses (kWh)")
st.plotly_chart(fig1)

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
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=months, y=monthly_percentage_losses, mode='lines+markers', marker=dict(color='blue')))
fig2.update_layout(title="Simulasi Pengurangan Persentase Losses",
                   xaxis_title="Bulan", yaxis_title="Losses (%)")
st.plotly_chart(fig2)

# --- Penutup ---
st.markdown("""
---
**Aplikasi ini dibuat untuk memvisualisasikan pengurangan losses dan analisis tegangan pada jaringan distribusi listrik di wilayah Boja, Semarang Timur, dan UP3 Semarang.**
Dengan memahami konsep losses dan metode Gauss-Seidel, kita dapat mengoptimalkan jaringan listrik untuk meningkatkan efisiensi.
""")
