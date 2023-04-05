import os
import random
import shutil
import sys
import time
import threading
import keyboard

class Snake:
    def __init__(self, rows, cols, asset_path, board_path):
        self.asset_path = asset_path 
        self.board_path = board_path

        self.cols = cols
        self.rows = rows

        self.body = [(0, 1), (0, 0)]

        self.next_piece = self.choose_coords()
        self.current_piece = None
        self.score = 0
 
        self.texture_head = 'moai.png'
        self.texture_body = 'lime.png'
        self.texture_food = 'amogus.png'
        self.texture_board = 'black.png'


    
    def choose_coords(self):
        all_coords = set((row, col) for row in range(self.rows)
                                for col in range(self.cols))
        free_coords = all_coords - set(self.body)
        return random.choice(list(free_coords))
 
    def increment_snake(self, dir):
        head = self.body[0]
        head = (head[0] + dir[0], head[1] + dir[1])

        # if dir[0] == 1:
        #     self.texture_head = 'moai_s.png'
        # elif dir[1] == 1:
        #     self.texture_head = 'moai_d.png'
        # elif dir[0] == -1:
        #     self.texture_head = 'moai_w.png'
        # else:
        #     self.texture_head = 'moai_a.png'

        dir_to_texture = {
            (1, 0): 'moai_s.png',
            (0, 1): 'moai_d.png',
            (-1, 0): 'moai_w.png',
            (0, -1): 'moai_a.png',
        }
        self.texture_head = dir_to_texture[dir]

        row, col = head
        if row < 0 or col < 0 or row >= self.rows or col >= self.cols or (head in self.body):
            print(self.score)
            return True
        else:
            pop = True
            self.body.insert(0, head)
            if head == self.next_piece:
                self.score += 1
                self.next_piece = self.choose_coords()
                pop = False
                self.draw()
            else:
                self.draw(pop=self.body.pop())
        
        return False
    def get_file(self, tuple):
        return f'{tuple[0]}_{tuple[1]}.png'
    
    def replace_coord(self, tuple, new):
        filename = self.get_file(tuple)
        shutil.copy(os.path.join(self.asset_path, new), 
                    os.path.join(self.board_path, filename))
        
    def draw(self, pop=None, init=False):
        if init:
            for tuple in self.body:
                self.replace_coord(tuple, self.texture_body)
            self.replace_coord(self.next_piece, self.texture_food)

        else: 
            self.replace_coord(self.body[0], self.texture_head)
            self.replace_coord(self.body[1], self.texture_body)
            if pop:
                self.replace_coord(pop, self.texture_board)
            else:
                self.replace_coord(self.next_piece, self.texture_food)

def key_listener():
    global dir, exit_flag

    while not exit_flag:
        if keyboard.is_pressed('w') and dir != (1, 0):
            dir = (-1, 0)

        elif keyboard.is_pressed('s') and dir != (-1, 0):
            dir = (1, 0)

        elif keyboard.is_pressed('d') and dir != (0, -1):
            dir = (0, 1)

        elif keyboard.is_pressed('a') and dir != (0, 1):
            dir = (0, -1)

        elif keyboard.is_pressed('t'):
            exit_flag = True

        time.sleep(0.01)
    return 0

def main():
    global dir, exit_flag
    board_path = './board/'
    asset_path = './assets/'
    rows = 12
    cols = 20
    delay = 1.5
    new_board = 1
    exit_flag = False

    SNAKE = Snake(rows, cols, asset_path, board_path)

    if new_board:
        # delete existing file grid
        files = os.listdir(board_path)
        for file in files:
            if file.endswith('.png'):
                os.remove(os.path.join(board_path, file))

        # create file grid
        for row in range(rows):
            for col in range(cols):
                file_path = os.path.join(board_path, f'{row}_{col}.png')
                shutil.copy(os.path.join(asset_path, 'black.png'), file_path)
                
    SNAKE.draw(init=True)

    dir = (0, 1)

    # create and start key listener thread
    key_listener_thread = threading.Thread(target=key_listener)
    key_listener_thread.start()

    while not exit_flag:
        exit_flag = SNAKE.increment_snake(dir)
        time.sleep(delay)
    print('Exit')
    
if __name__ == '__main__':
    main()
