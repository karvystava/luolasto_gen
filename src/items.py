import pygame
import math

class Passage():
    def __init__(self, a, b, color, screen, width):

        self.a = a
        self.b = b
        self.color = color
        self.screen = screen
        self.w = width
        self.d = math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

    def render(self):
        pygame.draw.line(self.screen, self.color, self.a, self.b, self.w)


class Room():
    def __init__(self, x, y, width, height, screen, colors, buffer):

        self.screen = screen
        self.room = pygame.Rect((x+buffer, y+buffer, width-buffer, height-buffer))
        self.buffer = pygame.Rect((x, y, width+buffer, height+buffer))
        self.colors = colors
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.mid = (x+width/2, y+height/2)

    def render(self):
        pygame.draw.rect(self.screen, self.colors['bg'], self.buffer)
        pygame.draw.rect(self.screen, self.colors['rooms'], self.room)

    def render_mid(self):
        pygame.draw.circle(self.screen, self.colors['mst'], self.mid, 3)


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


class InputBox():
    def __init__(self, x, y, w, h, font, screen, state, enter_function, type_function):

        self.font = font
        self.input_text = ''
        self.input_active = False
        self.enter_function = enter_function
        self.type_function = type_function
        self.screen = screen
        self.state = state
        self.error = False
        self.colors = {
            'passive': '#000000',
            'hover': '#666666',
            'active': '#333333'
        }

        self.input_box = pygame.Rect(x, y, w, h)

    def process(self, event=None):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.input_active = True
            else:
                self.input_active = False

        elif event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN and not self.error:
                self.enter_function()
                self.input_text = ''
                self.input_active = False

            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
                if len(self.input_text) != 0:
                    self.type_function(int(self.input_text))

            else:
                try:
                    if (int(self.input_text + event.unicode) >= 0 and int(self.input_text + event.unicode) < 51):
                        self.error = False
                        self.input_text += event.unicode
                        self.type_function(int(self.input_text))

                except:
                        self.error = True

    def render(self):

        color = self.colors['active'] if self.input_active else self.colors['passive']
        pygame.draw.rect(self.screen, color, self.input_box)
        pygame.draw.rect(self.screen, '#FFFFFF', self.input_box, 2)

        text_surf = self.font.render(self.input_text, True, '#FFFFFF')
        self.screen.blit(text_surf, (self.input_box.x + 10, self.input_box.y + 10))

        instruction = self.font.render("Type number of rooms to generate and press Enter", True, '#FFFFFF')
        error = self.font.render("Pick a number between 0-50", True, '#FF0000')
        
        if self.error:
            self.screen.blit(error, (300,15))
        if self.state == 'startscreen':
            self.screen.blit(instruction, (200,400))


