import pygame as pg
import os
pg.mixer.pre_init(44100,-16,2,512)
pg.init()

#initializing the variables

#Colours
GREEN=(128,255,0)
BLACK=(0,0,0)
WHITE=(255,255,255)


#Game settings
WIDTH=1024
HEIGHT=576
FPS=120 #High FPS because the game lags in my lap :)
PLAYER_GRAVITY=0.8
PLAYER_ACC=0.5
PLAYER_FRICTION=-0.12
PLAYER_JUMP=15
MOB_GRAVITY=1
BULLET_DELAY_TIME=1000
POWERUP_TIME=5000
POWERUP_VALUE=100
x=0;y=0;z=0

#Font 
FONT_NAME=pg.font.match_font('arial')   #To use the font available in the system

#platforms to be added
PLATFORM_LIST=[(0,HEIGHT-20),(100,HEIGHT-20),(200,HEIGHT-20),(0,HEIGHT-20),(300,HEIGHT-20),(400,HEIGHT-20),
               (500,HEIGHT-20),(600,HEIGHT-20),(700,HEIGHT-20),(800,HEIGHT-20),(900,HEIGHT-20),(1000,HEIGHT-20),
               (1100,HEIGHT-20),
               (80,HEIGHT-125),(180,HEIGHT-125),
               (WIDTH-280,HEIGHT-125),(WIDTH-180,HEIGHT-125),
               (240,HEIGHT-255),(340,HEIGHT-255),
               (WIDTH-380,HEIGHT-255),(WIDTH-480,HEIGHT-255),
               (80,180),(180,180),
               (380,180),(480,180),(680,180),(780,180)]

#File and images directory

current_dir=os.path.dirname(__file__)
img_dir=os.path.join(current_dir,'img')
sound_dir=os.path.join(current_dir,'sound')


BG_img=pg.image.load(os.path.join(img_dir,'background.png'))
Player_img=pg.image.load(os.path.join(img_dir,'Idle__000.png'))
Tile_img=pg.image.load(os.path.join(img_dir,'rock.png'))
start_screen_img=pg.image.load(os.path.join(img_dir,'ninja_scroll1.png'))

mob_image=pg.image.load(os.path.join(img_dir,'Enemy_Idle_000.png'))
bullet_img=pg.image.load(os.path.join(img_dir,'Kunai.png'))

icon=pg.image.load(os.path.join(img_dir,'Feelings.png'))
pg.transform.scale(icon,(32,32))

dim_img=pg.image.load(os.path.join(img_dir,'DIM BACK.png'))

#sound
jump_sound=pg.mixer.Sound(os.path.join(sound_dir,'Jump2.wav'))
jump_sound.set_volume(0.2)
shoot_sound=pg.mixer.Sound(os.path.join(sound_dir,'Laser.wav'))
shoot_sound.set_volume(0.2)
nani_sound=pg.mixer.Sound(os.path.join(sound_dir,'Nani.ogg'))
nani_sound.set_volume(0.3)
health_pow=pg.mixer.Sound(os.path.join(sound_dir,"Randomize.wav"))
health_pow.set_volume(0.3)
mob_death=pg.mixer.Sound(os.path.join(sound_dir,'Explosion.wav'))
mob_death.set_volume(0.1)

#powerup images
health_pu=pg.image.load(os.path.join(img_dir,'Energy1.png'))
health_pu.set_colorkey(WHITE)
weapon_pu=pg.image.load(os.path.join(img_dir,'Weapon.png'))
powerup_img={}
powerup_img['shield']=health_pu
powerup_img['weapon']=weapon_pu


#idle animation frames
idle_1_img=pg.image.load(os.path.join(img_dir,'Idle__000.png'))
idle_2_img=pg.image.load(os.path.join(img_dir,'Idle__001.png'))
idle_3_img=pg.image.load(os.path.join(img_dir,'Idle__002.png'))
idle_4_img=pg.image.load(os.path.join(img_dir,'Idle__003.png'))
idle_5_img=pg.image.load(os.path.join(img_dir,'Idle__004.png'))
idle_6_img=pg.image.load(os.path.join(img_dir,'Idle__005.png'))
idle_7_img=pg.image.load(os.path.join(img_dir,'Idle__006.png'))
idle_8_img=pg.image.load(os.path.join(img_dir,'Idle__007.png'))
idle_9_img=pg.image.load(os.path.join(img_dir,'Idle__008.png'))
idle_10_img=pg.image.load(os.path.join(img_dir,'Idle__009.png'))

#run frames
run_1_img=pg.image.load(os.path.join(img_dir,'Run__000.png'))
run_2_img=pg.image.load(os.path.join(img_dir,'Run__001.png'))
run_3_img=pg.image.load(os.path.join(img_dir,'Run__002.png'))
run_4_img=pg.image.load(os.path.join(img_dir,'Run__003.png'))
run_5_img=pg.image.load(os.path.join(img_dir,'Run__004.png'))
run_6_img=pg.image.load(os.path.join(img_dir,'Run__005.png'))
run_7_img=pg.image.load(os.path.join(img_dir,'Run__006.png'))
run_8_img=pg.image.load(os.path.join(img_dir,'Run__007.png'))
run_9_img=pg.image.load(os.path.join(img_dir,'Run__008.png'))
run_10_img=pg.image.load(os.path.join(img_dir,'Run__009.png'))

#THROW_FRAMES
throw_1_img=pg.image.load(os.path.join(img_dir,'Throw__004.png'))
throw_2_img=pg.image.load(os.path.join(img_dir,'Throw__005.png'))
throw_3_img=pg.image.load(os.path.join(img_dir,'Throw__006.png'))
throw_4_img=pg.image.load(os.path.join(img_dir,'Throw__007.png'))
throw_5_img=pg.image.load(os.path.join(img_dir,'Throw__008.png'))
throw_6_img=pg.image.load(os.path.join(img_dir,'Throw__009.png'))
throw_7_img=pg.image.load(os.path.join(img_dir,'Throw__000.png'))
throw_8_img=pg.image.load(os.path.join(img_dir,'Throw__001.png'))
throw_9_img=pg.image.load(os.path.join(img_dir,'Throw__002.png'))
throw_10_img=pg.image.load(os.path.join(img_dir,'Throw__003.png'))





