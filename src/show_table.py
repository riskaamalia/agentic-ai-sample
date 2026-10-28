"""Daftar tabel kebutuhan data (D1, D2, ...) yang bisa ditampilkan di dashboard."""

from src.tables.d01 import load_d01
from src.tables.d02 import load_d02

# Tabel lain ditambahkan di sini setelah sumbernya diverifikasi.
TABEL = {
    "D1": load_d01,
    "D2": load_d02,
}

SEMUA_KODE = [f"D{i}" for i in range(1, 13)]
