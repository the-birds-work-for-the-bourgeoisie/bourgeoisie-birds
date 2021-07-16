import os
import threading
from typing import List

from PIL import Image
import random
import time


class make_wall:
    def __init__(self, numbers, filename, choice):
        numbers = numbers[::-1]
        cwd = os.getcwd()
        # print("Current working directory: {0}".format(cwd))

        # print(numbers, filename, choice, wall_done)
        self.number_1_choice = numbers[0]
        self.number_2_choice = numbers[1]
        self.number_3_choice = numbers[2]
        self.wall = Image.new('RGB', (240, 650))
        self.path = "birds_game_wall/"
        self.file = filename
        self.choice = choice

    def put_numbers_on_wall(self, n, y_offset_n, x_offset_n):

        number_1 = [[0, 0, 1, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 1, 1, 1]]
        number_2 = [[0, 1, 1, 0], [1, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]]
        number_3 = [[0, 1, 1, 0], [1, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]]
        number_4 = [[0, 0, 1, 1], [0, 1, 0, 1], [1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
        number_5 = [[1, 1, 1, 1], [1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 1], [1, 1, 1, 0]]
        number_6 = [[0, 1, 1, 1], [1, 0, 0, 0], [1, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]]
        number_7 = [[1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]
        number_8 = [[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]]
        number_9 = [[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
        number_0 = [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]]

        numbers = [int(i) if i != '-' else "-" for i in str(n)]
        original_y = y_offset_n

        for number in numbers:
            original_x = x_offset_n
            y_offset_n = original_y
            if number == 0:
                choice = number_0
            elif number == 1:
                choice = number_1
            elif number == 2:
                choice = number_2
            elif number == 3:
                choice = number_3
            elif number == 4:
                choice = number_4
            elif number == 5:
                choice = number_5
            elif number == 6:
                choice = number_6
            elif number == 7:
                choice = number_7
            elif number == 8:
                choice = number_8
            elif number == 9:
                choice = number_9

            y = 0
            x = 0
            image_numbers = Image.open(self.path + 'brick_wall_letter.png')
            if number == '-':
                # handle negative
                self.wall.paste(image_numbers, (x_offset_n - 20, y_offset_n + 50))
                self.wall.paste(image_numbers, (x_offset_n - 20 - 10, y_offset_n + 50))
                continue

            while True:
                if choice[y][x] == 1:
                    self.wall.paste(image_numbers, (x_offset_n, y_offset_n))
                x_offset_n += image_numbers.size[0]
                x += 1
                if x == 4:
                    x_offset_n = original_x
                    y_offset_n += image_numbers.size[1]
                    x = 0
                    y += 1
                if y == 5:
                    break

            x_offset_n += 60

        return y_offset_n

    def create_wall(self, callback = None):
        x_offset = 0
        y_offset = 0
        y_wall = Image.new('RGB', (12, 650))
        wall_chosen = random.choice(['brick_wall_plain.png', 'red_brick.png', 'brown_brick.png'])
        image = Image.open(self.path + wall_chosen)
        for _ in range(650 // 25):
            y_wall.paste(image, (x_offset, y_offset))
            y_offset += image.size[1]
        y_offset = 0
        for _ in range(20):
            self.wall.paste(y_wall, (x_offset, y_offset))
            x_offset += image.size[0]

        image_window = Image.open(self.path + 'basicWindow.png')
        self.wall.paste(image_window, (0, 50))
        self.wall.paste(image_window, (0, 250))
        self.wall.paste(image_window, (0, 450))

        self.wall.paste(image_window, (230, 50))
        self.wall.paste(image_window, (230, 250))
        self.wall.paste(image_window, (230, 450))
        numbers = [self.number_1_choice, self.number_2_choice, self.number_3_choice]
        y_offset_n = 62
        x_offset_n = 40
        for number in numbers:
            y_offset_n = self.put_numbers_on_wall(number, y_offset_n, x_offset_n)
            y_offset_n += 75

        self.wall.save(self.path + self.file)
        callback and callback()


class WallGeneratorWorker(threading.Thread):
    def __init__(self, threadID, name, filename: str, numbers: List[int], callback=lambda: None):
        # print("WallGeneratorWorker")
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.filename = filename
        self.numbers = numbers
        self.callback = callback

    def run(self):
        # print("run")
        choice = True
        try:
            start = make_wall(self.numbers, self.filename, choice)
            # start_time = time.time()
            start.create_wall()
            # print("----------%s Time it Took-------------" % (time.time() - start_time))
        except Exception as e:
            print("error")
            print(str(e))
        time.sleep(1)
        self.on_done()

    def on_done(self):
        self.callback and self.callback()


if __name__ == "__main__":
    filename = 'current_wall1.png'
    choice = True


    def wall_done():
        print("Wall_Done")


    start = make_wall([-888, 600, 150], filename, choice)
    start.path = ""
    start_time = time.time()
    start.create_wall()
    print("----------%s Time it Took-------------" % (time.time() - start_time))
