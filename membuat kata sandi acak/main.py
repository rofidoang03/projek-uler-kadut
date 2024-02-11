#!/usr/bin/env python3

import sys
import random
import string

args = sys.argv[1:]
panjang = None
huruf_besar = False
huruf_kecil = False
simbol = False
angka = False

if not args or args[0] == "--bantuan":
    print(f"""Penggunaan: python3 {sys.argv[0]} [PILIHAN]

Program Python sederhana untuk membuat kata sandi acak.

Pilihan:

--panjang         : Menentukan panjang kata sandi.
--simbol          : Menggunakan simbol.
--angka           : Gunakan angka.
--huruf-besar     : Gunakan huruf besar.
--huruf-kecil     : Gunakan huruf kecil.
--bantuan         : Menampilkan informasi bantuan.

Contoh: python3 {sys.argv[0]} --panjang 12 --simbol --angka --huruf-besar --huruf-kecil""")
    sys.exit()

i = 0
while i < len(args):
    arg = args[i]
    if arg == "--panjang":
        i += 1
        if i < len(args):
            panjang = int(args[i])
            if panjang <= 0:
                print("Error: Panjang kata sandi harus lebih besar dari 0.")
                sys.exit()
        else:
            print("Error: Panjang kata sandi tidak valid.")
            sys.exit()
    elif arg == "--huruf-besar":
        huruf_besar = True
    elif arg == "--huruf-kecil":
        huruf_kecil = True
    elif arg == "--simbol":
        simbol = True
    elif arg == "--angka":
        angka = True
    else:
        print(f"Error: Argumen tidak valid: {arg}")
        print(f"Ketik 'python3 {sys.argv[0]} --bantuan' untuk menampilkan informasi bantuan.")
        sys.exit()
    i += 1

if panjang is None:
    print(f"Error: Mohon berikan panjang kata sandi.")
    print(f"Ketik 'python3 {sys.argv[0]} --bantuan' untuk menampilkan informasi bantuan.")
    sys.exit()

if not any([huruf_besar, huruf_kecil, simbol, angka]):
    print(f"Error: Anda perlu memilih setidaknya satu jenis karakter untuk kata sandi.")
    print(f"Ketik 'python3 {sys.argv[0]} --bantuan' untuk menampilkan informasi bantuan.")
    sys.exit()

karakter = ''
if huruf_besar:
    karakter += string.ascii_uppercase
if huruf_kecil:
    karakter += string.ascii_lowercase
if simbol:
    karakter += string.punctuation
if angka:
    karakter += string.digits

if not karakter:
    print(f"Error: Anda perlu memilih setidaknya satu jenis karakter untuk kata sandi.")
    sys.exit()

kata_sandi = ''.join(random.choice(karakter) for _ in range(panjang))
print(f"Kata sandi acak: {kata_sandi}")
