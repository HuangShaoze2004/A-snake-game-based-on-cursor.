import pygame
import time
import random
import math

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)  # Darker green for snake head
LIGHT_GREEN = (144, 238, 144)  # Light green for decorative elements
GRAY = (220, 220, 220)    # Light gray color for grid lines
GOLD = (255, 215, 0)      # Gold color for bonus food
BLUE = (50, 153, 213)     # Sky blue for background
GRASS_GREEN = (34, 139, 34)  # Grass green
PURPLE = (128, 0, 128)    # Purple color
ORANGE = (255, 165, 0)    # Orange color
YELLOW = (255, 255, 0)    # Yellow color

# Set game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

# Set game clock
clock = pygame.time.Clock()

# Set snake's initial position and size
SNAKE_BLOCK_SIZE = 20
SNAKE_SPEED_INITIAL = 10
SNAKE_SPEED_MAX = 20

# Load background image or create pattern
def create_background():
    # Create a grass pattern
    pattern = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    pattern.fill(BLUE)  # Fill with sky blue
    
    # Add some random grass patches
    for _ in range(50):
        size = random.randint(5, 15)
        x = random.randint(0, WINDOW_WIDTH-size)
        y = random.randint(0, WINDOW_HEIGHT-size)
        shade = random.randint(-20, 20)
        color = (max(0, min(255, GRASS_GREEN[0] + shade)), 
                max(0, min(255, GRASS_GREEN[1] + shade)), 
                max(0, min(255, GRASS_GREEN[2] + shade)))
        pygame.draw.ellipse(pattern, color, (x, y, size, size//2))
        
    return pattern

# Background pattern
background = create_background()

# Draw a decorative snake for the title screen
def draw_decorative_snake(animation_counter):
    # Create a snake path (sinusoidal movement)
    snake_points = []
    snake_length = 20
    start_x = WINDOW_WIDTH // 4
    start_y = WINDOW_HEIGHT // 4
    
    # Animation offset
    offset = animation_counter * 0.05
    
    for i in range(snake_length):
        x = start_x + i * 25
        y = start_y + math.sin(i * 0.5 + offset) * 30
        snake_points.append((x, y))
    
    # Draw snake body segments with gradient
    for i, point in enumerate(snake_points):
        if i == 0:  # Head
            # Draw head
            pygame.draw.circle(game_window, DARK_GREEN, point, SNAKE_BLOCK_SIZE)
            
            # Eyes
            eye_offset = 6
            pygame.draw.circle(game_window, WHITE, (point[0] - eye_offset, point[1] - eye_offset), 5)
            pygame.draw.circle(game_window, WHITE, (point[0] + eye_offset, point[1] - eye_offset), 5)
            
            # Pupils
            pygame.draw.circle(game_window, BLACK, (point[0] - eye_offset, point[1] - eye_offset), 2)
            pygame.draw.circle(game_window, BLACK, (point[0] + eye_offset, point[1] - eye_offset), 2)
            
            # Tongue
            tongue_length = 15
            pygame.draw.line(game_window, RED, (point[0], point[1] + 5), 
                           (point[0], point[1] + tongue_length), 2)
            pygame.draw.line(game_window, RED, (point[0], point[1] + tongue_length), 
                           (point[0] - 5, point[1] + tongue_length + 5), 2)
            pygame.draw.line(game_window, RED, (point[0], point[1] + tongue_length), 
                           (point[0] + 5, point[1] + tongue_length + 5), 2)
        else:  # Body
            # Calculate gradient color
            gradient_factor = i / snake_length
            color = (
                int(GREEN[0]),
                int(max(50, GREEN[1] - gradient_factor * 100)),
                int(GREEN[2])
            )
            pygame.draw.circle(game_window, color, point, max(5, SNAKE_BLOCK_SIZE - i/2))
    
    # Draw second snake at the bottom
    snake_points2 = []
    start_x2 = WINDOW_WIDTH * 3 // 4
    start_y2 = WINDOW_HEIGHT * 3 // 4
    
    for i in range(snake_length):
        x = start_x2 - i * 25
        y = start_y2 + math.cos(i * 0.5 + offset) * 30
        snake_points2.append((x, y))
    
    # Draw second snake
    for i, point in enumerate(snake_points2):
        if i == 0:  # Head
            pygame.draw.circle(game_window, DARK_GREEN, point, SNAKE_BLOCK_SIZE)
            
            # Eyes
            eye_offset = 6
            pygame.draw.circle(game_window, WHITE, (point[0] - eye_offset, point[1] - eye_offset), 5)
            pygame.draw.circle(game_window, WHITE, (point[0] + eye_offset, point[1] - eye_offset), 5)
            
            # Pupils
            pygame.draw.circle(game_window, BLACK, (point[0] - eye_offset, point[1] - eye_offset), 2)
            pygame.draw.circle(game_window, BLACK, (point[0] + eye_offset, point[1] - eye_offset), 2)
        else:  # Body
            gradient_factor = i / snake_length
            color = (
                int(GREEN[0]),
                int(max(50, GREEN[1] - gradient_factor * 100)),
                int(GREEN[2])
            )
            pygame.draw.circle(game_window, color, point, max(5, SNAKE_BLOCK_SIZE - i/2))

# Animated title text
def draw_animated_title(animation_counter):
    title_text = "SNAKE GAME"
    font_size = 90
    title_font = pygame.font.SysFont(None, font_size)
    
    # Draw each letter with animation
    total_width = 0
    for i, letter in enumerate(title_text):
        # Wave animation
        offset_y = math.sin(animation_counter * 0.1 + i * 0.5) * 10
        color_factor = (math.sin(animation_counter * 0.1 + i * 0.3) + 1) / 2  # Value between 0 and 1
        
        # Interpolate between green and yellow for a shimmering effect
        color = (
            int(GREEN[0] + (YELLOW[0] - GREEN[0]) * color_factor),
            int(GREEN[1] + (YELLOW[1] - GREEN[1]) * color_factor),
            int(GREEN[2] + (YELLOW[2] - GREEN[2]) * color_factor)
        )
        
        letter_surface = title_font.render(letter, True, color)
        letter_width = letter_surface.get_width()
        
        # Calculate position
        x_pos = (WINDOW_WIDTH - title_font.size(title_text)[0]) // 2 + total_width
        y_pos = WINDOW_HEIGHT // 8 + offset_y
        
        # Draw letter shadow for 3D effect
        shadow_surface = title_font.render(letter, True, (30, 30, 30))
        game_window.blit(shadow_surface, (x_pos + 3, y_pos + 3))
        
        # Draw letter
        game_window.blit(letter_surface, (x_pos, y_pos))
        
        total_width += letter_width

# Define text display function
def display_message(message, color, size, x_offset=0, y_offset=0):
    font = pygame.font.SysFont(None, size)
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = ((WINDOW_WIDTH / 2) + x_offset, (WINDOW_HEIGHT / 2) + y_offset)
    game_window.blit(text, text_rect)

# Display score in the top left corner
def display_score(score, color, size, animation_time=0):
    font = pygame.font.SysFont(None, size)
    
    # Score with animation effect
    if animation_time > 0:
        scale_factor = 1 + 0.5 * (1 - animation_time)  # Scale from 1.5 to 1.0
        scaled_size = int(size * scale_factor)
        anim_font = pygame.font.SysFont(None, scaled_size)
        anim_text = anim_font.render(f"Score: {score}", True, PURPLE)
        anim_rect = anim_text.get_rect()
        anim_rect.topleft = (10, 10)
        game_window.blit(anim_text, anim_rect)
    else:
        # Normal score display
        text = font.render(f"Score: {score}", True, color)
        game_window.blit(text, (10, 10))  # Position at the top left

# Draw snake function with distinctive head
def draw_snake(snake_block_size, snake_list, direction):
    # Draw body segments with gradient effect
    for i, block in enumerate(snake_list):
        # Create a gradient effect on the body
        if i < len(snake_list) - 1:  # Body segments
            # Calculate a gradient color based on position
            gradient_factor = i / max(1, len(snake_list) - 1)
            gradient_green = int(GREEN[1] - gradient_factor * 40)  # Gradually darker
            pygame.draw.rect(game_window, (GREEN[0], gradient_green, GREEN[2]), 
                            [block[0], block[1], snake_block_size, snake_block_size])
            
            # Add a small pattern/texture to each segment
            inner_margin = snake_block_size // 6
            inner_size = snake_block_size - 2 * inner_margin
            pygame.draw.rect(game_window, (GREEN[0], min(255, gradient_green + 40), GREEN[2]),
                            [block[0] + inner_margin, block[1] + inner_margin, 
                            inner_size, inner_size])
        else:  # This is the head
            # Draw head with darker color
            pygame.draw.rect(game_window, DARK_GREEN, [block[0], block[1], snake_block_size, snake_block_size])
            
            # Add eyes based on direction
            eye_size = snake_block_size // 5
            eye_offset = snake_block_size // 4
            
            # Left eye
            if direction == "RIGHT":
                left_eye_x = block[0] + snake_block_size - eye_offset
                left_eye_y = block[1] + eye_offset
            elif direction == "LEFT":
                left_eye_x = block[0] + eye_offset
                left_eye_y = block[1] + eye_offset
            elif direction == "UP":
                left_eye_x = block[0] + eye_offset
                left_eye_y = block[1] + eye_offset
            else:  # DOWN
                left_eye_x = block[0] + eye_offset
                left_eye_y = block[1] + snake_block_size - eye_offset
                
            # Right eye
            if direction == "RIGHT":
                right_eye_x = block[0] + snake_block_size - eye_offset
                right_eye_y = block[1] + snake_block_size - eye_offset
            elif direction == "LEFT":
                right_eye_x = block[0] + eye_offset
                right_eye_y = block[1] + snake_block_size - eye_offset
            elif direction == "UP":
                right_eye_x = block[0] + snake_block_size - eye_offset
                right_eye_y = block[1] + eye_offset
            else:  # DOWN
                right_eye_x = block[0] + snake_block_size - eye_offset
                right_eye_y = block[1] + snake_block_size - eye_offset
                
            # Draw eyes
            pygame.draw.circle(game_window, WHITE, (left_eye_x, left_eye_y), eye_size)
            pygame.draw.circle(game_window, WHITE, (right_eye_x, right_eye_y), eye_size)
            
            # Draw pupils
            pygame.draw.circle(game_window, BLACK, (left_eye_x, left_eye_y), eye_size // 2)
            pygame.draw.circle(game_window, BLACK, (right_eye_x, right_eye_y), eye_size // 2)

# Draw food with animation
def draw_food(x, y, size, food_type="regular", animation=0):
    if food_type == "regular":
        color = RED
        # Pulsating animation
        pulse_size = size * (1 + 0.2 * math.sin(animation * 0.2))
        offset = (size - pulse_size) / 2
        
        # Draw apple-like shape
        pygame.draw.circle(game_window, color, 
                         (int(x + size/2), int(y + size/2)), 
                         int(pulse_size/2))
        
        # Add stem
        pygame.draw.rect(game_window, (139, 69, 19), 
                       [x + size/2 - 2, y + offset, 4, 6])
    else:  # Bonus food
        color = GOLD
        # Rotating/spinning animation
        spin_x = x + size/2 + (size/4) * math.cos(animation * 0.3)
        spin_y = y + size/2 + (size/4) * math.sin(animation * 0.3)
        
        # Draw a star-like shape for bonus food
        points = 5
        inner_radius = size / 4
        outer_radius = size / 2
        
        star_points = []
        for i in range(points * 2):
            angle = math.pi * 2 * i / (points * 2)
            radius = outer_radius if i % 2 == 0 else inner_radius
            px = x + size/2 + radius * math.cos(angle + animation * 0.1)
            py = y + size/2 + radius * math.sin(angle + animation * 0.1)
            star_points.append((px, py))
            
        if len(star_points) >= 3:
            pygame.draw.polygon(game_window, color, star_points)

# Draw grid function
def draw_grid(block_size):
    for x in range(0, WINDOW_WIDTH, block_size):
        pygame.draw.line(game_window, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, block_size):
        pygame.draw.line(game_window, GRAY, (0, y), (WINDOW_WIDTH, y))

# Draw difficulty selector
def draw_difficulty_menu():
    # Animation variables
    animation_counter = 0
    start_time = time.time()
    
    # Difficulty options
    difficulties = [("Easy", SNAKE_SPEED_INITIAL - 3), 
                   ("Medium", SNAKE_SPEED_INITIAL), 
                   ("Hard", SNAKE_SPEED_INITIAL + 3)]
    
    button_width = 200
    button_height = 60
    button_margin = 30
    total_height = len(difficulties) * (button_height + button_margin) - button_margin
    start_y = (WINDOW_HEIGHT - total_height) // 2 + 50
    
    buttons = []
    for i, (text, speed) in enumerate(difficulties):
        button_x = (WINDOW_WIDTH - button_width) // 2
        button_y = start_y + i * (button_height + button_margin)
        buttons.append((button_x, button_y, button_width, button_height, text, speed))
    
    # Wait for selection
    waiting = True
    selected_speed = SNAKE_SPEED_INITIAL
    
    while waiting:
        # Update animation counter
        current_time = time.time()
        animation_counter = int((current_time - start_time) * 60)  # 60 fps equivalent
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for x, y, w, h, _, speed in buttons:
                    if x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h:
                        selected_speed = speed
                        waiting = False
                        break
        
        # Draw background with gradient
        game_window.fill(BLUE)
        
        # Draw animated decorative elements
        draw_decorative_snake(animation_counter)
        
        # Draw animated title
        draw_animated_title(animation_counter)
        
        # Draw "Select Difficulty" text
        subtitle_font = pygame.font.SysFont(None, 55)
        subtitle_text = subtitle_font.render("Select Difficulty:", True, WHITE)
        subtitle_rect = subtitle_text.get_rect()
        subtitle_rect.center = (WINDOW_WIDTH // 2, start_y - 50)
        game_window.blit(subtitle_text, subtitle_rect)
        
        # Draw buttons with hover effect
        mouse_pos = pygame.mouse.get_pos()
        for i, (x, y, w, h, text, _) in enumerate(buttons):
            # Check if mouse is hovering over button
            is_hover = x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h
            
            # Choose button color based on hover state
            if is_hover:
                button_color = LIGHT_GREEN  # Lighter color on hover
                scale_factor = 1.1  # Slightly larger on hover
            else:
                button_color = GREEN
                scale_factor = 1.0
                
            # Calculate scaled dimensions
            scaled_w = int(w * scale_factor)
            scaled_h = int(h * scale_factor)
            scaled_x = x - (scaled_w - w) // 2
            scaled_y = y - (scaled_h - h) // 2
            
            # Draw button with pulsating effect for hovered button
            if is_hover:
                pulse = math.sin(animation_counter * 0.1) * 5
                pygame.draw.rect(game_window, button_color, [scaled_x-pulse, scaled_y-pulse, scaled_w+pulse*2, scaled_h+pulse*2])
                pygame.draw.rect(game_window, WHITE, [scaled_x-pulse, scaled_y-pulse, scaled_w+pulse*2, scaled_h+pulse*2], 3)
            else:
                pygame.draw.rect(game_window, button_color, [scaled_x, scaled_y, scaled_w, scaled_h])
                pygame.draw.rect(game_window, WHITE, [scaled_x, scaled_y, scaled_w, scaled_h], 2)
            
            # Draw text
            font_size = 45 if is_hover else 40
            font = pygame.font.SysFont(None, font_size)
            text_surface = font.render(text, True, WHITE)
            text_rect = text_surface.get_rect()
            text_rect.center = (scaled_x + scaled_w // 2, scaled_y + scaled_h // 2)
            game_window.blit(text_surface, text_rect)
        
        # Add designer credit in the bottom right corner
        credit_font = pygame.font.SysFont(None, 25)
        credit_text = credit_font.render("Designed by HuangShaoze", True, WHITE)
        credit_rect = credit_text.get_rect()
        credit_rect.bottomright = (WINDOW_WIDTH - 20, WINDOW_HEIGHT - 15)
        game_window.blit(credit_text, credit_rect)
        
        # Add instructions
        instruction_font = pygame.font.SysFont(None, 30)
        instruction_text = instruction_font.render("Click a difficulty to start", True, WHITE)
        instruction_rect = instruction_text.get_rect()
        instruction_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
        game_window.blit(instruction_text, instruction_rect)
        
        pygame.display.update()
        clock.tick(60)  # Cap at 60 fps for smooth animation
    
    return selected_speed

# Draw game over menu with options
def draw_game_over_menu(score):
    # Animation variables
    animation_counter = 0
    start_time = time.time()
    
    # Menu options
    options = [
        ("Continue (C)", pygame.K_c),
        ("Difficulty (D)", pygame.K_d),
        ("Quit (Q)", pygame.K_q)
    ]
    
    button_width = 300
    button_height = 50
    button_margin = 20
    total_height = len(options) * (button_height + button_margin) - button_margin
    start_y = (WINDOW_HEIGHT // 2) + 30
    
    buttons = []
    for i, (text, key) in enumerate(options):
        button_x = (WINDOW_WIDTH - button_width) // 2
        button_y = start_y + i * (button_height + button_margin)
        
        # Choose different colors for different options
        if i == 0:  # Continue
            button_color = GREEN
        elif i == 1:  # Difficulty
            button_color = YELLOW
        else:  # Quit
            button_color = RED
            
        buttons.append((button_x, button_y, button_width, button_height, text, key, button_color))
    
    # Draw game over screen with animation
    while True:
        # Update animation counter
        current_time = time.time()
        animation_counter = int((current_time - start_time) * 60)  # 60 fps equivalent
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for x, y, w, h, _, key, _ in buttons:
                    if x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h:
                        return buttons  # Return on button click
            if event.type == pygame.KEYDOWN:
                if event.key in [option[1] for option in options]:
                    return buttons  # Return on valid key press
        
        # Draw background
        game_window.blit(background, (0, 0))
        draw_grid(SNAKE_BLOCK_SIZE)
        
        # Draw falling game over text with bounce effect
        bounce_progress = min(1.0, animation_counter / 60)  # Takes 1 second to complete bounce
        if bounce_progress < 1.0:
            # Quadratic ease-out for bounce
            if bounce_progress < 0.8:
                y_offset = -120 * (1 - (bounce_progress / 0.8) ** 2)
            else:
                # Small bounce at the end
                normalized = (bounce_progress - 0.8) / 0.2
                y_offset = -10 * math.sin(normalized * math.pi)
        else:
            y_offset = 0
            
        # Draw game over title - no glow effect
        title_size = 75
        
        # Draw main text without any glow or shadow
        game_over_font = pygame.font.SysFont(None, title_size)
        game_over_text = game_over_font.render("Game Over!", True, RED)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) - 120 + y_offset)
        game_window.blit(game_over_text, game_over_rect)
        
        # Draw score with shine effect
        score_size = 50
        score_text = f"Final Score: {score}"
        score_font = pygame.font.SysFont(None, score_size)
        
        # Draw score with animated highlight
        highlight_pos = (animation_counter % 100) / 100  # Position from 0 to 1
        for i, char in enumerate(score_text):
            char_pos = i / len(score_text)
            distance = abs(char_pos - highlight_pos)
            
            # Make characters brighter when highlight passes over them
            brightness = max(0, 1 - distance * 5)  # Higher brightness when distance is small
            char_color = (
                min(255, int(WHITE[0] + brightness * (GOLD[0] - WHITE[0]))),
                min(255, int(WHITE[1] + brightness * (GOLD[1] - WHITE[1]))),
                min(255, int(WHITE[2] + brightness * (GOLD[2] - WHITE[2])))
            )
            
            char_surface = score_font.render(char, True, char_color)
            char_width = char_surface.get_width()
            total_width = score_font.size(score_text)[0]
            x_pos = (WINDOW_WIDTH - total_width) // 2 + score_font.size(score_text[:i])[0]
            
            game_window.blit(char_surface, (x_pos, (WINDOW_HEIGHT // 2) - 50))
        
        # Draw floating particles for decoration
        for i in range(20):
            particle_x = (WINDOW_WIDTH // 2) + math.sin(animation_counter * 0.01 + i) * 100
            particle_y = (WINDOW_HEIGHT // 2) - 85 + math.cos(animation_counter * 0.01 + i * 2) * 30
            particle_size = 2 + math.sin(animation_counter * 0.05 + i) * 1
            pygame.draw.circle(game_window, GOLD, (int(particle_x), int(particle_y)), int(particle_size))
        
        # Draw buttons with hover effect
        mouse_pos = pygame.mouse.get_pos()
        for i, (x, y, w, h, text, _, color) in enumerate(buttons):
            is_hover = x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h
            
            # Choose button attributes based on hover state
            if is_hover:
                scale_factor = 1.05  # Slightly larger on hover
                border_size = 3
            else:
                scale_factor = 1.0
                border_size = 2
                
            # Calculate scaled dimensions
            scaled_w = int(w * scale_factor)
            scaled_h = int(h * scale_factor)
            scaled_x = x - (scaled_w - w) // 2
            scaled_y = y - (scaled_h - h) // 2
            
            # Draw button with pulsating effect for hovered button
            if is_hover:
                pulse = 2 + math.sin(animation_counter * 0.1) * 2
                pygame.draw.rect(game_window, color, [scaled_x-pulse, scaled_y-pulse, scaled_w+pulse*2, scaled_h+pulse*2])
                pygame.draw.rect(game_window, WHITE, [scaled_x-pulse, scaled_y-pulse, scaled_w+pulse*2, scaled_h+pulse*2], border_size)
            else:
                pygame.draw.rect(game_window, color, [scaled_x, scaled_y, scaled_w, scaled_h])
                pygame.draw.rect(game_window, WHITE, [scaled_x, scaled_y, scaled_w, scaled_h], border_size)
            
            # Draw text
            font_size = 38 if is_hover else 35
            font = pygame.font.SysFont(None, font_size)
            text_surface = font.render(text, True, BLACK)
            text_rect = text_surface.get_rect()
            text_rect.center = (scaled_x + scaled_w // 2, scaled_y + scaled_h // 2)
            game_window.blit(text_surface, text_rect)
        
        # Add designer credit in the bottom right corner
        credit_font = pygame.font.SysFont(None, 25)
        credit_text = credit_font.render("Designed by HuangShaoze", True, WHITE)
        credit_rect = credit_text.get_rect()
        credit_rect.bottomright = (WINDOW_WIDTH - 20, WINDOW_HEIGHT - 15)
        game_window.blit(credit_text, credit_rect)
        
        pygame.display.update()
        clock.tick(60)  # Cap at 60 fps for smooth animation

# Game main loop
def game_loop(initial_speed=None):
    # Select difficulty if not provided
    if initial_speed is None:
        snake_speed = draw_difficulty_menu()
    else:
        snake_speed = initial_speed
    
    game_over = False
    game_exit = False
    
    # Animation counters
    animation_counter = 0
    score_animation = 0
    
    # Snake's initial position
    x = WINDOW_WIDTH / 2
    y = WINDOW_HEIGHT / 2
    
    # Snake's movement direction
    x_change = 0
    y_change = 0
    direction = "RIGHT"  # Default direction
    
    # Make sure snake is stationary at start
    has_started = False
    
    # Initial snake body
    snake_list = []
    snake_length = 1
    
    # Food counters and flags
    food_eaten_count = 0
    bonus_active = False
    
    # Generate first food position
    food_x = round(random.randrange(0, WINDOW_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
    food_y = round(random.randrange(0, WINDOW_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
    
    # Bonus food position
    bonus_x = 0
    bonus_y = 0
    
    # Game main loop
    while not game_exit:
        
        # Game over handling
        if game_over:
            buttons = draw_game_over_menu(snake_length - 1)
            
            # Handle key events and mouse clicks
            got_input = False
            while not got_input and not game_exit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_exit = True
                        got_input = True
                    
                    # Handle keyboard input
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_exit = True
                            got_input = True
                        elif event.key == pygame.K_c:
                            game_over = False
                            got_input = True
                            game_loop(snake_speed)
                            return
                        elif event.key == pygame.K_d:
                            game_over = False
                            got_input = True
                            game_loop()  # Start new game with difficulty selection
                            return
                    
                    # Handle mouse input
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        for x, y, w, h, _, key, _ in buttons:
                            if x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h:
                                if key == pygame.K_q:
                                    game_exit = True
                                    got_input = True
                                elif key == pygame.K_c:
                                    game_over = False
                                    got_input = True
                                    game_loop(snake_speed)
                                    return
                                elif key == pygame.K_d:
                                    game_over = False
                                    got_input = True
                                    game_loop()  # Start new game with difficulty selection
                                    return
                
                # Small delay to prevent high CPU usage
                pygame.time.delay(30)
                        
        # Handle key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                has_started = True
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    x_change = -SNAKE_BLOCK_SIZE
                    y_change = 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    x_change = SNAKE_BLOCK_SIZE
                    y_change = 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    y_change = -SNAKE_BLOCK_SIZE
                    x_change = 0
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    y_change = SNAKE_BLOCK_SIZE
                    x_change = 0
                    direction = "DOWN"
                    
        # Check for wall collision
        if x >= WINDOW_WIDTH or x < 0 or y >= WINDOW_HEIGHT or y < 0:
            game_over = True
            
        # Update snake position
        if has_started:
            x += x_change
            y += y_change
        
        # Update animation counter
        animation_counter += 1
        if score_animation > 0:
            score_animation -= 0.05
            if score_animation < 0:
                score_animation = 0
                
        # Dynamic snake speed based on length
        current_speed = min(SNAKE_SPEED_MAX, snake_speed + (snake_length // 10))
        
        # Fill game window background
        game_window.blit(background, (0, 0))
        
        # Draw grid
        draw_grid(SNAKE_BLOCK_SIZE)
        
        # Draw regular food
        draw_food(food_x, food_y, SNAKE_BLOCK_SIZE, "regular", animation_counter)
        
        # Draw bonus food if active
        if bonus_active:
            draw_food(bonus_x, bonus_y, SNAKE_BLOCK_SIZE, "bonus", animation_counter)
        
        # Update snake body
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)
        
        if len(snake_list) > snake_length:
            del snake_list[0]
            
        # Check for self collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True
                
        # Draw snake with distinctive head
        draw_snake(SNAKE_BLOCK_SIZE, snake_list, direction)
        
        # Display score in top left corner with larger font and animation
        display_score(snake_length - 1, WHITE, 45, score_animation)
        
        # Update display
        pygame.display.update()
        
        # Check if regular food eaten
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WINDOW_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
            food_y = round(random.randrange(0, WINDOW_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
            snake_length += 1
            food_eaten_count += 1
            score_animation = 1.0  # Trigger score animation
            
            # Check if it's time to spawn a bonus food (every 3 regular foods)
            if food_eaten_count % 3 == 0 and not bonus_active:
                bonus_active = True
                # Make sure bonus food doesn't spawn on top of regular food or snake
                while True:
                    bonus_x = round(random.randrange(0, WINDOW_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
                    bonus_y = round(random.randrange(0, WINDOW_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
                    
                    # Check if bonus food position overlaps with regular food
                    if bonus_x == food_x and bonus_y == food_y:
                        continue
                        
                    # Check if bonus food position overlaps with snake
                    overlap = False
                    for segment in snake_list:
                        if segment[0] == bonus_x and segment[1] == bonus_y:
                            overlap = True
                            break
                            
                    if not overlap:
                        break
        
        # Check if bonus food eaten
        if bonus_active and x == bonus_x and y == bonus_y:
            snake_length += 2  # Bonus food gives 2 extra segments
            bonus_active = False  # Deactivate the bonus food
            score_animation = 1.0  # Trigger score animation
        
        # Control game speed
        clock.tick(current_speed)
        
    # Exit game
    pygame.quit()
    quit()

# Start game
game_loop()