import json
import logging
import scapy.all as scapy
from scapy.layers.http import HTTPRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def packet_handler(packet, detailed):
    try:
        if packet.haslayer(HTTPRequest) and packet[HTTPRequest].Host == b'localhost:8080':
            src_ip = packet[scapy.IP].src
            dst_ip = packet[scapy.IP].dst
            src_port = packet[scapy.TCP].sport
            dst_port = packet[scapy.TCP].dport
            protocol = "TCP"
            payload = packet[scapy.Raw].load if scapy.Raw in packet else None

            logger.info("Source IP: %s", src_ip)
            logger.info("Source Port: %s", src_port)
            logger.info("Destination IP: %s", dst_ip)
            logger.info("Destination Port: %s", dst_port)
            logger.info("Protocol: %s", protocol)

            if detailed and payload:
                logger.info("Payload: %s", payload)
            elif payload:
                logger.info("Payload (truncated): %s", payload[:50] + b'...')

            logger.info('-' * 40)

            packet_data = {
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "src_port": src_port,
                "dst_port": dst_port,
                "protocol": protocol,
                "payload": payload.decode('utf-8', 'ignore') if payload else None
            }

            with open("output.json", "a") as f:
                json.dump(packet_data, f)
                f.write("\n")
    except Exception as e:
        logger.error("Error handling packet: %s", e)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Network Sniffer')
    parser.add_argument('-i', '--interface', type=str, required=True, help='Network interface to sniff on')
    parser.add_argument('-c', '--count', type=int, default=0, help='Number of packets to capture (0 for infinite)')
    parser.add_argument('--list', action='store_true', help='List available interfaces')
    parser.add_argument('-d', '--detailed', action='store_true', help='Print detailed packet information')

    args = parser.parse_args()

    if args.list:
        logger.info("Available Interfaces:")
        for iface_name in scapy.get_if_list():
            iface_data = scapy.get_if_hwaddr(iface_name)
            iface_ip = scapy.get_if_addr(iface_name)
            logger.info("%s - IP: %s, MAC: %s", iface_name, iface_ip, iface_data)
        return

    scapy.sniff(iface=args.interface, prn=lambda x: packet_handler(x, args.detailed), count=args.count)

if __name__ == "__main__":
    main()
