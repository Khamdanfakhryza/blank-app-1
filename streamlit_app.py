import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Judul aplikasi
st.title("Simulasi Pengurangan Losses dan Analisis Tegangan")

# Data impedansi saluran (matriks admitansi Ybus)
Ybus = np.array([[complex(10, -5), complex(-5, 2)],
                 [complex(-5, 2), complex(8, -3)]])

# Data beban
P_load = np.array([0, 200])
Q_load = np.array([0, 100])

# Tegangan awal
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

V_final = gauss_seidel(Ybus, P_load, Q_load, V)

# Data losses
initial_losses = 229576732  # kWh
total_losses = 21343577  # kWh
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
    current_percentage_losses = (new_losses / initial_losses) * 100
    monthly_percentage_losses.append(current_percentage_losses)

# Grafik pengurangan losses
fig1 = go.Figure()
fig1.add_trace(go.Bar(x=['Initial Losses', 'Losses Sebelum Optimasi', 'Losses Setelah Optimasi'],
                      y=[initial_losses, total_losses, increased_losses],
                      marker_color=['red', 'orange', 'green']))
fig1.update_layout(title="Pengurangan Losses dalam Jaringan ULP SEMARANG TIMUR",
                   yaxis_title="Losses (kWh)")
st.plotly_chart(fig1)

# Grafik simulasi pengurangan losses bulanan
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=months, y=monthly_percentage_losses, mode='lines+markers', marker=dict(color='blue')))
fig2.update_layout(title="Simulasi Pengurangan Persentase Losses",
                   xaxis_title="Bulan", yaxis_title="Losses (%)")
st.plotly_chart(fig2)

# Grafik tegangan akhir pada setiap node
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=['Node 1', 'Node 2'], y=np.abs(V_final), marker_color=['blue', 'purple']))
fig3.update_layout(title="Tegangan Akhir pada Setiap Node",
                   yaxis_title="Tegangan (pu)")
st.plotly_chart(fig3)

# Menampilkan hasil perhitungan
st.write("## Hasil Perhitungan")
st.write(f"**Tegangan akhir pada setiap node:** {np.abs(V_final)} pu")
st.write(f"**Persentase losses:** {persentase_losses:.2f}%")
