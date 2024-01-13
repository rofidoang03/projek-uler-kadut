import hashlib
import bcrypt
from colorama import Fore
import sys
import getopt
import os

m = Fore.LIGHTRED_EX
h = Fore.LIGHTGREEN_EX
k = Fore.LIGHTYELLOW_EX
r = Fore.RESET
b = Fore.LIGHTBLUE_EX

def detect_hash_type(hash_value):
    hash_length = len(hash_value)

    if hash_length == 32:
        return 'md5'
    elif hash_length == 40:
        return 'sha1'
    elif hash_length == 64:
        return 'sha256'
    elif hash_length == 128:
        return 'sha512'
    elif hash_length == 60 and hash_value.startswith('$2a$'):
        return 'bcrypt'
    else:
        return 'unknown'

def generate_hashes(password):
    hashed_passwords = {}

    # MD5
    md5_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
    hashed_passwords['md5'] = md5_hash

    # SHA-1
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
    hashed_passwords['sha1'] = sha1_hash

    # SHA-256
    sha256_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    hashed_passwords['sha256'] = sha256_hash

    # SHA-512
    sha512_hash = hashlib.sha512(password.encode('utf-8')).hexdigest()
    hashed_passwords['sha512'] = sha512_hash

    # bcrypt
    salt = bcrypt.gensalt()
    bcrypt_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    hashed_passwords['bcrypt'] = bcrypt_hash

    return hashed_passwords

def read_hashes(hash_file):
    with open(hash_file, 'r', encoding='latin-1', errors='ignore') as file:
        hash_values = [line.strip() for line in file]
    return hash_values

def read_wordlist(wordlist_file):
    with open(wordlist_file, 'r', encoding='latin-1', errors='ignore') as file:
        wordlist = [line.strip() for line in file]
    return wordlist

def print_help():
    print("Usage:")
    print("  python3 hash-cracker.py --hash-file [hash_file] --wordlist-file [wordlist_file]")
    print("\nOptions:")
    print("  --hash-file       : Name of the file containing hashes to crack.")
    print("  --wordlist-file   : Name of the file containing the wordlist.")
    sys.exit(0)

def clear_terminal():
    # Check the operating system and execute the appropriate command
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_terminal()  # Clear the terminal screen

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["hash-file=", "wordlist-file="])
    except getopt.GetoptError:
        print_help()

    hash_file = None
    wordlist_file = None

    for opt, arg in opts:
        if opt == "--hash-file":
            hash_file = arg
        elif opt == "--wordlist-file":
            wordlist_file = arg

    if hash_file is None or wordlist_file is None:
        print_help()

    # Read hashes from the file
    hash_values = read_hashes(hash_file)

    # Display the number of hashes and passwords
    print(f"{b}[*] {r}Number of Hashes: {len(hash_values)}")

    # Read the wordlist from the file
    wordlist = read_wordlist(wordlist_file)

    # Display the number of passwords
    print(f"{b}[*] {r}Number of Passwords: {len(wordlist)}\n")

    try:
        # Compare hashes with passwords in the wordlist
        for hash_to_crack in hash_values:
            hash_type = detect_hash_type(hash_to_crack)
            found = False
            attempt_count = 0

            # Check if the hash matches any password in the wordlist
            for password in wordlist:
                attempt_count += 1
                hashed_passwords = generate_hashes(password)

                if hash_to_crack in hashed_passwords.values():
                    print(f"{r}[{h}Attempt {attempt_count}{r}/{h}{len(wordlist)}{r}] {h}{hash_type}{r}({h}{hash_to_crack}{r}):{h}{password} {r}[{h}FOUND{r}]")
                    found = True
                    break  # Exit the loop after finding the first match and move on to the next hash
                else:
                    print(f"{r}[{m}Attempt {attempt_count}{r}/{m}{len(wordlist)}{r}] {m}{hash_type}{r}({m}{hash_to_crack}{r}):{m}{password} {r}[{m}NOT FOUND{r}]")

                    # Continue to the next password if no match is found for the current hash
                    continue

            if not found:
                print(f"{r}[{k}Attempt {attempt_count}{r}/{k}{len(wordlist)}{r}] {k}{hash_type}{r}({k}{hash_to_crack}{r}):{k}{password} {r}[{k}NOT MATCH FOUND{r}]")
    except KeyboardInterrupt:
        print(f"\n{r}Good Bye :)")
        sys.exit(0)

if __name__ == "__main__":
    main()
