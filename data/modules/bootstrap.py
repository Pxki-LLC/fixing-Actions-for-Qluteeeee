#!/usr/bin/python3
#
#    Just Beats! (Qlute)
#    2020-2023 Pxki Games (Formally known as ??)
#    (Using Slyph Engine, Tinyworld's Game Engine)
#
#
import random,re,json,zipfile
from random import randint
import pygame, os, time, sys, threading, requests, socket
if "-user" in sys.argv:
    x=sys.argv.index('-user')+1
    print('Using',sys.argv[x])
    username=sys.argv[x]
nline='\n'
axe=0
gamename='Qlute'
gameeditions='Stable','Beta','Canary','Dev'
gameedition=gameeditions[1]
gamever='2023.12.16'
sylphenginever='2023.09.29'
gameverspl=gamever.split('.')
#gameminserve=int(gameverspl[0])+((1+float(gameverspl[1]))*float(gameverspl[2]))
modpath=datapath+'mods/'
gamepath=datapath+'beatmaps/'
downpath=datapath+'downloads/'
username='BTMC'
propath=datapath+'profiles/'
profilepath=propath+username+'/'
gameupdateurl='https://github.com/pxkidoescoding/Qlute/'
gameauthor='Pxki Games'
print('Starting Game...')
fpsmode=-1
button_size_height=33
stop=0
rankdiff='Easy','Normal','Hard','Extra','Expert','Impossible','WTF!'
rankdiffc=(0,100,200),(0,200,50),(150,200,0),(200,50,0),(0,0,0),(150,0,150)
pygame.mixer.init()
sa=time.time()
gametime=0
ismusic=0
paths=datapath,gamepath,propath,profilepath,modpath,downpath
prestart=1
reloaddatabase=1
vol=1
isonline=False
for a in paths:
    if not os.path.isdir(a):
        os.mkdir(a)
        print('Created', a.replace('./', ''))
keyspeed=1
getpoints=0
debugmode=True
fps=0
update=False
offset=20,20
beatsel=0
beatnowmusic=1
score=0
maxperf=0
betaperf=0
#pertok=30
perftok=12*2600
#*0.001
perfbom=(1/perftok)*0.5
diff=[]
diffmode=''
diffcon=0
bgcolour=0
perf=0
maxobjec=255
objecon=0
oldupdatetime=0
totscore=0
tick=0
combo=0
lastms=0
darkness=0
stripetime=[]
bgtime=time.time()
objects=[]
speedvel=[0,0]
modsen=[0,0,0,0,0,0,0,0,0,0]
scoremult=1
modshow=False
msg=''
totrank=0
prevrank=0
uptime=time.time()
if os.path.isfile(profilepath+'perf'):
    t=open(profilepath+'perf').read().rstrip('\n')
    totperf=int(float(t))
else:
    totperf=0
if os.path.isfile(profilepath+'score'):
    t=open(profilepath+'score').read().rstrip('\n')
    totscore=int(float(t))
else:
    totscore=0
rankmodes=('Ranked',(100,200,100)),('Unranked',(200,100,100)),('In Review',(200,200,100)),('Loading...',(200,200,200)),
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()
surface=[]
for a in range(1,10):
    surface.append(pygame.Surface((0,0)))
fontname=resource_path(datapath+'font.ttf')
clock=pygame.time.Clock()
activity=0
select=False
cross=[0,0]
crossboard=0
realid='' 
firstcom=False
combotime=0
maxplay=1000
menuback=0
backspeed=1
replaymen=0
beka='None'
actto=activity
transb=0
transa=0
voltime=0
#tmp!!!!
msgx=0
messagetime=0
change=False
colorstep = 0
loaded=[]
ama=0
bars=[0,0,0,0]
t=''
miss=20
hits=[0,0,0,0]
#hitperfect=keymap[0][1]
#hitperfect=keymap[0][1]
last=0
ismulti=False # Enabling this means Leaderboard is shown
keys=[0,0,0,0]
keyslight=[0,0,0,0]
pos=(64,192,320,448)
tip=0
sre=0
modsen[0]=1
crox=[]
def main():
    global fps, activity,oneperf,oneperfk, ingame, screen, settingskeystore,reloaddatabase,totrank, debugmode,sa,bgcolour,tick,scale,size,cardsize,bgtime,replaymen,allowed,posmouse,drawtime,scoremult,msg
    if gameedition!=gameeditions[0]:
        gs='/'+gameedition
    else:
        gs=''
    msg=''
    pygame.display.set_caption(gamename+gs+' '+str(gamever)+' ['+str(activity)+']')
    if not firstcom:
        pygame.display.set_icon(programIcon)
    pygame.mouse.set_visible(False)
    update=time.time()
    posmouse=pygame.mouse.get_pos()
#    if modsen[0]:
#        scoremult=1

    if time.time()-sa>0.1:
        sa=time.time()
        fps=int(clock.get_fps())
    allowed=[0,1,2,3,5,6,7,8,99,9]
    fullscreenchk()
    size=60
    scale=(w/400)
    if scale>=3:
        scale=3
    cardsize=int(300*scale)
    if activity==2:
        ingame=True
    else:
        ingame=False
    if "bpm" in globals():
        if activity in allowed:
            if len(p2)!=0:
                clear((maxt(20,bgcolour),maxt(20,bgcolour),maxt(50,bgcolour)))
            else:
                clear((20,20,50))
            tok=(1-((gametime/bpm)-tick))
            if tok<0:
                tok=0
            elif tok>1:
                tok=1
            elif gametime<=-1:
                tok=0
            if not settingskeystore[1]:
                bgcolour=30*tok
            else:
                bgcolour=0
        if gametime//bpm>tick:
            tick+=1
    for a in os.listdir(downpath):
        os.mkdir(gamepath+a.replace('.osz',''))
        with zipfile.ZipFile(downpath+a, 'r') as zip_ref:
            zip_ref.extractall(gamepath+a.replace('.osz','/'))
            reloaddatabase=1
        os.remove(downpath+a)
        print('Imported',a)
    #crok=10**len(str(oneperf))
    oneperf=(38000+((totperf+perf)*0.1*5))#+int(12*int(time.time()-uptime))
    totrank=get_rank(totperf)
    if totrank<1:
        totrank=1
    beatmapload()
    logo()
    beatres()
    mainmenu()
    settingspage()
    beatmenu()
    shopdirect()
    debuginfo()
    try:
        game()
    except Exception as error:
        crash(error)
        activity=1
    scoreboard()
#    if activity==4:
#        render('rect', arg=((18,28,300,100), (20,20,20), True), borderradius=5)
#        render('text',text='New Rank:'+str(get_rank(totperf+perf)),arg=((25,50),forepallete))
#        render('text',text='#1 Perf: '+str(oneperf),arg=((25,70),forepallete))
    if msg!='':
        tmp=(posmouse[0]+15,posmouse[1]+15,(10*len(msg))+5,25)
        render('rect', arg=(tmp, (20,20,20), True), borderradius=5)
        render('text',text=msg,arg=((0,0),forepallete,'center'),relative=tmp)
#    for a in crox:
#        render('rect', arg=((a[0]-10,a[1]-10,20,20), (80,80,255), True),borderradius=10)
    transitionto()
    #updateraw=(time.time()-update)/0.001
        #spectrum()
    if activity==1:
        of=35
    else:
        of=0
    if not int(time.time()-voltime)>1:
        render('rect', arg=((w//2-100, 55, 200, 20), (20,20,20), False), borderradius=15)
        render('rect', arg=((w//2-100, 55, 200*vol, 20), (20,50,20), False), borderradius=15)
        render('text',text=str(int(vol*100))+'%',arg=((0,0),forepallete,'center'),relative=(w//2-100, 56, 200, 20))
    if debugmode:
        updatetime=str((time.time()-update)/0.001)[:4]
        if updatetime[-1]=='.':
            updatetime=updatetime[:len(updatetime)-1]
        if (time.time()-update)/0.001>=6:
            fpscolour=(150,50,50)
        else:
            fpscolour=(50,150,50)
        render('rect', arg=((w-127, of+15, 120, 65), (fpscolour), False), borderradius=10)
        #render('rect', arg=((5, 5, struct, 5), (0,255,0), False), borderradius=10)
    fps_text = f'{fps}/{fpsmodes[fpsmode]}'
    render('text', text=fps_text, arg=((w - 120, 23), forepallete, 'center'), relative=(w - 127, of + 20, 120, 30))
    render('text', text=f'{updatetime}ms', arg=((w - 120, 43), forepallete, 'center'), relative=(w - 127, of + 45, 120, 30))        #render('text',text='TICK:'+str(tick)+'/'+str(gametime//bpm)+'/'+str(gametime)+'/'+str(bpm),arg=((20, 43),forepallete))
    #print((time.time()-gametime)/0.001)
    if activity in allowed:
        render('rect', arg=((posmouse[0]-10,posmouse[1]-10,20,20), (80,80,150), True),borderradius=10)
#    if not (posmouse[0],posmouse[1]) in crox:
#        crox.append((posmouse[0],posmouse[1]))
    pygame.display.update()
    drawtime=clock.tick(fpsmodes[fpsmode])/1000
    #print(drawtime)
if __name__  ==  "__main__":
    try:
        for a in os.listdir(modpath):
            print(a)
        if prestart:
            logotime=time.time()
        greph=[]
        for a in modsen:
            greph.append(randint(1,2)-1)
        programIcon = pygame.image.load(resource_path(datapath+'icon.png'))
        while True:
            if stop:
                sys.exit()
            main()
    except Exception as error:
        crasha(str(error))