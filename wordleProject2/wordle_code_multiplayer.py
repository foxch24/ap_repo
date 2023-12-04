import pygame
import socket
from words import WORDS  # Import the word list for validating guesses

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 633, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle Multiplayer")

# Colors and fonts (adapted from wordle_code.py)
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"
GUESSED_LETTER_FONT = pygame.font.Font(None, 50)  # Example font, adjust as needed

# Networking setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '127.0.0.1'  # Server IP
PORT = 5555
client_socket.connect((HOST, PORT))

# Initialize the Wordle game interface (from wordle_code.py)
# Assuming a 5x6 grid for Wordle (5 letters, 6 attempts)
GRID_POS = (50, 100)  # Adjust as needed
CELL_SIZE = 100
GRID = [[{'letter': '', 'color': GREY} for _ in range(5)] for _ in range(6)]

current_attempt = 0
current_letter = 0

# Function to draw the Wordle grid
def draw_grid():
    for y, row in enumerate(GRID):
        for x, cell in enumerate(row):
            letter = cell['letter']
            color = cell['color']
            # Draw cell background
            pygame.draw.rect(screen, color, (GRID_POS[0] + x * CELL_SIZE, GRID_POS[1] + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            # Draw letter
            text_surface = GUESSED_LETTER_FONT.render(letter.upper(), True, (0, 0, 0))
            screen.blit(text_surface, (GRID_POS[0] + x * CELL_SIZE + 30, GRID_POS[1] + y * CELL_SIZE + 30))

# Function to send a guess to the server
def send_guess(guess):
    if guess.lower() in WORDS:  # Validate the guess
        client_socket.send(guess.encode('utf-8'))

# Function to update the game interface based on server's response
def update_game_interface(server_response):
    global current_attempt
    if server_response == 'Correct!':
        # Update the grid for a correct guess
        for cell in GRID[current_attempt]:
            cell['color'] = GREEN
    else:
        # Update the grid for an incorrect guess
        # This part needs to be adapted based on the specific feedback logic in wordle_code.py
        # For example, marking some letters as yellow, others as grey
        pass
    current_attempt += 1

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            client_socket.close()
            exit()

        # Handle user input for guesses (adapted from wordle_code.py)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and current_letter == 5:
                guess = ''.join([cell['letter'] for cell in GRID[current_attempt]])
                send_guess(guess)
                current_letter = 0
            elif event.key == pygame.K_BACKSPACE and current_letter > 0:
                current_letter -= 1
                GRID[current_attempt][current_letter]['letter'] = ''
            elif current_letter < 5 and event.unicode.isalpha():
                GRID[current_attempt][current_letter]['letter'] = event.unicode
                current_letter += 1

    screen.fill((255, 255, 255))  # Clear screen
    draw_grid()  # Render the Wordle game interface

    # Check for messages from the server
    try:
        message = client_socket.recv(1024).decode('utf-8')
        if message:
            update_game_interface(message)
    except:
        pass

    pygame.display.flip()