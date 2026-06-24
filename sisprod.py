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

# =====================================================================
# 3. VISUALISASI TIME-PHASED FLOW (GANTT CHART)
# =====================================================================
fig, ax = plt.subplots(figsize=(11, 4))

# Batasan sumbu grafik
ax.set_ylim(0, 3)
ax.set_xlim(0, current_time + 2)  
ax.set_yticks([1.5])
ax.set_yticklabels(['Mesin Fotocopi'], fontsize=12, fontweight='bold')
ax.set_xlabel('Skala Waktu (Waktu Proses / Urutan Waktu)', fontsize=11)
ax.set_title('Time-Phased Flow Analisis Penjadwalan Metode STR', fontsize=14, fontweight='bold', pad=15)

# Perbaikan SyntaxError: Sudah ditutup menggunakan '}' dengan benar di akhir baris
colors = {'E': '#A8DADC', 'A': '#457B9D', 'B': '#1D3557', 'D': '#E63946', 'C': '#F4A261'}

# Gambar blok diagram satu per satu sesuai urutan hasil STR
for detail in solved_details:
    job_name = detail['Job']
    p_time = detail['Waktu Proses (P)']
    start = detail['Waktu Mulai']
    end = detail['Waktu Selesai (C)']
    
    # 1. Gambar kotak proses kerja Job
    ax.broken_barh([(start, p_time)], (0.8, 1.4), facecolors=colors[job_name], edgecolor='black')
    
    # 2. Teks Nama Job di tengah kotak
    text_color = 'white' if job_name in ['B', 'A', 'D'] else 'black'
    ax.text(start + (p_time / 2), 1.5, f"Job {job_name}", 
            color=text_color, ha='center', va='center', fontsize=12, fontweight='bold')
    
    # 3. Tambahkan tanda panah penyelesaian di bawah blok (Job Completed)
    ax.annotate(f"{job_name}\n(t={end})", 
                xy=(end, 0.7), 
                xytext=(end, 0.1),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
                ha='center', fontsize=10, fontweight='bold')

# Pengaturan grid garis bantu vertikal berdasarkan skala angka waktu
ax.set_xticks(range(0, current_time + 3))
ax.grid(axis='x', linestyle='--', alpha=0.5)

# Membersihkan tampilan frame atas dan kanan
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()
