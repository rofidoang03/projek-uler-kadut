package main

import (
	"fmt"
	"golang.org/x/crypto/ssh"
	"log"
)

func main() {
	// Ganti dengan informasi koneksi SSH Anda
	hostname := "example.com"
	port := 22
	username := "your_username"
	password := "your_password"

	config := &ssh.ClientConfig{
		User: username,
		Auth: []ssh.AuthMethod{
			ssh.Password(password),
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(), // Gunakan dengan hati-hati, sebaiknya gunakan HostKeyCallback yang lebih aman dalam produksi.
	}

	// Buka koneksi SSH
	conn, err := ssh.Dial("tcp", fmt.Sprintf("%s:%d", hostname, port), config)
	if err != nil {
		log.Fatalf("Unable to connect: %v", err)
	}
	defer conn.Close()

	fmt.Println("Connected to", hostname)

	// Dapat melakukan sesuatu dengan koneksi SSH di sini, seperti menjalankan perintah.
	// Contoh:
	session, err := conn.NewSession()
	if err != nil {
		log.Fatalf("Unable to create session: %v", err)
	}
	defer session.Close()

	output, err := session.CombinedOutput("echo Hello, SSH!")
	if err != nil {
		log.Fatalf("Unable to run command: %v", err)
	}

	fmt.Println("Command output:", string(output))
}
