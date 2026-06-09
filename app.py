import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

st.set_page_config(page_title="Cek Budget Pengobatan", page_icon="💊", layout="centered")

# Ambil credentials dari Streamlit Secrets
creds_json = st.secrets["GOOGLE_CREDENTIALS"]
creds_dict = json.loads(creds_json)

scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

# GANTI INI DENGAN SPREADSHEET ID KAMU
SPREADSHEET_ID = "18x-ECHxHjhIqGAtzj1X3kmyTj9l52W8ndsomh_pdrk8" 
sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Data")

st.title("💊 Cek Budget Pengobatan")
st.write("Masukkan NPK kamu untuk cek sisa budget")

nip_input = st.text_input("NPK", placeholder="Contoh: 1771839")

if st.button("Cek Budget"):
    if nip_input:
        data = sheet.get_all_records()
        hasil = next((row for row in data if str(row['NPK']) == nip_input), None)
        
        if hasil:
            st.success(f"Halo, {hasil['Nama']}!")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Budget", f"Rp {hasil['Total Budget']:,}")
                st.metric("Budget Terpakai", f"Rp {hasil['Budget Terpakai']:,}")
            with col2:
                st.metric("Sisa Budget", f"Rp {hasil['Sisa Budget']:,}", delta_color="normal")
        else:
            st.error("NPK tidak ditemukan. Hubungi HRD.")
    else:
        st.warning("Masukkan NPK dulu ya")