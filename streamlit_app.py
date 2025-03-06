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


import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Data Impedansi dan Beban ---
Ybus = np.array([[complex(12, -6), complex(-6, 3)],
                 [complex(-6, 3), complex(10, -4)]])

P_load = np.array([0, 250])  # kW
Q_load = np.array([0, 120])  # kVAR

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

V_final = gauss_seidel(Ybus, P_load, Q_load, V)

initial_losses = 73083664  # kWh
total_losses = 5193168     # kWh
increased_losses = total_losses / 1.445  # Losses setelah optimasi

persentase_losses = (total_losses / initial_losses) * 100

# --- Simulasi Pengurangan Losses ---
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

# --- Tampilan Streamlit ---
st.title("Simulasi Pengurangan Losses dan Analisis Tegangan")
st.header("Hasil Perhitungan Metode Gauss-Seidel")

st.write("**Tegangan Akhir pada Setiap Node:**")
for i, v in enumerate(V_final):
    st.write(f"Node {i+1}: {np.abs(v):.4f} pu")

st.header("Analisis Losses")
st.write(f"Persentase losses awal: {persentase_losses:.2f}%")

# --- Plot Grafik ---
fig, ax = plt.subplots(3, 1, figsize=(10, 18))

# Grafik Batang Losses
ax[0].bar(['Initial Losses', 'Losses Sebelum Optimasi', 'Losses Setelah Optimasi'],
          [initial_losses, total_losses, increased_losses],
          color=['red', 'orange', 'green'])
ax[0].set_title('Pengurangan Losses dalam Jaringan')
ax[0].set_ylabel('Losses (kWh)')

# Grafik Garis Simulasi Pengurangan Losses
ax[1].plot(months, monthly_percentage_losses, marker='o', color='blue')
ax[1].set_title('Simulasi Pengurangan Persentase Losses')
ax[1].set_ylabel('Losses (%)')
ax[1].set_xlabel('Bulan')

# Grafik Tegangan Node
ax[2].bar(['Node 1', 'Node 2'], np.abs(V_final), color=['blue', 'purple'])
ax[2].set_title('Tegangan Akhir pada Setiap Node')
ax[2].set_ylabel('Tegangan (pu)')

st.pyplot(fig)


import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Simulasi Pengurangan Losses dan Analisis Tegangan")

# Data impedansi saluran (matriks admitansi Ybus)
Ybus = np.array([[complex(12, -8), complex(-6, 4)],
                 [complex(-6, 4), complex(10, -6)]])

# Data beban
P_load = np.array([0, 180])  # kW
Q_load = np.array([0, 90])   # kVAR

# Tegangan awal
V = np.array([complex(1.02, 0), complex(0.98, 0.04)])

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
initial_losses = 1088249105  # kWh
total_losses = 66970914  # kWh
increased_losses = total_losses / 1.445

# Menghitung persentase losses
persentase_losses = (total_losses / initial_losses) * 100

# Simulasi pengurangan losses
months = ['May 24', 'June 24', 'July 24', 'August 24', 'September 24',
          'October 24', 'November 24', 'December 24', 'January 25',
          'February 25', 'March 25', 'April 25']
monthly_losses = [total_losses]
monthly_percentage_losses = [(total_losses / initial_losses) * 100]
current_losses = total_losses
current_percentage_losses = monthly_percentage_losses[0]

target_percentage = 4.0
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
col1, col2, col3 = st.columns(3)
col1.metric("Losses Awal", f"{initial_losses:,} kWh")
col2.metric("Losses Sebelum Optimasi", f"{total_losses:,} kWh")
col3.metric("Losses Setelah Optimasi", f"{int(increased_losses):,} kWh")

# Plot losses
fig, ax = plt.subplots()
ax.bar(['Initial Losses', 'Losses Sebelum Optimasi', 'Losses Setelah Optimasi'],
       [initial_losses, total_losses, increased_losses],
       color=['red', 'orange', 'green'])
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
ax.bar(['Node 1', 'Node 2'], np.abs(V_final), color=['blue', 'purple'])
ax.set_title("Tegangan Akhir pada Setiap Node")
ax.set_ylabel("Tegangan (pu)")
st.pyplot(fig)
