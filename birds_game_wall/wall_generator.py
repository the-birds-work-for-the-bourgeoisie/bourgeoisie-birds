from PIL import Image
import random
import time

class make_wall:
    def __init__(self, numbers, filename, choice, wall_done):
        self.number_1_choice = numbers[0]
        self.number_2_choice = numbers[1]
        self.number_3_choice = numbers[2]
        self.wall =  Image.new('RGB', (240,650))
        self.path = "bourgeoisie-birds/birds_game_wall/"
        self.file = filename
        self.choice = choice
        self.wall_done = wall_done

    def put_numbers_on_wall(self, n, y_offset_n, x_offset_n):
        
        number_1 = [[0,0,1,0],[0,1,1,0],[0,0,1,0],[0,0,1,0],[0,1,1,1]]
        number_2 = [[0,1,1,0],[1,0,0,1],[0,0,1,0],[0,1,0,0],[1,1,1,1]]
        number_3 = [[0,1,1,0],[1,0,0,1],[0,0,1,0],[1,0,0,1],[0,1,1,0]]
        number_4 = [[0,0,1,1],[0,1,0,1],[1,1,1,1],[0,0,0,1],[0,0,0,1]]
        number_5 = [[1,1,1,1],[1,0,0,0],[1,1,1,0],[0,0,0,1],[1,1,1,0]]
        number_6 = [[0,1,1,1],[1,0,0,0],[1,1,1,0],[1,0,0,1],[0,1,1,0]]
        number_7 = [[1,1,1,1],[0,0,0,1],[0,0,1,0],[0,0,1,0],[0,0,1,0]]
        number_8 = [[0,1,1,0],[1,0,0,1],[0,1,1,0],[1,0,0,1],[0,1,1,0]]
        number_9 = [[0,1,1,0],[1,0,0,1],[0,1,1,1],[0,0,0,1],[0,0,0,1]]
        number_0 = [[0,1,1,0],[1,0,0,1],[1,0,0,1],[1,0,0,1],[0,1,1,0]]

        numbers = [int(i) for i in str(n)]
        original_y = y_offset_n
        
        for number in numbers:
            original_x = x_offset_n
            y_offset_n = original_y
            if number == 0:
                choice = number_0
            if number == 1:
                choice = number_1
            if number == 2:
                choice = number_2
            if number == 3:
                choice = number_3
            if number == 4:
                choice = number_4
            if number == 5:
                choice = number_5
            if number == 6:
                choice = number_6
            if number == 7:
                choice = number_7
            if number == 8:
                choice = number_8
            if number == 9:
                choice = number_9
            
            y = 0
            x = 0
            while True:
                image_numbers = Image.open(self.path + 'brick_wall_letter.png')
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
                
            
    def create_wall(self):
        x_offset = 0
        y_offset = 0
        y_wall =  Image.new('RGB', (12,650))
        wall_chosen = random.choice(['brick_wall_plain.png', 'red_brick.png','brown_brick.png'])
        image = Image.open(self.path + wall_chosen)
        for _ in range(650//25):
            y_wall.paste(image, (x_offset,y_offset))
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
        numbers = [self.number_1_choice, self.number_2_choice,self.number_3_choice]
        y_offset_n = 62
        x_offset_n = 36
        for number in numbers:
            y_offset_n = self.put_numbers_on_wall(number, y_offset_n, x_offset_n)
            y_offset_n += 75

        self.wall.save(self.path + self.file)
        if self.wall_done is not None:
            self.wall_done()

                
filename = 'current_wall.png'
choice = True
def wall_done():
    print("Wall_Done")
start = make_wall([888,600,150], filename, choice, wall_done)
start_time = time.time()
start.create_wall()
print("----------%s Time it Took-------------" % (time.time() - start_time))

print('hello')