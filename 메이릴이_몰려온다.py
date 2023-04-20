import pygame, random, os

class Game:
    run = True
    re_run = False
    alt = False
    HP = 5
    Kill = 0
    size = (1200, 700)
    nari_size = (100, 100)
    mayreel_size = (100, 100)

class Image:
    path = os.path.dirname(__file__)
    # 배경, 캐릭터 이미지
    nari = pygame.image.load(os.path.join(path, "resoure", "images", "fox_mouse_nari.png"))
    mayreel = pygame.image.load(os.path.join(path, "resoure", "images", "bari_mayreel.png"))
    # 공격 이펙트
    yellow_ball = pygame.image.load(os.path.join(path, "resoure", "images", "fx_eighttail_fox_wisp_ball_yellow.png"))
    yellow_glow = pygame.image.load(os.path.join(path, "resoure", "images", "fx_eighttail_fox_wisp_glow_yellow.png"))
    blue_ball = pygame.image.load(os.path.join(path, "resoure", "images", "fx_eighttail_fox_wisp_ball_blue.png"))
    blue_glow = pygame.image.load(os.path.join(path, "resoure", "images", "fx_eighttail_fox_wisp_glow_blue.png"))
    pink_ball = pygame.image.load(os.path.join(path, "resoure", "images", "fx_eighttail_fox_wisp_ball_pink.png"))
    pink_glow = pygame.image.load(os.path.join(path, "resoure", "images", "fx_eighttail_fox_wisp_glow_pink.png"))
    # 아이템 및 기타
    nari_weapon = pygame.image.load(os.path.join(path, "resoure", "images", "cwp_eighttail.png"))
    attack_up = pygame.image.load(os.path.join(path, "resoure", "images", "cwp_knight.png"))
    laser_len_up = pygame.image.load(os.path.join(path, "resoure", "images", "cwp_futureknight_item.png"))
    HP = pygame.image.load(os.path.join(path, "resoure", "images", "hp_potion.png"))

class Music:
    def __init__(self):
        pygame.mixer.init()
        self.path = os.path.dirname(__file__)
        self.bgm = pygame.mixer.Sound(os.path.join(self.path, "resoure", "music", "rana-tema-guardian-tales-bgm.mp3"))
        self.bgm.set_volume(0.4)
        self.attack = pygame.mixer.Sound(os.path.join(self.path, "resoure", "music", "att_hit.mp3"))
        self.attack.set_volume(0.7)
        self.this_why = pygame.mixer.Sound(os.path.join(self.path, "resoure", "music", "this_why.mp3"))
        self.this_why.set_volume(0.6)
        self.run = pygame.mixer.Sound(os.path.join(self.path, "resoure", "music", "run.mp3"))
        self.run.set_volume(0.7)
    def bgm_play(self):
        self.bgm.play(-1)
    def bgm_stop(self):
        self.bgm.stop()
    def attact_play(self):
        self.attack.play(maxtime=300)
        self.attack.fadeout(300)
    def this_why_play(self):
        self.this_why.play(maxtime=4200)
    def this_why_stop(self):
        self.this_why.stop()
    def run_play(self):
        self.run.play(maxtime=300)

class TtatGee:
    global keyboard_group
    keyboard_group = set()
    def __init__(self, position):
        image = Image.nari.convert_alpha()
        image = pygame.transform.scale(image, Game.nari_size)
        self.image = image
        self.image_right = self.image
        self.image_left = pygame.transform.flip(self.image, True, False)
        self.img_width, self.img_height = self.image.get_size()
        self.x, self.y = position

        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y

        # 게임 변수
        self.attack = 1
        self.laser_len = 3
        self.speed = 0

    def dic(self):
        result = {
            "x": self.x,
            "y": self.y,
            "img_size": (self.img_width, self.img_height),
            "laser_len": self.laser_len,
            "attack": self.attack
        }
        return result
    def item_eat(self, item_dic):
        for option, value in item_dic.items():
            if option == "HP":
                Game.HP += value
            if option == "attack":
                self.attack += value
            if option == "laser_len":
                self.laser_len += value

    def move(self, FPS):
        if "A" in keyboard_group:
            self.speed -= 0.045 * FPS
            self.image = self.image_left
        if "D" in keyboard_group:
            self.speed += 0.045 * FPS
            self.image = self.image_right
        # 속도 제어
        if -0.3 < self.speed < 0.3:
            self.speed = 0
        elif 0 < self.speed:
            self.speed -= 0.025 * FPS
        elif self.speed < 0:
            self.speed += 0.025 * FPS
        # 벽에 부딪히면 튕기기
        if self.x <= 0 or Game.size[0] <= (self.x + self.img_width):
            self.speed *= -1

        self.x += self.speed
        # 창 못지나가도록
        self.x = max(0, min(self.x, Game.size[0] - self.img_width))
        # self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
    
    def update(self, screen, FPS):
        self.move(FPS)
        screen.blit(self.image, (self.x,self.y))

class Alpaca:
    li = []
    del_list =[]
    def __init__(self, floor_height, is_active=False, position=None):
        self.image = Image.mayreel.convert_alpha()
        self.image = pygame.transform.scale(self.image, Game.mayreel_size)
        self.make(floor_height, position)

        if is_active is True:
            self.li.append(self)
        elif is_active is False:
            self.del_list.append(self)
    
    def make(self, floor_height, position=None):
        self.img_show = self.image
        self.img_width, self.img_height = self.image.get_size()
        self.floor_height = floor_height
        self.x, self.y = (random.randint(0, Game.size[0] - Game.mayreel_size[0]), 0-self.img_height) if position == None else position

        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y

        # 게임 변수
        self.HP = 1 + (Game.Kill//10)
        self.x_speed = random.choice([0, 0,  0.03, 0.05, 0.07])
        if random.choice([0, 1]) and self.x_speed != 0:
            self.x_speed *= -1
            self.img_show = pygame.transform.flip(self.image.copy(), True, False)
        self.y_speed = random.choice([0.025, 0.034, 0.05, 0.065, 0.075]) + (Game.Kill/1000)

    def active(self, is_bool:bool, position=None):
        if is_bool is True:

            self.make(self.floor_height, position)

            i = self.del_list.index(self)
            o = self.del_list.pop(i)
            self.li.append(o)

            # del_list 에 항상 1개 넣어두기
            if len(self.del_list) == 0:
                Alpaca(self.floor_height)

        elif is_bool is False:
            self.x, self.y = Game.size

            i = self.li.index(self)
            o = self.li.pop(i)
            self.del_list.append(o)

    def move(self, FPS):
        self.x += self.x_speed * FPS
        self.y += self.y_speed * FPS
        if Game.size[1] - self.floor_height < self.y + (self.img_height/2):
            self.y = 0 - self.img_height
            if self.x_speed == 0:
                self.x = random.randint(0, Game.size[0] - self.img_width)
        if Game.size[0] < self.x :
            self.x = 0 - self.img_width
        elif self.x + self.img_width < 0:
            self.x = Game.size[0]

        self.rect.left = self.x
        self.rect.top = self.y
    
    def hit(self, attact, laser_att=False):
        self.HP -= attact
        if self.HP <= 0:
            dic = self.dic()
            self.make(self.floor_height)
            if laser_att:
                Game.Kill += 1
                if random.randint(1, 10) <= 2:
                    self.item_drop(dic)
        
    def item_drop(self, dic):
        Item.del_list[0].active(True, dic)
    
    def dic(self):
        result = {
            "x": self.x,
            "y": self.y,
            "img_size": (self.img_width, self.img_height),
        }
        return result

    def update(self, screen, FPS):
        self.move(FPS)

        screen.blit(self.img_show, (self.x,self.y))

    # 게임 시작 전 보여주기 용 쇼 함수, 이후 안쓰임
    def show(self, screen, FPS):
        if Game.size[1] < self.y:
            self.y += -Game.size[1] - self.img_height
        if Game.size[0] < self.x :
            self.x += -Game.size[0] - self.img_width
        self.x += 0.08 * FPS
        self.y += 0.08 * FPS
        screen.blit(self.image, (self.x,self.y))

class Laser:
    li = []
    del_list =[]
    def __init__(self, dic=None):
        if dic == None:
            self.del_list.append(self)
        else:
            self.make(self, dic)
            self.li.append(self)

    def make(self, dic):
        if 1 == dic["attack"]:
            self.image = Image.yellow_ball.convert_alpha()
            self.effect = Image.yellow_glow.convert_alpha()
        elif 2 <= dic["attack"] < 5:
            self.image = Image.blue_ball.convert_alpha()
            self.effect = Image.blue_glow.convert_alpha()
        elif 5 <= dic["attack"]:
            self.image = Image.pink_ball.convert_alpha()
            self.effect = Image.pink_glow.convert_alpha()

        self.rect = self.image.get_rect()
        self.img_width, self.img_height = self.image.get_size()

        self.x = dic["x"] + (dic["img_size"][0] / 2) - (self.img_width / 2)
        self.y = dic["y"] + (dic["img_size"][1] / 2) - (self.img_height / 2)

        self.rect.left = self.x
        self.rect.top = self.y
        # 이펙트 이미지
        self.eff_img_width, self.eff_img_height = self.effect.get_size()

        self.eff_x = dic["x"] + (dic["img_size"][0] / 2) - (self.eff_img_width / 2)
        self.eff_y = dic["y"] + (dic["img_size"][1] / 2) - (self.eff_img_height / 2)

        # 게임 변수
        self.attack = dic["attack"]
        self.rotat = 0

        if len(self.del_list) == 0:
            Laser()

    def active(self, is_bool:bool, dic=None):
        if is_bool is True:

            self.make(dic)

            i = self.del_list.index(self)
            o = self.del_list.pop(i)
            self.li.append(o)

            # del_list 에 항상 1개 넣어두기
            if len(self.del_list) == 0:
                Laser()

        elif is_bool is False:
            self.x, self.y = Game.size

            i = self.li.index(self)
            o = self.li.pop(i)
            self.del_list.append(o)

    def move(self, FPS):
        self.y -= 0.2 * FPS
        self.eff_y -= 0.2 * FPS
        if self.y < 0:
            self.active(False)

        self.rect.left = self.x
        self.rect.top = self.y
    
    def hit_attack(self):
        return self.attack
    
    def img_rotation(self):
        self.rotat += 4
        self.r_image = pygame.transform.rotate(self.image, self.rotat)
        self.img_width, self.img_height = self.image.get_size()

    def update(self, screen, FPS):
        self.move(FPS)
        self.img_rotation()
        screen.blit(self.effect, (self.eff_x,self.eff_y))
        # screen.blit(self.r_image, (self.x-(self.img_width/2),self.y-(self.img_height/2)))
        screen.blit(self.r_image, (self.x,self.y))

class Item:
    li = []
    del_list =[]
    def __init__(self, floor_height):
        self.floor_height = floor_height

        Item.del_list.append(self)

    def make(self, dic):
        rolling = random.randint(1, 10)
        if rolling == 1:
            self.image = Image.nari_weapon.convert_alpha()
            self.item_option = {"attack": 2, "laser_len":2}
        elif rolling <= 3: # att up [2, 3]
            self.image = Image.attack_up.convert_alpha()
            self.item_option = {"attack": 1}
        elif rolling <= 5: # att_len up [4, 5]
            self.image = Image.laser_len_up.convert_alpha()
            self.item_option = {"laser_len": 1}
        else: # HP up [6, 7, 8, 9, 10]
            self.image = Image.HP.convert_alpha()
            self.item_option = {"HP": 1}
        self.img_width, self.img_height = self.image.get_size()
        self.x = dic["x"] + (dic["img_size"][0] / 2) - (self.img_width / 2)
        self.y = dic["y"] + (dic["img_size"][1] / 2) - (self.img_height / 2)

        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y

    def active(self, is_bool:bool, dic=None):
        if is_bool is True:

            self.make(dic)

            i = self.del_list.index(self)
            o = self.del_list.pop(i)
            self.li.append(o)

            # del_list 에 항상 1개 넣어두기
            if len(self.del_list) == 0:
                Item(self.floor_height)

        elif is_bool is False:
            self.x, self.y = Game.size

            i = self.li.index(self)
            o = self.li.pop(i)
            self.del_list.append(o)
    
    def move(self, FPS):
        self.y += 0.4 * FPS
        if Game.size[1] - self.floor_height - self.img_height < self.y:
            self.y = Game.size[1] - self.floor_height - self.img_height

        self.rect.left = self.x
        self.rect.top = self.y

    def dic(self):
        return self.item_option

    def update(self, screen, FPS):
        self.move(FPS)

        screen.blit(self.image, (self.x,self.y))

def start_wait(win, clock, floor):
    wait_run = True
    zizzaz = True
    for y in range((Game.size[1]//100)+1):
        for x in range((Game.size[0]//100)+1):
            if zizzaz:
                Alpaca(floor.height, is_active=True, position=(x*100, y*100))
            else:
                Alpaca(floor.height, is_active=True, position=(x*100 + 50, y*100))
        zizzaz = not zizzaz
    while wait_run:
        FPS = clock.tick(60)
        # 창 끄거나 스페이스바 눌러 다시 시작
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.run = False
                Game.re_run = False
                wait_run = False
            if event.type == pygame.KEYDOWN: # 키보드 누를 때
                wait_run = False
        
        win.fill((255,200,108))
        for may in Alpaca.li:
            may.show(win, FPS)

        pygame.display.update()
    
    for idx in range(len(Alpaca.li))[::-1]:
        Alpaca.li[idx].active(False)

def game_over(win, big_font, small_font, music, player):
    # 창 끄거나 스페이스바 눌러 다시 시작
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.run = False
            Game.re_run = False
        if event.type == pygame.KEYDOWN: # 키보드 누를 때
            if event.key == pygame.K_r:
                Game.run = True
                Game.re_run = False
                reset(music, player) # 다시 시작
        if event.type == pygame.KEYUP: # 키보드 뗼 때
            if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and "A" in keyboard_group:
                keyboard_group.remove("A")
            elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and "D" in keyboard_group:
                keyboard_group.remove("D")
 
    black = (0,0,0)
    win.blit(big_font.render("게임 오버", True, black), (Game.size[0]*0.4, Game.size[1]*0.4))
    win.blit(small_font.render("다시 시작은 r 버튼을 부르세요", True, black), (Game.size[0]*0.4, Game.size[1]*0.55))

def reset(music, player):
    Game.re_run = False
    Game.alt = False
    Game.HP = 5
    Game.Kill = 0
    player.attack = 1
    player.laser_len = 3
    player.speed = 0
    music.this_why_stop()
    music.bgm_play()

    for i in range(len(Alpaca.li))[::-1]:
        Alpaca.li[i].active(False)
    for i in range(len(Laser.li))[::-1]:
        Laser.li[i].active(False)
    # for i in range(len(Item.li))[::-1]:
    #     Item.li[i].active(False)

def event(dic, music):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.run = False
        if event.type == pygame.KEYDOWN: # 키보드 누를 때
            if event.key == pygame.K_a or event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                keyboard_group.add("A")
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: # 캐릭터를 오른쪽으로
                keyboard_group.add("D")
            elif event.key == pygame.K_SPACE and len(Laser.li) < dic["laser_len"]:
                music.attact_play()
                Laser.del_list[0].active(True, dic)
            elif event.key == pygame.K_LALT:
                Game.alt = not Game.alt
        if event.type == pygame.KEYUP: # 키보드 뗼 때
            if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and "A" in keyboard_group:
                keyboard_group.remove("A")
            elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and "D" in keyboard_group:
                keyboard_group.remove("D")

def text_render(win, small_font, clock, timer, player):
    black = (0,0,0)
    win.blit(small_font.render(f"fps:{clock.get_fps():.2f}", True, black), (Game.size[0]*0.92, Game.size[1]*0.95))

    win.blit(small_font.render(f"시간 : {timer/1000:.2f}", True, black), (Game.size[0]*0.9, Game.size[1]*0.03))
    win.blit(small_font.render(f"메이릴 : {len(Alpaca.li)}", True, black), (0, 0))
    win.blit(small_font.render(f"kill : {Game.Kill}", True, black), (0, Game.size[1]*0.04))

    # HP 그림으로 표시
    x = Game.size[0]*0.01
    y = Game.size[1]*0.93
    for i in range(Game.HP):
        win.blit(Image.HP, (x, y))
        x += Game.size[0]*0.04

def info_render(win, small_font, player=None, mayreel=None):
    if Game.alt is False: # 알트키 비활성화 시 조기리턴
        return
    black = (0,0,0)
    mark = ["HP", "att", "num"]
    if player != None:
        # 플레이어 정보
        info = [Game.HP, player.attack, player.laser_len]
        x, y = (player.x + player.img_width, player.y)
        for i in range(len(info)):
            win.blit(small_font.render(f"{mark[i]}: {info[i]}", True, black), (x, y))
            y += Game.size[1]*0.03
    else:
        # 메이릴 정보
        info = [mayreel.HP]
        x, y = (mayreel.x + mayreel.img_width, mayreel.y)
        for i in range(len(info)):
            win.blit(small_font.render(f"{mark[i]}: {info[i]}", True, black), (x, y))
            y += Game.size[1]*0.03

def main():
    # 기본 작업
    pygame.init()
    win = pygame.display.set_mode(Game.size)
    pygame.display.set_caption("메이릴이 몰려온다")
    pygame.display.set_icon(Image.nari)

    # 기본 변수
    clock = pygame.time.Clock()
    timer = 0
    big_font = pygame.font.Font(os.path.join(Image.path, "resoure", "MaruBuriTTF", "MaruBuri-Regular.ttf"), 50)
    small_font = pygame.font.Font(os.path.join(Image.path, "resoure", "MaruBuriTTF", "MaruBuri-Regular.ttf"), 20)
    floor = pygame.Rect(0, Game.size[1] - (Game.size[1]/10), Game.size[0], Game.size[1]/10)
    music = Music()
    player = TtatGee((100, Game.size[1] - floor.height - Game.nari_size[1]))
    Item(floor.height)
    Alpaca(floor.height)
    Laser()

    start_wait(win, clock, floor) # 게임 시작 전 대기 장면

    music.bgm_play()

    while Game.run:
        FPS = clock.tick(60)
        timer += FPS 
        win.fill((255,200,108))

        event(player.dic(), music) # 키 이벤트외 이것저것

        #메이릴 만들기
        if len(Alpaca.li) < max(5, 5 + (Game.Kill//5)):
            Alpaca.del_list[0].active(True)
        # 아이템 리스트 업데이트
        for i_idx in range(len(Item.li))[::-1]:
            item = Item.li[i_idx]
            item.update(win, FPS)
            # 플레이어 - 아이템 충돌
            if pygame.sprite.collide_mask(player, item):
                player.item_eat(item.dic())
                item.active(False)
        is_laser_update = True
        # 메이릴 리스트 업데이트
        for m_idx in range(len(Alpaca.li))[::-1]:
            mayreel = Alpaca.li[m_idx]
            mayreel.update(win, FPS)
            info_render(win, small_font, mayreel=mayreel)
            # 메이릴 - 플레이어 충돌
            if pygame.sprite.collide_mask(mayreel, player):
                mayreel.make(floor.height)
                Game.HP -= 1
                continue
            # 메이릴 - 레이저 충돌
            for l_idx in range(len(Laser.li))[::-1]:
                laser = Laser.li[l_idx]
                if is_laser_update is True:
                    laser.update(win, FPS)
                if pygame.sprite.collide_mask(mayreel, laser):
                    mayreel.hit(laser.hit_attack(), laser_att=True)
                    laser.active(False)
            is_laser_update = False

        pygame.draw.rect(win, (9,174,25), floor)
        player.update(win, FPS)
        info_render(win, small_font, player=player)

        # 텍스트 및 기타 표시
        text_render(win, small_font, clock, timer, player)

        # 게임 종료
        if Game.HP <= 0:
            music.bgm_stop()
            music.this_why_play()
            Game.re_run = True
        while Game.re_run:
            clock.tick(60)
            game_over(win, big_font, small_font, music, player)
            timer = 0
            pygame.display.update()
        pygame.display.update()
    pygame.QUIT

if __name__ == "__main__":
    main()