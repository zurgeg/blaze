### --Backend Dear PyGUI--
'''
from dearpygui.core import *
from dearpygui.simple import *
from time import time, sleep
from threading import Thread
class Display:
    def __init__(self, native_display_size, window_size):
        self.window = add_window("Emulation", width=window_size[0], height=window_size[1])
        self.scale_factor = window_size[0] / native_display_size[0]
        print(f'Scale Factor {self.scale_factor}')
        sleep(5)
        self.dpgthread = Thread(target=lambda: start_dearpygui(primary_window="Emulation"))
        self.dpgthread.start()
        add_text('Hello!')
    def draw_pixel(self, x, y, color):
        if isinstance(color, int):
            color = (color, color, color, color)
        print(color)
        x_base = x * self.scale_factor
        y_base = y * self.scale_factor
        draw_rectangle('Emulation', [x_base, y_base], [self.scale_factor, self.scale_factor], color)
        
class Clock:
    def __init__(self):
        self.time = time()
    def tick(self, framerate):
        tick = 1/framerate + time()
        t = time()
        while t != tick:
            tick = t
'''
# --Backend PyGame--
from pygame import display, draw
from pygame.time import Clock as PClock
from time import time, sleep
class Display:
    def __init__(self, native_display_size, window_size):
        display.init()
        self.window = display.set_mode(window_size)
        self.scale_factor = window_size[0] / native_display_size[0]
        print(f'Scale Factor {self.scale_factor}')
    def draw_pixel(self, x, y, color):
        if isinstance(color, int):
            color = (color, color, color)
        x_base = x * self.scale_factor
        y_base = y * self.scale_factor
        print(color)
        draw.rect(self.window, 
            color,
            (x_base, y_base, self.scale_factor, self.scale_factor))
        display.flip()
        
class Clock:
    def __init__(self):
        self.time = time()
        self.clock = PClock()
    def tick(self, framerate):
        self.clock.tick(framerate)
