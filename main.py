import pygame
pygame.init()
screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
scsz = screen.get_size()
background = pygame.Surface(scsz)
background.fill((0, 0, 0))
background = background.convert()
cursor = pygame.cursors.compile(16*(8*" ",), black='X', white='.', xor='o')
pygame.mouse.set_cursor((8, 16), (0, 0), *cursor)


color=[(255,255,255), (255,255,255)]
x = False
q = 0


def revolve_color(colr, ref, sped):
    for f in range(sped):
        if colr[ref] == (255, 255, 255):
            colr[ref]=(255, 0, 0)
        if colr[ref][0] and colr[ref][1]==255:
            colr[ref]=(colr[ref][0]-1,255,0)
        elif colr[ref][1] and colr[ref][2]==255:
            colr[ref]=(0,colr[ref][1]-1,255)
        elif colr[ref][2] and colr[ref][0]==255:
            colr[ref]=(255,0,colr[ref][2]-1)
        elif colr[ref][0]==255:
            colr[ref]=(255,colr[ref][1]+1,0)
        elif colr[ref][1]==255:
            colr[ref]=(0,255,colr[ref][2]+1)
        elif colr[ref][2]==255:
            colr[ref]=(colr[ref][0]+1,0,255)
        else:
            colr[ref]=(255, 0, 0)

def change_color():
    global color, q
    if color[q]==(255,0,0):
        color[q]=(255,255,0)
    elif color[q]==(255,255,0):
        color[q]=(0,255,0)
    elif color[q]==(0,255,0):
        color[q]=(0,255,255)
    elif color[q]==(0,255,255):
        color[q]=(0,0,255)
    elif color[q]==(0,0,255):
        color[q]=(255,0,255)
    elif color[q]==(255,0,255):
        color[q]=(0,0,0)
    elif color[q]==(0,0,0):
        color[q]=(255,255,255)
    else:
        color[q]=(255,0,0)

def cyclein(leng, total):
    templis=[total//leng]*int(leng)
    if total!=sum(templis):
        ones=total-sum(templis)
        zeros=leng-ones
        grt=float(ones/zeros)
        addlis=[]
        while 0==0:
            if ones!=0 and (zeros==0 or float(ones/zeros)>=grt):
                addlis.append(1)
                ones-=1
            elif zeros!=0:
                addlis.append(0)
                zeros-=1
            else:
                for f in range(leng):
                    templis[f]+=addlis[f]
                break
    return templis

def mmul(vector, matrix):
    output = []
    for f in matrix:
        temp = 0
        for g in range(len(vector)):
            temp += vector[g]*f[g]
        output.append(temp)
    return output


clock = pygame.time.Clock()
mainloop = True
FPS = 30
playtime = 0.0
framecount = 0
myfont30 = pygame.font.SysFont("times new roman", 30)


class hilbert:

    def __init__(self):
        self.fract = [(scsz[0]/2-scsz[1]/4,3*scsz[1]/4),
                      (scsz[0]/2-scsz[1]/4,scsz[1]/4),
                      (scsz[0]/2+scsz[1]/4,scsz[1]/4),
                      (scsz[0]/2+scsz[1]/4,3*scsz[1]/4)]
        self.fdx = False

    def up(self):
        self.fdx=True
        templis = [[] for f in range(4)]
        if len(self.fract)<4**10:
            for f in self.fract:
                # bottom left
                point0 = (f[0]-scsz[0]/2+scsz[1]/2, f[1]-scsz[1]) # put origin at bottom left
                point0 = mmul(point0, [(0, -1/2), (-1/2, 0)]) # transform point
                templis[0].append((point0[0]+scsz[0]/2-scsz[1]/2, point0[1]+scsz[1])) # put origin back
                # top left
                point1 = (f[0]-scsz[0]/2+scsz[1]/2, f[1]) # put origin at top left
                point1 = mmul(point1, [(1/2, 0), (0, 1/2)]) # transform point
                templis[1].append((point1[0]+scsz[0]/2-scsz[1]/2, point1[1])) # put origin back
                # top right
                point2 = (f[0]-scsz[0]/2-scsz[1]/2, f[1]) # put origin at top right
                point2 = mmul(point2, [(1/2, 0), (0, 1/2)]) # transform point
                templis[2].append((point2[0]+scsz[0]/2+scsz[1]/2, point2[1])) # put origin back
                # bottom right
                point3 = (f[0]-scsz[0]/2-scsz[1]/2, f[1]-scsz[1]) # put origin at bottom right
                point3 = mmul(point3, [(0, 1/2), (1/2, 0)]) # transform point
                templis[3].append((point3[0]+scsz[0]/2+scsz[1]/2, point3[1]+scsz[1])) # put origin back
            self.fract = []
            for f in templis:
                self.fract += list(f)
        else:
            self.fdx=False

    def down(self):
        self.fdx = True
        templis = []
        if len(self.fract) > 4:
            for f in range(len(self.fract)//4):
                point = (self.fract[f][0]-scsz[0]/2+scsz[1]/2, self.fract[f][1]-scsz[1]) # put origin at bottom left
                point = mmul(point, [(0, -2), (-2, 0)]) # transform point
                templis.append((point[0]+scsz[0]/2-scsz[1]/2, point[1]+scsz[1])) # put origin back
            self.fract = list(templis)
        else:
            self.fdx=False


class peano:

    def __init__(self):
        self.fract = [(scsz[0]/2-scsz[1]/3, 5*scsz[1]/6),
                      (scsz[0]/2-scsz[1]/3, scsz[1]/6),
                      (scsz[0]/2, scsz[1]/6),
                      (scsz[0]/2, 5*scsz[1]/6),
                      (scsz[0]/2+scsz[1]/3, 5*scsz[1]/6),
                      (scsz[0]/2+scsz[1]/3, scsz[1]/6)]
        self.fdx = False

    def up(self):
        self.fdx=True
        templis = [[] for f in range(9)]
        if len(self.fract) < 10**6:
            for f in self.fract:
                # bottom left
                point0 = (f[0]-scsz[0]/2+scsz[1]/2, f[1]-scsz[1]) # put origin at bottom left
                point0 = mmul(point0, [(1/3, 0), (0, 1/3)]) # transform point
                templis[0].append((point0[0]+scsz[0]/2-scsz[1]/2, point0[1]+scsz[1])) # put origin back
                # mid left
                point1 = (f[0]-scsz[0]/2+scsz[1]/2, f[1]-scsz[1]/2) # put origin at mid left
                point1 = mmul(point1, [(-1/3, 0), (0, 1/3)]) # transform point
                templis[1].append((point1[0]+scsz[0]/2-scsz[1]/2+scsz[1]/3, point1[1]+scsz[1]/2)) # put origin back and shift a little
                # top left
                point2 = (f[0]-scsz[0]/2+scsz[1]/2, f[1]) # put origin at top left
                point2 = mmul(point2, [(1/3, 0), (0, 1/3)]) # transform point
                templis[2].append((point2[0]+scsz[0]/2-scsz[1]/2, point2[1])) # put origin back
                # top mid
                point3 = (f[0]-scsz[0]/2, f[1]) # put origin at top middle
                point3 = mmul(point3, [(1/3, 0), (0, -1/3)]) # transform point
                templis[3].append((point3[0]+scsz[0]/2, point3[1]+scsz[1]/3)) # put origin back and shift
                # mid mid
                point4 = (f[0]-scsz[0]/2, f[1]-scsz[1]/2) # put origin dead center
                point4 = mmul(point4, [(-1/3, 0), (0, -1/3)]) # transform point
                templis[4].append((point4[0]+scsz[0]/2, point4[1]+scsz[1]/2)) # put origin back
                # bottom mid
                point5 = (f[0]-scsz[0]/2, f[1]-scsz[1]) # put origin at bottom middle
                point5 = mmul(point5, [(1/3, 0), (0, -1/3)]) # transform point
                templis[5].append((point5[0]+scsz[0]/2, point5[1]+scsz[1]-scsz[1]/3)) # put origin back and shift
                # bottom right
                point6 = (f[0]-scsz[0]/2-scsz[1]/2, f[1]-scsz[1]) # put origin at bottom right
                point6 = mmul(point6, [(1/3, 0), (0, 1/3)]) # transform point
                templis[6].append((point6[0]+scsz[0]/2+scsz[1]/2, point6[1]+scsz[1])) # put origin back
                # mid right
                point7 = (f[0]-scsz[0]/2-scsz[1]/2, f[1]-scsz[1]/2) # put origin at middle right
                point7 = mmul(point7, [(-1/3, 0), (0, 1/3)]) # transform point
                templis[7].append((point7[0]+scsz[0]/2+scsz[1]/2-scsz[1]/3, point7[1]+scsz[1]/2)) # put origin back and shift
                # top right
                point8 = (f[0]-scsz[0]/2-scsz[1]/2, f[1]) # put origin at top right
                point8 = mmul(point8, [(1/3, 0), (0, 1/3)]) # transform point
                templis[8].append((point8[0]+scsz[0]/2+scsz[1]/2, point8[1])) # put origin back
            self.fract = []
            for f in templis:
                self.fract += list(f)
        else:
            self.fdx=False

    def down(self):
        self.fdx = True
        templis = []
        if len(self.fract) > 6:
            for f in range(len(self.fract)//9):
                point = (self.fract[f][0]-scsz[0]/2+scsz[1]/2, self.fract[f][1]-scsz[1]) # put origin at bottom left
                point = mmul(point, [(3, 0), (0, 3)]) # transform point
                templis.append((point[0]+scsz[0]/2-scsz[1]/2, point[1]+scsz[1])) # put origin back
            self.fract = list(templis)
        else:
            self.fdx=False


class zcurve:

    def __init__(self):
        self.fract = [(scsz[0]/2-scsz[1]/4,scsz[1]/4),
                      (scsz[0]/2+scsz[1]/4,scsz[1]/4),
                      (scsz[0]/2-scsz[1]/4,3*scsz[1]/4),
                      (scsz[0]/2+scsz[1]/4,3*scsz[1]/4)]
        self.fdx = False

    def up(self):
        self.fdx=True
        templis = [[] for f in range(4)]
        if len(self.fract)<4**10:
            for f in self.fract:
                # top left
                point0 = (f[0]-scsz[0]/2+scsz[1]/2, f[1]) # put origin at top left
                point0 = mmul(point0, [(1/2, 0), (0, 1/2)]) # transform point
                templis[0].append((point0[0]+scsz[0]/2-scsz[1]/2, point0[1])) # put origin back
                # top right
                point1 = (f[0]-scsz[0]/2-scsz[1]/2, f[1]) # put origin at top right
                point1 = mmul(point1, [(1/2, 0), (0, 1/2)]) # transform point
                templis[1].append((point1[0]+scsz[0]/2+scsz[1]/2, point1[1])) # put origin back
                # bottom left
                point2 = (f[0]-scsz[0]/2+scsz[1]/2, f[1]-scsz[1]) # put origin at bottom left
                point2 = mmul(point2, [(1/2, 0), (0, 1/2)]) # transform point
                templis[2].append((point2[0]+scsz[0]/2-scsz[1]/2, point2[1]+scsz[1])) # put origin back
                # bottom right
                point3 = (f[0]-scsz[0]/2-scsz[1]/2, f[1]-scsz[1]) # put origin at bottom right
                point3 = mmul(point3, [(1/2, 0), (0, 1/2)]) # transform point
                templis[3].append((point3[0]+scsz[0]/2+scsz[1]/2, point3[1]+scsz[1])) # put origin back
            self.fract = []
            for f in templis:
                self.fract += list(f)
        else:
            self.fdx=False

    def down(self):
        self.fdx = True
        templis = []
        if len(self.fract) > 4:
            for f in range(len(self.fract)//4):
                point = (self.fract[f][0]-scsz[0]/2+scsz[1]/2, self.fract[f][1]) # put origin at top left
                point = mmul(point, [(2, 0), (0, 2)]) # transform point
                templis.append((point[0]+scsz[0]/2-scsz[1]/2, point[1])) # put origin back
            self.fract = list(templis)
        else:
            self.fdx=False


class sierpinski:

    def __init__(self):
        self.fract = [(scsz[0]/2-scsz[1]/(3)**(1/2),scsz[1]),
                      (scsz[0]/2-scsz[1]/(3)**(1/2)/2,scsz[1]/2),
                      (scsz[0]/2+scsz[1]/(3)**(1/2)/2,scsz[1]/2),
                      (scsz[0]/2+scsz[1]/(3)**(1/2),scsz[1])]
        self.fdx=False

    def up(self):
        self.fdx = True
        templis1 = []
        templis2 = []
        templis3 = []
        if len(self.fract) < 4*3**10:
            for f in self.fract:
                # left side
                point1 = (f[0]-scsz[0]/2+scsz[1]/(3)**(1/2), f[1]-scsz[1]) # put origin at left corner of triagle
                point1 = mmul(point1, [(1/4, -3**(1/2)/4), (-3**(1/2)/4, -1/4)]) # transform point
                templis1.append((point1[0]+scsz[0]/2-scsz[1]/(3)**(1/2), point1[1]+scsz[1])) # put origin back
                # top bit
                point2 = (f[0]-scsz[0]/2, f[1]) # put origin at top center
                point2 = mmul(point2, [(1/2, 0), (0, 1/2)]) # transform point
                templis2.append((point2[0]+scsz[0]/2, point2[1])) # put origin back
                # right side
                point3 = (f[0]-scsz[0]/2-scsz[1]/(3)**(1/2), f[1]-scsz[1]) # put origin at left corner of triagle
                point3 = mmul(point3, [(1/4, 3**(1/2)/4), (3**(1/2)/4, -1/4)]) # transform point
                templis3.append((point3[0]+scsz[0]/2+scsz[1]/(3)**(1/2), point3[1]+scsz[1])) # put origin back
            self.fract = list(templis1)+list(templis2[1:])+list(templis3[1:])
        else:
            self.fdx = False

    def down(self):
        self.fdx = True
        templis = []
        if len(self.fract) > 4:
            third = len(self.fract)//3
            for f in range(third+1):
                point = (self.fract[third+f][0]-scsz[0]/2, self.fract[third+f][1]) # put origin at top center
                point = mmul(point, [(2, 0), (0, 2)]) # transform point
                templis.append((point[0]+scsz[0]/2, point[1])) # put origin back
            self.fract = list(templis)
        else:
            self.fdx = False


class dragon:

    def __init__(self):
        self.dragoff = scsz[0]/12
        self.fract=[(scsz[0]/4,scsz[1]/2-self.dragoff),
                    (scsz[0]/2,scsz[1]/2+scsz[0]/4-self.dragoff),
                    (3*scsz[0]/4,scsz[1]/2-self.dragoff)]
        self.fdx=False

    def up(self):
        self.fdx=True
        templis1 = []
        templis2 = []
        if len(self.fract) < 10**7:
            for f in self.fract:
                # left half
                point1 = (f[0]-scsz[0]/4, f[1]-scsz[1]/2+self.dragoff) # put origin at left point
                point1 = mmul(point1, [(0.5, -0.5), (0.5, 0.5)]) # transform point
                templis1.append((point1[0]+scsz[0]/4, point1[1]+scsz[1]/2-self.dragoff)) # put origin back
                # right half
                point2 = (f[0]-scsz[0]/2, f[1]-scsz[1]/2+self.dragoff) # put origin at center
                point2 = mmul(point2, [(-1, 0), (0, -1)]) # reverse point
                point2 = (point2[0]-scsz[0]/4, point2[1]) # put origin at right point
                point2 = mmul(point2, [(0.5, 0.5), (-0.5, 0.5)]) # transform point
                templis2.append((point2[0]+3*scsz[0]/4, point2[1]+scsz[1]/2-self.dragoff)) # put origin back
            self.fract = list(templis1)+list(templis2[-2::-1])
        else:
            self.fdx = False

    def down(self):
        self.fdx = True
        templis = []
        if len(self.fract) > 3:
            for f in range(len(self.fract)//2+1):
                point1 = (self.fract[f][0]-scsz[0]/4, self.fract[f][1]-scsz[1]/2+self.dragoff) # put origin at left point
                point1 = mmul(point1, [(1, 1), (-1, 1)]) # transform point
                templis.append((point1[0]+scsz[0]/4, point1[1]+scsz[1]/2-self.dragoff)) # put origin back
            self.fract = list(templis)
        else:
            self.fdx = False


class goldendragon:

    def __init__(self):
        self.dragoff = scsz[0]/12
        self.unit = scsz[0]/2
        phi = (1+5**0.5)/2
        r = (1/phi)**(1/phi)
        x = (1+r**2-r**4)/2
        self.vertex = (self.unit*x, self.unit*(r**2-x**2)**(1/2))
        self.fract = [(scsz[0]/4, scsz[1]/2-self.dragoff),
                    (scsz[0]/4+self.vertex[0], scsz[1]/2-self.dragoff+self.vertex[1]),
                    (3*scsz[0]/4, scsz[1]/2-self.dragoff)]
        self.fdx = False

    def up(self):
        self.fdx = True
        templis1 = []
        templis2 = []
        if len(self.fract) < 10**7:
            for f in self.fract:
                # left half
                point1 = (f[0]-scsz[0]/4, f[1]-scsz[1]/2+self.dragoff) # put origin at left point
                point1 = mmul(point1, [(self.vertex[0]/self.unit, -self.vertex[1]/self.unit),
                                       (self.vertex[1]/self.unit, self.vertex[0]/self.unit)]) # transform point
                templis1.append((point1[0]+scsz[0]/4, point1[1]+scsz[1]/2-self.dragoff)) # put origin back
                # right half
                point2 = (f[0]-scsz[0]/2, f[1]-scsz[1]/2+self.dragoff) # put origin at center
                point2 = mmul(point2, [(-1, 0), (0, -1)]) # reverse point
                point2 = (point2[0]-scsz[0]/4, point2[1]) # put origin at right point
                point2 = mmul(point2, [(-self.vertex[0]/self.unit+1, self.vertex[1]/self.unit),
                                       (-self.vertex[1]/self.unit, -self.vertex[0]/self.unit+1)]) # transform point
                templis2.append((point2[0]+3*scsz[0]/4, point2[1]+scsz[1]/2-self.dragoff)) # put origin back
            self.fract = list(templis1)+list(templis2[-2::-1])
        else:
            self.fdx = False

    def down(self):
        self.fdx = True
        templis = []
        if len(self.fract) > 3:
            for f in range(len(self.fract)//2+1):
                point = (self.fract[f][0]-scsz[0]/4, self.fract[f][1]-scsz[1]/2+self.dragoff) # put origin at left point
                a = self.vertex[0]/self.unit
                b = self.vertex[1]/self.unit
                point = mmul(point, [(a/(a**2+b**2), b/(a**2+b**2)),
                                     (-b/(a**2+b**2), a/(a**2+b**2))]) # transform point
                templis.append((point[0]+scsz[0]/4, point[1]+scsz[1]/2-self.dragoff)) # put origin back
            self.fract = list(templis)
        else:
            self.fdx = False


# define which curve will be displayed
curve = goldendragon()


while mainloop:
    milliseconds = clock.tick(FPS)
    playtime += milliseconds / 1000.0
    framecount += 1
    dsc = False
    if framecount == 1:
        dsc = True

    # ----- event handler -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:
            dsc = True
            if event.key == pygame.K_ESCAPE:
                # press escape to exit
                mainloop = False
            elif event.key == pygame.K_SPACE:
                # press space to iterate the fractal
                curve.up()
                dsc = bool(curve.fdx)
            elif event.key == pygame.K_BACKSPACE:
                # press backspace to de-iterate the fractal
                curve.down()
                dsc = bool(curve.fdx)
            elif event.key == pygame.K_c:
                # press c to cycle the color of the fractal
                change_color()
            elif event.key == pygame.K_q:
                # press q to toggle whether c cycles the primary or secondary color
                q = 1-q
            elif event.key == pygame.K_x:
                # press x to toggle rainbow mode
                x = not x

    # ----- update screen -----
    if dsc:
        background.fill((0, 0, 0))
        tot = len(curve.fract)-1
        if x:
            revlis = cyclein(tot, 1530)
        if color[0] == color[1] and not x:
            pygame.draw.lines(background, color[0], False, curve.fract)
        else:
            for f in range(tot):
                if x:
                    if f==0:
                        tempcol=list(color)
                    specol=(tempcol[0][0], tempcol[0][1], tempcol[0][2])
                    revolve_color(tempcol, 0, revlis[f])
                else:
                    specol=((tot-f)*color[0][0]/tot+f*color[1][0]/tot,(tot-f)*color[0][1]/tot+f*color[1][1]/tot,(tot-f)*color[0][2]/tot+f*color[1][2]/tot)
                pygame.draw.line(background, specol, curve.fract[f], curve.fract[f+1])
    screen.blit(background, (0, 0))
    fpstxt = myfont30.render("fps: {:0.2f}".format(clock.get_fps()), 1, (255, 255, 255))
##    screen.blit(fpstxt, (0, scsz[1]-30)) # display the fps
    pygame.display.flip()
pygame.quit()
