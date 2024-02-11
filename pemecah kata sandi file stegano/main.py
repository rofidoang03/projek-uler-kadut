# Program : Pemecah Kata Sandi File Stegano
# Pembuat : Rofidoang03
# Github : https://github.com/rofidoang/projek-uler-kadut

import os
import sys
import subprocess

# Memeriksa apakah jumlah argumen yang diberikan sesuai
if len(sys.argv) != 3:
    print(f"Penggunaan: python3 {sys.argv[0]} [file steghide] [file wordlist]")
    sys.exit(1)

# Mengambil argumen dari baris perintah
file_steghide = sys.argv[1]
wordlist = sys.argv[2]

# Memeriksa apakah file steghide ada
if not os.path.exists(file_steghide):
    print(f"File steghide '{file_steghide}' tidak ditemukan.")
    sys.exit(1)

# Memeriksa apakah file wordlist ada
if not os.path.exists(wordlist):
    print(f"File wordlist '{wordlist}' tidak ditemukan.")
    sys.exit(1)

# Membuka file wordlist dan mencoba setiap kata sandi
with open(wordlist, 'r', encoding='latin-1', errors='ignore') as w:
    for baris in w:
        kata_sandi = baris.strip()
        perintah = ['steghide', 'extract', '-sf', file_steghide, '-p', kata_sandi, '-f']

        try:
            # Menjalankan perintah steghide dan menangkap keluaran
            hasil = subprocess.run(perintah, capture_output=True, text=True, check=True)
            print(f"Kata sandi ditemukan: {kata_sandi}")
            break

        except subprocess.CalledProcessError:
            # Menangani jika kata sandi salah
            print(f"Kata sandi salah: {kata_sandi}")

    else:
        # Menampilkan pesan jika kata sandi tidak ditemukan dalam wordlist
        print(f"Kata sandi tidak ditemukan dalam wordlist '{wordlist}'.")
