# coding: utf-8

import pygame
import threading

from time import sleep
from .grid import RED, GRAY

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Timer():
    def __init__(self, time_, font):
        self.font = font
        self.time = time_
        self.is_stopped = False
        self.surface = self.font.render(
            self.text()+' '*10, False, GRAY)
        self.rect = self.surface.get_rect().move((0, 5))


    def text(self):
        return f'Your Time: {self.time}'

    def run_and_draw(self, surface, dest, frequency):
        while not self.is_stopped:
            sleep(frequency)

            self.update_surface()

            surface.fill(WHITE, rect=self.rect)
            surface.fill(BLACK, rect=self.rect)

            surface.blit(self.surface, dest)

            if not self.is_stopped:
                self.time += frequency

    def update_surface(self):
        self.surface = self.font.render(
            self.text(), False, GRAY)

    def start(self, *args):
        timer_thread = threading.Thread(target=self.run_and_draw, args=args)
        timer_thread.daemon = True
        timer_thread.start()

    def stop(self):
        self.is_stopped = True

