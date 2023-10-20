import socket

def check_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # Set a timeout for the connection attempt
        try:
            s.connect((ip, port))
            return True
        except (socket.timeout, socket.error):
            return False

def main():
    # Lists of IPs and ports to check
    ips = ['46.14.53.154', '8.8.8.8']
    ports = [80, 443, 22, 21, 10000]

    for ip in ips:
        for port in ports:
            if check_port(ip, port):
                print(f"Port {port} is open on {ip}")
            else:
                print(f"Port {port} is not open on {ip}")

if __name__ == "__main__":
    main()
