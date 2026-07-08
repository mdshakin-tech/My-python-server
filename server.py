import socket
import threading

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] Connected to client: {client_address}")
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
                
            print(f"[{client_address}] Received: {data}")
            
            try:
                number = int(data)
                result = f"Square of {number} is {number ** 2}"
            except ValueError:
                result = "Error: Please send a valid number."
            
            client_socket.send(result.encode('utf-8'))
        except ConnectionResetError:
            break

    print(f"[DISCONNECTED] Connection closed for {client_address}")
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # '0.0.0.0' allows connections from any public or local IP
    host = '0.0.0.0' 
    port = 12345
    server_socket.bind((host, port))
    
    server_socket.listen()
    print(f"[LISTENING] Server is running on port {port}...")
    
    while True:
        client_socket, client_address = server_socket.accept()
        # Create a new thread for each client connection
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_server()
