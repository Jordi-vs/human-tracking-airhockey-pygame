import cv2
import pygame
from cvzone.PoseModule import PoseDetector

from Ball import Ball
from Player import Player
from Player_enums import Players


def update_screen():
    screen.fill((0, 0, 0))
    screen.blit(air_hockey_table, (0, 0))
    p1.draw(screen)
    p2.draw(screen)
    ball.draw(screen)
    pygame.draw.rect(screen, (255, 0, 0), goal1)
    pygame.draw.rect(screen, (255, 0, 0), goal2)


def image_to_player_pos(cap):
    success, img = cap.read()
    img = detector.findPose(img)
    imlist, bbox = detector.findPosition(img)
    cv2.imshow("body", img)
    if len(bbox) != 0:
        p1.move(bbox["center"][0], bbox["center"][1])
        p2.move(bbox["center"][0], bbox["center"][1] - 100)


def mouse_to_player_pos():
    pos = pygame.mouse.get_pos()
    p1.move(pos[0], pos[1])
    p2.move(pos[0], pos[1] - 300)


def reset_game():
    return Ball(ball_image, speed_start=200, speed_limit=2000)


def check_player_ball_collision():
    if p1.rect.colliderect(ball) and ball.dy > 0:
        hit_sound.play()
        ball.player_collision()
    if p2.rect.colliderect(ball) and ball.dy < 0:
        hit_sound.play()
        ball.player_collision()


def update_score():
    score_text = my_font.render(str(score1), False, (255, 255, 255))
    high_score_text = my_font.render(str(score2), False, (255, 255, 255))
    screen.blit(score_text, (screen_x / 2 - 50, screen_y / 4 - 75))
    screen.blit(high_score_text, (screen_x / 2 - 50, screen_y / 4 * 3))


# Initialize cameras
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
detector = PoseDetector()

# Initialize game
pygame.init()
running = True

# Set screen width height
screen_x = 640
screen_y = 480 * 2
screen = pygame.display.set_mode((screen_x, screen_y))

# Load all sprites
sprite_path = 'sprites/'
ghost = pygame.image.load(sprite_path + 'ghost.png')
ghost = pygame.transform.flip(ghost, True, False)
bird = pygame.image.load(sprite_path + 'flappybird.png')
air_hockey_table = pygame.image.load(sprite_path + 'background_airhockey.png')
air_hockey_table = pygame.transform.rotate(air_hockey_table, 90)
air_hockey_table = pygame.transform.scale(air_hockey_table, (screen_x, screen_y))
ball_image = pygame.image.load(sprite_path + 'ball.png')

# Initialize players and ball
p1 = Player(ghost, Players.PLAYER_1)
p2 = Player(bird, Players.PLAYER_2)
ball = Ball(ball_image, speed_start=500, speed_limit=2000)

# Initialize goals
goal1 = pygame.Rect(160, 0, 320, 30)
goal2 = pygame.Rect(160, screen_y - 30, 320, 30)

# Start clocks
start_ticks = pygame.time.get_ticks()
clock = pygame.time.Clock()
FPS = 60

# Create score board
my_font = pygame.font.SysFont("monospace", 150)
score1 = 0
score2 = 0

# Music / SFX
sound_path = 'wav_sounds/'
hit_sound = pygame.mixer.Sound(sound_path + 'hit_sound.wav')
# pygame.mixer.music.load(sound_path + 'arcade_music.wav')
# pygame.mixer.music.play(-1)


while running:

    ms_frame = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    image_to_player_pos(cap1)
    # mouse_to_player_pos()
    ball.move(ms_frame)
    check_player_ball_collision()

    if ball.rect.colliderect(goal1):
        score2 += 1
        ball = reset_game()

    if ball.rect.colliderect(goal2):
        score1 += 1
        ball = reset_game()

    update_screen()
    update_score()
    pygame.display.flip()

cap1.release()
cv2.destroyAllWindows()
