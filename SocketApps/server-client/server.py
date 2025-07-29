import socket
import threading
import signal
import sys
import time


class TCPServer:
    def __init__(self, host="127.0.0.1", port=8888):
        self.host = host
        self.port = port
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.server_socket.settimeout(1.0)  # 1 second timeout
        print(f"[+] Server started on {self.host}:{self.port}")
        print("[*] Press Ctrl+C to stop the server.")

        try:
            while self.running:
                try:
                    client_socket, addr = self.server_socket.accept()
                    print(f"[+] Connection from {addr}")
                    client_thread = threading.Thread(
                        target=self.handle_client, args=(client_socket, addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    continue  # Timeout allows us to check self.running
        except KeyboardInterrupt:
            self.shutdown()

    def handle_client(self, client_socket, addr):
        with client_socket:
            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    message = data.decode("utf-8")
                    print(f"[{addr}] {message}")
                    response = f"Server received: {message}"
                    client_socket.sendall(response.encode("utf-8"))
                except ConnectionResetError:
                    print(f"[-] Connection with {addr} reset.")
                    break

        print(f"[-] Disconnected from {addr}")

    def shutdown(self):
        print("\n[*] Shutting down server...")
        self.running = False
        self.server_socket.close()
        time.sleep(1)
        print("\n[✓] Server shutdown success.\n")
        sys.exit(0)


if __name__ == "__main__":
    server = TCPServer()
    server.start()
