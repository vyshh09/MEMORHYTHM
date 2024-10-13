import pygame
import random
import time
import math

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800  
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memorhythm")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

LIGHT_RED = (255, 100, 100)
LIGHT_BLUE = (100, 100, 255)
LIGHT_GREEN = (100, 255, 100)
LIGHT_YELLOW = (255, 255, 100)
LIGHT_ORANGE = (255, 200, 100)
LIGHT_PURPLE = (200, 100, 200)
LIGHT_CYAN = (100, 255, 255)

# Drum pad positions, sizes, and labels
note_labels = ['Sa', 'Ri', 'Ga', 'Ma', 'Pa', 'Da', 'Ni']
keys = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j]


pads = {}
radius = 150 
center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2  

for i, key in enumerate(keys):
    angle = (i / len(keys)) * (2 * math.pi)  # Calculate angle for each pad
    pos = (center_x + int(radius * math.cos(angle)), center_y + int(radius * math.sin(angle)))  # Calculate position on circle

    pads[key] = {
        'color': RED if i == 0 else BLUE if i == 1 else GREEN if i == 2 else YELLOW if i == 3 else ORANGE if i == 4 else PURPLE if i == 5 else CYAN,
        'light_color': LIGHT_RED if i == 0 else LIGHT_BLUE if i == 1 else LIGHT_GREEN if i == 2 else LIGHT_YELLOW if i == 3 else LIGHT_ORANGE if i == 4 else LIGHT_PURPLE if i == 5 else LIGHT_CYAN,
        'pos': pos,
        'radius': 50,
        'sound': f'./audios/{i+1}.mp3',  # Assuming sound files are named 1.wav, 2.wav, etc.
        'label': note_labels[i]
    }

# Load sounds
for pad in pads.values():
    pad['sound'] = pygame.mixer.Sound(pad['sound'])

# Font setup
font = pygame.font.Font(None, 36)

def generate_sequence(length):
    return [random.choice(list(pads.keys())) for _ in range(length)]

def play_sequence(sequence):
    for key in sequence:
        pad = pads[key]
        pygame.draw.circle(screen, pad['light_color'], pad['pos'], pad['radius'])
        pygame.display.flip()
        pad['sound'].play()
        time.sleep(0.2)
        draw_background()
        draw_pads()
        pygame.display.flip()
        time.sleep(0.2)

def draw_background():
    # Set a background gradient
    for i in range(SCREEN_HEIGHT):
        color = (0, 0, 0)
        gradient = int(255 * (i / SCREEN_HEIGHT))
        pygame.draw.line(screen, (gradient, gradient, gradient), (0, i), (SCREEN_WIDTH, i))

def draw_pads():
    for key, pad in pads.items():
        pygame.draw.circle(screen, pad['color'], pad['pos'], pad['radius'])
        label = font.render(pad['label'], True, BLACK)
        label_rect = label.get_rect(center=pad['pos'])
        screen.blit(label, label_rect)

def draw_user_sequence(user_sequence):
    sequence_text = ' '.join([pads[key]['label'] for key in user_sequence])
    text_surface = font.render(f"Your input: {sequence_text}", True, BLACK)
    screen.blit(text_surface, (10, 10))

def handle_mouse_click(pos):
    for key, pad in pads.items():
        if (pad['pos'][0] - pad['radius'] < pos[0] < pad['pos'][0] + pad['radius'] and
                pad['pos'][1] - pad['radius'] < pos[1] < pad['pos'][1] + pad['radius']):
            pygame.draw.circle(screen, pad['light_color'], pad['pos'], pad['radius'])  # Highlight the pad
            label = font.render(pad['label'], True, BLACK)
            label_rect = label.get_rect(center=pad['pos'])
            screen.blit(label, label_rect)
            pygame.display.flip()
            pad['sound'].play()
            time.sleep(0.1)
            return key  # Return the key corresponding to the clicked pad
    return None

def display_message(message):
    text_surface = font.render(message, True, BLACK)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    time.sleep(0.3)

def game_loop():
    sequence = generate_sequence(3)  # Start with 3 beats
    level = 1
    user_sequence = []

    while True:
        draw_background()
        draw_pads()
        pygame.display.flip()

        time.sleep(0.2)
        display_message(f"Level {level}")
        play_sequence(sequence)

        waiting_for_input = True
        start_time = time.time()

        while waiting_for_input:
            draw_background()
            draw_pads()
            draw_user_sequence(user_sequence)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key in pads:
                        pad = pads[event.key]
                        pygame.draw.circle(screen, pad['light_color'], pad['pos'], pad['radius'])
                        label = font.render(pad['label'], True, BLACK)
                        label_rect = label.get_rect(center=pad['pos'])
                        screen.blit(label, label_rect)
                        pygame.display.flip()
                        pad['sound'].play()
                        user_sequence.append(event.key)
                        time.sleep(0.1)

                        if len(user_sequence) == len(sequence):
                            waiting_for_input = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    clicked_key = handle_mouse_click(mouse_pos)
                    if clicked_key:
                        user_sequence.append(clicked_key)
                        time.sleep(0.1)

                        if len(user_sequence) == len(sequence):
                            waiting_for_input = False

            if time.time() - start_time > 3 + len(sequence):  
                waiting_for_input = False

        if user_sequence == sequence:
            level += 1
            sequence = generate_sequence(1 + level) 
            display_message(f"Game Over! You reached level {level}.")
            break

        user_sequence = []
        time.sleep(0.3)

print("Welcome to Echo Beats!")
display_message("Watch and listen to the sequence, then repeat it using the Sa, Ri, Ga, Ma, Pa, Da, Ni keys or by clicking on the pads.")
pygame.event.wait()

game_loop()
pygame.quit()
