import socket
import requests
import urllib3

# Disable the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # Set a timeout for the connection attempt
        try:
            s.connect((ip, port))
            return True
        except (socket.timeout, socket.error):
            return False


def check_admin_interface(ip, port):
    try:
        url = f"https://{ip}:{port}/login"
        response = requests.get(url, timeout=1, verify=False)

        # Check if we get a successful response
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass

    return False
def main():
    # Lists of IPs and ports to check
    ips = ['46.14.53.154', '8.8.8.8', '193.33.142.200']
    ports = [80, 443, 22, 21, 10000]

    for ip in ips:
        for port in ports:
            if check_port(ip, port):
                print(f"Port {port} is open on {ip}")

                if port == 10000 and check_admin_interface(ip, port):
                    print(f"Admin interface is open on {ip}")

            else:
                print(f"Port {port} is not open on {ip}")

if __name__ == "__main__":
    main()