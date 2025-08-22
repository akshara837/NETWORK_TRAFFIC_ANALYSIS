import pandas as pd
import matplotlib.pyplot as plt

# Load packet data from CSV
df = pd.read_csv("ALL_packets.csv")

# =============================
# 1. Protocol Distribution
# =============================
protocol_counts = df['Protocol'].value_counts()
print("\nProtocol Distribution:\n", protocol_counts)

plt.figure(figsize=(6,6))
protocol_counts.plot(kind='pie', autopct='%1.1f%%', shadow=True)
plt.title("Protocol Distribution")
plt.ylabel("")
plt.savefig("protocol_distribution.png") 

# =============================
# 2. Packets Over Time
# =============================
try:
    df["Time"] = pd.to_datetime(df["Time"], unit="s")
except:
    df["Time"] = pd.to_datetime(df["Time"])

# Group packets over time (per second)
packets_over_time = df.groupby(df["Time"].dt.floor("s")).size()

plt.figure(figsize=(10, 4))
packets_over_time.plot(kind="line", marker="o", color="red")
plt.title("Packets Over Time")
plt.xlabel("Time (seconds)")
plt.ylabel("Number of Packets")
plt.grid(True)
plt.savefig("packet_over_time.png")

# =============================
# 3. Top Source IPs
# =============================
top_src_ips = df['Source_IP'].value_counts().head(10)
print("\nTop Source IPs:\n", top_src_ips)

plt.figure(figsize=(8,14))
top_src_ips.plot(kind='bar')
plt.title("Top 10 Source IPs")
plt.xlabel("Source IP")
plt.ylabel("Packet Count")
plt.savefig("Top_10_source.png") 

# =============================
# 4. Top Destination IPs
# =============================
top_dst_ips = df['Destination_IP'].value_counts().head(10)
print("\nTop Destination IPs:\n", top_dst_ips)

plt.figure(figsize=(8,14))
top_dst_ips.plot(kind='bar', color="orange")
plt.title("Top 10 Destination IPs")
plt.xlabel("Destination IP")
plt.ylabel("Packet Count")
plt.savefig("Top_10_dest.png") 

# =============================
# 5. Top Source Ports
# =============================
if 'Source_Port' in df.columns:
    top_src_ports = df['Source_Port'].value_counts().head(10)
    print("\nTop Source Ports:\n", top_src_ports)

    plt.figure(figsize=(8,12))
    top_src_ports.plot(kind='bar', color="green")
    plt.title("Top 10 Source Ports")
    plt.xlabel("Source Port")
    plt.ylabel("Count")
    plt.savefig("Top_10_sourceports.png") 

# =============================
# 6. Top Destination Ports
# =============================
if 'Destination_Port' in df.columns:
    top_dst_ports = df['Destination_Port'].value_counts().head(10)
    print("\nTop Destination Ports:\n", top_dst_ports)

# =============================
# 7. Packet Length Distribution
# =============================
if 'Length' in df.columns:
    plt.figure(figsize=(8,5))
    df['Length'].plot(kind='hist', bins=30, color="purple", alpha=0.7)
    plt.title("Packet Length Distribution")
    plt.xlabel("Packet Length")
    plt.ylabel("Frequency")
    plt.savefig("packet_length_distribution.png") 

# =============================
# 8. Bandwidth Utilization
# =============================
if "Length" in df.columns:
    # Convert Time column again to ensure datetime
    try:
        df["Time"] = pd.to_datetime(df["Time"], unit="s")
    except:
        df["Time"] = pd.to_datetime(df["Time"])

    # Group by second and sum packet lengths (bytes/sec)
    bandwidth = df.groupby(df["Time"].dt.floor("s"))["Length"].sum().reset_index()

    # Convert Bytes/sec → KB/sec
    bandwidth["KB_per_sec"] = bandwidth["Length"] / 1024

    # Plot Bandwidth Utilization
    plt.figure(figsize=(12, 6))
    plt.plot(bandwidth["Time"], bandwidth["KB_per_sec"], marker='o', linestyle='-', color='b')
    plt.title("Bandwidth Utilization Over Time")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Bandwidth (KB/sec)")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.savefig("bandwidth_utilization.png")

print("\nAnalysis completed ✅")
