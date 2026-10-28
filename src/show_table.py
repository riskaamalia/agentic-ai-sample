"""Daftar tabel kebutuhan data (D1, D2, ...) yang bisa ditampilkan di dashboard."""

from src.tables.d01 import load_d01

# Tabel lain ditambahkan di sini setelah sumbernya diverifikasi.
TABEL = {
    "D1": load_d01,
}

SEMUA_KODE = [f"D{i}" for i in range(1, 13)]
