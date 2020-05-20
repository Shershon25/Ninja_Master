#Ninja images-https://www.gameart2d.com/ninja-adventure---free-sprites.html
#Title icon: <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from/
                        #<a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
#Enemy image- https://www.gamedevmarket.net/member/segel-studio/
#Sound effects and music from opengameart.org
#Nani?! is famous anime meme and is used in this game as a sound effect.
import pygame as pg
import sys,os,random
from settings import *
from sprites import *
from pygame.locals import *
from sprites import Power_up
from sprites import Bullets

#Game class
class Game:
    def __init__(self):
        #initiating pygame
        pg.mixer.pre_init(44100,-16,2,512)
        pg.init()
        self.clock = pg.time.Clock()
        self.window = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption("NINJA MASTER")
        pg.display.set_icon(icon)
        self.running = True
        self.dim_screen = pg.Surface(self.window.get_size()).convert()
        self.dim_screen.fill((255,0,255))
        self.dim_screen.set_colorkey((255,0,255))  #to make the screen transparent
        self.bullet_time = Bullets(0,0,True)
        self.image=dim_img.convert()
        self.image.set_colorkey((255,255,255))
    
    def display_text(self,surf,text,size,x,y,colour):
        font = pg.font.Font(FONT_NAME,size)
        text_surface = font.render(text,True,colour) #True for antialiased-text
        text_rect = text_surface.get_rect()
        text_rect.center = (int(x),int(y))
        surf.blit(text_surface,text_rect)

    
    def health_status(self,surf,percent,x,y):
        if percent < 0:
            percent = 0 
        if percent >= 100:
            percent = 100
        BAR_LENGTH = 100
        BAR_HEIGHT = 15
        fill = (percent/100) * BAR_LENGTH
        outer_rect = pg.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
        inner_rect = pg.Rect(x,y,int(fill),BAR_HEIGHT)
        pg.draw.rect(surf,WHITE,outer_rect,2)
        pg.draw.rect(surf,GREEN,inner_rect)

  
    def new(self):
        #adding sprites 
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.bullet = pg.sprite.Group()
        self.mob = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for i in range(5):
            self.mobs = Mobs(self)
            self.all_sprites.add(self.mobs)
            self.mob.add(self.mobs)
        for plat in PLATFORM_LIST:
            p = Platform(*plat,self)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.pause = False
        pg.mixer.music.load(os.path.join(sound_dir,'Dark Blue.ogg'))
        pg.mixer.music.set_volume(0.1)
        self.run()

    def run(self):
        #Game loop
        pg.mixer.music.play(-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.pause:
                self.update()
            self.draw()
        pg.mixer.music.fadeout(1000)
            
    def update(self):
        global BULLET_DELAY_TIME
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y != 0 :   
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                if self.player.vel.y > 0:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
        
        hits = pg.sprite.groupcollide(self.mob, self.bullet,False,True)
        for hit in hits:
            self.player.points += 20
            hit.bullet_count += 1
            self.hit=hit.bullet_count
            if hit.bullet_count >= 2:
                hit.kill()
                mob_death.play()
                self.enemy = Mobs(self)
                self.all_sprites.add(self.enemy)
                self.mob.add(self.enemy)
                if random.random() > 0.5:
                    power = Power_up(self,hit.rect.center)
                    self.all_sprites.add(power)
                    self.powerups.add(power) 
                    
        hitting = pg.sprite.spritecollide(self.player, self.mob, True,pg.sprite.collide_mask)
        if hitting:
            self.player.health -= 30   
            enemy=Mobs(self)
            self.all_sprites.add(enemy)
            self.mob.add(enemy)         
        if self.player.health <= 0:
                self.playing = False
        
        hitting= pg.sprite.spritecollide(self.player, self.powerups, True,pg.sprite.collide_mask)
        for hit in hitting:
            if hit.type == 'shield':
                self.player.health += 20
                if self.player.health > 100:
                    self.player.health = 100
                health_pow.play()
            if hit.type == 'weapon':
                self.player.powerup()
                
    def events(self):
        #Game loop for events
        for event in pg.event.get():
            if event.type == QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == KEYDOWN:
                if event.key == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.key == K_UP:
                    self.player.jump()
                if event.key == K_SPACE:
                    self.player.throw_animate()  
                    self.player.shoot()
                if event.key == K_p:
                    self.pause = not self.pause

    def draw(self):
        self.window.fill(BLACK)
        BG_img.convert()
        self.background = pg.transform.scale(BG_img,(WIDTH,HEIGHT))
        self.window.blit(self.background,(0,0))
        self.all_sprites.draw(self.window)
        self.display_text(self.window,'SCORE :   {}'.format(self.player.points),15,45,20,WHITE)
        self.display_text(self.window,"HEALTH :",15,35,45,WHITE)
        self.health_status(self.window,self.player.health,70,35)
        if self.pause:
            self.window.blit(self.dim_screen,(0,0))
            self.window.blit(self.image,(240,244))
            self.display_text(self.dim_screen,"GAME PAUSED!",60,WIDTH/2,HEIGHT/4,WHITE)
            self.display_text(self.window,"Press P again to resume",22,WIDTH/2,HEIGHT/4+50,WHITE)
        pg.display.update()

    def start_window(self):   
        pg.mixer.music.load(os.path.join(sound_dir,'start_screen.wav'))
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play(-1)
        self.window.fill(BLACK)
        self.window.blit(start_screen_img,(0,0))
        self.display_text(self.window,"NINJA MASTER", 48, WIDTH / 2, HEIGHT / 4,GREEN)
        self.display_text(self.window,"INSTRUCTIONS", 22, WIDTH / 2, HEIGHT / 2-40,BLACK)
        self.display_text(self.window,"Use ARROWS to move and jump,SPACE to attack and P to pause", 20, WIDTH / 2, 315,WHITE)
        self.display_text(self.window,"One can move up through the platforms but not down ", 20, WIDTH / 2, 350,WHITE)
        self.display_text(self.window,"Attack the enemies in ninja style and collect special powers from them", 20, WIDTH / 2, 385,WHITE)
        self.display_text(self.window,"Press any key to play", 22, WIDTH / 2, HEIGHT * 3 / 4+45,BLACK)
        pg.display.flip()
        self.wait_for_key(False)
        pg.mixer.music.fadeout(100)

    def gameOver_window(self):  
        if not self.running:
            return  
        pg.mixer.music.load(os.path.join(sound_dir,'end_screen.ogg'))
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play(-1)
        self.window.fill(BLACK)
        self.window.blit(start_screen_img,(0,0))
        self.display_text(self.window,"YOU GOT DEFEATED!!", 48,  WIDTH / 2, HEIGHT / 4,WHITE)
        self.display_text(self.window,"Score: " + str(self.player.points), 22,  WIDTH / 2, HEIGHT / 2,WHITE)
        self.display_text(self.window,"Press R-key to play again", 22,  WIDTH / 2, HEIGHT * 3 / 4,WHITE)
        pg.display.flip()
        self.wait_for_key(True)
        pg.mixer.music.fadeout(100)

    def wait_for_key(self,gameover):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting=False
                    self.running=False
                if gameover:
                    if event.type == pg.KEYDOWN:
                        if event.key == K_r:
                            waiting=False
                else:
                    if event.type == pg.KEYDOWN:
                        waiting = False

g=Game()
g.start_window()
while g.running:
    g.new()
    g.gameOver_window()

pg.quit()