import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit Title
st.title("Simulasi Pengurangan Losses dan Analisis Tegangan")

# Data impedansi saluran (matriks admitansi Ybus)
Ybus = np.array([[complex(10, -5), complex(-5, 2)],
                 [complex(-5, 2), complex(8, -3)]])

# Data beban pada setiap node (daya nyata dan daya reaktif)
P_load = np.array([0, 200])
Q_load = np.array([0, 100])

# Tegangan awal pada setiap node (V)
V = np.array([complex(1.02, 0), complex(0.97, 0.03)])

def gauss_seidel(Ybus, P_load, Q_load, V, tol=1e-6, max_iter=1000):
    num_bus = len(V)
    for iteration in range(max_iter):
        V_new = np.copy(V)
        for i in range(num_bus):
            sum_YV = sum(Ybus[i, j] * V_new[j] for j in range(num_bus) if j != i)
            V_new[i] = (P_load[i] - 1j * Q_load[i]) / np.conj(V_new[i]) - sum_YV
            V_new[i] /= Ybus[i, i]
        if np.allclose(V, V_new, atol=tol):
            break
        V = V_new
    return V

# Jalankan metode Gauss-Seidel
V_final = gauss_seidel(Ybus, P_load, Q_load, V)

# Data Losses
initial_losses = 229576732  # kWh
total_losses = 21343577      # kWh
increased_losses = total_losses / 1.445

# Menghitung persentase losses
persentase_losses = (total_losses / initial_losses) * 100

# Simulasi pengurangan losses bulanan
months = ['May 24', 'June 24', 'July 24', 'August 24', 'September 24',
          'October 24', 'November 24', 'December 24', 'January 25',
          'February 25', 'March 25', 'April 25']
target_losses = total_losses * 0.04
target_percentage = 4.0

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
    current_percentage_losses = (new_losses / initial_losses) * 100
    monthly_percentage_losses.append(current_percentage_losses)

# Menampilkan hasil
st.subheader("Tegangan Akhir pada Setiap Node")
tegangan_df = pd.DataFrame({"Node": ["Node 1", "Node 2"], "Tegangan (pu)": np.abs(V_final)})
st.dataframe(tegangan_df)

# Plot Grafik Batang Losses
fig, ax = plt.subplots()
ax.bar(['Initial Losses', 'Losses Sebelum Optimasi', 'Losses Setelah Optimasi'],
       [initial_losses, total_losses, increased_losses],
       color=['red', 'orange', 'green'])
ax.set_title('Pengurangan Losses dalam Jaringan ULP SEMARANG TIMUR')
ax.set_ylabel('Losses (kWh)')
st.pyplot(fig)

# Plot Simulasi Pengurangan Losses Bulanan
fig, ax = plt.subplots()
ax.plot(months, monthly_percentage_losses, marker='o', color='blue')
ax.set_title('Simulasi Pengurangan Persentase Losses')
ax.set_ylabel('Losses (%)')
ax.set_xlabel('Bulan')
st.pyplot(fig)

# Plot Persentase Tegangan pada Setiap Node
fig, ax = plt.subplots()
ax.bar(['Node 1', 'Node 2'], np.abs(V_final), color=['blue', 'purple'])
ax.set_title('Tegangan Akhir pada Setiap Node')
ax.set_ylabel('Tegangan (pu)')
st.pyplot(fig)

st.success(f"Persentase losses: {persentase_losses:.2f}%")
