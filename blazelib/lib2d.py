### --Backend Dear PyGUI--
from dearpygui.core import *
from dearpygui.simple import *
from time import time, sleep
from threading import Thread
def tlwh_to_xy(bottom, left, width, height):
    point1 = (left, bottom)
    point2 = (left + width, bottom)
    point3 = (left + width, bottom + height)
    point4 = (left, bottom + height)
    return point1, point2, point3, point4
class Display:
    def __init__(self, native_display_size, window_size):
        self.window = add_window("Emulation", width=window_size[0], height=window_size[1])
        self.scale_factor = window_size[0] / native_display_size[0]
        print(f'Scale Factor {self.scale_factor}')
        self.dpgthread = Thread(target=lambda: start_dearpygui(primary_window="Emulation"))
        self.dpgthread.start()
        add_drawing('drawing##widget', width=window_size[0], height=window_size[1])
    def draw_pixel(self, x, y, color):
        if isinstance(color, int):
            color = (color, color, color, color)
        print(color)
        x_base = x * self.scale_factor
        y_base = y * self.scale_factor
        point1, point2, point3, point4 = tlwh_to_xy(y_base, x_base, self.scale_factor, self.scale_factor)
        log(f'{point1} {point2} {point3} {point4}')
        draw_rectangle('drawing##widget', point1, point3, color)
        
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
from pygame import display, draw, HWSURFACE, DOUBLEBUF, event
from pygame.time import Clock as PClock
from time import time, sleep
class Display:
    def __init__(self, native_display_size, window_size):
        display.init()
        self.window = display.set_mode(window_size, HWSURFACE | DOUBLEBUF)
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
        event.pump()
        self.clock.tick(framerate)
'''