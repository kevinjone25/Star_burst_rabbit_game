import pygame
import random
import os

FPS=60

WIDTH=500
HEIGHT=600

BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
YELLOW=(255,255,0)

#遊戲初始化和創建視窗
pygame.init()#pygame裡的東西都初始化
pygame.mixer.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))#視窗大小(寬度,高度)
pygame.display.set_caption("雜燴兔的逆襲")#標題
clock=pygame.time.Clock()#創建對時間做管理操控的物件

#載入圖片
background_img=pygame.image.load(os.path.join("img","background.png")).convert()
owada_img=pygame.image.load(os.path.join("img","owada.png")).convert()
player_img=pygame.image.load(os.path.join("img","player.png")).convert()
egg_img=pygame.image.load(os.path.join("img","egg.png")).convert()
topic_img=pygame.image.load(os.path.join("img","rab.png")).convert()
pygame.display.set_icon(topic_img)
player_mini_img=pygame.transform.scale(egg_img,(45,40))
player_mini_img.set_colorkey(BLACK)
#rock_img=pygame.image.load(os.path.join("img","rock.png")).convert()
bullet_img=pygame.image.load(os.path.join("img","bullet.png")).convert()
rock_imgs=[]
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rab{i}.png")).convert())
expl_anim={}
expl_anim['lg']=[]
expl_anim['sm']=[]
expl_anim['player']=[]
for i in range(9):
    expl_img=pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img,(75,75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img,(30,30)))
    player_expl_img=pygame.image.load(os.path.join("img",f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
power_imgs={}
power_imgs['shield']=pygame.image.load(os.path.join("img","wa1.png")).convert()
power_imgs['gun']=pygame.image.load(os.path.join("img","gun.png")).convert()

#載入音樂
shoot_sound=pygame.mixer.Sound(os.path.join("sound","shoot.wav"))#射擊聲
gun_sound=pygame.mixer.Sound(os.path.join("sound","pow1.ogg"))
shield_sound=pygame.mixer.Sound(os.path.join("sound","shield.wav"))
die_sound=pygame.mixer.Sound(os.path.join("sound","rumble.ogg"))#死亡聲
owada_sound=pygame.mixer.Sound(os.path.join("sound","owada.ogg"))
expl0_sound=pygame.mixer.Sound(os.path.join("sound","expl0.wav"))
expl1_sound=pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
"""expl_sounds=[
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")),#碰撞聲
    pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
]"""
music=pygame.mixer.music.load(os.path.join("sound","1.ogg"))#背景音樂
pygame.mixer.music.set_volume(0.02)#背景音樂音量
shoot_sound.set_volume(0.2)
gun_sound.set_volume(1)
shield_sound.set_volume(1)
die_sound.set_volume(1)
owada_sound.set_volume(1)
expl0_sound.set_volume(0.05)
expl1_sound.set_volume(1)

font_name=os.path.join("font.ttf")

def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,YELLOW)
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)

def new_rock():
    rock=Rock()
    all_sprites.add(rock)
    rocks.add(rock)

def draw_health(surf,hp,x,y):
    if hp<0:
        hp=0
    BAR_LENGTH=100
    BAR_HEIGHT=10
    fill=(hp/100)*BAR_LENGTH
    outline_rect=pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect=pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

def draw_lives(surf,lives,img,x,y):
    for i in range(lives):
        img_rect=img.get_rect()
        img_rect.x=x+50*i
        img_rect.y=y
        surf.blit(img,img_rect)

def draw_init():
    screen.blit(background_img,(0,0))
    draw_text(screen,'雜燴兔攻略戰',64,WIDTH/2,HEIGHT/4)
    draw_text(screen,'AD左右移動 空白鍵發射',35,WIDTH/2,HEIGHT/2)
    draw_text(screen,'按任意鍵開始遊戲',30,WIDTH/2,HEIGHT*3/4-28)
    pygame.display.update()
    waiting=True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:#如果事件包含關閉視窗則關閉視窗
                pygame.quit()
                return True
            elif event.type==pygame.KEYUP:
                waiting=False
                return False

def draw_dinit(sco):
    screen.blit(owada_img,(0,0))
    draw_text(screen,'結束...了嗎',50,WIDTH/2,HEIGHT/4-80)
    draw_text(screen,'狩獵雜燴兔%d'%(sco)+'隻',30,WIDTH/2,HEIGHT/2-80)
    draw_text(screen,'按任意鍵繼續',28,WIDTH/2,HEIGHT*3/4-150)
    pygame.display.update()
    owada_sound.play()
    waiting=True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:#如果事件包含關閉視窗則關閉視窗
                pygame.quit()
                return True
            elif event.type==pygame.KEYUP:
                waiting=False
                return False

#玩家
class Player(pygame.sprite.Sprite):#繼承內建的sprite類別
    def __init__(self):#這個初始函式需要image和rect兩種屬性
        #image顯示,rect定位
        pygame.sprite.Sprite.__init__(self)#呼叫sprite內建初始函式
        self.image=pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()#定位(框起來)
        self.redius=20
        #pygame.draw.circle(self.image,RED,self.rect.center,self.redius)
        self.rect.centerx=WIDTH/2#x座標
        self.rect.bottom=HEIGHT-10#y座標
        self.speedx=8#移動速度
        self.health=100
        self.lives=3
        self.hidden=False
        self.hide_time=0
        self.gun=1
        self.gun_time=0
    
    def update(self):
        now=pygame.time.get_ticks()
        if self.gun>1 and now-self.gun_time>5000:
            self.gun-=1
            self.gun_time=now
        if self.hidden and now-self.hide_time>1000:
            self.hidden=False
            self.rect.centerx=WIDTH/2#x座標
            self.rect.bottom=HEIGHT-10#y座標
        key_pressed=pygame.key.get_pressed()#判斷鍵盤是否被按下
        #左右移動
        if key_pressed[pygame.K_d]:
            self.rect.x+=self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x-=self.speedx
        #限制移動範圍
        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
        if self.rect.left<0:
            self.rect.left=0

    def shoot(self):
        if not(self.hidden):
            if self.gun==1:
                bullet=Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun>=2:
                bullet1=Bullet(self.rect.left,self.rect.centery)
                bullet2=Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden=True
        self.hide_time=pygame.time.get_ticks()
        self.rect.center=(WIDTH/2,HEIGHT+500)

    def gunup(self):
        self.gun+=1
        self.gun_time=pygame.time.get_ticks()

#石頭
class Rock(pygame.sprite.Sprite):#繼承內建的sprite類別
    def __init__(self):#這個初始函式需要image和rect兩種屬性
        #image顯示,rect定位
        pygame.sprite.Sprite.__init__(self)#呼叫sprite內建初始函式
        self.image_ori=random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image=self.image_ori.copy()
        self.rect=self.image.get_rect()#定位(框起來)
        self.redius=self.rect.width*0.85/2
        #pygame.draw.circle(self.image,RED,self.rect.center,self.redius)
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)#x座標
        self.rect.y=random.randrange(-180,-100)#y座標
        self.speedy=random.randrange(10,15)#落下速度
        self.speedx=random.randrange(-6,6)#水平速度
        self.total_degree=0
        self.rot_degree=random.randrange(-3,3)

    def rotate(self):
        self.total_degree+=self.rot_degree
        self.total_degree=self.total_degree%360
        self.image=pygame.transform.rotate(self.image_ori,self.total_degree)
        center=self.rect.center
        self.rect=self.image.get_rect()
        self.rect.center=center

    def update(self):
        self.rotate()
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top>HEIGHT or self.rect.left>WIDTH or self.rect.right<0:#越界重製位置
            self.rect.x=random.randrange(0,WIDTH-self.rect.width)#x座標
            self.rect.y=random.randrange(-100,-40)#y座標
            self.speedy=random.randrange(10,15)#落下速度
            self.speedx=random.randrange(-6,6)#水平速度

#子彈
class Bullet(pygame.sprite.Sprite):#繼承內建的sprite類別
    def __init__(self,x,y):#這個初始函式需要image和rect兩種屬性
        #image顯示,rect定位
        pygame.sprite.Sprite.__init__(self)#呼叫sprite內建初始函式
        self.image=bullet_img
        self.image.set_colorkey(RED)
        self.rect=self.image.get_rect()#定位(框起來)
        self.rect.centerx=x#x座標
        self.rect.bottom=y#y座標
        self.speedy=-10
    
    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom<0:#移除子彈
            self.kill()

#爆炸
class Explosion(pygame.sprite.Sprite):#繼承內建的sprite類別
    def __init__(self,center,size):#這個初始函式需要image和rect兩種屬性
        #image顯示,rect定位
        pygame.sprite.Sprite.__init__(self)#呼叫sprite內建初始函式
        self.size=size
        self.image=expl_anim[self.size][0]
        self.rect=self.image.get_rect()#定位(框起來)
        self.rect.center=center
        self.frame=0
        self.last_update=pygame.time.get_ticks()
        self.frame_rate=50#動畫速度
    
    def update(self):
        now=pygame.time.get_ticks()
        if now-self.last_update>self.frame_rate:
            self.last_update=now
            self.frame+=1
            if self.frame==len(expl_anim[self.size]):
                self.kill()
            else:
                self.image=expl_anim[self.size][self.frame]
                center=self.rect.center
                self.rect=self.image.get_rect()
                self.rect.center=center

#寶物
class Power(pygame.sprite.Sprite):#繼承內建的sprite類別
    def __init__(self,center):#這個初始函式需要image和rect兩種屬性
        #image顯示,rect定位
        pygame.sprite.Sprite.__init__(self)#呼叫sprite內建初始函式
        self.type=random.choice(['shield','gun'])
        self.image=power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()#定位(框起來)
        self.rect.center=center
        self.speedy=3
    
    def update(self):
        self.rect.y+=self.speedy
        if self.rect.top>HEIGHT:
            self.kill()

pygame.mixer.music.play(-1)

#遊戲迴圈
show_init=True#顯示初始畫面
running=True
while running:
    if show_init:
        pygame.mixer.music.play(-1)
        close=draw_init()
        if close:
            break
        show_init=False
        all_sprites=pygame.sprite.Group()#創建一個sprite群組
        rocks=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        powers=pygame.sprite.Group()
        player=Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score=0
    clock.tick(FPS)#一秒鐘內最多被執行幾次
    #取得輸入
    # #event.get()回傳現在發生的事件(list，因為同時可能多種事件)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:#如果事件包含關閉視窗則關閉視窗
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:#按下空白鍵射擊
                player.shoot()
    #更新遊戲
    all_sprites.update()#更新sprites裡物件的update函式

    #判斷石頭子彈相撞
    hits=pygame.sprite.groupcollide(rocks,bullets,True,True)#後面的bool是判斷碰到要不要消失
    for hit in hits:#補回被刪的石頭
        expl0_sound.play()
        score+=1
        expl=Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        if random.random()>0.95:#掉寶機率
            pow=Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()
    
    #判斷石頭飛船碰撞
    hits=pygame.sprite.spritecollide(player,rocks,True,pygame.sprite.collide_circle_ratio(0.7))#後面的bool是判斷石頭要不要消失
    for hit in hits:
        new_rock()
        player.health-=hit.radius
        expl=Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        if player.health<=0:
            death_expl=Explosion(player.rect.center,'player')
            all_sprites.add(death_expl)
            if player.lives>1:
                die_sound.play()
            player.lives-=1
            player.health=100
            player.hide()
        else:
            expl1_sound.play()
        if player.lives<1:
            player.health=0

    #判斷寶物飛船碰撞
    hits=pygame.sprite.spritecollide(player,powers,True)
    for hit in hits:
        if hit.type=='shield':
            player.health+=20
            if player.health>100:
                player.health=100
            shield_sound.play()
        elif hit.type=='gun':
            player.gunup()
            gun_sound.play()

    if player.lives==0 and not(death_expl.alive()):
        pygame.mixer.music.stop()
        cl=draw_dinit(score)
        if cl:
            break
        show_init=True

    #畫面顯示
    screen.fill((BLACK))#視窗顏色(顏色,顏色,顏色)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)#畫出sprites到screen
    draw_text(screen,str(score),18,WIDTH/2,10)
    draw_health(screen,player.health,5,14)
    draw_lives(screen,player.lives-1,player_mini_img,WIDTH-100,15)
    pygame.display.update()#更新畫面

pygame.quit()