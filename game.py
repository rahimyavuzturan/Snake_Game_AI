import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf',25)
Point = namedtuple('Point', 'x, y')

#RGB COLORS
WHITE = (0 ,0 ,0 )
FOOD = (232, 184, 109)
BACKGROUND = (241, 243, 194)
SNAKE_OUTLINE = (161, 214, 178)
SNAKE_INLINE = (181, 223, 178)

BLOCK_SIZE = 20
SPEED = 10


# reward
# play(action) -> direction
# game_iteration
# is_collision  

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGame():
    # en ve boy
    def __init__(self, w = 640, h = 480):
        self.w = w
        self.h = h
    
        # pygame ekranı ayarlama
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        
    def reset(self):
        #başlangıç durumları
        self.direction = Direction.RIGHT
        self.old_direction = Direction.RIGHT

        self.head = Point(self.w/2 , self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.reset()
        self.frame_iteration = 0

    def _place_food(self):
        x=random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y=random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()  

    def _move(self,action):
        # straight,right,left

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx+1) % 4  
            new_dir = clock_wise[next_idx]
        else
            next_idx = (idx-1) % 4  
            new_dir = clock_wise[next_idx]

        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        
        self.head = Point(x,y)
    
    def _is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        #sınırlara çarpma
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        
        #kendine çarpma
        if pt in self.snake[1:]:
            return True
        
        return False


    def play_step(self, action):
        self.frame_iteration += 1
        # 1.agent
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. hareketi yap
        self._move(action)
        self.snake.insert(0,self.head)

        # 3. oyunun bitip bitmediğini kontrol et
        reward = 0
        game_over = False
        if self._is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward -= 10
            return reward, game_over, self.score

        # 4. hareket et (head ileri gittiği için kuyruk silincek) ya da _place_food (yemeği yemiş)
        if self.head == self.food:
            self.score += 1
            reward += 10
            self._place_food()
        else:
            self.snake.pop()
        
        
        # 5. ui ve clock güncelle
        self._update_ui()
        self.clock.tick(SPEED) 

        # 6. oyun bitişini ve sonucu döndür
        game_over = False
        return reward, game_over, self.score
    
    def _update_ui(self):
        self.display.fill(BACKGROUND)

        for pt in self.snake:
            pygame.draw.rect(self.display,SNAKE_OUTLINE, pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE)) # 20 ye 20 rectangle
            pygame.draw.rect(self.display,SNAKE_INLINE, pygame.Rect(pt.x+4,pt.y+4,12,12)) # x+4 konumundan 12 ye 12 rectanngle

        pygame.draw.rect(self.display,FOOD,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))

        text = font.render("Score: " + str(self.score),True,WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()

if __name__ == '__main__':
    game = SnakeGame()

    # loop
    while True:
        game_over, score = game.play_step()

        #oyun bitişi kontrolü
        if game_over == True:
            break   #döngüden çıkış

    pygame.quit()