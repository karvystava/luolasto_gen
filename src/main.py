import sys
import pygame
from map import Map
from items import Button, InputBox

class DungeonGen():
    def __init__(self):

        pygame.init()
        pygame.display.set_caption("Dungeon Generator")
        pygame.key.set_repeat(200, 25)

        self.screen_w = 1000
        self.screen_h = 1000
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        self.map_surface = pygame.Surface((980, 980))
        self.font = pygame.font.SysFont("katextypewriter", 23)
        self.colors = {
            'bg': '#000000',
            'rooms': '#FFFFFF', 
            'hallways': '#FFFFFF', 
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
        self.number_of_rooms = 0
        self.objects = {'buttons': [], 'inputbox':[]}

        #self.create_button(300, 400, 400, 100, self.font, self.screen, 'startscreen', 'Generate a Dungeon', self.new_map)
        self.create_button(30, 20, 100, 30, self.font, self.screen, 'dungeon', 'New', self.new_map)
        self.create_input_box(30, 60, 100, 40, self.font, self.screen, 'dungeon', self.new_map, self.update_room_number)
        self.create_input_box(420, 450, 130, 50, self.font, self.screen, 'startscreen', self.new_map, self.update_room_number)

        self.loop()

    def new_map(self):
        self.state = 'dungeon'
        self.map = Map(self.screen, self.screen_w, self.screen_h, 16, self.number_of_rooms, self.colors)

    def update_room_number(self, number):
        self.number_of_rooms = number

    def create_button(self, x, y, w, h, font, screen, state, button_text='Button', click_function=None, one_press=False):
        self.objects['buttons'].append(Button(x, y, w, h, font, screen, state, button_text, click_function, one_press))

    def create_input_box(self, x, y, w, h, font, screen, state, enter_function, type_function):
        self.objects['inputbox'].append(InputBox(x, y, w, h, font, screen, state, enter_function, type_function))

    def loop(self):

        while True:
            events = pygame.event.get()


            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                for box in self.objects['inputbox']:
                    if box.state == self.state:
                        box.process(event)

            for button in self.objects['buttons']:
                if button.state == self.state:
                    button.process()

            self.display_screen()
            self.fps_clock.tick(self.fps)


    def display_screen(self):

        self.screen.fill(self.colors['bg'])

        if self.state == 'dungeon':

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

        for box in self.objects['inputbox']:
            if box.state == self.state:
                box.render()

        pygame.display.flip()


if __name__ == "__main__":
    DungeonGen()
