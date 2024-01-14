import time
import hashlib
import bcrypt
import os
import itertools
import string
from colorama import Fore, Style

def detect_hash_type(hash_value):
    if hash_value.startswith('$2a$'):
        return 'bcrypt'

    hash_length = len(hash_value)

    if hash_length == 32:
        return 'md5'
    elif hash_length == 40:
        return 'sha1'
    elif hash_length == 64:
        return 'sha256'
    elif hash_length == 128:
        return 'sha512'
    else:
        return 'unknown'

def generate_hashes(password, hash_type):
    if hash_type == 'bcrypt':
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    else:
        hash_function = getattr(hashlib, hash_type)
        hashed_password = hash_function(password.encode('utf-8')).hexdigest()

    return hashed_password

def read_file(file_path, file_type):
    try:
        with open(file_path, 'r', encoding='latin-1', errors='ignore') as file:
            content = [line.strip() for line in file]
        return content
    except FileNotFoundError as e:
        print(f"Error: {file_type} file '{file_path}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error reading {file_type} file: {e}")
        exit(1)

def print_help():
    print("Usage:")
    print("  python3 hash-cracker.py")
    exit(1)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def brute_force_attack(hash_to_crack, hash_type, min_length, max_length, output_file):
    found = False
    attempt_count = 0

    for password_length in range(int(min_length), int(max_length) + 1):
        for combination in itertools.product(string.ascii_letters + string.digits + string.punctuation, repeat=password_length):
            attempt_count += 1
            current_attempt = ''.join(combination)
            hashed_password = generate_hashes(current_attempt, hash_type)

            if hash_to_crack == hashed_password:
                print(f"Hash: {hash_to_crack}, Password: {Fore.GREEN}{current_attempt}{Style.RESET_ALL}, Attempt Count: {attempt_count}, Status: FOUND")
                found = True
                with open(output_file, 'a') as out_file:
                    out_file.write(f"{hash_to_crack}:{current_attempt}\n")
                break
            else:
                print(f"Hash: {hash_to_crack}, Password: {current_attempt}, Attempt Count: {attempt_count}, Status: NOT FOUND")

        if found:
            break

    return found

def dictionary_attack(hash_to_crack, hash_type, wordlist, output_file):
    found = False
    attempt_count = 0

    for password in wordlist:
        attempt_count += 1
        hashed_password = generate_hashes(password, hash_type)

        if hash_to_crack == hashed_password:
            print(f"Hash: {hash_to_crack}, Password: {Fore.GREEN}{password}{Style.RESET_ALL}, Attempt Count: {attempt_count}, Status: FOUND")
            found = True
            with open(output_file, 'a') as out_file:
                out_file.write(f"{hash_to_crack}:{password}\n")
            break
        else:
            print(f"Hash: {hash_to_crack}, Password: {password}, Attempt Count: {attempt_count}, Status: NOT FOUND")

    return found

def main():
    clear_terminal()

    banner_text = """
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
   
     RAPTOR is a simple Python3 program designed to assist in decrypting (cracking) 
       hashed passwords stored in a file. This program supports two attack modes, 
                    namely Dictionary Attack and Brute-Force Attack.

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""

    print(banner_text)

    try:
        hash_file = input("Enter the path to the hash file: ")
        hash_values = read_file(hash_file, 'hash')

        print(f"\n[*] Number of Hashes: {len(hash_values)}")

        print("\nSelect Attack Mode\n")
        print("1. Dictionary Attack")
        print("2. Brute-Force Attack\n")

        attack_mode_choice = input("Enter your choice (1 or 2): ")
        if attack_mode_choice not in {'1', '2'}:
            raise ValueError
        
        if attack_mode_choice == '1':
            mode = 'dictionary'
            print("\n[*] Selected Attack Mode: Dictionary Attack\n")
            wordlist_file = input("Enter the path to your wordlist: ")
            wordlist = read_file(wordlist_file, 'wordlist')
            print(f"\n[*] Number of Passwords in Wordlist: {len(wordlist)}")
            confirmation = input("\nDo you want to start dictionary attack? (Type 'YES' to proceed): ")
            if confirmation.upper() != 'YES':
                print("Attack aborted. Good Bye:).")
                exit(0)
            output_file = input("Enter the path to the output file (to save results): ")
            print("")
        elif attack_mode_choice == '2':
            mode = 'brute-force'
            print("\n[*] Selected Attack Mode: Brute-Force Attack\n")
            min_length = input("Enter the minimum length of passwords: ")
            max_length = input("Enter the maximum length of passwords: ")
            confirmation = input("\nDo you want to start brute-force attack? (Type 'YES' to proceed): ")
            if confirmation.upper() != 'YES':
                print("Attack aborted. Good Bye:).")
                exit(0)
            output_file = input("Enter the path to the output file (to save results): ")
            print("")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except ValueError:
        print("Invalid input. Please enter a valid choice.")
        exit(1)
    except KeyboardInterrupt:
        print("\nGood Bye:).")
        exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

    try:
        for hash_to_crack in hash_values:
            hash_type = detect_hash_type(hash_to_crack)
            found = False
            attempt_count = 0

            if mode == 'brute-force':
                found = brute_force_attack(hash_to_crack, hash_type, min_length, max_length, output_file)
            elif mode == 'dictionary':
                found = dictionary_attack(hash_to_crack, hash_type, wordlist, output_file)

            if not found:
                print(f"Hash: {hash_to_crack}, Password: -, Attempt Count: {attempt_count}, Status: NOT MATCH FOUND")

        
    except KeyboardInterrupt:
        print("\nGood Bye:).")
        exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
