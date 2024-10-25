
import pygame,sys, random
from pygame.math import Vector2
#Definitions
pygame.init()

title_font=pygame.font.Font(None,60)
score_font=pygame.font.Font(None,40)
 
green = (173,204,96)
dark_green = (43,51,24)

cell_size =30
number_of_cell = 25

OFFSET = 75

class food:
    def __init__(self, snake_body):
        self.position=self.generation_random_pos(snake_body) 

    def draw(self):
        food_rect=pygame.Rect(OFFSET+self.position.x*cell_size,OFFSET+ self.position.y*cell_size,cell_size,cell_size) #(x,y,h,w)
        #pygame.draw.rect(screen, dark_green, food_rect) #(surface,color,rect) #tạo một chấm đen -> food có hình chữ nhật
        screen.blit(food_surface,food_rect) #thay thế chấm đen bằng ảnh food.png

    def generation_random_cell(self):
        x=random.randint(0,number_of_cell-1)
        y=random.randint(0,number_of_cell-1)
        return Vector2(x,y)

    def generation_random_pos(self, snake_body): #hàm cho food xuất hiện random trên canva
        position= self.generation_random_cell()
        while position in snake_body:
            position = self.generation_random_cell()
        return position

class snake:
    def __init__(self):
        self.body=[Vector2(6,9),Vector2(5,9),Vector2(4,9)] 
        self.direction = Vector2(1,0)
        self.add_segment=False
        self.eat_sound=pygame.mixer.Sound("Sound\eat.mp3")
        self.hit_sound=pygame.mixer.Sound("Sound\wall.mp3")
    
    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET+segment.x*cell_size,OFFSET+segment.y*cell_size,cell_size,cell_size)
            pygame.draw.rect(screen,dark_green, segment_rect,0,7)

    def update(self):
        self.body.insert(0,self.body[0] +self.direction)
        if self.add_segment == True:
            self.add_segment=False
        else:
            self.body=self.body[:-1]

    def reset(self):
        self.body=[Vector2(6,9),Vector2(5,9),Vector2(4,9)] 
        self.direction = Vector2(1,0)

class game:
    def __init__(self):
        self.snake=snake()
        self.food=food(self.snake.body)
        self.state = "RUNNING"
        self.score=0

    def draw(self):
        self.food.draw()
        self.snake.draw()

    def update(self):
        if self.state=="RUNNING":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()

    def check_collision_with_food(self): #food sẽ biến mất nếu rắn ăn nó và tạo ra 1food mới
        if self.snake.body[0] == self.food.position:
            #print("Eating food")
            self.food.position = self.food.generation_random_pos(self.snake.body)
            self.snake.add_segment=True
            self.score+=1
            self.snake.eat_sound.play()

    def check_collision_with_edges(self): #nếu rắn tông vào tường (cạnh của canva) hoặc tông vào chính nó =>chết
        if self.snake.body[0].x==number_of_cell or self.snake.body[0].x==-1:
            self.game_over()
        if self.snake.body[0].y==number_of_cell or self.snake.body[0].y==-1:
            self.game_over()

    def game_over(self):
        print("Game Over")
        self.snake.reset()
        self.food.position = self.food.generation_random_pos(self.snake.body)
        self.state="STOPPED"
        self.score=0
        self.snake.hit_sound.play()
        
    def check_collision_with_tail(self):
        headless_body=self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()

screen = pygame.display.set_mode((2*OFFSET+cell_size*number_of_cell, 2*OFFSET+cell_size*number_of_cell)) 

pygame.display.set_caption("Retro Snake")

clock=pygame.time.Clock()

game=game()
food_surface = pygame.image.load("Graphic/food.png") #nếu k muốn food là một chấm đen, ta có thể chèn ảnh hiển thị trên food

snake_update = pygame.USEREVENT
pygame.time.set_timer(snake_update, 200)
#Game Loop
while True: #while the loop, tất cả các câu lệnh trong while sẽ được thực hiện 60 lần mỗi giây
    for event in pygame.event.get(): 
        if event.type == snake_update:
            game.update() #moving
        if event.type == pygame.QUIT: #trong quá trình game đang thực hiện nếu nhấn vào QUIT button thì sẽ dừng -> thoát game
            pygame.quit()
            sys.exit() 
        
        if event.type == pygame.KEYDOWN: #điều kiện and phía sau nhằm giúp cho rắn k di chuyển theo chiều ngược lại
            if game.state=="STOPPED": 
                game.state="RUNNING" #nhấn phím bất kì trên bàn phím để restart game
            if event.key == pygame.K_UP and game.snake.direction!=Vector2(0,1):
                game.snake.direction=Vector2(0,-1)
            if event.key==pygame.K_DOWN and game.snake.direction!=Vector2(0,-1):
                game.snake.direction=Vector2(0,1)
            if event.key==pygame.K_LEFT and game.snake.direction!=Vector2(1,0):
                game.snake.direction=Vector2(-1,0)
            if event.key==pygame.K_RIGHT and game.snake.direction!=Vector2(-1,0):
                game.snake.direction=Vector2(1, 0)

    #drawing
    screen.fill(green) #blank canvas có màu xanh
    #pygame.draw.rect(surface,color,rect,border_size) vẽ khung
    pygame.draw.rect(screen,dark_green,(OFFSET-5,OFFSET-5,cell_size*number_of_cell+10,cell_size*number_of_cell+10),5)
    game.draw() #giúp gọn code
    #food.draw() #vẽ food lên canva
    #snake.draw() #vẽ rắn lên canva
    title_surface = title_font.render("Retro Snake", True, dark_green)
    score_surface=score_font.render(str(game.score),True, dark_green)
    screen.blit(title_surface,( OFFSET-5,20))
    screen.blit(score_surface,(OFFSET-5,OFFSET+cell_size*number_of_cell+10))
    pygame.display.update()
    clock.tick(60) #frame per second
 
 