import cv2
import pygame
from cvzone.PoseModule import PoseDetector

from Ball import Ball
from Player import Player
from Player_enums import Players


def update_screen(current_screen):
    """
    Updates the screen with all the player/ball/goal positions
    :param current_screen: the screen on which to update it on
    """
    current_screen.fill((0, 0, 0))
    current_screen.blit(air_hockey_table, (0, 0))
    p1.draw(current_screen)
    p2.draw(current_screen)
    ball.draw(current_screen)
    pygame.draw.rect(current_screen, (255, 0, 0), goal1)
    pygame.draw.rect(current_screen, (255, 0, 0), goal2)


def image_to_player_pos(player):
    """
    Takes a player and translates their respective camera position
    to the in-game position.
    :param player: The player whose position is to be translated
    """
    success, img = player.capture.read()
    img = detector.findPose(img)
    imlist, bbox = detector.findPosition(img)
    cv2.imshow(str(player.player), img)
    if len(bbox) != 0:
        player.move(bbox["center"][0], bbox["center"][1])


def mouse_to_player_pos():
    """
    Translates current mouse position to character position.
    Utilizes 1 mouse and spreads the players apart by 300 pixels.
    """
    pos = pygame.mouse.get_pos()
    p1.move(pos[0], pos[1])
    p2.move(pos[0], pos[1] - 300)


def reset_game():
    """
    Resets the ball position to its original beginning spot
    :return: A new ball object with new starting position
    """
    return Ball(ball_image, speed_start=200, speed_limit=2000)


def check_player_ball_collision(player1, player2, current_ball):
    """
    Checks if the ball collides with any of the players. Collision only
    occurs if the ball is moving towards the player, thus making a double
    hit impossible.
    :param player1: The first player
    :param player2: The second player
    :param current_ball: The ball in play
    """
    if player1.rect.colliderect(current_ball) and current_ball.dy > 0:
        hit_sound.play()
        current_ball.player_collision()
    if player2.rect.colliderect(current_ball) and current_ball.dy < 0:
        hit_sound.play()
        current_ball.player_collision()


def update_score(current_score1, current_score2):
    """
    Draws the current score onto the board
    :param current_score1: the score of player 1
    :param current_score2: the score of player 2
    """
    score_text = my_font.render(str(current_score1), False, (255, 255, 255))
    high_score_text = my_font.render(str(current_score2), False, (255, 255, 255))
    screen.blit(score_text, (SCREEN_X / 2 - 50, SCREEN_Y / 4 - 75))
    screen.blit(high_score_text, (SCREEN_X / 2 - 50, SCREEN_Y / 4 * 3))


# Initialize cameras
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
detector = PoseDetector()

# Initialize game
pygame.init()
RUNNING = True

# Set screen width height
SCREEN_X = 640
SCREEN_Y = 480 * 2
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

# Load all sprites
SPRITE_PATH = 'sprites/'
ghost = pygame.image.load(SPRITE_PATH + 'ghost.png')
ghost = pygame.transform.flip(ghost, True, False)
bird = pygame.image.load(SPRITE_PATH + 'flappybird.png')
air_hockey_table = pygame.image.load(SPRITE_PATH + 'background_airhockey.png')
air_hockey_table = pygame.transform.rotate(air_hockey_table, 90)
air_hockey_table = pygame.transform.scale(air_hockey_table, (SCREEN_X, SCREEN_Y))
ball_image = pygame.image.load(SPRITE_PATH + 'ball.png')

# Initialize players and ball
p1 = Player(ghost, Players.PLAYER_1, cap1)
p2 = Player(bird, Players.PLAYER_2, cap2)
ball = Ball(ball_image, speed_start=500, speed_limit=2000)

# Initialize goals
goal1 = pygame.Rect(160, 0, 320, 30)
goal2 = pygame.Rect(160, SCREEN_Y - 30, 320, 30)

# Start clocks
start_ticks = pygame.time.get_ticks()
clock = pygame.time.Clock()
FPS = 60

# Create score board
my_font = pygame.font.SysFont("monospace", 150)
SCORE_1 = 0
SCORE_2 = 0

# Music / SFX
SOUND_PATH = 'wav_sounds/'
hit_sound = pygame.mixer.Sound(SOUND_PATH + 'hit_sound.wav')
pygame.mixer.music.load(SOUND_PATH + 'arcade_music.wav')
pygame.mixer.music.play(-1)


while RUNNING:

    ms_frame = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            break

    # FOR 2 CAMERA MULTI PLAYER (Uncomment)
    image_to_player_pos(p1)
    image_to_player_pos(p2)

    # FOR 1 MOUSE SINGLE PLAYER (Uncomment)
    # mouse_to_player_pos()

    ball.move(ms_frame)
    check_player_ball_collision(p1, p2, ball)

    if ball.rect.colliderect(goal1):
        SCORE_2 += 1
        ball = reset_game()

    if ball.rect.colliderect(goal2):
        SCORE_1 += 1
        ball = reset_game()

    update_screen(screen)
    update_score(SCORE_1, SCORE_2)
    pygame.display.flip()

cap1.release()
cap2.release()
cv2.destroyAllWindows()
