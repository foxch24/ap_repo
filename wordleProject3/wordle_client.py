import pygame
import socket
import json
import threading

# Constants
SERVER_HOST = 'localhost'
SERVER_PORT = 65432
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 30

# Pygame Initialization
# Constants
WIDTH, HEIGHT = 633, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.image.load("Starting Tiles.png")
BACKGROUND_RECT = BACKGROUND.get_rect(center=(317, 300))
ICON = pygame.image.load("Icon.png")
pygame.display.set_caption("Wordle!")
pygame.display.set_icon(ICON)
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"
pygame.init()
pygame.mixer.init()
# Load your music file
pygame.mixer.music.load('song2.mp3')
# Play the music
pygame.mixer.music.play(-1)
CORRECT_WORD = "coder"
ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
GUESSED_LETTER_FONT = pygame.font.Font("FreeSansBold.otf", 50)
AVAILABLE_LETTER_FONT = pygame.font.Font("FreeSansBold.otf", 25)
SCREEN.fill("white")
SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
pygame.display.update()
LETTER_X_SPACING = 85
LETTER_Y_SPACING = 12
LETTER_SIZE = 75.
pygame.display.set_caption("Multiplayer Wordle")
font = pygame.font.Font(None, FONT_SIZE)

# Client Class


class Letter:
    def __init__(self, text, bg_position):
        # Initializes all the variables, including text, color, position, size, etc.
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], self.bg_y, LETTER_SIZE, LETTER_SIZE)
        self.text = text
        self.text_position = (self.bg_x+36, self.bg_position[1]+34)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        # Puts the letter and text on the screen at the desired positions.
        pygame.draw.rect(SCREEN, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pygame.draw.rect(SCREEN, FILLED_OUTLINE, self.bg_rect, 3)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        # Fills the letter's spot with the default square, emptying it.
        pygame.draw.rect(SCREEN, "white", self.bg_rect)
        pygame.draw.rect(SCREEN, OUTLINE, self.bg_rect, 3)
        pygame.display.update()



class Indicator:
    def __init__(self, x, y, letter):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.rect = (self.x, self.y, 57, 75)
        self.bg_color = OUTLINE

    def draw(self):
        # Puts the indicator and its text on the screen at the desired position.
        pygame.draw.rect(SCREEN, self.bg_color, self.rect)
        self.text_surface = AVAILABLE_LETTER_FONT.render(self.text, True, "white")
        self.text_rect = self.text_surface.get_rect(center=(self.x+27, self.y+30))
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

class WordleClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server_host, server_port))
        self.game_state = None
        self.input_text = ""

    def start(self):
        receive_thread = threading.Thread(target=self.receive_game_state)
        receive_thread.start()

        running = True
        while running:
            SCREEN.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.send_guess(self.input_text)
                        self.input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if len(self.input_text) < 5:
                            self.input_text += event.unicode

            self.draw_game_state()
            pygame.display.flip()

        pygame.quit()

    def receive_game_state(self):
        while True:
            try:
                message = self.socket.recv(1024).decode()
                if message:
                    print(f"Received message: {message}")  # Debugging print
                    self.game_state = json.loads(message)
            except:
                print("Error receiving game state")  # Error handling
                break

    def send_guess(self, guess):
        message = json.dumps({"type": "guess", "guess": guess})
        self.socket.sendall(message.encode())

    def draw_game_state(self):
        if self.game_state:
            y = 50
            for guess in self.game_state["guesses"]:
                guess_text = f"{guess['guess']}: {' '.join(guess['result'])}"  # Include guess results
                text = font.render(guess_text, True, BLACK)
                SCREEN.blit(text, (50, y))
                y += FONT_SIZE + 10

        input_text = font.render(self.input_text, True, BLACK)
        SCREEN.blit(input_text, (50, HEIGHT - 50))

# Starting the client
if __name__ == "__main__":
    client = WordleClient(SERVER_HOST, SERVER_PORT)
    client.start()
# Drawing the indicators on the screen.

indicator_x, indicator_y = 20, 600

for i in range(3):
    for letter in ALPHABET[i]:
        new_indicator = Indicator(indicator_x, indicator_y, letter)
        indicators.append(new_indicator)
        new_indicator.draw()
        indicator_x += 60
    indicator_y += 100
    if i == 0:
        indicator_x = 50
    elif i == 1:
        indicator_x = 105

