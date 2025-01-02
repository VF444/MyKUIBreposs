import socket
import threading
import sys
import os


# Функція для обробки клієнта (для echo-сервера та багатокористувацького сервера)
def handle_client(client_socket):
    data = client_socket.recv(1024).decode('utf-8')
    print(f"Received: {data}")
    client_socket.send(data.encode('utf-8'))
    client_socket.close()


# Функція для роботи як TCP-сервер
def start_server(mode):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server is running...")

    if mode == "echo" or mode == "multi":
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connected to {addr}")

            if mode == "echo":
                # Обробка одного клієнта
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Received: {data}")
                client_socket.send(data.encode('utf-8'))
                client_socket.close()
            elif mode == "multi":
                # Обробка кількох клієнтів послідовно
                threading.Thread(target=handle_client, args=(client_socket,)).start()

    elif mode == "file_receive":
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connected to {addr}")
            with open('received_file.txt', 'wb') as f:
                print("Receiving file...")
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    f.write(data)
            print("File received successfully.")
            client_socket.close()


# Функція для роботи як TCP-клієнт
def start_client(mode):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    if mode == "echo":
        message = input("Enter message to send: ")
        client_socket.send(message.encode('utf-8'))
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received from server: {data}")
        client_socket.close()

    elif mode == "file_send":
        file_path = input("Enter the file path to send: ")
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                print("Sending file...")
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    client_socket.sendall(data)
            print("File sent successfully.")
            client_socket.close()
        else:
            print(f"File {file_path} does not exist!")


# Основна функція
def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <role> <mode>")
        print("Roles: server, client")
        print("Modes: echo, multi, file_send, file_receive")
        sys.exit(1)

    role = sys.argv[1]
    mode = sys.argv[2]

    if role == "server":
        start_server(mode)
    elif role == "client":
        start_client(mode)
    else:
        print("Invalid role. Use 'server' or 'client'.")


if __name__ == "__main__":
    main()
