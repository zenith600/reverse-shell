# Reverse Shell Multi-Client Management

This project implements a **multi-client reverse shell** using Python, allowing a server to manage multiple client connections, list clients, and execute PowerShell commands on them.

## Features

- Handle multiple reverse shell connections.
- List connected clients with IP and username.
- Select a client to interact with.
- Execute commands remotely via PowerShell.

## Prerequisites

- Python 3.x on both server and client.
- Open port on the server for incoming connections.

## Setup

### Server Setup

1. **Edit server IP and port** in `server.py`:
   ```python
   server_ip = "localhost"
   server_port = 4444
   ```

2. **Run the server**:
   ```bash
   python server.py
   ```

### Client Setup

1. **Edit server IP and port** in `client.py`:
   ```python
   server_ip = "localhost"
   server_port = 4444
   ```

2. **Run the client**:
   ```bash
   python client.py
   ```

## Usage

- **`list`**: List connected clients with IP and username.
- **`details <index>`**: Show details of a specific client.
- **`select <index>`**: Select a client to send commands.
- **`exit`**: Exit the shell or stop interacting with a client.

### Example

```bash
ServerShell> list
[0] IP: 192.168.1.10, Username: user1
[1] IP: 192.168.1.12, Username: user2

ServerShell> select 0
Shell(192.168.1.10)> dir
```

## Security

⚠️ **Use this system responsibly** in trusted environments. For security, implement encryption and authentication.

