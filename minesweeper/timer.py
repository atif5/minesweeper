# coding: utf-8

import pygame
import threading

from time import sleep

class Timer():
    def __init__(self, time_, font):
        self.font = font
        self.time = time_

        self.surface = self.font.render(
            'Time: 0', False, (255, 110, 0))
        self.rect = self.surface.get_rect().move((0, 5))

    def run_and_draw(self, surface, dest, frequency):
        while True:
            self.time += frequency
            sleep(frequency)

            self.update_surface()

            surface.fill((255, 255, 255), rect=self.rect)
            surface.fill((0, 0, 0), rect=self.rect)

            surface.blit(self.surface, dest)

    def update_surface(self):
        self.surface = self.font.render(
            f'Time: {self.time}', False, (171, 174, 171))

    def start(self, *args):
        timer_thread = threading.Thread(target=self.run_and_draw, args=args)
        timer_thread.daemon = True

        timer_thread.start()