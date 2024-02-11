import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys
import os
from PIL import Image

def get_all_image_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    image_links = []

    # Menampilkan semua tautan gambar yang ditemukan pada URL
    print(f"\nGambar yang tersedia pada {url}:")
    for i, img_tag in enumerate(soup.find_all('img'), start=1):
        src = img_tag.get('src')
        if src:
            image_links.append(urljoin(url, src))
            print(f"{i}. {urljoin(url, src)}")

    return image_links

def download_images(url, image_links):
    # Membuat folder dengan nama URL
    folder_name = urlparse(url).hostname
    os.makedirs(folder_name, exist_ok=True)

    # Mendownload dan menyimpan gambar-gambar dengan nama asli di dalam folder
    for i, img_url in enumerate(image_links, start=1):
        response = requests.get(img_url)

        # Mengekstrak nama file dari URL
        file_name = os.path.basename(urlparse(img_url).path)

        print(f"\nSedang mendownload gambar ({file_name})...")

        # Menggunakan PIL untuk menyimpan gambar dengan kualitas tertinggi
        img = Image.open(response.content)
        img.save(f'{folder_name}/{file_name}', quality=95)  # Sesuaikan nilai kualitas sesuai kebutuhan

        print(f"Download gambar {i} selesai.")

def print_help():
    print("Cara Penggunaan:")
    print("python script.py <URL> [--unduh]")
    print("\nOpsi:")
    print("  --unduh   : Mengunduh semua gambar dari URL")

def main():
    # Membaca URL dan opsi dari argumen baris perintah
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print_help()
        sys.exit(1)

    # Menampilkan menu bantuan jika argumen adalah '--help' atau '-h'
    if sys.argv[1] in ['--help', '-h']:
        print_help()
        sys.exit(0)

    url_to_detect = sys.argv[1]
    unduh_flag = "--unduh" in sys.argv

    # Mendapatkan semua tautan gambar dari URL
    image_links = get_all_image_links(url_to_detect)

    # Jika opsi '--unduh' disertakan, maka unduh semua gambar
    if unduh_flag:
        download_images(url_to_detect, image_links)
        print("\nSeluruh pengunduhan gambar selesai.")
    else:
        # Jika tidak ada opsi '--unduh', tampilkan pesan deteksi gambar selesai
        print("\nDeteksi gambar selesai.")

if __name__ == "__main__":
    main()
