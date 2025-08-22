from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
import pandas as pd

# List to store packet information
packet_list = []

# Function to process each packet
def process_packet(pkt):
    if IP in pkt:
        protocol = ""
        src_port = ""
        dst_port = ""
        flags = ""
        http_info = ""

        # TCP packets
        if TCP in pkt:
            protocol = "TCP"
            src_port = pkt[TCP].sport
            dst_port = pkt[TCP].dport
            flags = pkt[TCP].flags

            # Check if it contains HTTP data (port 80)
            if pkt[TCP].dport == 80 or pkt[TCP].sport == 80:
                if Raw in pkt:
                    payload = pkt[Raw].load.decode(errors='ignore')
                    lines = payload.split("\r\n")
                    http_info = "; ".join([line for line in lines[:5]])  # first 5 lines of HTTP header

        # UDP packets
        elif UDP in pkt:
            protocol = "UDP"
            src_port = pkt[UDP].sport
            dst_port = pkt[UDP].dport

        # ICMP packets
        elif ICMP in pkt:
            protocol = "ICMP"

        # Add packet info
        packet_list.append({
            "Time": pkt.time,
            "Source_IP": pkt[IP].src,
            "Destination_IP": pkt[IP].dst,
            "Protocol": protocol,
            "Source_Port": src_port,
            "Destination_Port": dst_port,
            "Length": len(pkt),
            "Flags": flags,
            "HTTP_Info": http_info
        })

# --- User Settings ---
num_packets = 50  # number of packets to capture
filter_protocol = input("Enter protocol to filter (TCP/UDP/ICMP/HTTP/ALL): ").upper()

# Define a filter function
def protocol_filter(pkt):
    if filter_protocol == "ALL":
        return IP in pkt
    if filter_protocol == "TCP" and TCP in pkt:
        return True
    if filter_protocol == "UDP" and UDP in pkt:
        return True
    if filter_protocol == "ICMP" and ICMP in pkt:
        return True
    if filter_protocol == "HTTP":
        if TCP in pkt and (pkt[TCP].dport == 80 or pkt[TCP].sport == 80):
            return True
    return False

# Capture packets
print(f"Capturing {num_packets} packets with filter: {filter_protocol}...")
sniff(prn=process_packet, lfilter=protocol_filter, count=num_packets)

# Export to CSV
df = pd.DataFrame(packet_list)
csv_file = f"{filter_protocol}_packets.csv"
df.to_csv(csv_file, index=False)
print(f"CSV exported successfully as {csv_file}!")

