# -*- coding: utf-8 -*-
import sys, time, random, math, pygame,locale
from pygame.locals import *
from basic import *
#from music_analysis import music
import json

"""
#music dealing
import time
import librosaBeat
import playMusic
import threading
stressTime = librosaBeat.find_stress()
waitTime = []
waitTime.append(int(round(stressTime[0]*1000))-0)
for i in range(1,len(stressTime)):
    waitTime.append(int(round(stressTime[i]*1000)) - int(round(stressTime[i-1]*1000)))

print(waitTime)
#end
"""

src0 = "Star2.wav"
src1 = "ThePiano.wav"
src2 = "TheWinter.wav"
src3 = "Luv_Letter.wav"
src4 = "EverlastingTruth.wav"
src5 = "Faded.wav"

#4'19 1'23 1'48 4'30  3'51 2'15
#music_time_ms=[259000, 83000, 108000, 270000, 231000, 135000]
#waitTime[6][] waitTime[i]是第i首歌的数组
#waiting for revise:存下重音数组 
#waitTime = music()
#modified:
with open('stress_time.json','r') as f:
   waitTime = json.load(f)
#print(len(waitTime))
 
#攻击类
def Arrow():
    #revise 0627
    y = 350
    #y = random.randint(270,350)
    arrow.position = 800,y
    #revise0626
    #bullent_sound.play_sound()

#滚动地图类
class MyMap(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.bg = pygame.image.load("backgroundd.jpg").convert_alpha()
    def map_rolling(self):
        if self.x < -300:
            self.x = 300
        else:
            self.x -=5
    def map_update(self):
        screen.blit(self.bg, (self.x,self.y))
    def set_pos(x,y):
        self.x =x
        self.y =y
        
#定义一个按钮类
class Button(object):
    def __init__(self, upimage, downimage,position):
        self.imageUp = pygame.image.load(upimage).convert_alpha()
        self.imageDown = pygame.image.load(downimage).convert_alpha()
        self.position = position
        self.game_start = False
        self.game_change = False
        
    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self. position
        w, h = self.imageUp.get_size()

        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y

    def render(self):
        w, h = self.imageUp.get_size()
        x, y = self.position
        
        if self.isOver():
            screen.blit(self.imageDown, (x-w/2,y-h/2))
        else:
            screen.blit(self.imageUp, (x-w/2, y-h/2))
    def is_start(self):
        if self.isOver():
            b1,b2,b3 = pygame.mouse.get_pressed()
            if b1 == 1:
                
                if(self.game_start == False):
                  self.game_start = True
                elif(self.game_change == True):
                  self.game_change = False
                  
                bg_sound.play_pause()
                btn_sound.play_sound()
                bg_sound.play_sound()
"""
def replay_music():
    bg_sound.play_pause()
    bg_sound = bg_sound_all[round_]
    bg_sound.play_sound()
"""

#定义一个数据IO的方法
def data_read():
    fd_1 = open("data.txt","r")
    best_score = fd_1.read()
    fd_1.close()
    return best_score

   
#定义一个控制声音的类和初始音频的方法
def audio_init():
    global hit_au,btn_au,bg_au,bullent_au
    pygame.mixer.init()
    hit_au = pygame.mixer.Sound("exlposion.wav")
    btn_au = pygame.mixer.Sound("button.wav")
    #revise
    bg_au = pygame.mixer.Sound("background.ogg")
    #
    #bg_au = pygame.mixer.Sound("ThePiano.wav")
    bullent_au = pygame.mixer.Sound("bullet.wav")
    
class Music():
    def __init__(self,sound):
        self.channel = None
        self.sound = sound     
    def play_sound(self):
        self.channel = pygame.mixer.find_channel(True)
        self.channel.set_volume(0.5)
        self.channel.play(self.sound)
    def play_pause(self):
        self.channel.set_volume(0.0)
        self.channel.play(self.sound)

      
#主程序部分
pygame.init()
audio_init()
screen = pygame.display.set_mode((800,600),0,32)
##游戏名设定
pygame.display.set_caption("守株不待兔")
font = pygame.font.Font(None, 22)
font1 = pygame.font.Font(None, 40)
framerate = pygame.time.Clock()
upImageFilename = 'game_start_up.png'
downImageFilename = 'game_start_down.png'

#按钮对象
button = Button(upImageFilename,downImageFilename, (400,500))
interface = pygame.image.load("back.png")

#地图对象
bg1 = MyMap(0,0)
bg2 = MyMap(300,0)

#精灵组
group = pygame.sprite.Group()
group_exp = pygame.sprite.Group()
group_fruit = pygame.sprite.Group()
group_arrow = pygame.sprite.Group()

#猎狗
dragon = MySprite()
dragon.load("dog2.png", 200, 180, 4)
dragon.position = 100, 200
group.add(dragon)

#爆炸
explosion = MySprite()
explosion.load("exp1.png",128,128,5)

#rabbit玩家
player = MySprite()
player.load("rab2.png", 100, 100, 4)
player.position = 400, 270
group.add(player)

#子弹攻击
arrow = MySprite()
arrow.load("flame.png", 40, 16, 1)
arrow.position = 800,320
group.add(arrow)



#定义一些变量
arrow_vel = 10.0
game_over = False
you_win = False
player_jumping = False
jump_vel = 0.0
player_start_y = player.Y
player_hit = False
monster_hit = False
p_first = True
m_first = True
best_score = 0

global bg_sound,hit_sound,btn_sound,bullent_sound
#revise

bg_sound1=Music(pygame.mixer.Sound(src0))
bg_sound2=Music(pygame.mixer.Sound(src1))
bg_sound3=Music(pygame.mixer.Sound(src2))
bg_sound4=Music(pygame.mixer.Sound(src3))
bg_sound5=Music(pygame.mixer.Sound(src4))
bg_sound6=Music(pygame.mixer.Sound(src5))
bg_sound_all = [bg_sound1,bg_sound2,bg_sound3,bg_sound4,bg_sound5,bg_sound6]
round_ = 0
bg_sound = bg_sound_all[round_]
#
hit_sound=Music(hit_au)
btn_sound=Music(btn_au)
bullent_sound =Music(bullent_au)
#0627 revise The first -> Level One
game_round = {1:'Level One ',2:'Level Two',3:'Level Three',4:'Level Four',5:'Level Five'}
game_pause = True
index =0
current_time = 0
start_time = 0
music_time = 0
score =0
replay_flag = True

#add：
bullet_speed = 100
#
#循环
#revise

lastTime = pygame.time.get_ticks()
index2 = 1
interval = waitTime[round_][0]
bg_sound.play_sound()
music_start = pygame.time.get_ticks()

best_score = data_read()
ticks = 0
while True:
    framerate.tick(60)
    #0627：子弹不匀速 时间差估计？
    #print(pygame.time.get_ticks()-ticks)
    ticks = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()
        
    elif keys[K_SPACE]:
        if not player_jumping:
            player_jumping = True
            jump_vel = -12.0
            
    screen.blit(interface,(0,0))
    button.render()
    button.is_start()
    #pygame.display.update()
    
    #while button.game_change == True:
       # a=1
        #screen.blit(interface,(0,0))
        #button.render()
        #button.is_start()
    """
    while(button.game_start == False or button.game_change == True):
        a = 1
        #screen.blit(interface,(0,0))
        #button.render()
        #button.is_start()
        #pygame.display.update()
        #button.render()
        #button.is_start()
        #button.is_start()
        #abc=1
    """
    if button.game_start == True and button.game_change == False:
        if game_pause :
            index +=1
            tmp_x =0
            if score >int (best_score):
                best_score = score
            fd_2 = open("data.txt","w+")
            fd_2.write(str(best_score))
            fd_2.close()
            #判断游戏是否通关
            if index == 7:
                you_win = True
            if you_win:
                start_time = time.clock()
                current_time =time.clock()-start_time
                while current_time<5:
                    screen.fill((200, 200, 200))
                    print_text(font1, 270, 150,"YOU WIN THE GAME!",(240,20,20))
                    current_time =time.clock()-start_time
                    print_text(font1, 320, 250, "Best Score:",(120,224,22))
                    print_text(font1, 370, 290, str(best_score),(255,0,0))
                    print_text(font1, 270, 330, "This Game Score:",(120,224,22))
                    print_text(font1, 385, 380, str(score),(255,0,0))
                    pygame.display.update()
                pygame.quit()
                sys.exit()
                
            for i in range(0,200):
                carrot = MySprite()
                eggplant=MySprite()
                carrot.load("carrot.png", 75, 20, 1)
                eggplant.load("eggplant.png",75,20,1)
                
                tmp_x +=random.randint(50,120)
                
                carrot.X = tmp_x+300
                carrot.Y = random.randint(80,200)
                eggplant.X=tmp_x+400
                eggplant.Y=random.randint(80,200)
                
                group_fruit.add(carrot)
                group_fruit.add(eggplant)
                
            #revise 0626    
            start_time = time.clock()
            current_time =time.clock()-start_time
            #while current_time < 3:
            while current_time < 0.5:
                screen.fill((200, 200, 200))
                print_text(font1, 320, 250,game_round[index],(240,20,20))
                pygame.display.update()
                game_pause = False
                current_time =time.clock()-start_time
                
        else:
            #更新子弹
            if not game_over:
                #waiting for revise:加上移动到中间的时间
                #revise 0627:
                #arrow.X -= (int)(bullet_speed*(pygame.time.get_ticks()-lastTime)/1000)
                arrow.X -= 10
                #revise
                #提前1s生成
                #forward_time = 400 / bullet_speed
                #forward_time = (int)(400/bullet_speed*1000)
                forward_time = 0
            if (pygame.time.get_ticks() + forward_time -lastTime >= interval):
                Arrow()
                lastTime = pygame.time.get_ticks()
                if(index2 + 1 < len(waitTime[round_])):
                #revise 0627:
                  index2 += 1
                  if(index2+1 < len(waitTime[round_]) and waitTime[round_][index2-1] < 500 and waitTime[round_][index2] < 500):
                    interval = waitTime[round_][index2] + waitTime[round_][index2+1]
                    index2 += 1
                  else:
                    interval = waitTime[round_][index2]     #0627谜之list index out of range solved
                #
                  
            #碰撞检测，子弹是否击中玩家
            if pygame.sprite.collide_rect(arrow, player):
                #Arrow()
                explosion.position =player.X,player.Y
                player_hit = True
                #revise0626
                #hit_sound.play_sound()
                if p_first:
                    group_exp.add(explosion)
                    p_first = False
                #player.X -= 10
                dragon.X += 15
                #if(score > 5):
                    #score -= 5

            #碰撞检测，子弹是否击中怪物
            if pygame.sprite.collide_rect(arrow, dragon):
                #revise
                #Arrow()
                explosion.position =dragon.X+50,dragon.Y+50
                monster_hit = True
                #revise0626
                #hit_sound.play_sound()
                if m_first:
                    group_exp.add(explosion)
                    m_first = False
                if(dragon.X > -100):
                    dragon.X -= 10

            #碰撞检测，玩家是否被怪物追上
            if pygame.sprite.collide_rect(player, dragon):
                game_over = True
            #遍历果实，使果实移动
            for e in group_fruit:
                e.X -=5
            collide_list = pygame.sprite.spritecollide(player,group_fruit,True)
            score += len(collide_list)
            
            #是否通过关卡
            #revise0626:
            music_now = pygame.time.get_ticks()
            #if (dragon.X < -100 and (music_now - music_start >= music_time_ms[round_])):
            #if dragon.X < -100:
            #if (index2 >= len(waitTime[round_])-1):
            #if False:
            if (index2 >= len(waitTime[round_])-1):
                game_pause = True
                round_+=1
                lastTime = pygame.time.get_ticks()
                index2 = 1
                if(round_<=5):
                  interval = waitTime[round_][0]
                  bg_sound = bg_sound_all[round_]
                  bg_sound.play_sound()
                  music_start = pygame.time.get_ticks()
                #Arrow()
                #replay_music()
                
                #waiting for revise : add a button 
                #button.render()
                #button.is_start()
                  
                player.X = 400
                dragon.X = 100
                button.game_change = True

            #检测玩家是否处于跳跃状态
            if player_jumping:
                if jump_vel <0:
                    jump_vel += 0.6
                elif jump_vel >= 0:
                    jump_vel += 0.8
                player.Y += jump_vel
                if player.Y > player_start_y:
                    player_jumping = False
                    player.Y = player_start_y
                    jump_vel = 0.0


            #绘制背景
            bg1.map_update()
            bg2.map_update()
            bg1.map_rolling()
            bg2.map_rolling()
            
            #更新精灵组
            if not game_over:
                group.update(ticks, 60)
                group_exp.update(ticks,60)
                group_fruit.update(ticks,60)
                
            #循环播放背景音乐
                """
            music_time = time.clock()
            if music_time   > 150 and replay_flag:
                replay_music()
                replay_flag =False
                """
                
            #绘制精灵组
            group.draw(screen)
            group_fruit.draw(screen)
            if player_hit or monster_hit:
                group_exp.draw(screen)
            print_text(font, 330, 560, "Rabbit run! Watch out for the hounds!")
            print_text(font, 200, 20, "You have get Score:",(219,224,22))
            print_text(font1, 380, 10, str(score),(255,0,0))
            if game_over:
                start_time = time.clock()
                current_time =time.clock()-start_time
                while current_time<5:
                    screen.fill((200, 200, 200))
                    print_text(font1, 300, 150,"GAME OVER!",(240,20,20))
                    current_time =time.clock()-start_time
                    print_text(font1, 320, 250, "Best Score:",(120,224,22))
                    if score >int (best_score):
                        best_score = score
                    print_text(font1, 370, 290, str(best_score),(255,0,0))
                    print_text(font1, 270, 330, "This Game Score:",(120,224,22))
                    print_text(font1, 370, 380, str(score),(255,0,0))
                    pygame.display.update()
                fd_2 = open("data.txt","w+")
                fd_2.write(str(best_score))
                fd_2.close()
                pygame.quit()
                sys.exit()
    pygame.display.update()

#  0627 problem:
#1.胡萝卜和茄子在中段音乐没出现---胡萝卜出现在地上比较正常吧 或者低一点？
#2.爆炸效果持续时间太长
#3.计算树桩移动到中间的时间
#4.在节奏紧凑的时候树桩生成太快 换慢一点的音乐或者筛掉一些重音
#5.换关的时候加按钮
#6.迷之list index out of range:interval = waitTime[round_][index2]  solved

