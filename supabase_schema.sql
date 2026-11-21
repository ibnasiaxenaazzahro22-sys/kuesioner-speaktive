-- Jalankan di Supabase > SQL Editor.
-- Tabel ini menyimpan satu baris untuk setiap pengiriman kuesioner.
create table if not exists public.responses (
    id bigint generated always as identity primary key,
    respondent_name text not null,
    respondent_code text not null,
    institution text not null,
    response_date date not null,
    answers jsonb not null,
    total_score integer not null check (total_score between 30 and 120),
    created_at timestamptz not null default now()
);

-- RLS tetap aktif. Aplikasi Streamlit mengakses tabel dari sisi server
-- menggunakan SERVICE ROLE KEY yang disimpan di Secrets, bukan di kode publik.
alter table public.responses enable row level security;
