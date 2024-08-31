import pygame
import random
import sys

# Inisialisasi pygame
pygame.init()

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Ukuran layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cat and Dog Game")

# Kecepatan
cat_speed = 5
dog_speed = 1  # Reduced dog speed from 3 to 1

# Muat gambar
cat_img = pygame.image.load('cat.png')
dog_img = pygame.image.load('dog.png')
fish_img = pygame.image.load('fish-bone.gif')
brick_img = pygame.image.load('wall.png')
home_img = pygame.image.load('house.png')
grass_img = pygame.image.load('grass.png')  # Load grass image

# Skala gambar
cat_img = pygame.transform.scale(cat_img, (50, 50))
dog_img = pygame.transform.scale(dog_img, (50, 50))
fish_img = pygame.transform.scale(fish_img, (30, 30))
brick_img = pygame.transform.scale(brick_img, (50, 50))
home_img = pygame.transform.scale(home_img, (70, 70))
grass_img = pygame.transform.scale(grass_img, (50, 50))  # Scale grass image

# Membuat posisi brick yang lebih rapi
brick_size = 50
num_rows = HEIGHT // brick_size
num_cols = WIDTH // brick_size
brick_list = []
for row in range(num_rows):
    for col in range(num_cols):
        if random.random() < 0.1:  # 10% chance to place a brick
            brick_list.append((col * brick_size, row * brick_size))

# Fungsi untuk mengecek tabrakan
def check_collision(rect1, rect2):
    return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))

# Fungsi untuk menempatkan objek tanpa tumpang tindih
def place_object(obj_size, existing_objects):
    while True:
        x = random.randint(0, WIDTH - obj_size[0])
        y = random.randint(0, HEIGHT - obj_size[1])
        new_rect = pygame.Rect(x, y, *obj_size)
        if not any(check_collision(new_rect, obj) for obj in existing_objects):
            return x, y

# Posisi awal
existing_objects = [pygame.Rect(brick[0], brick[1], 50, 50) for brick in brick_list]

cat_x, cat_y = place_object((50, 50), existing_objects)
existing_objects.append(pygame.Rect(cat_x, cat_y, 50, 50))

dog_x, dog_y = place_object((50, 50), existing_objects)
existing_objects.append(pygame.Rect(dog_x, dog_y, 50, 50))

home_x, home_y = place_object((70, 70), existing_objects)
existing_objects.append(pygame.Rect(home_x, home_y, 70, 70))

fish_list = []
for _ in range(5):
    fish_x, fish_y = place_object((30, 30), existing_objects)
    fish_list.append((fish_x, fish_y))
    existing_objects.append(pygame.Rect(fish_x, fish_y, 30, 30))

fish_collected = 0

# Fungsi untuk menggambar
def draw_objects():
    screen.fill(WHITE)
    # Draw grass everywhere
    for y in range(0, HEIGHT, 50):
        for x in range(0, WIDTH, 50):
            screen.blit(grass_img, (x, y))
    screen.blit(cat_img, (cat_x, cat_y))
    screen.blit(dog_img, (dog_x, dog_y))
    screen.blit(home_img, (home_x, home_y))
    for fish in fish_list:
        screen.blit(fish_img, fish)
    for brick in brick_list:
        screen.blit(brick_img, brick)
    
    # Display fish collected
    font = pygame.font.Font(None, 36)
    fish_text = font.render(f"Fish: {fish_collected}/5", True, BLACK)
    screen.blit(fish_text, (10, 10))
    
    pygame.display.update()

# Fungsi untuk menggerakkan anjing ke arah kucing
def move_dog_towards_cat():
    global dog_x, dog_y
    if cat_x > dog_x:
        dog_x += dog_speed
    elif cat_x < dog_x:
        dog_x -= dog_speed
    if cat_y > dog_y:
        dog_y += dog_speed
    elif cat_y < dog_y:
        dog_y -= dog_speed

# Fungsi untuk memulai ulang permainan
def restart_game():
    global cat_x, cat_y, dog_x, dog_y, fish_list, brick_list, home_x, home_y, fish_collected
    brick_list = []
    for row in range(num_rows):
        for col in range(num_cols):
            if random.random() < 0.1:  # 10% chance to place a brick
                brick_list.append((col * brick_size, row * brick_size))
    
    existing_objects = [pygame.Rect(brick[0], brick[1], 50, 50) for brick in brick_list]
    
    cat_x, cat_y = place_object((50, 50), existing_objects)
    existing_objects.append(pygame.Rect(cat_x, cat_y, 50, 50))
    
    dog_x, dog_y = place_object((50, 50), existing_objects)
    existing_objects.append(pygame.Rect(dog_x, dog_y, 50, 50))
    
    home_x, home_y = place_object((70, 70), existing_objects)
    existing_objects.append(pygame.Rect(home_x, home_y, 70, 70))
    
    fish_list = []
    for _ in range(5):
        fish_x, fish_y = place_object((30, 30), existing_objects)
        fish_list.append((fish_x, fish_y))
        existing_objects.append(pygame.Rect(fish_x, fish_y, 30, 30))
    
    fish_collected = 0

# Game loop
def game_loop():
    global cat_x, cat_y, dog_x, dog_y, fish_collected
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        new_cat_x, new_cat_y = cat_x, cat_y
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            new_cat_y -= cat_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            new_cat_y += cat_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            new_cat_x -= cat_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            new_cat_x += cat_speed

        # Check collision with bricks
        cat_rect = pygame.Rect(new_cat_x, new_cat_y, 50, 50)
        if not any(check_collision(cat_rect, pygame.Rect(brick[0], brick[1], 50, 50)) for brick in brick_list):
            cat_x, cat_y = new_cat_x, new_cat_y

        # Gerakkan anjing ke arah kucing
        move_dog_towards_cat()

        cat_rect = pygame.Rect(cat_x, cat_y, 50, 50)
        dog_rect = pygame.Rect(dog_x, dog_y, 50, 50)

        # Cek tabrakan dengan ikan
        for fish in fish_list[:]:
            fish_rect = pygame.Rect(fish[0], fish[1], 30, 30)
            if check_collision(cat_rect, fish_rect):
                fish_list.remove(fish)
                fish_collected += 1

        # Cek tabrakan dengan anjing
        if check_collision(cat_rect, dog_rect):
            print("Game Over! The cat met the dog.")
            return "game_over"

        # Cek kemenangan
        if fish_collected >= 5:
            home_rect = pygame.Rect(home_x, home_y, 70, 70)
            if check_collision(cat_rect, home_rect):
                print("Congratulations! The cat has collected all the fish and reached home.")
                return "win"

        draw_objects()
        pygame.time.delay(30)

# Main game loop
while True:
    result = game_loop()
    if result == "game_over" or result == "win":
        font = pygame.font.Font(None, 36)
        if result == "game_over":
            text = font.render("Game Over! Press R to restart or Q to quit", True, BLACK)
        else:
            text = font.render("You Win! Press R to restart or Q to quit", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, text_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart_game()
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

pygame.quit()
