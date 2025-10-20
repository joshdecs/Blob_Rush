import pyxel 
# variables
SCREEN_WIDTH =  128
SCREEN_HEIGHT = 128
WALKING_MAX_RIGHT = 100
WALKING_MAX_LEFT = 20
MAX_UP= 10
MAX_DOWN = 100
TRANSPARENT_COLOR= 5
OBSTACLES_LIST = [(0,1), (1,1), (2,1), (0,4), (1,4), (2,4),(3,1),(3,2),(3,3),(0,2), (1,2), (2,2),(0,3), (1,3), (2,3)]
FENCE_CO = [(5,6), (6, 6), (7, 6)]
DOOR_CO = [(2, 6), (2, 6)]
COIN_CO = (6, 5)
LADDER_CO = [(9, 1), (9, 2), (9, 3)]
SCROLL_X = 0
SCROLL_Y = 128
GAME_START = True
GAME = False
GAME_WON = False

class Coin():
    def __init__(self):
        self.player = Player()
        self.number = 0
        self.coin_used = []

    def update(self):
        self.player.update()
        if pyxel.tilemap(0).pget(self.player.x//8, self.player.y//8) == COIN_CO and not ([self.player.x//8, self.player.y//8] in self.coin_used):
            self.number += 1
            self.coin_used.append([self.player.x//8, self.player.y//8])

    def draw(self):
        if self.player.life > 0 :
            for i in self.coin_used:
                pyxel.rect(i[0]*8, i[1]*8, 8, 8, 5)
        

class Player():
    def __init__(self):
        global SCROLL_X, SCROLL_Y
        self.x_init =  24
        self.y_init = 224
        self.x =  self.x_init
        self.y = self.y_init
        self.player_blob = False
        self.life = 3
        self.speed_init = 2
        self.speed = 2
        self.max_speed = 5
        self.direction = 0
        self.player_moving = False
        self.gravity = 1
        self.max_gy = 6
        self.gy = 0
        self.jump_strength = 5
        self.max_jump_strength = 10
        self.is_jumping = False

        # collision variables
        self.collision_down = False
        self.collision_up = False
        self.collision_right =  False
        self.collision_left = False
        
        # self.img_n= [u, v, width, height]
        self.img_blob_1 = [41, 90, 6, 6]
        self.img_blob_2 = [48, 90, 8, 6]
        self.img_blob_3 = [56, 90, 8, 6]
        self.human_img_1 = [0, 72, 8 , 8]
        self.human_img_2 = [8, 72, 8 , 8]
        self.human_img_3 = [0, 88, 8 , 8]
        self.human_img_4 = [8, 88, 8 , 8]
        self.human_img_5 = [0, 80, 8 , 8]
        self.human_img_6 = [24, 88, 8 , 8]
        self.used_img = self.img_blob_1
        self.trail_1 = [33,61,6,3]
        self.trail_2 = [41,62,4,2]
        self.trail_3 = [46,63,4,2]
        self.trail_used = self.trail_2
        self.debut_chute = -1
    
    def scroll_player(self):
        global SCROLL_X, SCROLL_Y
        if self.x > (SCROLL_X + WALKING_MAX_RIGHT) and SCROLL_X < 128:
            SCROLL_X = self.x - WALKING_MAX_RIGHT

        if self.x < (SCROLL_X + WALKING_MAX_LEFT) and SCROLL_X > 2:
            SCROLL_X = self.x - WALKING_MAX_LEFT
        
        if self.y > (SCROLL_Y + MAX_DOWN) and SCROLL_Y < 128:
            SCROLL_Y = self.y - MAX_DOWN
        
        if self.y < (SCROLL_Y + MAX_UP) and SCROLL_Y > 0:
            SCROLL_Y = self.y - MAX_UP

    def ladder_use(self):
        if self.player_blob == False :    
            if pyxel.tilemap(0).pget(self.x//8, self.y //8) in LADDER_CO:
                if pyxel.btn(pyxel.KEY_UP):
                    self.y -= self.speed
                    self.gy = 0
            

    def detect_collision(self):
        
        # detection collisions right
        r_x = (self.x + self.used_img[2]) // 8
        r_y1 = (self.y)//8
        r_y2 = (self.y + self.used_img[3] - 1)//8
        for r_yi in range(r_y1, r_y2 + 1):
            if pyxel.tilemap(0).pget(r_x, r_yi) in OBSTACLES_LIST:
                self.collision_right = True
                break
            else:
                self.collision_right = False
    
    
        # detection collision left
        l_x = (self.x-1)//8
        l_y1 = (self.y)//8 
        l_y2 = (self.y + self.used_img[3] - 1)//8
        for l_yi in range(l_y1, l_y2 + 1):
            if pyxel.tilemap(0).pget(l_x, l_yi) in OBSTACLES_LIST:
                self.collision_left = True
                break
            else:
                self.collision_left = False
            
    
        # detection collision up
        h_x1 = (self.x)//8
        h_x2 = (self.x + self.used_img[2])//8 
        h_y = (self.y - 1)//8
        for h_xi in range(h_x1, h_x2 + 1):
            if pyxel.tilemap(0).pget(h_xi, h_y) in OBSTACLES_LIST :
                self.collision_up = True
                break
            else:
                self.collision_up = False
    
        # detection collision down
        d_x1 = (self.x)//8
        d_x2 = (self.x + self.used_img[2] - 1)//8 
        d_y = (self.y + self.used_img[3] + self.gy)//8
        for d_xi in range(d_x1, d_x2 + 1):
            if pyxel.tilemap(0).pget(d_xi, d_y) in OBSTACLES_LIST :
                self.collision_down = True
                break
            else:
                self.collision_down = False


    ''' 
    Function that manages the Blob's speed acceleration through time
    '''    
    def speed_raise(self):
        if self.player_moving == True and self.player_blob == True :
            #if self.speed <= self.max_speed :
            if (pyxel.frame_count % 60 == 0) :   
                self.speed += 1
        else : 
            self.speed = self.speed_init + 1
    ''' 
    Function that manages the player's animations 
    '''
    def player_animation(self):
        if (pyxel.frame_count % 10 == 0) :
            if self.player_blob == True :
                self.used_img = self.img_blob_1 if self.used_img == self.img_blob_2 else self.img_blob_2
            else : 
                self.used_img = self.human_img_1 if self.used_img == self.human_img_2 else self.human_img_2
    '''
    Function that manages the Blob's trail animations
    '''         
    def trail_animation(self):
        if (pyxel.frame_count % 5 == 0) :
            if self.trail_used == self.trail_2:
                self.trail_used = self.trail_3
            else:
                self.trail_used = self.trail_2




    ''' 
    Function that manages the player's movements
    '''
    def player_move(self):
        if pyxel.btn(pyxel.KEY_RIGHT) and self.collision_right == False:
            self.x += self.speed
            self.direction = 1
            
            self.player_moving = True
            
        elif pyxel.btn(pyxel.KEY_LEFT) and self.collision_left == False:
            self.x -= self.speed
            self.direction = -1
            self.player_moving = True
        else : 
            self.player_moving = False

        if self.collision_down == True:
            if pyxel.btn(pyxel.KEY_SPACE) and not self.collision_up:
                self.is_jumping = True 
                self.gy -= self.jump_strength


            else:
                self.gy = 0
                self.is_jumping = False
            
        elif self.collision_down == False:
            if self.debut_chute >= 0:
                self.debut_chute = self.y
            if self.gy < self.max_gy:
                self.gy += self.gravity
            
            self.y += self.gy
            if self.player_blob == False and self.debut_chute>=0:    
                print(self.y)
                print(self.debut_chute)
                if self.y - self.debut_chute > 4:
                    self.life -= 1
                    self.debut_chute = -1
            

        if self.player_moving == True :
            if self.player_blob == True :
                self.used_img = self.img_blob_3 
            else :
                if (pyxel.frame_count % 15 == 0) :
                    if self.used_img == self.human_img_2 or self.used_img == self.human_img_1:
                        self.used_img = self.human_img_3
                    elif self.used_img == self.human_img_3 :
                        self.used_img = self.human_img_4 
                    elif self.used_img == self.human_img_4 :
                        self.used_img = self.human_img_5
                    elif self.used_img == self.human_img_5 :
                        self.used_img = self.human_img_6
                    elif self.used_img == self.human_img_6 :
                        self.used_img = self.human_img_3



            
        elif self.player_moving == False :
            self.player_animation()

    def transform(self) :
        if pyxel.btnr(pyxel.KEY_C) :
            if self.player_blob == True :
                self.player_blob = False
                self.y -= 2 
                
            elif self.player_blob == False :
                self.player_blob = True
    
    def charge_jump(self) :
        if self.player_blob == True :
            if self.player_moving == True :
                if (pyxel.frame_count % 10 == 0) :
                    if self.jump_strength < self.max_jump_strength :
                        self.jump_strength += 2
        if self.is_jumping == False and self.player_moving == False:
            self.jump_strength = 5
    
    def player_health(self) :
        if self.y+ SCROLL_Y > 380 and self.life > 0:
            self.life -= 1
            self.x = self.x_init 
            self.y = self.y_init
    
            
    def update(self):
        self.player_move()
        self.speed_raise()
        self.detect_collision()
        self.transform()
        self.trail_animation()
        self.charge_jump()
        self.player_health()
        self.scroll_player()
        self.ladder_use()
        print(self.life)
        
        
        
        

    def draw(self):
        if self.life > 0 :    
            if self.player_blob == True:
                w = self.used_img[2] if self.direction == -1 else -self.used_img[2]

            else:
                w = self.used_img[2] if self.direction == 1 else -self.used_img[2]

            pyxel.blt(self.x, self.y, 0, self.used_img[0], self.used_img[1], w, self.used_img[3], TRANSPARENT_COLOR)
            if self.player_moving == True and self.player_blob == True and self.is_jumping == False:
                inverse1 = self.x+10 if self.direction == -1 else self.x-10
                pyxel.blt(inverse1,self.y+3,0, self.trail_1[0],self.trail_1[1], self.trail_1[2], self.trail_1[3], TRANSPARENT_COLOR)
                inverse2 = self.x+20 if self.direction == -1 else self.x-20
                if self.trail_used == self.trail_3:
                    trail_y = self.y+5
                else:
                    trail_y = self.y+4
                pyxel.blt(inverse2,trail_y, 0, self.trail_used[0], self.trail_used[1], self.trail_used[2], self.trail_used[3], TRANSPARENT_COLOR)
        
        


        
class App:
    
    def __init__(self):
        pyxel.init(128, 128, title = "NDC 2023")
        pyxel.load("4.pyxres")
        self.player = Player()
        self.coin = Coin()
        self.start_timer = False
        self.time = 0
        self.activate = 0
        pyxel.run(self.update, self.draw)

    def timer(self) :
        if (pyxel.frame_count % 30 == 0) :
            self.time += 1 
        
        

    def update(self):
        global GAME, GAME_START, GAME_WON
        if GAME_START:
            if pyxel.btn(pyxel.KEY_G):
                GAME_START = False
                GAME = True
        if GAME:
            self.player.update()
            self.coin.update()
            if self.player.player_moving == True :
                self.activate = 1
            if self.activate == 1 :
                self.timer()
            if self.coin.number == 8:
                GAME_WON = True
                GAME = False

    
               

    def draw(self):
        global SCROLL_X,SCROLL_Y
        if GAME_START:
            pyxel.camera()
            pyxel.cls(5)
            pyxel.text(SCREEN_HEIGHT//2 - 27, SCREEN_HEIGHT//2 - 25, "BLOCK COIN", 0)
            pyxel.text(SCREEN_HEIGHT//2 - 60 + 12, SCREEN_HEIGHT//2 + 10, "g to start", 0)
            pyxel.text(SCREEN_HEIGHT//2 - 60 + 15, SCREEN_HEIGHT//2 + 18, " right arrow to go right ", 0)
            pyxel.text(SCREEN_HEIGHT//2 - 60 + 15, SCREEN_HEIGHT//2 + 26, "left arrow to go left", 0)
            pyxel.text(SCREEN_HEIGHT//2 - 60 + 19, SCREEN_HEIGHT//2 + 34, "space to jump", 0)
            pyxel.text(SCREEN_HEIGHT//2 - 60 + 19, SCREEN_HEIGHT//2 + 44, "c to transform", 0)
            pyxel.text(SCREEN_HEIGHT//2 - 60 + 13, SCREEN_HEIGHT//2 + 50, "space to restart after death", 0)
            
        if GAME_WON:
            pyxel.camera()
            pyxel.cls(5)
            pyxel.text(SCREEN_HEIGHT//2 - 27, SCREEN_HEIGHT//2 - 25, "BLOCK COIN", 0)
            pyxel.text(SCREEN_HEIGHT//2 - 60 + 12, SCREEN_HEIGHT//2 + 10, "YOU WON", 0)
            
            
        if GAME:
            if self.player.life > 0 :    
                pyxel.cls(5)
                pyxel.camera()
                pyxel.bltm(0, 0, 0,SCROLL_X, SCROLL_Y,  SCREEN_WIDTH, SCREEN_HEIGHT, None)
                pyxel.camera(SCROLL_X, SCROLL_Y)
                self.coin.draw()
                self.player.draw()
                pyxel.text(98+SCROLL_X, 1 + SCROLL_Y,"TIME: ",7)
                pyxel.text(120+SCROLL_X, 1 + SCROLL_Y,str(self.time),7)
                if self.player.life == 3 :
                    pyxel.rect(SCROLL_X+2,SCROLL_Y+1,4,4,8)
                    pyxel.rect(SCROLL_X+8,SCROLL_Y+1,4,4,8)
                    pyxel.rect(SCROLL_X+14,SCROLL_Y+1,4,4,8)
                elif self.player.life == 2 :
                    pyxel.rect(SCROLL_X+2,SCROLL_Y+1,4,4,8)
                    pyxel.rect(SCROLL_X+8,SCROLL_Y+1,4,4,8)
                elif self.player.life == 1 :
                    pyxel.rect(SCROLL_X+2,SCROLL_Y+1,4,4,8)
                pyxel.text(58+SCROLL_X, 1 + SCROLL_Y,str(self.coin.number),7)
                pyxel.blt(66+SCROLL_X, SCROLL_Y, 0, 48, 40, 8, 8)
            else : 
                pyxel.cls(0)
                pyxel.text(SCREEN_HEIGHT, 96 ,"GAME OVER",7)
                if pyxel.btn(pyxel.KEY_SPACE) :
                    self.player.life = 3 
       



App()
