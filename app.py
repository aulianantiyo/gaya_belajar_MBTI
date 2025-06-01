import streamlit as st
import pandas as pd

# Load datasets
gaya_belajar_df = pd.read_csv("rekomendasi gaya belajar.csv")
platform_df = pd.read_csv("rekomendasi platform.csv")
platform_links_df = pd.read_csv("link platform.csv")

# Ubah data link platform menjadi dictionary: { "Platform Name": "URL" }
platform_links = dict(zip(platform_links_df['Platform Name'], platform_links_df['URL']))

# Styling halaman
st.set_page_config(page_title="Rekomendasi Gaya Belajar MBTI", layout="wide")
st.markdown("<h1 style='color: teal;'>📘 Rekomendasi Gaya Belajar Berdasarkan MBTI</h1>", unsafe_allow_html=True)

# Info jika belum tahu MBTI
with st.expander("🔍 Belum tahu MBTI Anda?"):
    st.markdown("Silakan lakukan tes kepribadian MBTI gratis melalui tautan berikut:")
    st.markdown("👉 [Tes MBTI Gratis - 16Personalities](https://www.16personalities.com/)")
    st.markdown("---")

# Pilihan MBTI
mbti_list = sorted(gaya_belajar_df['mbti_type'].unique())
mbti_input = st.selectbox("🧠 Pilih Tipe MBTI Anda:", [""] + mbti_list)

# Fungsi rekomendasi berdasarkan MBTI
def rekomendasi_mbti(mbti_input):
    mbti_input = mbti_input.upper()
    data_gaya = gaya_belajar_df[gaya_belajar_df['mbti_type'] == mbti_input]

    if data_gaya.empty:
        st.error(f"MBTI {mbti_input} tidak ditemukan dalam data.")
        return

    tools_list = data_gaya.iloc[0]['tools'].split(', ')
    rekomendasi_platform = {}

    for tool in tools_list:
        match = platform_df[platform_df['tools'].str.contains(tool, case=False, na=False)]
        if not match.empty:
            platform_names = match.iloc[0]['platform'].split(', ')
            links = []
            for name in platform_names:
                url = platform_links.get(name.strip(), None)
                links.append((name, url))
            rekomendasi_platform[tool] = links
        else:
            rekomendasi_platform[tool] = []

    # Tampilkan hasil
    st.markdown(f"### ✨ MBTI: `{mbti_input}`")
    st.success(f"**Gaya Belajar:** {data_gaya.iloc[0]['learning_style']}")
    st.info(f"**Saran Belajar:** {data_gaya.iloc[0]['study_suggestion']}")

    st.markdown("### 🧰 Tools dan Platform yang Direkomendasikan:")
    for tool, platforms in rekomendasi_platform.items():
        st.markdown(
            f"<div style='background-color: #f0f9ff; padding: 10px; border-radius: 10px;'><b>{tool}</b></div>",
            unsafe_allow_html=True
        )
        for name, url in platforms:
            if url:
                st.markdown(f"- [{name}]({url})", unsafe_allow_html=True)
            else:
                st.markdown(f"- {name}")

# Tampilkan hasil jika sudah pilih MBTI
if mbti_input:
    rekomendasi_mbti(mbti_input)
else:
    st.warning("Silakan pilih tipe MBTI terlebih dahulu untuk melihat rekomendasi.")
