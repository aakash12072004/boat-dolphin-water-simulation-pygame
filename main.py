# ---------------- IMPORT LIBRARIES ----------------
import pygame
import random
import sys
import cv2

# ---------------- INITIALIZE ----------------
pygame.init()

# ---------------- WINDOW SETTINGS ----------------
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boat & Dolphins - Horizontal Water Flow")

clock = pygame.time.Clock()

# ---------------- LOAD VIDEO ----------------
cap = cv2.VideoCapture("water and background.mp4")

# ---------------- LOAD IMAGES ----------------
boat_img = pygame.image.load("boatnew1.png").convert_alpha()
dolphin_img = pygame.image.load("dolphin.png").convert_alpha()

# Resize images
boat_img = pygame.transform.scale(boat_img, (300, 180))
dolphin_img = pygame.transform.scale(dolphin_img, (120, 60))

# ---------------- BOAT SETTINGS ----------------
boat_rect = boat_img.get_rect()
boat_rect.centerx = WIDTH // 2
base_boat_y = HEIGHT // 2 - 85
boat_rect.y = base_boat_y

float_offset = 0
float_direction = 1

# ---------------- DOLPHIN SETTINGS ----------------
dolphins = []
for i in range(5):
    x = random.randint(50, WIDTH - 170)
    y = random.randint(HEIGHT//2 + 120, HEIGHT - 100)  # start deeper in water
    dy = random.choice([1, 2, 3])
    dolphins.append([x, y, dy])

# ---------------- WATER FLOW SETTINGS ----------------
water_x = 0
water_speed = 2

# ================= MAIN GAME LOOP =================
running = True
while running:

    # -------- READ VIDEO FRAME --------
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.rotate(frame, -90)
    frame = pygame.transform.flip(frame, True, False)

    # -------- HORIZONTAL WATER SCROLL --------
    water_x -= water_speed
    if water_x <= -WIDTH:
        water_x = 0

    screen.blit(frame, (water_x, 0))
    screen.blit(frame, (water_x + WIDTH, 0))

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -------- BOAT MOVEMENT --------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        boat_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        boat_rect.x += 5

    if boat_rect.left < 0:
        boat_rect.left = 0
    if boat_rect.right > WIDTH:
        boat_rect.right = WIDTH

    # Floating effect (wave)
    float_offset += float_direction * 0.5
    if abs(float_offset) > 5:
        float_direction *= -1

    boat_rect.y = base_boat_y + float_offset

    screen.blit(boat_img, boat_rect)

    # -------- DOLPHIN MOVEMENT --------
    water_top = HEIGHT//2 + 80   # keep dolphins lower
    water_bottom = HEIGHT - 80

    for d in dolphins:
        d[1] += d[2]

        # Vertical boundary reminder
        if d[1] <= water_top or d[1] >= water_bottom:
            d[2] *= -1

        # Create dolphin rectangle
        dolphin_rect = pygame.Rect(d[0], d[1], 120, 60)

        # -------- COLLISION AVOIDANCE WITH BOAT --------
        if dolphin_rect.colliderect(boat_rect):
            d[1] += 10   # push dolphin downward into water
            d[2] = abs(d[2])  # ensure it moves downward

        screen.blit(dolphin_img, (d[0], d[1]))

    pygame.display.update()
    clock.tick(30)

# ---------------- EXIT ----------------
cap.release()
pygame.quit()
sys.exit()