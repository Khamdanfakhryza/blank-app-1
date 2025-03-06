import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Simulasi Pengurangan Losses dan Analisis Tegangan")

# Data impedansi saluran (matriks admitansi Ybus)
Ybus = np.array([[complex(12, -6), complex(-6, 3)],
                 [complex(-6, 3), complex(10, -4)]])

# Data beban
P_load = np.array([0, 250])  # kW
Q_load = np.array([0, 120])  # kVAR

# Tegangan awal
V = np.array([complex(1, 0), complex(0.98, 0.02)])

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

# Menjalankan metode Gauss-Seidel
V_final = gauss_seidel(Ybus, P_load, Q_load, V)

# Data losses
initial_losses = 73083664  # kWh
total_losses = 5193168     # kWh
increased_losses = total_losses / 1.445
persentase_losses = (total_losses / initial_losses) * 100

# Simulasi pengurangan losses
months = ['May 24', 'June 24', 'July 24', 'August 24', 'September 24',
          'October 24', 'November 24', 'December 24', 'January 25',
          'February 25', 'March 25', 'April 25']

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
    monthly_percentage_losses.append((new_losses / initial_losses) * 100)

# Menampilkan hasil losses
st.subheader("Losses dalam Jaringan")
st.metric("Losses Awal", f"{initial_losses:,} kWh")
st.metric("Losses Sebelum Optimasi", f"{total_losses:,} kWh")
st.metric("Losses Setelah Optimasi", f"{int(increased_losses):,} kWh")

# Plot losses
titles = ["Initial Losses", "Losses Sebelum Optimasi", "Losses Setelah Optimasi"]
values = [initial_losses, total_losses, increased_losses]
colors = ['red', 'orange', 'green']

fig, ax = plt.subplots()
ax.bar(titles, values, color=colors)
ax.set_title("Pengurangan Losses")
ax.set_ylabel("Losses (kWh)")
st.pyplot(fig)

# Plot simulasi pengurangan losses
fig, ax = plt.subplots()
ax.plot(months, monthly_percentage_losses, marker='o', color='blue')
ax.set_title("Simulasi Pengurangan Losses Bulanan")
ax.set_ylabel("Losses (%)")
ax.set_xlabel("Bulan")
st.pyplot(fig)

# Menampilkan hasil tegangan
st.subheader("Tegangan Akhir pada Setiap Node")
tegangan_df = pd.DataFrame({
    "Node": ["Node 1", "Node 2"],
    "Tegangan (pu)": np.abs(V_final)
})
st.table(tegangan_df)

# Plot tegangan
fig, ax = plt.subplots()
ax.bar(["Node 1", "Node 2"], np.abs(V_final), color=['blue', 'purple'])
ax.set_title("Tegangan Akhir pada Setiap Node")
ax.set_ylabel("Tegangan (pu)")
st.pyplot(fig)
