import sys
import pygame
from map import Map
from items import Button

class DungeonGen():
    def __init__(self):

        pygame.init()
        pygame.display.set_caption("Dungeon Generator")
        pygame.key.set_repeat(200, 25)

        self.screen_w = 1000
        self.screen_h = 1000
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        self.map_surface = pygame.Surface((980, 980))
        self.font = pygame.font.SysFont("Arial", 24)
        self.colors = {
            'rooms': '#CCE5FF', 
            'hallways': '#CCE5FF', 
            'mst': '#FF007F', 
            'tri':'#80FF00'}

        self.fps_clock = pygame.time.Clock()
        self.fps = 60

        self.state = 'startscreen'
        self.show_mid = False
        self.show_triangulation = False
        self.show_prim = False
        self.show_hallways = True
        self.show_grid = False
        self.number_of_rooms = 30
        self.objects = {'buttons': []}

        self.create_button(300, 400, 400, 100, self.font, self.screen, 'startscreen', 'Generate a Dungeon', self.new_map)
        self.create_button(30, 60, 100, 30, self.font, self.screen, 'dungeon', 'New', self.new_map)

        self.loop()

    def new_map(self):
        self.state = 'dungeon'
        self.map = Map(self.screen, self.screen_w, self.screen_h, 16, self.number_of_rooms, self.colors)

    def create_button(self, x, y, width, height, font, screen, state, button_text='Button', click_function=None, one_press=False):
        self.objects['buttons'].append(Button(x, y, width, height, font, screen, state, button_text, click_function, one_press))


    def loop(self):

        while True:
            events = pygame.event.get()


            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

            for button in self.objects['buttons']:
                if button.state == self.state:
                    button.process()

            self.display_screen()
            self.fps_clock.tick(self.fps)


    def display_screen(self):

        if self.state == 'startscreen':
            self.screen.fill((0,0,70))
            title_txt = "Dungeon Generator (startscreen)"
            title = self.font.render(title_txt, True, (255,0,0))
            self.screen.blit(title, (30,10))

        else:
            self.screen.fill((0,0,70))
            title_txt = "Dungeon Generator (map)"
            title = self.font.render(title_txt, True, (255,0,0))
            self.screen.blit(title, (30,10))

            if self.show_grid:
                for line in self.map.grid_lines:
                    line.render()

            for room in self.map.rooms:
                room.render()
                if self.show_mid:
                    room.render_mid()

            if self.show_hallways:
                for hallway in self.map.hallways['psg']:
                    hallway.render()

            if self.show_triangulation:
                for passage in self.map.passages['psg']:
                    passage.render()

            if self.show_prim:
                for passage in self.map.tree['psg']:
                    passage.render()


        for button in self.objects['buttons']:
            if button.state == self.state:
                button.render()

        pygame.display.flip()


if __name__ == "__main__":
    DungeonGen()
