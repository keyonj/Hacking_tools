# Network Scanning and Penetration Testing Tools

This repository contains a set of Python-based tools designed for network scanning and penetration testing. These tools can be used to identify vulnerabilities in networks, scan ports, and detect various network properties like operating systems and MAC addresses.

## Features

- **IP Range Scanning**: Scan a range of IP addresses to discover live hosts.
- **OS and MAC Address Detection**: Identify the operating system and MAC address of target devices.
- **TCP/UDP Port Scanning**: Scan for open or closed ports on the target system.
- **Fast Scanning**: Perform a quick scan on the first 20 ports.
- **Detailed Scan**: Get more in-depth results with full port range scans and protocol analysis.
- **Multithreaded Scanning**: Scan multiple ports in parallel to speed up the process.

## Requirements

- Python 3.x
- Scapy
- Colorama
- Pyfiglet
- Tabulate

You can install the required dependencies using pip:

```bash
pip install scapy colorama pyfiglet tabulate

Usage

To use the tool, run the script with the following options

python scan_tool.py -t [TARGET_IP] -r [NETWORK_RANGE] -p [PORT_RANGE] -s -P [PROTOCOL]

Arguments:

    -t, --target: Target IP address to scan.
    -r, --range: IP range to scan (e.g., 192.168.1.0/24).
    -p, --ports: Port range to scan (e.g., 20-80).
    -s, --fast: Enable fast scanning mode (scans first 20 ports only).
    -P, --protocol: Choose protocol for scanning (TCP or UDP)Example:

Scan a specific target IP on ports 80-100 using TCP protocol
python scan_tool.py -t 192.168.1.1 -p 80-100 -P TCP

Scan a range of IPs for live hosts:
python scan_tool.py -r 192.168.1.0/24 -p 20-100

Output

The results will display:

    Operating System and MAC Address: Information about the target device.
    Port Scan Results: Whether the ports are open, closed, or filtered
Port Scan Results for 192.168.1.1:
+-------+---------+
| Port  | Status  |
+-------+---------+
| 80    | Open    |
| 443   | Closed  |
+-------+---------+
