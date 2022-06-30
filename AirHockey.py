from Player import Player
from Ball import Ball
import cv2
import pygame
from cvzone.PoseModule import PoseDetector
from Player_enums import Players
import random

cap = cv2.VideoCapture(0)
detector = PoseDetector()

pygame.init()

screenX = 640
screenY = 480 * 2
CENTER = 0

screen = pygame.display.set_mode((screenX, screenY))


def update_screen():
    screen.fill((0, 0, 0))
    screen.blit(airhockey_table, (0, 0))
    p1.draw(screen)
    p2.draw(screen)
    ball.draw(screen)
    # racket.draw(screen)
    # ice_ball.draw(screen)


def image_to_player_pos():
    success, img = cap.read()
    img = detector.findPose(img)
    imlist, bbox = detector.findPosition(img)
    cv2.imshow("body", img)
    if len(bbox) != 0:
        print(bbox["center"][0], bbox["center"][1])
        # p1.move(imlist[8][1], imlist[8][2])
        # p2.move(imlist[8][1], imlist[8][2] - 100)
        p1.move(bbox["center"][0], bbox["center"][1])
        p2.move(bbox["center"][0], bbox["center"][1] - 100)
        p2.keep_in_border(0, 0, screenX, screenY / 2)
        p1.keep_in_border(0, screenY / 2, screenX, screenY)
        # p2.keep_in_border(0, screenY / 2, 0, screenX)
        # p1.keep_in_border(screenY / 2, screenY, 0, screenX)


def mouse_to_player_pos():
    pos = pygame.mouse.get_pos()
    p1.move(pos[0], pos[1])
    p2.move(pos[0], pos[1] - 300)
    # racket.move(pos[0], pos[1])


def collision_cooldown():
    now = pygame.time.get_ticks() - start_ticks
    if now - start_ticks > 1000:
        return True
    else:
        return False


def reset_game():
    return Ball(ball_image)


running = True
path = 'sprites/'
ghost = pygame.image.load(path + 'ghost.png')
ghost = pygame.transform.flip(ghost, True, False)
print("FIRST GHOST", ghost.get_height())
flappy = pygame.image.load(path + 'flappybird.png')
airhockey_table = pygame.image.load(path + 'background_airhockey.png')
airhockey_table = pygame.transform.rotate(airhockey_table, 90)
airhockey_table = pygame.transform.scale(airhockey_table, (screenX, screenY))
ball_image = pygame.image.load(path + 'ball.png')
p1 = Player(ghost, Players.PLAYER_1)
p2 = Player(flappy, Players.PLAYER_2)
ball = Ball(ball_image)
# ball = Ball((screenX / 2) - 25, (screenY - 25) / 2, 50, 50, ball_image)
goal1 = pygame.Rect(160, 0, 320, 1)
goal2 = pygame.Rect(160, screenY - 2, 320, 1)
print("SECOND GHOST", p1.img.get_height())
# racket = Circle(screenX / 2, screenY / 3, 50, 0.01, 0.01, ball_image)
# ice_ball = Circle(screenX / 2, screenY / 3, 50, 0.1, 0.1, ball_image)
olist = []
start_ticks = pygame.time.get_ticks()
cooldown = False

myfont = pygame.font.SysFont("monospace", 150)
score1 = 0
score2 = 0
sound_path = 'wav_sounds/'
hit_sound = pygame.mixer.Sound(sound_path + 'hit_sound.wav')
# pygame.mixer.music.load('arcade_music.wav')
# pygame.mixer.music.play(-1)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    # image_to_player_pos()
    mouse_to_player_pos()
    # p2.keep_in_border(0, 0, screenX, screenY / 2)
    # p1.keep_in_border(0, screenY / 2, screenX, screenY)
    ball.move(screenX, screenY)
    if p1.rect.colliderect(ball) and ball.dy > 0:
        hit_sound.play()
        ball.player_collision()

    if p2.rect.colliderect(ball) and ball.dy < 0:
        hit_sound.play()
        ball.player_collision()

    if ball.rect.colliderect(goal1):
        score2 += 1
        ball = reset_game()

    if ball.rect.colliderect(goal2):
        score1 += 1
        ball = reset_game()

    score_text = myfont.render(str(score1), False, (255, 255, 255))
    high_score_text = myfont.render(str(score2), False, (255, 255, 255))
    update_screen()
    pygame.draw.rect(screen, (255, 0, 0), goal1)
    pygame.draw.rect(screen, (255, 0, 0), goal2)
    screen.blit(score_text, (screenX / 2 - 50, screenY / 4 - 75))
    screen.blit(high_score_text, (screenX / 2 - 50, screenY / 4 * 3))
    pygame.display.flip()

cap.release()
cv2.destroyAllWindows()
