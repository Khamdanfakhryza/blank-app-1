import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Analisis Jaringan Distribusi", layout="wide")
st.title("⚡ Analisis Losses dan Tegangan pada Jaringan Distribusi")
st.markdown("""
**Aplikasi untuk menganalisis losses dan profil tegangan pada jaringan distribusi di wilayah UP3 Semarang**
""")

# Data untuk masing-masing daerah
data_daerah = {
    "UP3 Semarang": {
        "Ybus": np.array([[complex(12, -8), complex(-6, 4)],
                         [complex(-6, 4), complex(10, -6)]]),
        "P_load": [0, 180],
        "Q_load": [0, 90],
        "V_initial": [complex(1.02, 0), complex(0.98, 0.04)],
        "losses": {
            "initial": 1088249105,
            "current": 66970914
        }
    },
    "Boja": {
        "Ybus": np.array([[complex(12, -6), complex(-6, 3)],
                         [complex(-6, 3), complex(10, -4)]]),
        "P_load": [0, 250],
        "Q_load": [0, 120],
        "V_initial": [complex(1, 0), complex(0.98, 0.02)],
        "losses": {
            "initial": 73083664,
            "current": 5193168
        }
    },
    "Semarang Timur": {
        "Ybus": np.array([[complex(10, -5), complex(-5, 2)],
                         [complex(-5, 2), complex(8, -3)]]),
        "P_load": [0, 200],
        "Q_load": [0, 100],
        "V_initial": [complex(1.02, 0), complex(0.97, 0.03)],
        "losses": {
            "initial": 229576732,
            "current": 21343577
        }
    }
}

# Sidebar untuk seleksi daerah
selected_daerah = st.sidebar.selectbox(
    "Pilih Daerah:",
    list(data_daerah.keys()),
    index=0
)

# Fungsi Gauss-Seidel
def gauss_seidel(Ybus, P_load, Q_load, V, tol=1e-6, max_iter=1000):
    num_bus = len(V)
    for iteration in range(max_iter):
        V_new = np.copy(V)
        for i in range(1, num_bus):
            sum_YV = sum(Ybus[i, j] * V_new[j] for j in range(num_bus) if j != i)
            V_new[i] = (P_load[i] - 1j * Q_load[i]) / np.conj(V_new[i]) - sum_YV
            V_new[i] /= Ybus[i, i]
        if np.allclose(V, V_new, atol=tol):
            break
        V = V_new
    return V

# Ambil data untuk daerah terpilih
daerah = data_daerah[selected_daerah]
V_final = gauss_seidel(daerah["Ybus"], 
                      np.array(daerah["P_load"]), 
                      np.array(daerah["Q_load"]), 
                      np.array(daerah["V_initial"]))

# Hitung losses
initial_losses = daerah["losses"]["initial"]
total_losses = daerah["losses"]["current"]
increased_losses = total_losses / 1.445
persentase_losses = (total_losses / initial_losses) * 100

# Tampilkan hasil dalam tabs
tab1, tab2, tab3 = st.tabs(["Hasil Perhitungan", "Analisis Losses", "Simulasi Bulanan"])

with tab1:
    st.header(f"Hasil Perhitungan untuk {selected_daerah}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tegangan Akhir")
        tegangan_df = pd.DataFrame({
            "Node": ["Node 1", "Node 2"],
            "|V| (pu)": np.abs(V_final),
            "∠V (°)": np.angle(V_final, deg=True)
        })
        st.dataframe(tegangan_df.style.format({"|V| (pu)": "{:.4f}", "∠V (°)": "{:.2f}"}))
    
    with col2:
        st.subheader("Parameter Jaringan")
        st.write("**Matriks Admitansi (Ybus):**")
        st.write(daerah["Ybus"])
        st.write("**Beban Node 2:**")
        st.write(f"P: {daerah['P_load'][1]} kW")
        st.write(f"Q: {daerah['Q_load'][1]} kVAR")

with tab2:
    st.header(f"Analisis Losses {selected_daerah}")
    
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    
    # Grafik Batang Losses
    ax[0].bar(['Awal', 'Sebelum Optimasi', 'Setelah Optimasi'],
             [initial_losses, total_losses, increased_losses],
             color=['red', 'orange', 'green'])
    ax[0].set_title('Perbandingan Losses')
    ax[0].set_ylabel('Losses (kWh)')
    for i, val in enumerate([initial_losses, total_losses, increased_losses]):
        ax[0].text(i, val, f'{val/1e6:.2f} MWh', ha='center', va='bottom')
    
    # Grafik Pie Persentase
    sizes = [persentase_losses, 100 - persentase_losses]
    ax[1].pie(sizes, labels=['Losses', 'Daya Terkirim'], 
             autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
    ax[1].set_title('Persentase Losses')
    
    st.pyplot(fig)

with tab3:
    st.header(f"Simulasi Pengurangan Losses {selected_daerah}")
    
    # Simulasi bulanan
    months = ['May 24', 'June 24', 'July 24', 'August 24', 'September 24',
             'October 24', 'November 24', 'December 24', 'January 25',
             'February 25', 'March 25', 'April 25']
    
    monthly_losses = [total_losses]
    monthly_percentage = [persentase_losses]
    current = total_losses
    
    for _ in months[1:]:
        current *= 0.85  # Reduksi 15% per bulan
        monthly_losses.append(current)
        monthly_percentage.append((current/initial_losses)*100)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(months, monthly_percentage, marker='o', linestyle='--')
    ax.set_title('Proyeksi Pengurangan Losses')
    ax.set_ylabel('Persentase Losses (%)')
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    st.write("**Detail Simulasi Bulanan:**")
    simulasi_df = pd.DataFrame({
        "Bulan": months,
        "Losses (kWh)": monthly_losses,
        "Persentase (%)": monthly_percentage
    })
    st.dataframe(simulasi_df.style.format({"Losses (kWh)": "{:,.0f}", "Persentase (%)": "{:.2f}"}))

# Informasi daerah di sidebar
st.sidebar.markdown("""
---
**Informasi Daerah:**
- **UP3 Semarang**: Wilayah pelayanan distribusi listrik di Kota Semarang
- **Boja**: Kecamatan di Kabupaten Kendal dengan beban industri
- **Semarang Timur**: Wilayah padat penduduk dengan kebutuhan komersial tinggi
""")
