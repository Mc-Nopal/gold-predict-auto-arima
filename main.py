import streamlit as st
import pandas as pd
from function import fetch_gold_history_yf, predict_gold_arima

# TODO : Config Page
st.set_page_config(
    page_title="Gold Predict - Auto ARIMA",
    page_icon="🪙",
    layout="wide"
)

_, centercol ,_= st.columns([1,3,1])
with centercol :
# TODO : Header & Deskripsi
    st.markdown("<h2 style='text-align: center; color: #FFD700'>🪙 Gold Prediction App</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>Aplikasi prediksi harga emas efisien tanpa boros kuota API menggunakan Yahoo Finance & Auto ARIMA.</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: gray;'>Prediksi pergerakan harga emas masa depan berdasarkan data historis terkini. "
        "Hasil otomatis dikonversi dari Troy Ounce ke Harga per Gram dalam Rupiah (IDR).</p>", 
        unsafe_allow_html=True
    )
    st.markdown("---")

#TODO : Panel Kontrol Input (Form/Widget)
    st.subheader("⚙️ Parameter Prediksi")

    col1, col2= st.columns([2,1])
    with col1:
        n_data = st.slider("Banyak Hari yang digunakan", min_value=50, max_value=100, value=75, step=5)
    with col2:
        n_days = st.number_input("Banyak Hari yang diprediksi", min_value=1, max_value=30, value=7)
    currency = st.selectbox("Pilih Mata Uang (Currency)", ["USD", "IDR", "EUR", "SGD", "GBP"])
    # Tombol Eksekusi Prediksi
    predict_button = st.button("Jalankan Prediksi 🚀", use_container_width=True)

    if predict_button :
        with st.spinner("Mengambil data dan melatih model Auto ARIMA..."):
            
            # 1. Tarik Data Historis
            df_history = fetch_gold_history_yf(days=n_data, currency=currency)
            
            # 2. Jalankan Auto ARIMA Forecasting & Ambil Akurasi
            df_forecast, accuracy_score = predict_gold_arima(df_history, n_forecast_days=n_days)
            
            st.success("Analisis Berhasil Dibuat!")
            
            # --- Perhitungan Tren dengan Presisi Tinggi ---
            harga_awal_prediksi = df_forecast["Prediksi_Harga_Gram"].iloc[0]
            harga_akhir_prediksi = df_forecast["Prediksi_Harga_Gram"].iloc[-1]
            
            selisih = harga_akhir_prediksi - harga_awal_prediksi
            # Menggunakan persentase perubahan dari awal ke akhir periode prediksi
            persentase_perubahan = (selisih / harga_awal_prediksi) * 100
            
            curr_symbol = "Rp" if currency == "IDR" else "$"
            
            # --- Layout Metrik & Tren di UI ---
            col_metric1, col_metric2 = st.columns(2)
            
            with col_metric1:
                st.metric(
                    label="📈 Tingkat Estimasi Akurasi Model", 
                    value=f"{accuracy_score:.2f}%",
                    help="Dihitung berdasarkan tingkat kesalahan (MAPE) kecocokan model terhadap data historis."
                )
                
            with col_metric2:
                # Menampilkan persentase dengan 2 desimal agar gap kecil terlihat tajam
                delta_val = f"{persentase_perubahan:+.2f}% ({curr_symbol} {selisih:+,.2f})"
                
                st.metric(
                    label="Tren Pergerakan Periode Prediksi",
                    value=f"{curr_symbol} {harga_akhir_prediksi:,.2f}",
                    delta=delta_val,
                    delta_color="normal"
                )
            
            # Banner Keterangan Tren yang Lebih Responsif
            if persentase_perubahan > 0:
                st.markdown(
                    f"<div style='padding: 12px; border-radius: 6px; background-color: rgba(0, 255, 0, 0.1); border: 1px solid rgba(0, 255, 0, 0.4); text-align: center;'>"
                    f"🟢 **Kesimpulan Tren:** Harga emas diproyeksikan **NAIK** sebesar **+{persentase_perubahan:.2f}%** ({curr_symbol} {selisih:+,.2f}) selama periode prediksi."
                    f"</div>", 
                    unsafe_allow_html=True
                )
            elif persentase_perubahan < 0:
                st.markdown(
                    f"<div style='padding: 12px; border-radius: 6px; background-color: rgba(255, 0, 0, 0.1); border: 1px solid rgba(255, 0, 0, 0.4); text-align: center;'>"
                    f"🔴 **Kesimpulan Tren:** Harga emas diproyeksikan **TURUN** sebesar **{persentase_perubahan:.2f}%** ({curr_symbol} {selisih:,.2f}) selama periode prediksi."
                    f"</div>", 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='padding: 12px; border-radius: 6px; background-color: rgba(255, 255, 0, 0.1); border: 1px solid rgba(255, 255, 0, 0.4); text-align: center;'>"
                    f"🟡 **Kesimpulan Tren:** Harga emas diproyeksikan **STABIL** (mendatar) selama periode prediksi."
                    f"</div>", 
                    unsafe_allow_html=True
                )
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 3. Tampilkan Grafik Hasil Prediksi
            st.subheader(f"📊 Grafik Prediksi Harga Emas per Gram ({currency}) — Akurasi: {accuracy_score:.2f}%")
            st.line_chart(df_forecast)
            
            # Tampilkan Tabel Detail Prediksi
            with st.expander("Lihat Detail Tabel Angka Prediksi"):
                st.dataframe(df_forecast.style.format(curr_symbol + " {:,.2f}"))
                
            # Tampilkan Grafik Data Historis
            with st.expander("Lihat Grafik Data Historis Asli"):
                st.line_chart(df_history)