import psutil
from scapy.all import sniff, IP, UDP
from collections import Counter, deque

import subprocess
import re

'''
get_pid_by_name - Gets the process id of 'halo5forge.exe'

parameters:
    process_name (str) - The string of the process to pattern match, 'halo5forge.exe'
returns:
    None if process could not be found
    proc.info['pid'] (int) - The PID of the given process
'''
def get_pid_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None


'''
get_game_ip - Gets the most likely local ip of 'halo5forge.exe'
THIS IS NOT YOUR PUBLIC IP. This should be a 192.168.X.X address. This means it's local, just within your network.
This is what Microsoft uses to communicate to your game player position, score, updates, etc.
Traffic goes from Microsoft/Halo servers to your router (public IP, which we don't touch). Then the router decides
    what computer to send it to. This is the IP we check against, the local one that takes in the information.

parameters:
    pid (int) - the PID of the process we're looking for
returns:
    None if an IP couldn't be found
    matches[0] (str) - The string of the local IP of the game (should be 192.168.4.67 from my testing)
'''
def get_game_ip(pid):
    command = f"netstat -ano | findstr {pid}"
    output = subprocess.check_output(command, shell=True, text=True)
    ip_pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+):\d+")

    for line in output.splitlines():
        if "ESTABLISHED" in line:
            matches = ip_pattern.findall(line)
            if matches and matches[0] != "127.0.0.1":
                return matches[0]
    return None


'''
analyze_traffic - This analyzes the UDP packets coming to and from the game (from the source and destination IP)
    to determine what game server we are connected to.

parameters:
    game_ip (str) - The local IP of the game
    exclude_ip (str, "66.22.212.149") - This is the authentication/handshake for Xbox Live Profiles
        We filter this out because we don't care that we're connected to the xbox service

returns:
    Nothing

prints:
    "New server detected" - This is the server that we are most likely connected to given the last 200 packets
'''
def analyze_traffic(game_ip, exclude_ip="66.22.212.149"):
    recent_packets = deque(maxlen=200) # Limit of the last number of packets we store
    packet_counter = Counter()
    current_server = None

    def packet_handler(packet):
        nonlocal current_server
        if UDP in packet and IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst

            if game_ip in (src_ip, dst_ip) and exclude_ip not in (src_ip, dst_ip):
                key = (src_ip, dst_ip)

                if len(recent_packets) == recent_packets.maxlen:
                    oldest_packet = recent_packets.popleft()
                    packet_counter[oldest_packet] -= 1
                    if packet_counter[oldest_packet] == 0:
                        del packet_counter[oldest_packet]

                recent_packets.append(key)
                packet_counter[key] += 1

                most_common = packet_counter.most_common(1)[0]
                most_common_ip = most_common[0][0] if most_common[0][1] == game_ip else most_common[0][1]

                if most_common_ip != current_server:
                    current_server = most_common_ip
                    print(f"New server detected: {current_server}")
                #print(f"Most communicated server: {most_common[0]} -> {most_common[1]} packets")
    
    sniff(filter=f"udp and (host {game_ip})", prn=packet_handler, store=False)



if __name__ == "__main__":
    try:
        process_name = 'halo5forge.exe'
        pid = get_pid_by_name(process_name)

        if pid:
            print(f"Found PID: {pid}")
            game_ip = get_game_ip(pid)

            if game_ip:
                print(f"Game IP: {game_ip}")
                print("Starting traffic analysis...")
                analyze_traffic(game_ip)
            else:
                print("Could not find game IP.")
        else:
            print(f"Process {process_name} not found.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please make an issue on github describing the problem and what occurred")
    finally:
        input("Press 'enter' to exit...")