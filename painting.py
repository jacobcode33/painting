import pygame as pg
from pygame.locals import *
import time, math, random
from PIL import Image

pg.init() #start the game
screenxy=(800,538)#screen setup
screen = pg.display.set_mode(screenxy)
pg.display.set_caption("prototype")
white = [255,255,255]
grey1 = [100,100,100]
grey2 = [20,20,20]
black = [0,0,0]
green = [30,200,30]
def setup(width,col):
    screen.fill(grey1)
    pg.draw.rect(screen, grey2, (538,13,262,262))
    for x in range(13):
        for y in range(8):
            changecol(0,x,y)
    changecol(2,col[0],col[1]) # the highlighted started one

    pg.draw.rect(screen,white,(542,177,124,50)) #clear button
    font = pg.font.SysFont(None, 24)
    img = font.render('fill', True, black)
    screen.blit(img, (590,194))

    pg.draw.rect(screen,white,(671,177,124,50)) #save button
    font = pg.font.SysFont(None, 24)
    img = font.render('save', True, black)
    screen.blit(img, (717,194))

    for x in range(width):
        for y in range(width):
            changecol2(0,x,y,getcol(col[0],col[1]),width)

    pic = []
    for y in range(width):
        row = []
        for x in range(width):
            row.append((col[0],col[1]))
        pic.append(row)
    return pic

def getcol(x,y):
    def restrain(c):
        if c > 255:
            c = 255
        elif c < 0:
            c = 0
        return c
    if x == 12:
        r,g,b = 128,128,128
    elif 0<=x<=12:
        if x > 6:
            r = round((4-abs(12-x))*0.5*255)
        else:
            r = round((4-abs(0-x))*0.5*255)
        g = round((4-abs(4-x))*0.5*255)
        b = round((4-abs(8-x))*0.5*255)
        
        r=restrain(r)
        g=restrain(g)
        b=restrain(b)

    r+=51*(y-4)
    g+=51*(y-4)
    b+=51*(y-4)

    r=restrain(r)
    g=restrain(g)
    b=restrain(b)
    return [r,g,b]

def changecol2(size, x,y,col,w):
    w = round(512/w)
    if size == 0:
        pg.draw.rect(screen, col, ((13+x*w),(13+y*w),(w),(w)))
    elif size == 1:
        pg.draw.rect(screen, black, ((13+x*w),(13+y*w),(w),(w)))
        pg.draw.rect(screen, col, ((14+x*w),(14+y*w),(w-2),(w-2)))
        

def changecol(size, x,y):
    col = getcol(x,y)
    if size == 1:
        pg.draw.rect(screen, col, ((539+x*20),(14+y*20),(20),(20)))
    elif size == 0:
        pg.draw.rect(screen, grey2, ((538+x*20),(13+y*20),(22),(22)))
        pg.draw.rect(screen, col, ((540+x*20),(15+y*20),(18),(18)))
    elif size == 2:
        pg.draw.rect(screen, white, ((538+x*20),(13+y*20),(22),(22)))
        pg.draw.rect(screen, col, ((540+x*20),(15+y*20),(18),(18)))

def fix(pic, w):
    new = []
    for y in range(w):
        for x in range(w):
            hold = (getcol(pic[x][y][0],pic[x][y][1]))
            new.append((hold[0],hold[1],hold[2]))
    return new

def mouse():
    pos = pg.mouse.get_pos()
    state = pg.mouse.get_pressed()
    return (pos,state)

width = 16
pencol = (12,7)
pic = setup(width,pencol)
run = True
last = (0,0,0) #x,y,tab
pressing = False
saved = 0
while run:
    pos,state = mouse()
    if 540<pos[0]<800 and 13<pos[1]<173: #if selecting a colour
        x = math.floor((pos[0]-540)/20)
        y = math.floor((pos[1]-13)/20)
        if x!=last[1] or y!=last[2]:
            if last[0] == 1: #if it was last over the colours
                changecol(0,last[1],last[2])
            changecol(1,x,y)
            last = (1,x,y)
            changecol(2,pencol[0],pencol[1])
        if state[0]:
            changecol(0,pencol[0],pencol[1])
            pencol = (x,y)
            changecol(2,pencol[0],pencol[1]) 

    elif last[0] == 1: #if it was last over the colours
        changecol(0,last[1],last[2])

    if 13<pos[0]<525 and 13<pos[1]<525: #if drawing
        x = math.floor((pos[0]-13)/(512/width))
        y = math.floor((pos[1]-13)/(512/width))
        if x!=last[1] or y!=last[2]:
            if last[0] == 2: #if it was last over the colours
                changecol2(0,last[1],last[2],getcol(pic[last[1]][last[2]][0],pic[last[1]][last[2]][1]),width)
            changecol2(1,x,y,getcol(pic[x][y][0],pic[x][y][1]),width) #edges
            last = (2,x,y)
        if state[0]:
            pic[x][y] = pencol
            changecol2(1,x,y,getcol(pic[x][y][0],pic[x][y][1]),width) 

    elif last[0] == 2:
        changecol2(0,last[1],last[2],getcol(pic[last[1]][last[2]][0],pic[last[1]][last[2]][1]),width)

    if 542<pos[0]<666 and 177<pos[1]<237: # if over the clear button
        if state[0]:
            pic = setup(width,pencol)

    if 671<pos[0]<795 and 177<pos[1]<237: # if over the save button
        if state[0]:
            pressing = True
        elif pressing:
            fixed = fix(pic, width)
            final = Image.new(mode='RGB', size=(width,width))
            final.putdata(fixed)
            final.save('data/final.jpg', 'JPEG', subsampling=0, quality=100)

            saved = 300
            pg.draw.rect(screen,green,(671,177,124,50)) #save button
            font = pg.font.SysFont(None, 24)
            img = font.render('save', True, black)
            screen.blit(img, (717,194))
    if not state[0]:
        pressing = False
    if saved > 0:
        saved -=1
    if saved == 1:
        saved -=1
        pg.draw.rect(screen,white,(671,177,124,50)) #save button
        font = pg.font.SysFont(None, 24)
        img = font.render('save', True, black)
        screen.blit(img, (717,194))





    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            pg.quit()