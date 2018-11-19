from pygame import *
import random 

display_width = 550              
display_height = 550             

init()  
#pink = (223, 172, 125)
gameDisplay = display.set_mode((display_width, display_height)) 
display.set_caption('Panda')  
clock = time.Clock() 

class Panda:            
    def __init__(self):  
        self.pandaImg = image.load('panda12.png') 
        self.readjust() 

    def readjust(self):
        self.speed_x = 0 
        self.speed_y = 0  
        self.max_speed_x = 5 
        self.max_speed_y = 15  
        self.x_acceleration = 0.5 #how quick panda move
        self.img = self.pandaImg
        self.jump_speed = 15

        scale = 7 
        self.width, self.height = 12 * scale, 12 * scale   # width of panda and height of panda
        self.scale = scale

        self.x = (display_width - self.width) / 2     
        self.y = display_height - self.height         
       
    def update(self,p):
        self.side_control()  ####the names of the functions
        self.physics(p)
        self.move()

        self.x += self.speed_x  
        self.y -= self.speed_y   

        return (self.img, (self.x, self.y, self.width, self.height)) 

    def physics(self, p): 
        
        on = False    #start with false, in func is true, as in quit func, that this func work
       
        for colour, rect in p:   #for loops
            x,y,w,h = rect       #x, y, w, h, all this equals to rect

            #range X 
            if self.x + self.width / 2 > x and self.x - self.width / 2 < x + w:  
                #range Y                                                         
                if self.y + self.height >= y and self.y + self.height <= y + h:   
                                                                                  
                    if self.speed_y < 0:                                        
                        on = True                                                 
       

        if not on and not self.y >= display_height - self.height:       
            self.speed_y -= 0.5                                          
        elif on:                                                            
            self.speed_y = self.jump_speed                             
        else:
            self.y = display_height - self.height
            self.speed_x = 0                                                  
            self.speed_y = 0
            if self.x != (display_width - self.width) / 2:                         
                if self.x > (display_width - self.width) / 2:                     
                    self.x = max((display_width - self.width) / 2, self.x - 6)      
                else:                                                              
                    self.x = min((display_width - self.width) / 2, self.x + 6)     
                                                                                   
            else:        
                keys = key.get_pressed()                                            
                if keys[K_SPACE]:                                                      
                    self.speed_y = self.jump_speed                                                         

    
    def side_control(self):                                   #next function in class
        if self.x + self.width < 0:                            
            self.x = display_width - self.scale               
        if self.x > display_width:                            
            self.x = -self.width                              

    
       
    def slow_character(self):                                                                     
        if self.speed_x < 0: self.speed_x = min(0, self.speed_x + self.x_acceleration / 6)        
        if self.speed_x > 0: self.speed_x = max(0, self.speed_x - self.x_acceleration / 6)       

    def move(self):   
        keys = key.get_pressed()                       
       
        if not self.y >= display_height - self.height:                                      
 
            if keys[K_LEFT] and keys[K_RIGHT]: self.slow_character()                        
            elif keys[K_LEFT]: self.speed_x -= self.x_acceleration                          
            elif keys[K_RIGHT]: self.speed_x += self.x_acceleration                      
            else: self.slow_character()                                                     

                                                                                            #without it panda will be move so quick when you jump on platform
            self.speed_x = max(-self.max_speed_x, min(self.max_speed_x, self.speed_x))      
            self.speed_y = max(-self.max_speed_y, min(self.max_speed_y, self.speed_y))      
            
            
platform_spacing = 100  #if number is more than less platform and when is less, more platform            

class Platform_Motion:           #new class about how platforms move
    def __init__(self):                   
        self.platforms = []         
        self.spawns = 0              #space between button and first platform
        self.start_spawn = display_height 

        scale = 0                                      
        self.width, self.height = 25 * scale, 6 * scale              

    def update(self):         
        self.spawner()
        return self.manage()

    def spawner(self):                                                         
        if display_height - info['screen_y'] > self.spawns * platform_spacing: 
            self.spawn()                                                      
    
    def spawn(self):
        y = self.start_spawn - self.spawns * platform_spacing                  
        x = random.randint(-self.width, display_width)                             
      
        self.platforms.append(Platform(x,y,random.choice([1,-1])))          
        self.spawns += 1                   
        
    def manage(self):                      
        u = []
        b = []
        for i in self.platforms:
            i.move()
            i.change_direction()
            b.append(i.show())
 
            if i.on_screen():
                u.append(i)
           
        self.platforms = u
        return b    

class Platform:                                             #new class platform 
    def __init__(self,x,y,direction):
        self.x = x
        self.y = y
        self.direction = direction                            
        self.speed = 2                                         
        self.colour = (random.randint(0,223), random.randint(0,172), random.randint(0,125))      
        scale = 3
        self.width, self.height = 28 * scale, 7 * scale         
    
    def move(self):                                        #here is how quick move platform together with 'speed'
        self.x += self.speed * self.direction            
        self.change_direction()                        
    
    def change_direction(self):           #it;s about walls for platforms
        if self.x <= 0:                                  #if locarion of panda(horisont) <=0
            self.direction = 1                           #direction of panda will be 1
        if self.x + self.width >= display_width:              #and if locarion of panda + width >= near 580
            self.direction = -1                                #than direction -1
        
    def on_screen(self):                                                
        if self.y > info['screen_y'] + display_height:                
            return False                                                
        return True    

    def show(self):                                        
        return ((0,0,0), (self.x, self.y, self.width, self.height))  #here is color of platforms and some puncts about width and height

def random_colour(l,h): 
    return (random.randint(l,h),random.randint(l,h),random.randint(l,h))

def blit_images(x):                      
    for i in x:
        gameDisplay.blit(transform.scale(i[0], (i[1][2],i[1][3])), (i[1][0], i[1][1] - info['screen_y'])) 

def event_loop():
    for loop in event.get():                
        if loop.type == KEYDOWN:           
            if loop.key == K_ESCAPE:         
                quit()
        if loop.type == QUIT:
            quit()

f = font.SysFont('', 50)           
def show_score(score, pos):
    message = f.render(str(round(score)), True, (100,100,100))    
    rect = message.get_rect()                         
                                                 #it's about visiable score
    if pos == 0:                                 #
        x = display_width - rect.width - 10      #
    else:                                        #
        x = 10                                   #
    y = rect.height + 10                         #
       
    gameDisplay.blit(message, (x, y))                 
  
info = {
    'screen_y': 0,
    'score': 0,
    'high_score': 0               
    }  
  
  
panda_player = Panda()                        #equals class to variables
platform_motion = Platform_Motion()


while True:
    #MATH THINGS
 
    event_loop()          
 
    platform_blit = platform_motion.update()         
    stick_blit = panda_player.update(platform_blit)            
    info['screen_y'] = min(min(0,stick_blit[1][1] - display_height*0.4),info['screen_y'])      
    info['score'] = (-stick_blit[1][1] + 470)/50                               #it's about how score count


    print(stick_blit[1][1], info['screen_y'])                        
    if stick_blit[1][1] - 470 > info['screen_y']:      
        info['score'] = 0           
        info['screen_y'] = 0   
        panda_player = Panda() 
        platform_motion = Platform_Motion()

    clock.tick(60)      
                        #how quickly panda and plates move

    gameDisplay.fill((223,172,125)) #make an image
 
    blit_images([stick_blit])   

    for x in platform_blit:                   
        i = list(x)
        i[1] = list(i[1])
        i[1][1] -= info['screen_y']
        draw.rect(gameDisplay, i[0], i[1])
 
    info['high_score'] = max(info['high_score'], info['score'])
 
    show_score(info['score'],1)
    show_score(info['high_score'],0)
 
    display.update()

