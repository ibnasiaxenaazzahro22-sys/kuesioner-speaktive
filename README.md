# Kuesioner SPEAKTIVE - Need Analysis

Proyek awal website kuesioner berdasarkan file "QUESTIONNAIRE SHEET OF STUDENTS NEED ANALYSIS".
Berisi 30 pernyataan bilingual (Inggris dan Indonesia), identitas responden, skala Likert 4 poin,
penyimpanan Supabase, dashboard admin, dan ekspor CSV/Excel.

## A. Siapkan Supabase
1. Buka https://supabase.com/ dan buat project.
2. Buka menu SQL Editor.
3. Jalankan seluruh isi file `supabase_schema.sql`.
4. Buka Project Settings > API (atau API Keys).
5. Salin Project URL dan `service_role` / secret key. Jangan bagikan key ini.

## B. Siapkan Python
1. Instal Python 3.10 atau lebih baru.
2. Ekstrak folder proyek.
3. Buka terminal di folder `kuesioner_speaktive`.
4. Buat virtual environment (opsional tetapi disarankan):
   - Windows: `py -m venv .venv`
   - Aktifkan: `.venv\Scripts\activate`
5. Instal paket: `pip install -r requirements.txt`
6. Buat folder `.streamlit` bila belum ada dan buat file `secrets.toml`.
7. Isi `secrets.toml` dengan URL, service role key, dan password admin:
   ```
   SUPABASE_URL = "https://PROJECT_ID.supabase.co"
   SUPABASE_SERVICE_ROLE_KEY = "..."
   ADMIN_PASSWORD = "..."
   ```
8. Jalankan: `streamlit run app.py`

## C. Deploy supaya bisa dibuka responden
1. Buat repository GitHub dan unggah `app.py`, `requirements.txt`, serta file SQL/README.
2. JANGAN unggah `.streamlit/secrets.toml` atau service role key ke GitHub.
3. Buka https://share.streamlit.io/ dan hubungkan repository.
4. Pilih `app.py` sebagai Main file path.
5. Di App settings > Secrets, masukkan isi secrets (URL, service role key, password admin).
6. Deploy, lalu bagikan URL aplikasi kepada responden.

## D. Catatan keamanan dan penelitian
- Admin page memakai password aplikasi. Gunakan password kuat dan jangan membagikannya.
- Service role key hanya boleh berada di Secrets/server, tidak boleh ditaruh di source code publik.
- Data identitas dan jawaban responden bersifat privat. Batasi akses admin dan minta persetujuan responden.
- Versi awal ini belum membatasi satu kode responden untuk satu kali pengisian. Jika dibutuhkan, tambahkan aturan unik dan validasi duplikasi setelah keputusan peneliti.
- Persentase skor per butir dihitung dengan rumus: total skor aktual / (jumlah jawaban valid x 4) x 100.
- Pastikan redaksi, identitas yang diminta, dan prosedur persetujuan sesuai arahan dosen/penelitian sebelum disebarkan.
