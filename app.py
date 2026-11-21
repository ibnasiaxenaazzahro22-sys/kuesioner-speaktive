import io
from datetime import datetime, timezone

import pandas as pd
import streamlit as st
from supabase import create_client

# ---------------------------------------------------------
# KONFIGURASI HALAMAN
# ---------------------------------------------------------
st.set_page_config(
    page_title="Need Analysis - SPEAKTIVE",
    page_icon="📝",
    layout="wide",
)

st.title("Questionnaire Sheet of Students Need Analysis")
st.subheader("Development of the VR and LMS Based SPEAKTIVE Model to Improve Speaking for General Communication")

st.write(
    "Kuesioner ini digunakan sebagai dasar analisis kebutuhan (need analysis) "
    "dalam pengembangan model pembelajaran SPEAKTIVE berbasis Virtual Reality (VR) "
    "dan Learning Management System (LMS)."
)

# ---------------------------------------------------------
# INSTRUMEN: 30 BUTIR SESUAI DOKUMEN YANG DIUNGGAH
# Skala: 1=STS, 2=TS, 3=S, 4=SS
# ---------------------------------------------------------
QUESTIONS = [
    {
        "no": 1, "aspect": "Phonological",
        "en": "I can distinguish between similar English sounds when listening to others speak.",
        "id": "Saya dapat membedakan bunyi-bunyi bahasa Inggris yang mirip saat mendengarkan orang lain berbicara."
    },
    {
        "no": 2, "aspect": "Phonological",
        "en": "I can use short forms of words (such as gonna, wanna) reasonably in conversation.",
        "id": "Saya dapat menggunakan bentuk singkat kata (seperti gonna, wanna) secara wajar dalam percakapan."
    },
    {
        "no": 3, "aspect": "Self-Monitor",
        "en": "I can correct my own speech when I realize I have made a mistake while speaking.",
        "id": "Saya dapat memperbaiki ucapan saya sendiri ketika menyadari ada kesalahan saat berbicara."
    },
    {
        "no": 4, "aspect": "Grammatical Structure",
        "en": "I can use the correct tenses when speaking English.",
        "id": "Saya dapat menggunakan bentuk waktu (tense) yang tepat saat berbicara bahasa Inggris."
    },
    {
        "no": 5, "aspect": "Communication Function",
        "en": "I can convey my intention according to my communicative purpose (e.g., requesting, refusing, etc.).",
        "id": "Saya dapat menyampaikan maksud saya sesuai dengan tujuan komunikasi (misalnya meminta, menolak, dan sebagainya)."
    },
    {
        "no": 6, "aspect": "Nonverbal Communication",
        "en": "I use body movements (gestures) to help convey my intended meaning.",
        "id": "Saya menggunakan gerakan tubuh (gesture) untuk membantu menyampaikan maksud saya."
    },
    {
        "no": 7, "aspect": "Strategic Competence",
        "en": "I ask for help (e.g., asking someone to repeat or explain) when I have difficulty speaking.",
        "id": "Saya meminta bantuan (misalnya bertanya ulang atau meminta penjelasan) ketika saya kesulitan berbicara."
    },
    {
        "no": 8, "aspect": "Speaking Fluency",
        "en": "I can speak English fluently without many pauses.",
        "id": "Saya dapat berbicara bahasa Inggris dengan lancar tanpa banyak jeda."
    },
    {
        "no": 9, "aspect": "Linguistic",
        "en": "I have a sufficient vocabulary to convey ideas in line with my communication goals.",
        "id": "Saya memiliki kosakata yang cukup untuk menyampaikan ide sesuai tujuan komunikasi saya."
    },
    {
        "no": 10, "aspect": "Task Preparation",
        "en": "I find it helpful to be given time to plan and carry out a speaking task directly.",
        "id": "Saya merasa terbantu ketika diberikan waktu untuk merencanakan dan melaksanakan tugas berbicara secara langsung."
    },
    {
        "no": 11, "aspect": "Comprehensibility",
        "en": "I can express my ideas in a way that others can easily understand.",
        "id": "Saya dapat menyampaikan ide saya dengan cara yang mudah dipahami oleh orang lain."
    },
    {
        "no": 12, "aspect": "Affective",
        "en": "I feel confident when speaking English in front of other people.",
        "id": "Saya merasa percaya diri ketika berbicara dalam bahasa Inggris di depan orang lain."
    },
    {
        "no": 13, "aspect": "Learning Cycle",
        "en": "I find it easier to learn to speak English through direct experience, such as practice or real simulations.",
        "id": "Saya lebih mudah belajar berbicara bahasa Inggris melalui pengalaman langsung, seperti praktik atau simulasi nyata."
    },
    {
        "no": 14, "aspect": "Learning Cycle",
        "en": "I find it easier to learn to speak English by directly trying to apply what I have learned.",
        "id": "Saya lebih mudah belajar berbicara bahasa Inggris dengan langsung mencoba menerapkan apa yang saya pelajari."
    },
    {
        "no": 15, "aspect": "Grammatical Competence",
        "en": "I can construct grammatically correct sentences when speaking English.",
        "id": "Saya dapat menyusun kalimat yang benar secara tata bahasa ketika berbicara dalam bahasa Inggris."
    },
    {
        "no": 16, "aspect": "Sociolinguistic Competence",
        "en": "I can choose language expressions that are appropriate to the social situation and the person I am talking to.",
        "id": "Saya dapat memilih ungkapan bahasa yang sesuai dengan situasi sosial dan lawan bicara saya."
    },
    {
        "no": 17, "aspect": "Discourse Competence",
        "en": "I can organize my spoken ideas in a logical sequence.",
        "id": "Saya dapat menyampaikan ide-ide saya secara lisan dalam urutan yang logis."
    },
    {
        "no": 18, "aspect": "Discourse Competence",
        "en": "I can use connecting words and expressions (e.g., because, therefore, however) to link my ideas when speaking.",
        "id": "Saya dapat menggunakan kata atau ungkapan penghubung (misalnya because, therefore, however) untuk menghubungkan ide-ide saya saat berbicara."
    },
    {
        "no": 19, "aspect": "Strategic Competence",
        "en": "I can use different words or explanations when my listener does not understand my message.",
        "id": "Saya dapat menggunakan kata-kata atau penjelasan lain ketika lawan bicara tidak memahami pesan saya."
    },
    {
        "no": 20, "aspect": "Task Implementation",
        "en": "I find it helpful when the lecturer introduces the topic and provides preparation before a speaking task begins.",
        "id": "Saya merasa terbantu ketika dosen memperkenalkan topik dan memberikan persiapan sebelum tugas berbicara dimulai."
    },
    {
        "no": 21, "aspect": "Task Implementation",
        "en": "I find it helpful to complete speaking tasks through practice, performance, and reporting activities.",
        "id": "Saya merasa terbantu menyelesaikan tugas berbicara melalui kegiatan latihan, penampilan, dan pelaporan hasil."
    },
    {
        "no": 22, "aspect": "Task Implementation",
        "en": "I find it helpful when language forms and expressions are discussed after completing a speaking task.",
        "id": "Saya merasa terbantu ketika bentuk dan ungkapan bahasa dibahas setelah menyelesaikan tugas berbicara."
    },
    {
        "no": 23, "aspect": "VR Expectation",
        "en": "I feel I would be more focused and confident practicing speaking if I used technology that makes me feel “present” in the situation.",
        "id": "Saya merasa akan lebih fokus dan lebih percaya diri berlatih berbicara jika menggunakan teknologi yang membuat saya merasa “berada” dalam situasi tersebut."
    },
    {
        "no": 24, "aspect": "VR Expectation",
        "en": "I am interested in being able to interact directly with situations or digital characters while practicing speaking.",
        "id": "Saya tertarik jika saya bisa berinteraksi langsung dengan situasi atau tokoh digital saat berlatih berbicara."
    },
    {
        "no": 25, "aspect": "VR Expectation",
        "en": "I would like to interact with virtual objects, environments, or characters while practicing speaking English.",
        "id": "Saya ingin dapat berinteraksi dengan objek, lingkungan, atau karakter virtual saat berlatih berbicara dalam bahasa Inggris."
    },
    {
        "no": 26, "aspect": "VR Expectation",
        "en": "I would like a virtual environment that provides realistic visual and audio feedback during speaking practice.",
        "id": "Saya menginginkan lingkungan virtual yang memberikan umpan balik visual dan audio yang realistis selama latihan berbicara."
    },
    {
        "no": 27, "aspect": "LMS Expectation",
        "en": "I need a digital platform that makes it easy for me to access speaking learning materials anytime.",
        "id": "Saya membutuhkan platform digital yang memudahkan saya mengakses materi belajar berbicara kapan saja."
    },
    {
        "no": 28, "aspect": "LMS Expectation",
        "en": "I need a system that can provide digital assessment and feedback on my speaking ability.",
        "id": "Saya membutuhkan sistem yang dapat memberikan penilaian dan umpan balik terhadap kemampuan berbicara saya secara digital."
    },
    {
        "no": 29, "aspect": "LMS Expectation",
        "en": "I am interested if VR-based speaking practice can be connected to materials and tasks online through a single platform.",
        "id": "Saya tertarik jika praktik berbicara berbasis VR dapat terhubung dengan materi dan tugas secara online melalui satu platform."
    },
    {
        "no": 30, "aspect": "Implementation of TPACK",
        "en": "I believe speaking activities are more effective when learning materials, teaching strategies, and technology are integrated in a balanced way.",
        "id": "Saya meyakini bahwa aktivitas berbicara akan lebih efektif ketika materi pembelajaran, strategi pengajaran, dan teknologi diintegrasikan secara seimbang."
    },
]

SCALE = {
    "1 - Sangat Tidak Setuju (STS)": 1,
    "2 - Tidak Setuju (TS)": 2,
    "3 - Setuju (S)": 3,
    "4 - Sangat Setuju (SS)": 4,
}

# ---------------------------------------------------------
# KONEKSI DATABASE
# ---------------------------------------------------------
@st.cache_resource
def get_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
    )

# ---------------------------------------------------------
# MENU
# ---------------------------------------------------------
menu = st.sidebar.radio("Menu", ["Isi Kuesioner", "Admin"])

if menu == "Isi Kuesioner":
    st.header("Identitas Responden")
    st.caption("Mohon isi identitas yang diminta. Pastikan kode responden sesuai arahan peneliti.")

    with st.form("speaktive_questionnaire"):
        name = st.text_input("Name / Nama")
        nim = st.text_input("NIM / Kode Responden")
        institution = st.text_input("Institution / Institusi")
        date_value = st.date_input("Day / Date")

        st.divider()
        st.header("Petunjuk Pengisian")
        st.write(
            "Berikan satu jawaban pada setiap pernyataan. "
            "Pastikan seluruh 30 pernyataan telah dijawab."
        )
        st.write(
            "**1 = Sangat Tidak Setuju | 2 = Tidak Setuju | "
            "3 = Setuju | 4 = Sangat Setuju**"
        )

        answers = {}
        for item in QUESTIONS:
            st.markdown(f"**{item['no']}. {item['en']}**")
            st.write(item["id"])
            selected = st.radio(
                "Pilih skor:",
                options=list(SCALE.keys()),
                index=None,
                key=f"q_{item['no']}",
                horizontal=True,
                label_visibility="collapsed",
            )
            answers[str(item["no"])] = {
                "aspect": item["aspect"],
                "question_en": item["en"],
                "question_id": item["id"],
                "answer_label": selected,
                "score": SCALE[selected] if selected else None,
            }
            st.divider()

        consent = st.checkbox(
            "Saya bersedia jawaban saya digunakan untuk keperluan analisis penelitian."
        )
        submitted = st.form_submit_button("Kirim Jawaban", use_container_width=True)

    if submitted:
        if not name.strip() or not nim.strip() or not institution.strip():
            st.error("Nama, NIM/kode responden, dan institusi wajib diisi.")
        elif not consent:
            st.error("Mohon konfirmasi persetujuan sebelum mengirim jawaban.")
        elif any(v["score"] is None for v in answers.values()):
            st.error("Masih ada pernyataan yang belum dijawab. Periksa kembali nomor 1–30.")
        else:
            try:
                score_values = [v["score"] for v in answers.values()]
                total_score = sum(score_values)
                payload = {
                    "respondent_name": name.strip(),
                    "respondent_code": nim.strip(),
                    "institution": institution.strip(),
                    "response_date": str(date_value),
                    "answers": answers,
                    "total_score": total_score,
                }
                client = get_supabase()
                client.table("responses").insert(payload).execute()
                st.success("Terima kasih. Jawaban kamu berhasil direkam.")
                st.info("Total skor jawaban berhasil disimpan. Silakan tutup halaman ini.")
            except Exception as exc:
                st.error("Jawaban belum berhasil disimpan. Periksa koneksi atau hubungi admin.")
                st.exception(exc)

elif menu == "Admin":
    st.header("Dashboard Admin")
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    if not st.session_state.admin_authenticated:
        password = st.text_input("Password Admin", type="password")
        if st.button("Login Admin"):
            if password == st.secrets["ADMIN_PASSWORD"]:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Password tidak sesuai.")
    else:
        if st.button("Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()

        try:
            client = get_supabase()
            result = (
                client.table("responses")
                .select("*")
                .order("created_at", desc=True)
                .execute()
            )
            records = result.data or []

            if not records:
                st.info("Belum ada jawaban responden yang masuk.")
            else:
                df = pd.DataFrame(records)
                col1, col2, col3 = st.columns(3)
                col1.metric("Jumlah responden", len(df))
                col2.metric("Rata-rata total skor", round(df["total_score"].mean(), 2))
                col3.metric("Skor maksimum per responden", 120)

                st.subheader("Data Responden")
                respondent_view = df[
                    ["respondent_name", "respondent_code", "institution",
                     "response_date", "total_score", "created_at"]
                ].copy()
                st.dataframe(respondent_view, use_container_width=True)

                detail_rows = []
                for record in records:
                    for number, answer in (record.get("answers") or {}).items():
                        detail_rows.append({
                            "Nama": record.get("respondent_name"),
                            "Kode Responden": record.get("respondent_code"),
                            "Institusi": record.get("institution"),
                            "Nomor": int(number),
                            "Aspek": answer.get("aspect"),
                            "Pernyataan (EN)": answer.get("question_en"),
                            "Pernyataan (ID)": answer.get("question_id"),
                            "Jawaban": answer.get("answer_label"),
                            "Skor": answer.get("score"),
                        })

                detail_df = pd.DataFrame(detail_rows).sort_values(
                    ["Kode Responden", "Nomor"]
                )

                st.subheader("Detail Jawaban")
                st.dataframe(detail_df, use_container_width=True)

                st.subheader("Rekapitulasi per Butir")
                if not detail_df.empty:
                    summary = (
                        detail_df.groupby(["Nomor", "Aspek", "Pernyataan (ID)"])
                        .agg(
                            Jumlah_Jawaban=("Skor", "count"),
                            Total_Skor=("Skor", "sum"),
                            Rata_Rata=("Skor", "mean"),
                        )
                        .reset_index()
                    )
                    summary["Persentase_Skor"] = (
                        summary["Total_Skor"] / (summary["Jumlah_Jawaban"] * 4) * 100
                    ).round(2)
                    summary["Rata_Rata"] = summary["Rata_Rata"].round(2)
                    st.dataframe(summary, use_container_width=True)
                    st.bar_chart(summary.set_index("Nomor")["Persentase_Skor"])

                st.subheader("Unduh Data")
                csv_bytes = detail_df.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    "Download detail jawaban (CSV)",
                    data=csv_bytes,
                    file_name="detail_jawaban_speaktive.csv",
                    mime="text/csv",
                )

                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                    respondent_view.to_excel(writer, sheet_name="Responden", index=False)
                    detail_df.to_excel(writer, sheet_name="Detail Jawaban", index=False)
                    if not detail_df.empty:
                        summary.to_excel(writer, sheet_name="Rekap Butir", index=False)

                st.download_button(
                    "Download laporan lengkap (Excel)",
                    data=excel_buffer.getvalue(),
                    file_name="laporan_kuesioner_speaktive.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

        except Exception as exc:
            st.error("Data gagal dimuat. Periksa pengaturan Supabase dan secrets aplikasi.")
            st.exception(exc)

