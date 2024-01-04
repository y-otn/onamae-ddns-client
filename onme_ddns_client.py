import socket
import ssl
import time
from datetime import datetime

# Official client minimum is 300 seconds. Do not set below this value.
# 公式クライアントの最小値は300秒です。これより小さい値を設定しないでください。
INTERVAL = 1800
USERID = '1234567'
PASSWORD = 'password'
HOSTNAME = ''  # optional
DOMNAME = 'example.com'

# Check configuration values and support for Japanese domain names.
assert INTERVAL >= 300
HOSTNAME = HOSTNAME.encode('idna').decode()
DOMNAME = DOMNAME.encode('idna').decode()


def recv_message(ssl_sock):
    buffer = bytearray()
    while True:
        data = ssl_sock.recv(4096)
        buffer += data
        if b'\n.' in buffer or not data:
            break
    return buffer.decode()


def send_message(ssl_sock, message):
    ssl_sock.sendall(message.encode())


def get_ipv4_address():
    with socket.create_connection(('ddnsclient.onamae.com', 65000), timeout=15) as sock:
        message = recv_message(sock)
    return message.split()[1]


def check_ipv4_domain(ipv4):
    domain = (HOSTNAME + '.' if HOSTNAME else '') + DOMNAME
    addresses = socket.gethostbyname_ex(domain)[2]
    return ipv4 in addresses


def check_server_status(ssl_sock, logged_in=False):
    message = recv_message(ssl_sock)
    status_code = int(message.split()[0])
    if status_code:
        if logged_in:
            send_message(ssl_sock, 'LOGOUT\n.\n')
        print(f'{datetime.now()} - Failed to update DNS records. Status: {message.splitlines()[0]}')
    return status_code


def update_dns_records():
    try:
        ipv4 = get_ipv4_address()
        if check_ipv4_domain(ipv4):
            print(f'{datetime.now()} - No update necessary, DNS records are current.')
            return
        context = ssl.create_default_context()
        with socket.create_connection(('ddnsclient.onamae.com', 65010), timeout=15) as sock, \
                context.wrap_socket(sock, server_hostname='ddnsclient.onamae.com') as ssl_sock:
            if check_server_status(ssl_sock):
                return
            send_message(ssl_sock, f'LOGIN\nUSERID:{USERID}\nPASSWORD:{PASSWORD}\n.\n')
            if check_server_status(ssl_sock, logged_in=True):
                return
            send_message(ssl_sock, f'MODIP\nHOSTNAME:{HOSTNAME}\nDOMNAME:{DOMNAME}\nIPV4:{ipv4}\n.\n')
            if check_server_status(ssl_sock, logged_in=True):
                return
            send_message(ssl_sock, 'LOGOUT\n.\n')
            if check_server_status(ssl_sock):
                return
        print(f'{datetime.now()} - DNS records updated successfully. IPv4: {ipv4}')
    except Exception as e:
        print(f'{datetime.now()} - Failed to update DNS records. Exception: {e}')


def main():
    while True:
        update_dns_records()
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()
