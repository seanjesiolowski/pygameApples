# graphics credit
# https://opengameart.org/content/zelda-like-tilesets-and-sprites

# splash sound credit
# https://freesound.org/people/tran5ient/sounds/190080/

from surface import SURFACE_HEIGHT, SURFACE_WIDTH
from apples import APPLE_RADIUS, make_apples
from load_image import player, pond, rocks
from pond import POND_COOR
import pygame


def main():
    pygame.init()

    pygame.display.set_caption("How many apples does a guy need?")
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    CAVE_BROWN = (121, 88, 79)
    display_font = pygame.font.SysFont(None, 35)
    surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))

    chomp_sound = pygame.mixer.Sound(r'snds\chomp.wav')
    splash_sound = pygame.mixer.Sound(r'snds\190080__tran5ient__splash7.wav')
    oh_yeah_sound = pygame.mixer.Sound(r'snds\oh_yeah.wav')
    rocks_sound = pygame.mixer.Sound(r'snds\rocks.wav')
    lose_sound = pygame.mixer.Sound(r'snds\lose_sound.wav')

    def chomp():
        chomp_sound.play()

    def splash(justSplashed):
        if justSplashed:
            splash_sound.play()

    def oh_yeah():
        oh_yeah_sound.play()

    rockSoundGo = True

    def rocks_func():
        rocks_sound.play()

    def lose_sound_func():
        lose_sound.play()

    class Player:
        def __init__(self, player_xpos, player_ypos, player_xpos_change, player_ypos_change, energy, DECLINE_RATE, collected_apples):
            self.player_xpos = player_xpos
            self.player_ypos = player_ypos
            self.player_xpos_change = player_xpos_change
            self.player_ypos_change = player_ypos_change
            self.energy = energy
            self.DECLINE_RATE = DECLINE_RATE
            self.collected_apples = collected_apples

    player_object = Player(10, 10, 0, 0, 100.00, 0.01, 0)
    reset_menu = True
    running = True
    while running:
        if reset_menu:
            player_xpos = player_object.player_xpos
            player_ypos = player_object.player_ypos
            player_xpos_change = player_object.player_xpos_change
            player_ypos_change = player_object.player_ypos_change
            player_place_rect = surface.blit(
                player, (player_xpos, player_ypos))
            energy = player_object.energy
            DECLINE_RATE = player_object.DECLINE_RATE
            collected_apples = player_object.collected_apples
            yet_good_apples = False
            while not yet_good_apples:
                apples = make_apples(5)
                for index, apple in enumerate(apples):
                    apple_rect = pygame.draw.circle(
                        surface, RED, apple[0], APPLE_RADIUS)
                    if apple_rect.colliderect(player_place_rect):
                        break
                    elif index == len(apples) - 1:
                        yet_good_apples = True
            surface.fill(WHITE)
            surface.blit(
                player, (player_xpos, player_ypos))
            surface.blit(display_font.render(
                "         Before your energy expires, collect all the apples to win!", True, BLACK), (0, 100))
            surface.blit(display_font.render(
                "                    The pond restores your ever-waning health.", True, BLACK), (0, 160))
            surface.blit(display_font.render(
                "      Press W, A, S, D keys to start the game and move your player.", True, BLACK), (0, 220))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        reset_menu = False
                    if event.key == pygame.K_a:
                        reset_menu = False
                    if event.key == pygame.K_s:
                        reset_menu = False
                    if event.key == pygame.K_d:
                        reset_menu = False
        else:
            # GAME EVENT HANDLING
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        player_ypos_change = -0.1
                    if event.key == pygame.K_a:
                        player_xpos_change = -0.1
                    if event.key == pygame.K_s:
                        player_ypos_change = 0.1
                    if event.key == pygame.K_d:
                        player_xpos_change = 0.1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        player_ypos_change = 0
                    if event.key == pygame.K_a:
                        player_xpos_change = 0
                    if event.key == pygame.K_s:
                        player_ypos_change = 0
                    if event.key == pygame.K_d:
                        player_xpos_change = 0

            # PLAYER MOVEMENT AND BOUNDS
            player_xpos += player_xpos_change
            player_ypos += player_ypos_change
            if (player_xpos < 0):
                player_xpos = 0
            if (player_xpos > SURFACE_WIDTH - player.get_rect().width):
                player_xpos = SURFACE_WIDTH - player.get_rect().width
            if (player_ypos < 0):
                player_ypos = 0
            if (player_ypos > SURFACE_HEIGHT - player.get_rect().height):
                player_ypos = SURFACE_HEIGHT - player.get_rect().height
            PLAYER_COOR = (player_xpos, player_ypos)

            # DISPLAY, COLLISION, ETC.
            surface.fill(CAVE_BROWN)
            rocks1 = surface.blit(rocks, (100, 100))
            rocks2 = surface.blit(rocks, (130, 150))
            rocks3 = surface.blit(rocks, (300, 400))

            pond_place_rect = surface.blit(pond, POND_COOR)
            player_place_rect = surface.blit(player, PLAYER_COOR)

            if rocks1.colliderect(player_place_rect) or rocks2.colliderect(player_place_rect) or rocks3.colliderect(player_place_rect):
                if rockSoundGo:
                    rocks_func()
                    rockSoundGo = False
            else:
                rockSoundGo = True

            if energy > 0 and collected_apples != len(apples):
                allowWinSound = True
                allowLoseSound = True
                energy_string = "{:.0f}".format(energy)
                text_rect = surface.blit(display_font.render(
                    f"Energy: {energy_string}", True, BLACK), (50, 50))
                energy -= DECLINE_RATE
                if player_place_rect.colliderect(pond_place_rect):
                    energy = 100.0
                    splash(not nextSplash)
                    nextSplash = True
                else:
                    nextSplash = False
                for apple in apples:
                    is_touching_player = False
                    if apple[1]:
                        apple_rect = pygame.draw.circle(
                            surface, RED, apple[0], APPLE_RADIUS)
                        if apple_rect.colliderect(text_rect) or apple_rect.colliderect(pond_place_rect):
                            apples = make_apples(5)
                            break
                        is_touching_player = apple_rect.colliderect(
                            player_place_rect)
                    if is_touching_player:
                        chomp()
                        apple[1] = False
                        collected_apples += 1
            else:
                if player_place_rect.colliderect(pond_place_rect):
                    reset_menu = True
                if collected_apples == len(apples):
                    if allowWinSound:
                        oh_yeah()
                        allowWinSound = False
                    final_message = "           You won! Visit the pond to play again."
                else:
                    if allowLoseSound:
                        lose_sound_func()
                        allowLoseSound = False
                    final_message = "          Game over! Visit the pond to play again."
                surface.blit(display_font.render(
                    f"{final_message}", True, BLACK), (100, 50))

        # UPDATE THE DISPLAY
        pygame.display.update()


if __name__ == "__main__":
    main()
