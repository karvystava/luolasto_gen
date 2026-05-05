import pygame
import math

class Passage():
    def __init__(self, a, b, color, screen, width):
        self.a = a
        self.b = b
        self.color = color
        self.screen = screen
        self.w = width
        self.color = color
        self.d = math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

    def render(self):
        pygame.draw.line(self.screen, self.color, self.a, self.b, self.w)


class Room():
    def __init__(self, x, y, width, height, screen, color, buffer):
        self.screen = screen
        self.room = pygame.Rect((x+buffer, y+buffer, width-buffer, height-buffer))
        self.buffer = pygame.Rect((x, y, width+buffer, height+buffer))
        self.color = color
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.mid = (x+width/2, y+height/2)

    def render(self):
        pygame.draw.rect(self.screen, (0,0,70), self.buffer)
        pygame.draw.rect(self.screen, self.color, self.room)

    def render_mid(self):
        pygame.draw.circle(self.screen, '#FF66B2', self.mid, 3)


class Button():
    def __init__(self, x, y, w, h, font, screen, state, button_text, click_function, one_press):
        self.click_function = click_function
        self.one_press = one_press
        self.already_pressed = False
        self.screen = screen
        self.state = state

        self.fill_colors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333'
        }

        self.button_surface = pygame.Surface((w, h))
        self.button_rect = pygame.Rect(x, y, w, h)

        self.button_surf = font.render(button_text, True, (20, 20, 20))

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        self.button_surface.fill(self.fill_colors['normal'])
        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fill_colors['pressed'])
                if self.one_press:
                    self.click_function()
                elif not self.already_pressed:
                    self.click_function()
                    self.already_pressed = True
            else:
                self.already_pressed = False

    def render(self):
        self.button_surface.blit(self.button_surf, [
        self.button_rect.width/2 - self.button_surf.get_rect().width/2,
        self.button_rect.height/2 - self.button_surf.get_rect().height/2
        ])
        self.screen.blit(self.button_surface, self.button_rect)
