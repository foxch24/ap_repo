
import pygame
import socket

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 633, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle Multiplayer")

# Colors and fonts
font = pygame.font.Font(None, 36)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive

# Input box setup
input_box = pygame.Rect(50, 850, 140, 40)
active = False
text = ''
done = False

# Networking setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '10.1.132.152'  # Server IP
PORT = 5555
client_socket.connect((HOST, PORT))

# Function to send a guess to the server
def send_guess(guess):
    client_socket.send(guess.encode('utf-8'))

# Main game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    send_guess(text)
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    screen.fill((255, 255, 255))
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, color, input_box, 2)

    # Check for messages from the server
    try:
        message = client_socket.recv(1024).decode('utf-8')
        if message:
            print(message)  # For now, just print the message. This could be displayed on the screen.
    except:
        pass

    pygame.display.flip()

pygame.quit()
client_socket.close()
