
import socket
import threading
import random
from words import WORDS  # Importing the word list

# Constants
PORT = 5555
HOST = '0.0.0.0'
MAX_PLAYERS = 2

# Game state
target_word = random.choice(WORDS)  # Randomly select a word from the list
players = []  # List to keep track of players
guesses = {player: [] for player in range(MAX_PLAYERS)}  # Dictionary to track each player's guesses

# Function to handle client communication
def handle_client(client_socket, player_id):
    global guesses
    while True:
        try:
            guess = client_socket.recv(1024).decode('utf-8').strip().lower()
            if guess:
                print(f"Player {player_id} guessed: {guess}")
                response = check_guess(guess)
                client_socket.send(response.encode('utf-8'))
                if response == 'Correct!':
                    announce_winner(player_id)
                    break
        except:
            break
    client_socket.close()

# Function to check the guess against the target word
def check_guess(guess):
    if guess == target_word:
        return 'Correct!'
    else:
        # Implement logic to give feedback on the guess (similar to original Wordle logic)
        return 'Incorrect'

# Function to announce the winner
def announce_winner(winner_id):
    for player in players:
        try:
            player.send(f"Player {winner_id} wins!".encode('utf-8'))
        except:
            continue

# Main function to set up the server
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_PLAYERS)
    print(f"Server started on {HOST}:{PORT}, waiting for {MAX_PLAYERS} players...")

    player_id = 0
    while len(players) < MAX_PLAYERS:
        client, addr = server.accept()
        print(f"Player {player_id} connected from {addr}")
        players.append(client)
        threading.Thread(target=handle_client, args=(client, player_id)).start()
        player_id += 1

    print("All players connected. Game starts!")

if __name__ == '__main__':
    main()
