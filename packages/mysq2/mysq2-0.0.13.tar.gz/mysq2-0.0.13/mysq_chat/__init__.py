import socket
import threading
import json
import sys  # Import sys module for exit()

class mysq2:

    def __init__(self):
        self.host = '13.233.166.198'
        self.port = 9989
        self.username = "Kinjal"
        self.ADDR = (self.host, self.port)
        self.main()


    def receive_messages(self, client_socket):
        """Receives messages from the server."""
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message.lower() == f"{self.username} is Disconnected!":
                    break
                print(message)
            except Exception as e:
                print("EXITED FROM SERVER")
                break

    def main(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(self.ADDR)

        # Receive chat history from server
        history = json.loads(client_socket.recv(4096).decode())
        print("Chat history:")
        for msg in history:
            if msg['address'] != self.username:  # Exclude own messages
                print(f"{msg['address']}: {msg['message']}")

        # Start receiving messages from server
        receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
        receive_thread.start()

        # Send messages to the server
        while True:
            message = input("")
            if message.lower() == 'exit':
                client_socket.send(f"{self.username} is Disconnected!".encode())
                client_socket.close()  # Close the client socket
                sys.exit(0)  # Terminate the program
            client_socket.send(f"{self.username}: {message}".encode())

        receive_thread.join()

mysq2()