import pygame

import math
from random import randint
pygame.font.init()

WIDTH, HEIGHT = 750, 750
MINTILEWIDTH, MINTILEHEIGHT = 10, 10
TILEWIDTH, TILEHEIGHT = WIDTH/20, HEIGHT/20

PRES = 100

COLWIDTH = WIDTH/PRES

global vis

global chars



FOV = 3.14159/4
PFOV = 1.5078

max_depth = 20

WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption('PyTrace')


class Map:
    def __init__(self):
        self.map = [[1,1,1,1,1,1,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,1,1,1,1,1,1,1,1,1]]
        self.fs = True
        self.mode = 2

    def reset(self):
        self.map = [[1,1,1,1,1,1,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1],
                    [1,1,1,1,1,1,1,1,1,1]]

    def toggle(self):
        if self.mode == 5:
            self.mode = 0
            return
        self.mode = self.mode + 1
        return

    def get_mode(self):
        return self.mode


    def get_map(self):
        return self.map

    def set_fs(self):
        self.fs = False

    def get_fs(self):
        return self.fs


    def get_tile_val(self,x,y):
        return self.map[x][y]

    def place(self, x, y):
        tx, ty = int(x),int(y)
        self.map[tx][ty] = self.mode

    def draw_map(self,p):
        if self.fs:
            self.draw_max(p)
        else:
            self.draw_min(p)

    def clear(self):
        WIN.fill((0,0,0))

    def draw_min(self,p):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.get_tile_val(i, j) == 0:
                    pygame.draw.rect(WIN,(0,0,0),((i)*MINTILEWIDTH,(j)*MINTILEHEIGHT,MINTILEWIDTH,MINTILEHEIGHT))
                elif self.get_tile_val(i,j) == 1:
                    pygame.draw.rect(WIN, (255,255,255),((i) * MINTILEWIDTH, (j) * MINTILEHEIGHT, MINTILEWIDTH, MINTILEHEIGHT))
                elif self.get_tile_val(i,j) == 2:
                    pygame.draw.rect(WIN, (0,255,0),((i) * MINTILEWIDTH, (j) * MINTILEHEIGHT, MINTILEWIDTH, MINTILEHEIGHT))
                elif self.get_tile_val(i,j) == 3:
                    pygame.draw.rect(WIN, (255,0,0),((i) * MINTILEWIDTH, (j) * MINTILEHEIGHT, MINTILEWIDTH, MINTILEHEIGHT))
                elif self.get_tile_val(i,j) == 4:
                    pygame.draw.rect(WIN, (0,0,255),((i) * MINTILEWIDTH, (j) * MINTILEHEIGHT, MINTILEWIDTH, MINTILEHEIGHT))
                elif self.get_tile_val(i,j) == 5:
                    pygame.draw.rect(WIN, (70,50,120),((i) * MINTILEWIDTH, (j) * MINTILEHEIGHT, MINTILEWIDTH, MINTILEHEIGHT))
        pygame.draw.rect(WIN, (255,0,0),((p.get_x()) * MINTILEWIDTH, (p.get_y()) * MINTILEHEIGHT, MINTILEWIDTH, MINTILEHEIGHT))


    def draw_max(self,p):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.get_tile_val(i,j) == 0:
                    pygame.draw.rect(WIN,(0,0,0),(i*TILEWIDTH,j*TILEHEIGHT,TILEWIDTH,TILEHEIGHT))
                elif self.get_tile_val(i,j) == 1:
                    pygame.draw.rect(WIN,(255,255,255),(i*TILEWIDTH,j*TILEHEIGHT,TILEWIDTH,TILEHEIGHT))
                elif self.get_tile_val(i,j) == 2:
                    pygame.draw.rect(WIN,(0,255,0),(i*TILEWIDTH,j*TILEHEIGHT,TILEWIDTH,TILEHEIGHT))
                elif self.get_tile_val(i,j) == 3:
                    pygame.draw.rect(WIN,(255,0,0),(i*TILEWIDTH,j*TILEHEIGHT,TILEWIDTH,TILEHEIGHT))
                elif self.get_tile_val(i,j) == 4:
                    pygame.draw.rect(WIN,(0,0,255),(i*TILEWIDTH,j*TILEHEIGHT,TILEWIDTH,TILEHEIGHT))
                elif self.get_tile_val(i,j) == 5:
                    pygame.draw.rect(WIN,(70,50,120),(i*TILEWIDTH,j*TILEHEIGHT,TILEWIDTH,TILEHEIGHT))
        pygame.draw.rect(WIN, (255, 0, 0), ((p.get_x()) * TILEWIDTH, (p.get_y()) * TILEHEIGHT, TILEWIDTH, TILEHEIGHT))


class Screen:
    def __init__(self): pass

    def calculate(self,p,m):
        rays = []
        temp = -1
        for i in range(0,WIDTH):
            ray_angle = (p.get_angle() - float(FOV)/2.0) + (((i*1.0)/float(WIDTH)) * float(FOV))

            #print(ray_angle)


            dist = 0.0
            hit_wall = False

            eyeX = math.sin(ray_angle)
            eyeY = math.cos(ray_angle)

            while not hit_wall and dist < max_depth:
                val = 0
                dist = float(dist) + vis
                tempx = (p.get_x() + eyeX * dist)
                tempy = (p.get_y() + eyeY * dist)
                #print(str(tempx) + " " + str(tempy))
                if tempx < 0 or tempx >= max_depth or tempy < 0 or tempy >= max_depth:
                    hit_wall = True
                    dist = 20

                elif m.get_tile_val(int(tempx),int(tempy)) == 1:
                        #dist = math.sqrt((tempx-p.get_x())**2+(tempy-p.get_y())**2)
                        hit_wall = True
                        val = 1
                elif m.get_tile_val(int(tempx),int(tempy)) == 2:
                        #dist = math.sqrt((tempx-p.get_x())**2+(tempy-p.get_y())**2)
                        hit_wall = True
                        val = 2
                elif m.get_tile_val(int(tempx),int(tempy)) == 3:
                        #dist = math.sqrt((tempx-p.get_x())**2+(tempy-p.get_y())**2)
                        hit_wall = True
                        val = 3
                elif m.get_tile_val(int(tempx),int(tempy)) == 4:
                        #dist = math.sqrt((tempx-p.get_x())**2+(tempy-p.get_y())**2)
                        hit_wall = True
                        val = 4


            start = float(HEIGHT)/2 - (float(HEIGHT) / float(dist))
            end = float(HEIGHT)/2 + (float(HEIGHT)/float(dist))
            print(str(start))
            print(str(end))

            #pygame.draw.line(WIN,(255,0,0),(p.get_x()*TILEWIDTH,p.get_y()*TILEHEIGHT),(tempx*TILEWIDTH,tempy*TILEHEIGHT),1)

            #if i == 0 or i == WIDTH-1:
             #   pygame.draw.line(WIN, (0, 255, 0), (p.get_x() * TILEWIDTH, p.get_y() * TILEHEIGHT), (tempx * TILEWIDTH, tempy * TILEHEIGHT),5)
            hue = 255 * dist / max_depth
            color1,color2,color3 = 0,0,0
            #print(color1)
            #print(color2)
            #print(color3)
            #print(val)

            if val == 1:
                color1 = 255-hue
                color2 = 255-hue
                color3 = 255-hue
            elif val == 2:
                color1 = 0
                color2 = 255-hue
                color3 = 0
            elif val == 3:
                color1 = 255-hue
                color2 = 0
                color3 = 0
            elif val == 4:
                color1 = 0
                color2 = 0
                color3 = 255-hue



            #pygame.draw.line(WIN,(255,0,0),(p.get_x()*MINTILEWIDTH,p.get_y()*MINTILEHEIGHT),(tempx*MINTILEWIDTH,tempy*MINTILEHEIGHT),1)

            pygame.draw.line(WIN,(color1,color2,color3),(i,start),(i,end),1)

            rays.append((p.get_x(),p.get_y(),tempx,tempy))


        return rays










class Player:
    def __init__(self,x,y,a):
        self.x = x
        self.y = y
        self.a = a

    def get_angle(self):
        return self.a

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def lt(self,t):
        self.a = self.a - t

    def rt(self,t):
        self.a = self.a + t

    def fw(self,t,m):

        v1 = math.cos(self.a)
        v2 = math.sin(self.a)
        if m.get_tile_val(int(self.x + v2*t),int(self.y + v1*t)) == 0:
            self.x = self.x + v2*t
            self.y = self.y + v1*t









def main():
    run = True
    FPS = 1000
    clock = pygame.time.Clock()

    m = Map()

    global vis
    vis = 1

    s = Screen()

    p = Player(2, 2, 0)
    m.draw_max(p)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ld = m.get_map()
                st = ""
                st = st + "["
                for i in range(len(ld)):
                    st = st + "["
                    for j in range(len(ld[i])):
                        st = st + str(ld[i][j]) + ", "
                    st = st + "], \n"
                st = st + "]"
                f = open("map_cache.txt","w")
                f.write(st)
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    m.clear()
                    m.set_fs()
                    m.draw_min(p)
                if event.key == pygame.K_LSHIFT:
                    m.toggle()
                if event.key == pygame.K_1:
                    vis = 1
                if event.key == pygame.K_2:
                    vis = .1
                if event.key == pygame.K_3:
                    vis = .01
                if event.key == pygame.K_4:
                    vis = .001
                if event.key == pygame.K_r:
                    m.reset()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and m.get_fs():
                mx, my = pygame.mouse.get_pos()
                m.place(mx/TILEWIDTH,my/TILEHEIGHT)

        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            p.lt(.1)
        if key[pygame.K_d]:
            p.rt(.1)
        if key[pygame.K_w]:
            p.fw(.1,m)
        if key[pygame.K_s]:
            p.fw(-.1,m)

        m.clear()
        rays = []
        if not m.get_fs():
            rays = s.calculate(p,m)


        m.draw_map(p)

        for i in rays:
            pygame.draw.line(WIN,(255,255,255),((i[0]*MINTILEHEIGHT)+MINTILEHEIGHT/2,(i[1]*MINTILEWIDTH)+MINTILEHEIGHT/2),(i[2]*MINTILEHEIGHT,i[3]*MINTILEWIDTH),1)


        pygame.display.update()






main()
