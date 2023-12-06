
import socket
import threading
import json
from random import choice
from words import *
# Constants
HOST = 'localhost'
PORT = 65432
MAX_CLIENTS = 2

# Server Class
class WordleServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.game_state = {
            "word": choice(WORDS),
            "guesses": [],
            "max_attempts": 6
        }
        self.lock = threading.Lock()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(MAX_CLIENTS)
        print(f"Server started on {self.host}:{self.port}")

        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Connected to {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        self.clients.append(client_socket)

        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"Received message: {message}")
                    self.process_message(client_socket, message)
            except ConnectionResetError:
                break

        client_socket.close()
        self.clients.remove(client_socket)
        print("Client disconnected")

    def process_message(self, client_socket, message):
        data = json.loads(message)
        if data["type"] == "guess":
            self.process_guess(client_socket, data["guess"])

    def process_guess(self, client_socket, guess):
        with self.lock:
            result = self.check_guess(guess)
            self.game_state["guesses"].append({"guess": guess, "result": result})
            if len(self.game_state["guesses"]) >= self.game_state["max_attempts"] or guess == self.game_state["word"]:
                self.end_game()
            else:
                self.send_game_state()

    def check_guess(self, guess):
        result = []
        for i, letter in enumerate(guess):
            if letter == self.game_state["word"][i]:
                result.append("correct")
            elif letter in self.game_state["word"]:
                result.append("present")
            else:
                result.append("absent")
        return result

    def send_game_state(self):
        state = json.dumps(self.game_state)
        for client in self.clients:
            client.sendall(state.encode())

    def end_game(self):
        self.send_game_state()
        self.game_state["word"] = choice(WORDS)
        self.game_state["guesses"] = []

# Starting the server
if __name__ == "__main__":
    server = WordleServer(HOST, PORT)
    server.start()
