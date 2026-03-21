import pygame

class StartScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640,480))
        pygame.display.set_caption("Dungeon Generator")
        self.font = pygame.font.SysFont("Arial", 24)
        self.loop()

    def loop(self):
        while True:
            self.display_screen()

    def display_screen(self):
        self.screen.fill((0,0,70))
        title_txt = "Dungeon Generator"
        title = self.font.render(title_txt, True, (255,0,0))
        self.screen.blit(title, (30,10))
        pygame.display.flip()


if __name__ == "__main__":
    StartScreen()