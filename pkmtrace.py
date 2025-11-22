import streamlit as st

from datetime import datetime

st.set_page_config(page_title="TRACE", layout="wide")

# ===============================
# 1. INISIALISASI STORAGE
# ===============================
if "data" not in st.session_state:
    st.session_state.data = []   # <-- tanpa pandas, pakai list of dict

if "threshold" not in st.session_state:
    st.session_state.threshold = {
        "tmin": 15,
        "tmax": 25,
        "hmin": 30,
        "hmax": 60
    }

# ===============================
# 2. FUNGSI HITUNG STATUS
# ===============================
def hitung_status(temp, rh):
    tmin = st.session_state.threshold["tmin"]
    tmax = st.session_state.threshold["tmax"]
    hmin = st.session_state.threshold["hmin"]
    hmax = st.session_state.threshold["hmax"]

    if tmin <= temp <= tmax and hmin <= rh <= hmax:
        return "OK"
    return "ALERT"

# ===============================
# 3. JUDUL WEB
# ===============================
st.title("🌡 TRACE — Tracking and Control of Environmental Conditions")
st.write("Website pemantauan suhu & kelembaban berdasarkan No Batch (tanpa pandas)")

# ===============================
# 4. INPUT DATA
# ===============================
st.subheader("📥 Input Pemeriksaan")

col1, col2, col3 = st.columns(3)

with col1:
    batch = st.text_input("No Batch")

with col2:
    suhu = st.number_input("Suhu (°C)", step=0.1)

with col3:
    kelembaban = st.number_input("Kelembaban (%)", step=0.1)

if st.button("Simpan Pemeriksaan", use_container_width=True):
    if batch == "":
        st.warning("No Batch belum diisi!")
    else:
        status = hitung_status(suhu, kelembaban)

        new_row = {
            "Batch": batch,
            "Suhu": suhu,
            "Kelembaban": kelembaban,
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Status": status
        }
        
        st.session_state.data.append(new_row)
        st.success("Data berhasil disimpan!")

# ===============================
# 5. PENGATURAN THRESHOLD
# ===============================
st.subheader("⚙ Pengaturan Threshold (Batas Aman)")

t1, t2, t3, t4 = st.columns(4)

with t1:
    tmin = st.number_input("Suhu Min", value=st.session_state.threshold["tmin"])
with t2:
    tmax = st.number_input("Suhu Max", value=st.session_state.threshold["tmax"])
with t3:
    hmin = st.number_input("RH Min", value=st.session_state.threshold["hmin"])
with t4:
    hmax = st.number_input("RH Max", value=st.session_state.threshold["hmax"])

if st.button("Simpan Threshold", use_container_width=True):
    st.session_state.threshold = {
        "tmin": tmin,
        "tmax": tmax,
        "hmin": hmin,
        "hmax": hmax
    }
    st.success("Threshold berhasil disimpan!")

# ===============================
# 6. FILTER & TABEL DATA
# ===============================
st.subheader("📊 Riwayat Pemeriksaan")

cari = st.text_input("Cari berdasarkan No Batch (biarkan kosong untuk tampil semua)")

# Filter manual tanpa pandas
if cari:
    data_tampil = [row for row in st.session_state.data if cari.lower() in row["Batch"].lower()]
else:
    data_tampil = st.session_state.data

# Tampilkan tabel
if data_tampil:
    st.table(data_tampil)
else:
    st.write("Belum ada data atau tidak ditemukan.")

# ===============================
# 7. RESET SEMUA DATA
# ===============================
if st.button("🗑 Hapus Semua Data", use_container_width=True):
    st.session_state.data = []
    st.warning("Semua data telah dihapus.")