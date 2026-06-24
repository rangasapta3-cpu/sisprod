import matplotlib.pyplot as plt
import pandas as pd

# =====================================================================
# 1. DEFINISI DATA (Berdasarkan Soal Kasus Tukang Fotocopi)
# =====================================================================
data_jobs = [
    {'job': 'A', 'p_time': 3, 'due_date': 5, 'slack': 2},
    {'job': 'B', 'p_time': 4, 'due_date': 6, 'slack': 2},
    {'job': 'C', 'p_time': 2, 'due_date': 7, 'slack': 5},
    {'job': 'D', 'p_time': 6, 'due_date': 9, 'slack': 3},
    {'job': 'E', 'p_time': 1, 'due_date': 2, 'slack': 1},
]

# =====================================================================
# 2. PERHITUNGAN PENJADWALAN METODE STR
# =====================================================================
# Urutkan berdasarkan nilai slack terkecil ke terbesar
str_schedule = sorted(data_jobs, key=lambda x: x['slack'])

current_time = 0
solved_details = []

for job in str_schedule:
    start_time = current_time
    current_time += job['p_time']  # Waktu Selesai (Completion Time)
    
    # Hitung Keterlambatan (Tardiness) -> T = max(0, C - D)
    tardiness = max(0, current_time - job['due_date'])
    
    solved_details.append({
        'Job': job['job'],
        'Waktu Proses (P)': job['p_time'],
        'Batas Waktu (D)': job['due_date'],
        'Slack Awal': job['slack'],
        'Waktu Mulai': start_time,
        'Waktu Selesai (C)': current_time,
        'Keterlambatan (T)': tardiness
    })

# Tampilkan tabel hasil penyelesaian di konsol/terminal
df_solusi = pd.DataFrame(solved_details)
print("============ URUTAN PENJADWALAN METODE STR ============")
print(df_solusi.to_string(index=False))
print("=======================================================\n")

# Hitung Rata-rata Performansi untuk Ringkasan Analisis
mean_flow_time = df_solusi['Waktu Selesai (C)'].mean()
max_tardiness = df_solusi['Keterlambatan (T)'].max()
jumlah_terlambat = (df_solusi['Keterlambatan (T)'] > 0).sum()

print(f"Rata-rata Waktu Alir (Mean Flow Time) : {mean_flow_time:.2f}")
print(f"Keterlambatan Maksimum (Max Tardiness): {max_tardiness}")
print(f"Jumlah Job yang Terlambat             : {jumlah_terlambat} dari {len(data_jobs)} job\n")


# =====================================================================
# 3. VISUALISASI TIME-PHASED FLOW (GANTT CHART)
# =====================================================================
fig, ax = plt.subplots(figsize=(11, 4))

# Batasan sumbu grafik
ax.set_ylim(0, 3)
ax.set_xlim(0, current_time + 2)  # Dinamis mengikuti total waktu selesai + buffer
ax.set_yticks([1.5])
ax.set_yticklabels(['Mesin Fotocopi'], fontsize=12, fontweight='bold')
ax.set_xlabel('Skala Waktu (Waktu Proses / Urutan Waktu)', fontsize=11)
ax.set_title('Time-Phased Flow Analisis Penjadwalan Metode STR', fontsize=14, fontweight='bold', pad=15)

# Palet warna representasi tiap Job (bisa disesuaikan)
colors = {'E': '#A8DADC',
