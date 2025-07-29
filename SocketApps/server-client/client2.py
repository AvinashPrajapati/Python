import socket
import sys


def main():
    host = "127.0.0.1"
    port = 8888

    with socket.create_connection((host, port)) as sock:
        print("[+] Connected to server. Type messages, or 'exit' to quit.\n")

        while True:
            message = input("You: ")
            if message.lower() == "exit":
                print("[*] Closing connection.")
                break

            sock.sendall(message.encode("utf-8"))

            try:
                data = sock.recv(1024)
                if not data:
                    print("[-] Server closed the connection.")
                    break
                print("Server:", data.decode("utf-8"))
            except ConnectionResetError:
                print("[-] Connection reset by server.")
                break


if __name__ == "__main__":
    main()
