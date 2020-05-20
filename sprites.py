#Sprites used in the game
import pygame as pg,os,random
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self) #game makes a copy of the Game class 
        self.game=game
        self.walking=False
        self.jumping=False
        self.direction=True #Right facing
        self.health=100
        self.points=0
        self.current_frame=0
        self.jump_no=0
        self.last_update=0
        self.past=0
        self.power=1
        self.powerup_time=0
        self.load_sprites()
        self.image=pg.transform.scale(Player_img,(32,60))
        self.rect=self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT-50)
        self.pos = vec(WIDTH / 2, HEIGHT -50)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0) 
    def load_sprites(self):
        self.idle_frames=[idle_1_img,idle_2_img,idle_3_img,idle_4_img,idle_5_img,
                          idle_6_img,idle_7_img,idle_8_img,idle_9_img,idle_10_img]
        self.run_frames_r=[run_1_img,run_2_img,run_3_img,run_4_img,run_5_img,
                           run_6_img,run_7_img,run_8_img,run_9_img,run_10_img]
        self.run_frames_l=[]
        for frame in self.run_frames_r:
            self.run_frames_l.append(pg.transform.flip(frame,True,False))
        self.throw_frames_r=[throw_1_img,throw_2_img,throw_3_img,throw_4_img,throw_5_img,
                           throw_6_img,throw_7_img,throw_8_img,throw_9_img,throw_10_img]
        self.throw_frames_l=[]
        for frame in self.throw_frames_r:
            self.throw_frames_l.append(pg.transform.flip(frame,True,False))

    def update(self):
        now = pg.time.get_ticks()
        if now - self.powerup_time >= POWERUP_TIME:
            self.power=1
            self.powerup_time=pg.time.get_ticks() 
        self.animate()
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] :
            self.direction=False
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] :
            self.direction=True
            self.acc.x = PLAYER_ACC
        if keys[pg.K_SPACE] :
            self.throw_animate()

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        #to make the player stop 
        if abs(self.vel.x) < 0.5:
            self.vel.x=0
        self.pos += self.vel + 0.5 * self.acc
        
        
        if self.pos.x >= WIDTH:
            self.pos.x = WIDTH
        if self.pos.x <= 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos
    
    def powerup(self):
        self.power+=1
        self.powerup_time=pg.time.get_ticks()
        nani_sound.play()

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits:
            self.vel.y = -PLAYER_JUMP #vel
            self.jumping=True
            jump_sound.play()

    def animate(self):
        now=pg.time.get_ticks() #time passed since beginning
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        #walking animation
        if self.walking:
            if now-self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.run_frames_l)
                bottom=self.rect.bottom
                if self.vel.x > 0:
                    self.direction=True
                    image = self.run_frames_r[self.current_frame]
                    self.image=pg.transform.scale(image,(47,60))
                else:
                    self.direction=False
                    image = self.run_frames_l[self.current_frame]
                    self.image=pg.transform.scale(image,(47,60))
                self.rect.bottom=bottom
    

        #idle animation
        if not self.jumping and not self.walking or self.vel.x==0 :
            if now-self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom=self.rect.bottom
                image = self.idle_frames[self.current_frame]
                self.image=pg.transform.scale(image,(32,60))
                self.rect.bottom=bottom
        self.mask=pg.mask.from_surface(self.image)

    def throw_animate(self):
        self.jumping=False
        self.walking=False
        now=pg.time.get_ticks()
        if now-self.last_update == 0:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.throw_frames_r)
            bottom=self.rect.bottom
            if self.vel.x > 0:  
                self.direction=True   
                image = self.throw_frames_r[self.current_frame]
                self.image=pg.transform.scale(image,(50,60))
            elif self.vel.x < 0:
                self.direction=False
                image = self.throw_frames_l[self.current_frame]
                self.image=pg.transform.scale(image,(50,60))
            else:
                if self.direction:  
                    self.direction=True   
                    image = self.throw_frames_r[self.current_frame]
                    self.image=pg.transform.scale(image,(50,60))
                    self.shoot()
                else:
                    self.direction=False
                    image = self.throw_frames_l[self.current_frame]
                    self.image=pg.transform.scale(image,(50,60))  
                    self.shoot()
            self.rect.bottom=bottom
    def shoot(self):
            now= pg.time.get_ticks()
            if self.power==1:
                if now-self.past > BULLET_DELAY_TIME:
                    shoot_sound.play()
                    bult=Bullets(self.rect.centerx,self.rect.centery,self.direction)
                    self.game.all_sprites.add(bult)
                    self.game.bullet.add(bult)
                    self.past=pg.time.get_ticks()
            if self.power >=2:
                if now - self.past > POWERUP_VALUE :
                    shoot_sound.play()
                    bult=Bullets(self.rect.centerx,self.rect.centery,self.direction)
                    self.game.all_sprites.add(bult)
                    self.game.bullet.add(bult)
                    self.past=pg.time.get_ticks()
        
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y,game):
        pg.sprite.Sprite.__init__(self)
        self.game=game
        image=Tile_img
        self.image = image
        self.rect = self.image.get_rect()
        self.mask=pg.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

class Mobs(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game=game
        image=mob_image.convert()
        self.image=pg.transform.scale(image,(70,60))
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.mask=pg.mask.from_surface(self.image)
        self.bullet_count=0
        self.vx=2
        self.vy=0
        global x,y,z
        self.rect.y = random.choice([122,HEIGHT-315,HEIGHT-185])
        if self.rect.y==HEIGHT-315:
            self.rect.centerx=random.randrange(215,609)     
        else :
            self.rect.centerx=random.randrange(55,WIDTH-115)
        self.center=self.rect.center
    def update(self):
        if self.rect.centerx >= WIDTH-115 or self.rect.centerx < 55:
            self.vx *=-1
            self.image=pg.transform.flip(self.image,True,False)
        self.rect.x += self.vx
        self.rect.y += self.vy

class Bullets(pg.sprite.Sprite):
    def __init__(self,x,y,direction):
        pg.sprite.Sprite.__init__(self)
        image=bullet_img.convert()
        self.direction = direction
        self.image=pg.transform.scale(image,(30,10))
        if self.direction:
            self.image=self.image
        else:
            self.image=pg.transform.flip(self.image,True,False)
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.mask=pg.mask.from_surface(self.image)
        self.rect.bottom=y
        self.rect.centerx = x
        self.speed = 10
        self.past=0
    def update(self):
        if self.direction == True:     #right
            self.rect.centerx += self.speed
        elif self.direction == False:
            self.rect.centerx -= self.speed
        self.past=pg.time.get_ticks()
        if self.rect.x < -20 or self.rect.x > WIDTH +20:
            self.kill()
class Power_up(pg.sprite.Sprite):
    def __init__(self,game,center):
        pg.sprite.Sprite.__init__(self)
        self.game=game
        self.type=random.choice(['shield','weapon'])
        image = powerup_img[self.type].convert()
        self.image=pg.transform.scale(image,(40,30))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.mask=pg.mask.from_surface(self.image)
        self.rect.center=center
        self.timer=pg.time.get_ticks()
    def update(self):
        now = pg.time.get_ticks()
        if now - self.timer >= 6000:
            self.kill()


    
      
 

        