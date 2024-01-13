import instaloader

def download_from_url(url):
    # Inisialisasi objek Instaloader
    L = instaloader.Instaloader()

    try:
        # Mendownload dari URL postingan
        post = instaloader.Post.from_shortcode(L.context, url)
        L.download_post(post, target=post.owner_username)

        print("Unduhan dari URL selesai.")
    except instaloader.exceptions.PostNotExistsException:
        print(f"Postingan dengan URL {url} tidak ditemukan.")

def download_all_posts(target_username):
    # Inisialisasi objek Instaloader
    L = instaloader.Instaloader()

    try:
        # Profil target
        profile = instaloader.Profile.from_username(L.context, target_username)

        # Mendownload seluruh gambar dan video
        L.download_profile(profile, profile_pic_only=False)

        print("Unduhan seluruh postingan selesai.")
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Akun dengan username {target_username} tidak ditemukan.")

if __name__ == "__main__":
    print("Pilih opsi:")
    print(\n"1. Download dari URL postingan")
    print("2. Download semua postingan dari akun tertentu\n")
    
    option = input("Masukkan nomor opsi (1/2): ")

    if option == "1":
        url = input("Masukkan URL postingan: ")
        download_from_url(url)
    elif option == "2":
        target_username = input("Masukkan username target: ")
        download_all_posts(target_username)
    else:
        print("Opsi tidak valid.")
      
