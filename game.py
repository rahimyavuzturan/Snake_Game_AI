import pygame
import random
from enum import Enum
from collections import namedtuple

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
SPEED = 20

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

    def _place_food(self):
        x=random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y=random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()  

    def _move(self,direction):
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
    
    def _is_collision(self):
        #sınırlara çarpma
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        
        #kendine çarpma
        if self.head in self.snake[1:]:
            return True
        
        return False


    def play_step(self):
        # 1. user input al
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

        # 2. hareketi yap
        self._move(self.direction)
        self.snake.insert(0,self.head)

        # 3. oyunun bitip bitmediğini kontrol et
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. hareket et (head ileri gittiği için kuyruk silincek) ya da _place_food (yemeği yemiş)
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        
        # 5. ui ve clock güncelle
        self._update_ui()
        self.clock.tick(SPEED) 

        # 6. oyun bitişini ve sonucu döndür
        game_over = False
        return game_over, self.score
    
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