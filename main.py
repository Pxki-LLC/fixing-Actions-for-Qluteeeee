#!/usr/bin/python3
#
#    Just Beats! (Qlute)
#    2023-2023 Pxki Games
#    (Using Slyph Engine, Tinyworld's Game Engine)
# 
#

import random,re,json,zipfile
from random import randint
import pygame, os, time, sys, threading, urllib.request, socket
nline='\n'
axe=0
gamename='Qlute'
gameeditions='Stable','Beta','Canary','Dev'
gameedition=gameeditions[1]
gamever='2023.11.09'
sylphenginever='2023.09.29'
gameverspl=gamever.split('.')
datapath='./data/'
modpath=datapath+'mods/'
gamepath=datapath+'beatmaps/'
downpath=datapath+'downloads/'
username='Guest'
if "-user" in sys.argv:
    x=sys.argv.index('-user')+1
    print('Using',sys.argv[x])
    username=sys.argv[x]
propath=datapath+'profiles/'
profilepath=propath+username+'/'
gameupdateurl='N/A'
gameauthor='Pxki Games'
print('Starting Game...')
fpsmode=1
forepallete=(255,255,255)
fpsmodes=[30,60,120,1000]
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
for a in paths:
    if not os.path.isdir(a):
        os.mkdir(a)
        print('Created', a.replace('./', ''))
mtext='Play','Options','ScoreBoard List','Exit'
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
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def test(arg, arg2):
    try:
        arg[arg2]
        return True
    except Exception:
        return False
if os.path.isfile(datapath+'settings.db'):
    if not len(open(datapath+'settings.db').read().rstrip("\n").split("\n"))<3:
        settingskeystore=open(datapath+'settings.db').read().rstrip("\n").split("\n")
        for a in range(len(settingskeystore)):
            if settingskeystore[a].isdigit() or settingskeystore[a] == 'True' or settingskeystore[a] == 'False':
              settingskeystore[a]=eval(settingskeystore[a])
        print(settingskeystore)
        if len(settingskeystore) >= 4 and str(settingskeystore[3]).isdigit():
            if int(settingskeystore[3]) in fpsmodes:
                fpsmode=int(settingskeystore[3])
                print('FPS set to '+str(fpsmodes[fpsmode]))
            elif test(fpsmodes, settingskeystore[3]):
                fpsmode=int(settingskeystore[3])
                print('FPS set to '+str(fpsmodes[fpsmode]))
            else:
                print('FPS '+str(settingskeystore[3])+' is not valid,  set back to 60 (Normal)')
                fpsmode=1
else:
    settingskeystore=[]
    for a in range(1, 4):
        settingskeystore.append(False)
    settingskeystore.append(1)
def stopnow():
    global stop
    stop=1
def cbytes(size):
    units = ['B',  'KB',  'MB',  'GB',  'TB']
    unit_index = 0

    while size  >=  1000 and unit_index < len(units) - 1:
        size /= 1000
        unit_index += 1

    converted_size = f"{size:.2f} {units[unit_index]}"
    return converted_size
def settingspage():
    global settingskeystore, activity, screen, firstcom, change, fpsmode,totperf,totscore,msg
    if activity==2:
        if change:
            tmp=open(datapath+'settings.db', 'w')
            for a in settingskeystore:
                tmp.write(str(a)+'\n')
            tmp.close()
            change=False
        #settingskeystore[2], settingskeystore[1], fullscreen
        if str(fpsmodes[fpsmode])!='1000':
            tmp=str(fpsmodes[fpsmode])
        else:
            tmp='Unlimited'
        render('text', text=gamename + ' - Options', arg=(offset, forepallete))
        setuplist=['FPS: '+tmp,'Reset Card','Fullscreen: '+str(settingskeystore[0]),'Effects: '+str(not settingskeystore[1]),'Allow Skins: '+str(settingskeystore[2]),'Debug Info']
        setuplistpos=[]
#        for a in range(1,6):
#            setuplist.append('Unknown')
        for a in range(1,len(setuplist)+1):
            poof=offset[1]+10
            setuplistpos.append((w//2-110,  poof+(50*a),  220,  button_size_height))
        setbutton=menu_draw((setuplistpos), (setuplist))
        sysbutton=menu_draw(((-10,h-50,100,40),),('Back',))
        if setbutton == 1:
            msg='Changes how fast this game goes'
        elif setbutton == 2:
            al=w//2
            print_card(totperf,totscore,username,(posmouse[0]-50,posmouse[1]+20),1)
        elif setbutton == 3:
            msg='Makes the Screen Fullscreen, what do you expect'
        elif setbutton == 4:
            msg='Changes the Flashing Effect'
        elif setbutton == 5:
            msg='Allows Skinning'
            
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
            if event.type  ==  pygame.MOUSEBUTTONDOWN: 
                if setbutton:
                  change=True
                if setbutton  ==  1:
                    change=True
                    if fpsmode<1:
                        fpsmode=len(fpsmodes)-1
                    else:
                        fpsmode-=1
                    settingskeystore[3]=fpsmode
                elif setbutton  ==  2:
                    if os.path.isfile(profilepath+'perf'):
                        os.remove(profilepath+'perf')
                    if os.path.isfile(profilepath+'score'):
                        os.remove(profilepath+'score')
                    if os.path.isfile(profilepath+'scoreboard'):
                        os.remove(profilepath+'scoreboard')
                    totperf=0
                    totscore=0
                    print('Card Reset')
                elif setbutton == 3:
                  settingskeystore[0] = not settingskeystore[0]
                  firstcom=False
                elif setbutton == 4:
                  settingskeystore[1] = not settingskeystore[1]
                elif setbutton == 5:
                  settingskeystore[2] = not settingskeystore[2]
                elif setbutton == 6:
                  transitionprep(99)
                elif sysbutton:
                    transitionprep(1)

            if event.type  ==  pygame.KEYDOWN:
                if event.key  ==  pygame.K_q:
                    transitionprep(1)
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
def render(type, arg=(0, 0) ,  text='N/A', bordercolor=forepallete, borderradius=0,relative=(0,0,0,0),surf=''):
    off=0
    grad2=False
    if surf=='':
      surf=screen
    try:
        bordercolor=mint(bordercolor[0],darkness),mint(bordercolor[1],darkness),mint(bordercolor[2],darkness)
        try:
            colour=mint(arg[1][0],darkness),mint(arg[1][1],darkness),mint(arg[1][2],darkness)
        except Exception:
            colour=mint(arg[1],darkness)
        relative=pygame.Rect(relative)
        if type == 'text':
            if "min" in arg:
                surf.blit(fonts[1].render(str(text),  True,  colour),  arg[0])
            elif "grade" in arg:
                if "center" in arg:
                    tmp = fonts[2].render(str(text),  True,  colour)
                    centertext = tmp.get_rect(center=relative.center)
                    surf.blit(tmp,  centertext)
                    grad2=True
                else:
                    surf.blit(fonts[2].render(str(text),  True,  colour),  arg[0])
            elif not "center" in arg:
                surf.blit(fonts[0].render(str(text),  True,  colour),  arg[0])
            if "center" in arg and not grad2:
                tmp = fonts[0].render(str(text),  True,  colour)
                centertext = tmp.get_rect(center=relative.center)
                surf.blit(tmp,  centertext)
        elif type == 'clear':
            screen.fill(arg)
        elif type == 'line':
            pygame.draw.line(surf,colour,arg[0],arg[2])
        elif type == 'rect':
#			print(arg[0][0], arg[0][1], arg[0][2], arg[0][3])
            pygame.draw.rect(surf, colour, (arg[0][0], arg[0][1], arg[0][2]-off, arg[0][3]-off), border_radius=borderradius)
            if arg[2]:
                pygame.draw.rect(surf, bordercolor, (arg[0][0], arg[0][1], arg[0][2]-off, arg[0][3]-off), 2, border_radius=borderradius)
            ## This was for a "Wireframe" Like Square
#            pygame.draw.rect(screen, (0, 255, 0), (arg[0][0], arg[0][1], arg[0][2], arg[0][3]), 1)
        elif type == 'header':
            render('rect', arg=((0, -40, w, 100), (50, 50, 100), False), borderradius=20)
        else:
            crash('Render unsupported Type')
    except Exception as error:
        crash(str(error)+' (renderer)')
def notify(text):
    global message, messagetime
    messagetime = time.time() + 5
    message = text      
firstcom=False
def fullscreenchk():
    global w, h, w, h, screen, button_size_width, firstcom,tal,keymap,fonts,transa
    reload=False
    if not settingskeystore[0]:
        if not firstcom:
            w=800
            h=600
            screenw=w
            screenh=h
        else:
            w=screen.get_width()
            h=screen.get_height()

    flags=pygame.DOUBLEBUF|pygame.RESIZABLE|pygame.HWSURFACE
    bit=24
    if settingskeystore[0]:
        if not firstcom:
            screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN|flags, bit)
            reload=True
    else:
        if not firstcom:
            screen=pygame.display.set_mode((w, h), flags, bit)
            reload=True
    if not firstcom:
        firstcom=True
    w=screen.get_width()
    h=screen.get_height()
    ins=1
    if reload:
        f=24
        fonts = pygame.font.Font(fontname,  int(f//1.2)),pygame.font.Font(fontname,  f//2),pygame.font.Font(fontname,  f*2),pygame.font.Font(fontname,  int(f//1.5))
        button_size_width=w//2
    tal=25*(w/25)//len(bars)
    scroll=h-60
    #scroll=h//2
    keymap=(pygame.Rect(w//2-(50*4),scroll,100,30),pygame.Rect(w//2-(50*2),scroll,100,30),pygame.Rect(w//2-(50*0),scroll,100,30),pygame.Rect(w//2-(50*-2),scroll,100,30),)
def textbox():
    global maxtext
    maxtext=24*(w//640+1)
    render('rect', arg=(((w - button_size_width) // 2,  ((h - button_size_height) // 2) + (button_size_height - 60), button_size_width,  60), (0, 0, 0), True), bordercolor=forepallete)
    if len(textbox_text)<maxtext:
        colortext=255, 255, 255
    else:
        colortext=255, 0, 0
    render('text', arg=(((w - button_size_width) // 2+10, ((h - button_size_height) // 2) + (button_size_height//4)), colortext), text=textbox_text)
def menu_draw(instruction, text=None, istextbox=False, selected_button=0,enabled_button=[],enable_border=False, hidebutton=False,bigmode=False,startlimit=1,endlimit=None,styleid=1):
    if endlimit==None:
        endlimit=len(instruction)
    elif endlimit>=len(instruction):
        endlimit=len(instruction)
    if startlimit<1:
        startlimit=1
    button=0
    if istextbox:
        button_idle=0, 0, 0
    else:
        if styleid==0:
            button_idle=30, 100, 120
        elif styleid==1:
            button_idle=70,70,120
    for a in range(startlimit,  endlimit+1):	
        tmp=instruction[a-1]
        tmp=pygame.Rect(tmp[0],tmp[1],tmp[2],tmp[3])
        if tmp.collidepoint(pygame.mouse.get_pos()):
            select=True
            buttcolour = (button_idle[0]+10,button_idle[1]+10,button_idle[2]+10)
            if pygame.mouse.get_focused():
                button=a
        else:
            buttcolour = button_idle
            select=False
        b = (buttcolour[0]-10,buttcolour[1]-10,buttcolour[2]-10)
        if not hidebutton:
            if selected_button == a or (len(enabled_button)>0 and enabled_button[a-1]):
                render('rect', arg=((tmp), buttcolour, True),borderradius=10, bordercolor=(0, 150, 150))
            elif select:
                render('rect', arg=((tmp), buttcolour, enable_border),borderradius=10,bordercolor=b)
            else:
                render('rect', arg=((tmp), buttcolour, enable_border),borderradius=10, bordercolor=b)
        if not text == None:
            if bigmode:
                render('text', text=text[a-1], arg=((0,0), forepallete,'center','grade'),relative=instruction[a-1])
            else:
                
                render('text', text=text[a-1], arg=((0,0), forepallete,'center'),relative=instruction[a-1])
    return button
combotime=0
def reloadstats():
    global objects,difficulty,metadata,level,bpm,songoffset,maxperf,scoremult,ismulti,perfect,great,ok,diffmode
    diffmode=diff[diffcon][1]
    beatmap=open(gamepath+beatlist[beatsel]+'/'+pref+'['+diffmode+']'+'.osu').read().rstrip('\n').split('\n')
    objects=beatmap[beatmap.index('[HitObjects]')+1:]
    if modsen[4]:
        print('RND MODE')
        lol=0
        tmp=''
        for a in objects:
            tmp=''
            tok=a.split(',')[1:]
            for b in tok:
                tmp+=','+str(b)
            key=randint(1,len(pos))-1
            objects[lol]=str(pos[key])+tmp
            lol+=1


    difficulty=beatmap[beatmap.index('[Difficulty]')+1:]
    difficulty=difficulty[:difficulty.index('')]
    metadata=beatmap[beatmap.index('[Metadata]')+1:beatmap.index('[Difficulty]')-1]
    level=float(difficulty[2].split(':')[-1])+float(difficulty[1].split(':')[-1])+float(difficulty[0].split(':')[-1])
    bpm=float(beatmap[beatmap.index('[TimingPoints]')+1:][0].split(',')[1])
    songoffset=float(beatmap[beatmap.index('[TimingPoints]')+1:][0].split(',')[0])
    scoremult=1
    inc=0.5
    inf=0.1
    perfect=30*int(11-float(difficulty[2].split(':')[-1]))
    great=perfect*2
    ok=perfect*3
    ismulti=modsen[4]
    for a in range(2,len(modsen)+1):
        if modsen[a-1] and a==2:
            scoremult+=inc*3
        elif modsen[a-1] and not a in (4,5):
            scoremult+=inc
        elif modsen[a-1] and a==4:
            scoremult-=inc
    maxperf=int((len(objects)*300)*(perfbom*level*scoremult))
def beatmapload():
    global p2,p1,beatnowmusic,gametime,beatlist,objects,betaperf,reloaddatabase,maxperf,ranktype,diff,diffmode,pref,level,ismusic,bpm,realid,prestart,beatsel,tick,lastms,combotime,songoffset,metadata,id
    a=0
    p1=[]
    p2=[]
    if reloaddatabase:
        beatlist=[tmp for tmp in os.listdir(gamepath)]
        reloaddatabase=0
    if prestart:
        if len(beatlist)!=0:
            beatsel=random.randint(1,len(beatlist))-1
        prestart=0
    for b in beatlist:
#        tmp.append(str(b))
        p1.append(((w//2-(cardsize//2)-((size+5)*cross[0])+((size+5)*(a)),(h//2-size)-((size+5)*cross[0])+((size+5)*(a)),cardsize,size)))
        p2.append(str(b)[str(b).index(' ')+1:])
        a+=1
    if ismusic:
        gametime=pygame.mixer.music.get_pos()
        pygame.mixer.music.set_volume(vol)
        #pygame.mixer.music.set_pos(time.time()-gametime)
        #pass
#        if gametime<0:
#            gametime=0
        #pygame.mixer.music.play(-1,(time.time()-gametime))
    try:
        if beatnowmusic:
            ranktype=3
            gametime=0
            tick=0
    #        if activity==4:
    #            if int(time.time()-wait)>=1:
    #                wait=time.time()+3
    #                pygame.mixer.music.stop()
    #        else:
    #            wait=int(time.time())
            ismusic=False
            if len(beatlist)!=0:
                if os.path.isdir(gamepath+beatlist[beatsel]):
                    ah=os.listdir(gamepath+beatlist[beatsel])
                    for bop in ah:
                        if bop.endswith('.mp3') or bop.endswith('.ogg'):
                            music=bop
                            ismusic=True
                            break
                        else:
                            ismusic=False
            if ismusic:
                #if not int(time.time()-wait)<=-1:
                if 1==1:
                    beatnowmusic=0
                    realid=beatlist[beatsel]
                    diff=[]
                    pref=''
                    if activity in allowed:
                        loop=-1
                        print(loop)
                    else:
                        loop=0
                    for a in ah:
                        if a.endswith('.osu'):
                            ax=re.findall(r'\[(.*?)\]', a)
                            if len(str(ax))>2:
                                diff.extend(ax)
                        if pref=='' and a.endswith('.osu'):
                            pref=a.replace('.osu','')
                            pref=pref[:pref.index('[')]
                    diffp=[]
                    for difftmp in diff:
                        beatmap=open(gamepath+beatlist[beatsel]+'/'+pref+'['+difftmp+']'+'.osu').read().rstrip('\n').split('\n')
                        objects=len(beatmap[beatmap.index('[HitObjects]')+1:])*300
                        diffp.append((objects,difftmp))
                    diff=sorted(diffp, key=lambda x: x[0])
                    diffp=[]

                    pygame.mixer.music.load(gamepath+beatlist[beatsel]+'/'+music)
                    pygame.mixer.music.play(loop,0,1000)
                    #print(ids)
                    gametime=pygame.mixer.music.get_pos()
                    reloadstats()
                    betaperf=0
                    ptick=0
                    gener=0
                    perfnerf=0.00975*level
                    perfntot=0
                    for a in objects:
                        if int(a.split(',')[2])//100>ptick:
                            ptick=int(a.split(',')[2])//100
                            perfntot=0
                        else:
                            perfntot+=perfnerf
                        betaperf+=perfntot
                    betaperf=betaperf
                    if betaperf>1500:
                        betaperf=1500
                    lastms=int(objects[-1].split(',')[2])
                    for a in metadata:
                        if 'BeatmapID' in a:
                            id=int(a.replace('BeatmapID:',''))
                            break
                        else:
                            id=None
                    threading.Thread(target=getstat).start()
#                    else:
#                        ranktype=
            else:
                lastms=1
                bpm=60000
                level=1
                #objects=['','']
                #metadata=beatmap[beatmap.index('[Metadata]')+1:]
#            for a in beatmap[:3]:
#                print(a)
#            sys.exit()
    except Exception as error:
        print('Could not load Song: '+str(error))
        crash(str(error))
        song_change(1)
def getstat():
    global ranktype,getpoints
    print('Loading...')
    req = urllib.request.Request(
    'https://api.osu.direct/v2/b/'+str(id), 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    })
    try:
        ranktypetmp=int(json.load(urllib.request.urlopen(req,timeout=2))['ranked'])
    except Exception as error:
        print(error,'(Returning as Unranked)')
        ranktypetmp=99
    print('Completed Rank Status')
    print('Status :',ranktypetmp)
    getpoints=0
    if id!=None:
        print(ranktypetmp)
    if ranktypetmp==3:
        print(rankmodes[2][0])
        ranktype=2
    elif ranktypetmp>0:
        print(rankmodes[0][0])
        ranktype=0
    else:
        print(rankmodes[1][0])
        ranktype=1
        getpoints=1
maxplay=1000
def resetscore():
    global score,barclicked,perf,scorew,bgcolour,objecon,combo,sre,health,healthtime,combotime,hits,last,stripetime,ppcounter,pptime,pptmp,modshow,ranking,playboard
    last=0

    playboard=[]
    healthtime=time.time()
    for players in range(1,maxplay+2):
        if players==maxplay-1:
                pass
                #playboard.append((username,(255,255,0),int((perf/maxperf)*1000000)))
                #print(players)
#                   render('text',text='#'+str(players)+' '+username,arg=((20, 70+(50*(players-1))),(255,255,0)))
#                   render('text',text=int((perf/maxperf)*1000000),arg=((20, 95+(50*(players-1))),(255,255,0),'min'))
        else:
            playboard.append(('DevUser #'+str(players),forepallete,(randint(1,1234567))))
    ranking=51
    health=100
    stripetime=[]
    objecon=0
    pptime=time.time()
    pptmp=0
    modshow=False
    ppcounter=0
    if activity==4:
        bgcolour=235
        combo=0
    sre=0
    combotime=0
    hits=[0,0,0,0]
    score=0
    scorew=score
    perf=0
    barclicked=[]
menuback=0
backspeed=1
replaymen=0
def beatres():
    global activity,replaymen
    if activity==5:
        if replaymen:
            title='Replay Screen'
        else:
            title='Results Screen'
        grade=(perf/maxperf)*100
        if grade>=100:
            gradet='X'
        elif grade>95:
            gradet='S'
        elif grade>90:
            gradet='A'
        elif grade>85:
            gradet='B'
        elif grade>69:
            gradet='C'
        elif grade<1:
            gradet='?'
        else:
            gradet='D'
        #render('rect',arg=((w//2-310,h//2-110,620,260),(100,100,150),False),borderradius=20)
        render('rect',arg=((w//2-305,h//2-105,610,250),(50,50,100),True),bordercolor=(30,30,80),borderradius=20)
        render('rect',arg=((w//2-300,h//2-100,600,40),(20,20,50),False),borderradius=20)
        render('rect',arg=((w//2-300+20,h//2-100+50,100,100),(20,20,100),False),borderradius=20)
        render('text', text=gradet, arg=((w//2-300+40,h//2-100+75), forepallete,'grade','center'),relative=(w//2-300+20,h//2-100+60,100,90))
        render('text', text='Score - '+str(format(score,',')), arg=((w//2-150,h//2-100+45), forepallete))
        render('text', text='pp - '+str(str(format(perf,',')))+'/'+str(str(str(format(maxperf,',')))), arg=((w//2-150,h//2-100+75), forepallete))
        render('text', text='300 - '+str(hits[0]), arg=((w//2-150,h//2-100+105), forepallete))
        render('text', text='100 - '+str(hits[1]), arg=((w//2-150,h//2-100+135), forepallete))
        render('text', text='50 - '+str(hits[2]), arg=((w//2-150,h//2-100+165), forepallete))
        render('text', text='Miss - '+str(hits[3]), arg=((w//2-150,h//2-100+195), forepallete))
        render('text', text=title, arg=((w//2-280,h//2-90), forepallete))
        butt=menu_draw(((w//2-280,h//2+75,100,40),),('Return',))
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
            if event.type  ==  pygame.MOUSEBUTTONDOWN:
                if butt:
                    if replaymen:
                        transitionprep(6)
                        replaymen=not replaymen
                    else:
                        transitionprep(3)
            if event.type  ==  pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if replaymen:
                        transitionprep(6)
                        replaymen=not replaymen
                    else:
                        transitionprep(3)
def shopdirect():
    global activity
    if activity==8:
        shoplist=[]
        sdol=18
        for a in range(1,6):
            dol=int(sdol**a)
            shoplist.append(('Shop Entry #'+str(a),dol))
        b=0
        render('rect', arg=((20,40,w-300,h-80), (50,50,50), False),borderradius=10)
        for a in shoplist:
            render('rect', arg=((40,60+(100*b),w-330,80), (50,50,80), False),borderradius=10)
            render('text', text=a[0], arg=((50,70+(100*b)), forepallete))
            render('text', text=format(a[1],',')+'$', arg=((50,90+(100*b)), forepallete))
            b+=1

        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()

            if event.type  ==  pygame.KEYDOWN:
                if event.key  ==  pygame.K_q or event.key  ==  pygame.K_ESCAPE:
                    transitionprep(1)
def sh():
    global activity
    if activity==8:
        pass

def change_diff():
    global diffcon,beatnowmusic
    if not diffcon+1>=len(diff):
        diffcon+=1
    else:
        diffcon=0
    beatnowmusic=1
def beatmenu():
    global activity,beatsel,beatnowmusic,menuback,cross,diffcon,hits,modshow,modsen,speedvel,scoremult,msg
    go=False
    if activity==3 or activity==7:
        a=0
        speed=0.05*speedvel[0]
        tmp=(h//60)//2
        if activity==7:
            soup=1
            sel=diffcon
            bp1=[]
            bp2=[]
            a=0
            for b in diff:
                bp1.append(((w//2-(cardsize//2)-((size+5)*diffcon)+((size+5)*(a)),(h//2-size)-((size+5)*diffcon)+((size+5)*(a)),cardsize,size)))
                bp2.append(str(b[1]))
                a+=1
            button=menu_draw(bp1,bp2,selected_button=sel+1,startlimit=int(cross[1])-tmp+1,endlimit=int(cross[1])+tmp,styleid=1)
        else:
            soup=0
            sel=beatsel
            button=menu_draw(p1,p2,selected_button=sel+1,startlimit=int(cross[0])-tmp+1,endlimit=int(cross[0])+tmp,styleid=1)
        if len(p2)==0:
            crok=999
        else:
            crok=0
        sysbuttonpos=(-10,h-50,100+menuback,40),(140,h-50+crok,100,40),
        if ranktype and not ranktype==3:
            if not modshow:
                of=110
            else:
                of=0
            render('rect', arg=((0,h-200+of,500,25), (50,50,130), False),borderradius=10)
            render('text', text='You will not earn Points!', arg=((0,0), forepallete,"center"),relative=(0,h-200+of,500,25))
        if modshow:
            render('rect', arg=((0,h-170,500,120), (30,30,80), False),borderradius=10)
            mod=menu_draw(((20,h-160,90,40),(20,h-110,90,40),(130,h-160,90,40),(130,h-110,90,40),(230,h-160,90,40),),("Auto",'Blind','Slice','EZ','Random'),enabled_button=modsen)
            render('text', text=str(scoremult)+'x', arg=((0,0), forepallete,"center"),relative=(315,h-170,200,120))
            if mod==1:
                msg='the game plays itself ooooo~'
            elif mod==2:
                msg='wait... this is a real mod-'
            elif mod==3:
                msg='half of the screen is gone'
            elif mod==4:
                msg="This doesn't do anything"
            elif mod==5:
                msg='ad8sad9989h'
        else:
            mod=0
            #mod=menu_draw(((20,h-160,80,40),),('Auto',),selected_button=modsen[0])
        render('rect', arg=((0,h-60,w,60), (50,50,100), False))
#        for systrocity in sysbuttonpos:
#            render('rect', arg=((systrocity), (100,100,150), True),bordercolor=(80,80,100),borderradius=10)
        gobutton=menu_draw(((w-125,h-75,120,70),),("->",),bigmode=True,styleid=1)
        sysbutton=menu_draw(sysbuttonpos,('Back','Mods'),styleid=1)
        if cross[soup]>sel-0.01 and cross[soup]>sel+0.01:
            cross[soup]-=speed*(drawtime)
            speedvel[soup]+=1
        elif int(round(cross[soup]))<sel:
            cross[soup]+=speed*drawtime
            speedvel[soup]+=1
        else:
            speedvel[soup]=0
        if sysbutton==1:
            if not menuback>=30:
                menuback+=backspeed
        else:
            if not menuback<=0:
                menuback-=backspeed
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
            if event.type  ==  pygame.MOUSEBUTTONDOWN:
                if sysbutton  ==  1:
                    if not activity==7:
                        transitionprep(1)
                    else:
                        transitionprep(3)
                elif sysbutton == 2:
                    modshow=not modshow
                    print(modshow)
                else:
                    if gobutton:        
                        if not activity==7:
                            transitionprep(7)
                        else:
                            go=True
                    else:
                        if mod:
                            for a in range(1,len(modsen)+1):
                                if mod==a:
                                    modsen[a-1]=not modsen[a-1]
                                    reloadstats()
                        else:
                            if button:
                                if button-1!=beatsel:
                                    beatnowmusic=1
                                    beatsel=button-1
                                else:
                                    if not activity==7:
                                        transitionprep(7)
                                    else:
                                        go=True
            if event.type  ==  pygame.KEYDOWN:
                if event.key  ==  pygame.K_RETURN:
                    if not activity==7:
                        transitionprep(7)
                    else:
                        go=True
                if event.key  ==  pygame.K_UP:
                    if activity!=7:
                        song_change(0)
                    else:
                        diff_change(0)
                if event.key  ==  pygame.K_DOWN:
                    if activity!=7:
                        song_change(1)
                    else:
                        diff_change(1)
                        
                if event.key  ==  pygame.K_e:
                    change_diff()
                if event.key  ==  pygame.K_F5:

                    if debugmode:
                        debugmode = False
                    else:
                        debugmode = True
                if event.key  ==  pygame.K_q or event.key  ==  pygame.K_ESCAPE:                    
                    if not activity==7:
                        transitionprep(1)
                    else:
                        transitionprep(3)
        tmp=0
        if maxperf>=1000:
            beatcol=rankdiffc[-1]
        elif maxperf>=800:
            beatcol=rankdiffc[3]
        elif maxperf>=80:
            beatcol=rankdiffc[2]
        elif maxperf>=31:
            beatcol=rankdiffc[1]
        elif maxperf<=30:
            beatcol=rankdiffc[0]
        beatname=rankdiff[rankdiffc.index(beatcol)]
        render('header')
        hax=300*(w//600)
        popupw=w//2-hax
        if len(p2)==0:
            render('text', text='No Beatmap Installed', arg=(offset, forepallete))
        else:
            #pass
            render('text', text=p2[beatsel], arg=(offset, forepallete))
            render('rect',arg=((popupw,40,hax*2,130),(50,50,100),False),borderradius=20)
            render('text', text=rankmodes[ranktype][0], arg=((popupw+20+hax,70), rankmodes[ranktype][1])) # Rank Type
            render('text', text=str(len(diff))+' Diff ['+str(diffcon)+']', arg=((popupw+20+hax,100), forepallete))
            render('text', text='BPM - '+str(int(60000/bpm)+1), arg=((popupw+20,70), forepallete))
            render('text', text=str(maxperf*0.01123)[:4]+' Stars', arg=((popupw+20,130), forepallete))
            render('text', text='Max pp - '+str(format(maxperf,',')), arg=((popupw+20,100), forepallete))
            render('rect', arg=((270-(bgcolour//2),h-45,140+bgcolour,30), (beatcol[0]-20,beatcol[1]-20,beatcol[2]-20), False),borderradius=10)
            render('rect', arg=((270,h-45,140,30), beatcol, False),borderradius=10)
            render('text', text=beatname, arg=((0,0), forepallete,"center"),relative=(270,h-45,140,30))
    if go:
        transitionprep(4)
        beatnowmusic=1
        resetscore()
        #render('text', text='E - Change Diff', arg=((140,h-45), forepallete))
def print_card(pp,score,name,pos,rank,isgrayed=False):
    if isgrayed:
        tmp=70,70,100
        tmpt=150,150,150
    else:
        tmp=50,50,100
        tmpt=forepallete
    if not pos[0]+300>w:
        render('rect',arg=((pos[0],pos[1],300,80),(tmp),False),borderradius=10)
        render('text', text=name+' (#'+str(rank)+')', arg=((pos[0]+10,pos[1]+10), tmpt))
        render('text', text='Score - '+str(format(int(score),',')), arg=((pos[0]+10,pos[1]+40), tmpt,'min'))
        render('text', text='pp - '+str(format(int(pp),',')), arg=((pos[0]+10,pos[1]+60), tmpt,'min'))
beka='None'
actto=activity
transb=0
transa=0
voltime=0
def volchg(t):
    global vol,voltime
    voltime=time.time()+1
    step=0.1
    if t:
        vol+=step
    else:
        if not vol<=0.01:
            vol-=step
def transitionto():
    global activity,transa,transb,actto
    if transb:
        render('rect', arg=((w-transa,0,w,h), (0,100,200), False),borderradius=10)
        if transa>=w and activity!=actto:
            activity=actto
        elif transa>=w+w+20:
            transa=0
            transb=0
        else:
            transa+=2
def transitionprep(act):
    global transa,transb,activity
    activity=act
#    transb=1
#    transa=0
def mainmenu():
    global debugmode, activity,beatnowmusic, totperf,totscore
    if activity==1:
        mmenu=((w//2-(button_size_width//2)-100,h//2-(button_size_height+10),button_size_width,button_size_height),
           (w//2-(button_size_width//2)-50,h//2-(button_size_height-30),button_size_width,button_size_height),
           (w//2-(button_size_width//2)+50,h//2-(button_size_height-70),button_size_width,button_size_height),
           (w//2-(button_size_width//2)+100,h//2-(button_size_height-110),button_size_width,button_size_height),)
#           (20,150,100,40),
#           )
        menubutton=menu_draw(mmenu, text=mtext)
        render('rect',arg=((0,0,w,45),(0,0,0),False))#,surf=surface[0])
#        for a in range(1,len(rankdiffc)+1):
#            render('rect',arg=((0+(60*(a-1)),h-150,50,20),rankdiffc[a-1],False),borderradius=20)
#        render('text', text=gametime/lastms, arg=((20,h-80), forepallete))
        #print(1-((gametime/(lastms+1000))))
        if gametime>=lastms+1000 or gametime<=-1:
            song_change(1)
        if gametime<=1000:
            tmp=(gametime/1000)*1
 #       elif gametime>=lastms-1000:
 #           tmp=1-((gametime/(lastms)))
 #           if tmp<=0:
 #               tmp=0
        else:
            tmp=1
        tmp2=tmp
        tmp=(255*tmp,255*tmp,255*tmp)
        if len(p2)!=0:
            render('text', text='Now Playing - '+p2[beatsel], arg=((20*(tmp2),10), tmp))
        else:
            render('text', text='Add Songs!', arg=((20*(tmp2),10), tmp))
        render('text', text='Note: you can get songs from osu.ppy.sh.', arg=((20,150), forepallete))
        print_card(totperf,totscore,username,(20,60),1)
        rank=2
        b=1
        if 0==1:
            for a in os.listdir(propath):
                if not username in a:
                    if os.path.isfile(propath+a+'/score'):
                        a1=int(open(propath+a+'/score').read().rstrip('\n'))
                        print(a1)
                    else:
                        a1=0
                    if os.path.isfile(propath+a+'/perf'):
                        a2=int(float(open(propath+a+'/perf').read().rstrip('\n')))
                    else:
                        a2=0
                    if rank==2:
                        print_card(a2,a1,a,(20+(320*b),60),rank,isgrayed=1)
                    else:
                        print_card(a2,a1,a,(20+(320*b),60),rank,isgrayed=1)
                    b+=1
                    rank+=1
        #print_card(totperf//2,totscore//2,'MiXer',(340,60),2,isgrayed=1)
        render('text', text=gamename+'/'+gameedition+' ('+str(gamever)+')', arg=((0,0), forepallete,'center'),relative=(w//2,h-30,0,0))
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
            if event.type  ==  pygame.MOUSEBUTTONDOWN:
                if menubutton  ==  1:
                    transitionprep(3)
                elif menubutton  ==  2:
                    transitionprep(2)
                elif menubutton  ==  3:
                    transitionprep(6)
                elif menubutton  ==  4:
                    stopnow()
                elif menubutton  ==  5:
                    transitionprep(8)
            if event.type  ==  pygame.KEYDOWN:
                if event.key  ==  pygame.K_MINUS:
                    volchg(0)
                if event.key  ==  pygame.K_EQUALS:
                    volchg(1)
                if event.key  ==  pygame.K_x:
                    pygame.mixer.music.set_pos((lastms-5000)*0.001)
                if event.key  ==  pygame.K_F5:
                    if debugmode:
                        debugmode = False
                    else:
                        debugmode = True
                if event.key  ==  pygame.K_q or event.key  ==  pygame.K_ESCAPE:
                    stopnow()
#        render('rect', arg=((-10,150,350,60), (maxt(40,bgcolour),maxt(40,bgcolour),maxt(100,bgcolour)), False),borderradius=10)
#        render('text', text='WILL CHANGE', arg=((25,155), (255,255,maxt(0,bgcolour)),'grade'))
        screen.blit(surface[0],(0,0))
        song_progress()
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
def spectrum():
    global bars
    for a in range(1,len(bars)+1):
        ral=random.randint(1,100)
        bars[a-1]=ral
        render('rect', arg=(((tal)*(a-1),h-ral,(tal),ral), (30,30,30), False),borderradius=10)
keys=[0,0,0,0]
keyslight=[0,0,0,0]
pos=(64,192,320,448)
tip=0
sre=0
def submit_score(perf,score,other=''):
    global totscore,totperf
    with open(profilepath+'perf','w') as x:
        x.write(str(perf))
    with  open(profilepath+'score','w') as x:
        x.write(str(score))
    with  open(profilepath+'scoreboard','a') as x:
        x.write(str(p2[beatsel])+';'+str(perf-totperf)+';'+str(score-totscore)+';'+other+'\n')
    totperf=perf
    totscore=score
def song_progress():
    render('rect', arg=((0,h-10,w,10), (50,50,50), False),borderradius=10)
    render('rect', arg=((0,h-10,(gametime/lastms)*w,10), (50,150,50), False),borderradius=10)
def iscatched(block,isauto,ob):
    lean=(perfect//2,great//2,ok//2,miss)
    tick=0
    #render('rect', arg=((0, keymap[0][1]-lean[0], lean[0]*2, lean[0]), (255,0,0), False))
    if block>=h-lean[3]:
        lastcall=True
        tick=3
    elif block>=keymap[0][1]-lean[0] and block<=keymap[0][1]+lean[0]:
        lastcall=True
        tick=0
    elif block>=keymap[0][1]-lean[1] and block<=keymap[0][1]+lean[1] and not isauto:
        lastcall=True
        tick=1
#    elif block>=keymap[0][1]-(lean[2]*2) and block<=keymap[0][1]+(lean[2]*2):
#        if keys:
#            lastcall=True
#            tick=3
#        else:
#            lastcall=False
    elif block>=keymap[0][1]-lean[2] and block<=keymap[0][1]+lean[2] and not isauto:
        lastcall=True
        tick=2
    else:
        lastcall=False
    return (lastcall,tick)
modsen[0]=1
def game():
    global activity,debugmode,beatnowmusic,fpsmode,score,scorew,bgcolour,totperf,totscore,objecon,healthtime,health,ranking,oldupdatetime,t,tip,gametime,combo,sre,combotime,sre,hits,last,stripetime,tmp,pptime,pptmp,ppcounter,perf
    if activity==4:
        if bgcolour>=1:
            bgcolour-=1
        playfield=(maxt(20,bgcolour),maxt(20,bgcolour),maxt(20,bgcolour))
        screen.fill(playfield)
        maxscore=300*len(objects)
        score=int((int((hits[0]*300)+(hits[1]*100)+(hits[2]*50))*scoremult)-(hits[3]*50))
        tmp=0.1
        sretemplate=(tmp-(time.time()-combotime))/tmp
        sre=(sretemplate)*20
        if sre<=0:
            sre=0
        #if reall<0:
        #    pygame.mixer.music.play(-1,0)

        b=0
        tot=perfbom*level
        perf=score*tot
        if int(maxperf)!=0:
            end=(score/maxscore)
        else:
            end=0
        if health<0:
            health=100
            transitionprep(3)
        elif health>=110:
            health=110
        t1=0.01
        maxt1=0.15
        if combo!=0:
            t1=t1*combo
        if t1>=maxt1:
            t1=maxt1
        reall=gametime
        #if iscatched(h//2+reall-(int(objects[-1].split(',')[2]))):
        if  gametime>=lastms+1000:# or combo>49:
            print('Completed')
            transitionprep(5)
            if 1==1:
                submit_score(totperf+perf,totscore+score,other=str(hits[0])+';'+str(hits[1])+';'+str(hits[2])+';'+str(hits[3])+';'+str(diffmode)+';'+str(level))
        ob=0
        temp=h//2+reall
        #for a in range(1,5):
#        render('rect', arg=((0,h-miss,w,miss), (250,0,0), False),borderradius=10)
#        render('rect', arg=((keymap[0][0],keymap[0][1]-(ok//2),keymap[0][2]*4,30+ok), (150,150,0), False),borderradius=10)
#        render('rect', arg=((keymap[0][0],keymap[0][1]-(great//2),keymap[0][2]*4,30+great), (0,180,0), False),borderradius=10)
#        render('rect', arg=((keymap[0][0],keymap[0][1]-(perfect//2),keymap[0][2]*4,30+perfect), (0,100,150), False),borderradius=10)
#        transition=0.3
#        for a in stripetime[:4]:
#            if time.time()-a[0]>transition:
#                stripetime.remove(a)
#            t=(transition-(time.time()-a[0]))*keymap[0][2]
#            render('rect', arg=((t+a[1],0,t,h), (150,150,150), False))
        render('rect', arg=((keymap[0][0],keymap[0][1]-10,keymap[0][2]*4,10), (100,140,220), False),borderradius=0)
        for a in keys:
            mopa=(0.1-(time.time()-keyslight[b]))/0.1
            if mopa<0:
                mopa=0
            co=(100,int(100+(20*mopa)),int(100+(120*mopa)))
            render('rect', arg=(keymap[b], co, False),borderradius=0)
            render('line',arg=((keymap[b][0],0),(255,255,255),(keymap[b][0],keymap[b][1]+30)))
            #render('text', text=str(mopa)[:6], arg=((0,0), forepallete, 'center'), relative=(keymap[b]))
            b+=1
        render('line',arg=((keymap[3][0]+100,0),(255,255,255),(keymap[3][0]+100,keymap[3][1]+30)))
        clicked=0
        hit=-1
        for a in objects[objecon:maxobjec+objecon]:
            tok=a.split(',')
            block=temp-(int(tok[2]))+(h//2)#(60000/333)
            if block <=h+100 and block>=-40:
                if ob==0:
                    if not end*1000000 >=999000:
                        health-=t1
                ob+=1
                notfound=True
                for kik in range(1,len(pos)+1):
                    if int(tok[0])==pos[kik-1]:
                        keypos=keymap[kik-1][0]
                        notfound=False
                        break
                if notfound:
                    for a in range(1,6):
                        if int(tok[0])>=512-(128*(a-1)):
                            keypos=keymap[a-1][0]
                notecolour=(25,64,255)
                if not (keypos,int(tok[2])) in barclicked:
                    if not modsen[1]:
                        render('rect', arg=((keypos,block-30,100,30), (notecolour), False),borderradius=0)
#                        render('text',text=block,arg=((keypos,block-30),forepallete))
                        #pygame.draw.line(screen,(255,255,255),(0,block),(w,block))
#                else:
#                    notecolour=(112, 168, 66)
                judge=iscatched(block,modsen[0],0)
                if modsen[0]:
                    if judge[0]:
                        keys[kik-1]=1
                        keyslight[kik-1]=time.time()
                    else:
                        keys[kik-1]=0
                if (judge[0] and keys[kik-1]) or judge[1]==3: 
                    hit=judge[1]
                    clicked=1
                    stripetime.append((keypos,int(tok[2])))
                if pygame.Rect.colliderect(pygame.Rect(0,h+20,w,20),pygame.Rect(keypos,block,100,30)):
                    objecon+=1
        if clicked:
            for notes in stripetime:
                if not (notes[0],int(notes[1])) in barclicked:
                    if hit==3:
                        health-=t1
                    else:
                        health+=10
                    hits[hit]+=1
                    bgcolour+=1
                    barclicked.append((notes[0],int(notes[1])))
                    #stripetime.append((time.time(),keypos))
                    if not hit==3:
                        combo+=1
                        t=a.split(':')[-1]
                        combotime=time.time()
                        if not t=='':
                            pygame.mixer.Sound(gamepath+realid+'/'+str(t)).play()
                            print('Played',t)
                    else:
                        combotime=time.time()
                        combo=0
            stripetime=[]
        if modsen[2]:
            render('rect', arg=((0,0,w,h//2), playfield, False))
        
        if ismulti:
            players=1
            t=1
            playboard[len(playboard)-1]=(username,(255,255,0),int(end*1000000))
            for tmp in sorted(playboard, key=lambda x: x[2],reverse=True):
                if tmp[0]==username:
                    pcolor=(50,50,150)
                else:
                    pcolor=(50,50,100)
                if tmp[0]==username:
                    ranking=players
                if ranking>=players-3 and ranking<=players+3:
                    render('rect', arg=((-30,65+(50*(t)),225,50), pcolor, False),borderradius=20)
                    #render('text',text='#'+str(players),arg=((20, 80+(50*(t))),(pcolor[0]-20,pcolor[1]-20,pcolor[2]-20)))
                    render('text',text=tmp[0],arg=((20, 70+(50*(t))),tmp[1])) #'#'+str(players)+' '+
                    render('text',text='#'+str(players)+' '+str(tmp[2]),arg=((20, 95+(50*(t))),tmp[1],'min'))
                    t+=1
                players+=1
        if end*1000000<0:
            t=(255,0,0)
        else:        
            t=forepallete
        render('rect', arg=((0,-20,w,55), (50,50,60), False),borderradius=20)
        render('rect', arg=((w//2-200,19,401,61), (50,50,80), False),borderradius=20)
        render('text',text=int(end*1000000),arg=((20, 20),t,'grade','center'),relative=(w//2-200,22,400,60))
        if combo!=0:
            comboo=str(format(int(combo),','))
            render('text',text=comboo+'x',arg=((40-sre, h-80),(255,0,0),'grade'))
            render('text',text=comboo+'x',arg=((40+sre, h-80),(0,0,255),'grade'))
            render('text',text=comboo+'x',arg=((40, h-80+sre),(0,255,0),'grade'))
            render('text',text=comboo+'x',arg=((40+sre, h-80-sre),forepallete,'grade'))
        #render('text',text=h//2+reall-(int(objects[0].split(',')[2])),arg=((20, 80),forepallete))
        render('text',text=str(hits),arg=((20, 130),forepallete))
        render('line',arg=((0,h-miss),(255,255,255),(w,h-miss)))
            

        if 0:
            render('text',text=int(score),arg=((20, 70),forepallete))
            render('text',text=int(maxscore),arg=((20, 100),forepallete))
            render('text',text=str(hits),arg=((20, 130),forepallete))
            render('text',text=str(((hits[0]+hits[1]+hits[2]+hits[3])/300*(hits[0]+hits[1]+hits[2]+hits[3]))),arg=((20, 150),forepallete))
            render('text',text=str(int(100-((hits[0]+hits[1]+hits[2]-hits[3])/len(objects))))+'%',arg=((20, 70),forepallete))
            render('text',text=str(diffmode),arg=((20, 100),forepallete))
            render('text',text='pp - '+str(perf),arg=((20, 130),forepallete))
            render('text',text='Max pp - '+str(maxperf),arg=((20, 160),forepallete))
            render('text',text=hits,arg=((20, 190),forepallete))
            render('text',text=str(len(objects))+'x MAX',arg=((20, 220),forepallete))
#            render('text',text=str(objecon)+'/'+str(maxobjec+objecon)+'/'+str(ob),arg=((20, 190),forepallete))
#            render('text',text=str(reall)+'/'+str(t),arg=((20, 220),forepallete))
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
            if event.type  ==  pygame.KEYDOWN:
                if event.key  ==  pygame.K_d:
                    keys[0]=1
                    keyslight[0]=time.time()
                if event.key  ==  pygame.K_f:
                    keys[1]=1
                    keyslight[1]=time.time()
                if event.key  ==  pygame.K_j:
                    keys[2]=1
                    keyslight[2]=time.time()
                if event.key  ==  pygame.K_k:
                    keys[3]=1
                    keyslight[3]=time.time()
                if event.key  ==  pygame.K_BACKQUOTE:
                    beatnowmusic=1
                    resetscore()
                if event.key  ==  pygame.K_q or event.key  ==  pygame.K_ESCAPE:
                    activity=3
            if event.type  ==  pygame.KEYUP:
                if event.key  ==  pygame.K_t:
                    tip=0
                if event.key  ==  pygame.K_d:
                    keys[0]=0
                if event.key  ==  pygame.K_f:
                    keys[1]=0
                if event.key  ==  pygame.K_j:
                    keys[2]=0
                if event.key  ==  pygame.K_k:
                    keys[3]=0
                if event.key  ==  pygame.K_F5:
                    if debugmode:
                        debugmode = False
                    else:
                        debugmode = True
        render('rect', arg=((w//2-200,5,400,10), (20,20,20), False),borderradius=10)
        #render('rect', arg=((w//2-200,50,((maxscore-score)/maxscore)*400,20), (255,0,0), True),borderradius=10)
        tmp=(health/100)*400
        if tmp<0:
            tmp=0
        elif tmp>400:
            tmp=400
        render('rect', arg=((w//2-200,5,tmp,10), (0,180,0), False),borderradius=10)
#        tmp=end*400
#        if tmp<0:
#            tmp=0
#        elif tmp>400:
#            tmp=400
#        render('rect', arg=((w//2-200,5,tmp,10), (0,150,0), False),borderradius=10)
        song_progress()
def maxt(t,o):
    if t+o>254:
        return 255
    elif t+o<t:
        return t
    else:
        return t+o
def mint(t,o):
    if t-o<1:
        return 0
    else:
        return t-o

def song_change(switch):
    global beatsel,beatnowmusic,diffcon
    if not switch:
        if not beatsel-1<=-1:
            beatsel-=1
        else:
            beatsel=len(p2)-1
    else:
        if not beatsel+1>=len(p2):
            beatsel+=1
        else:
            beatsel=0
    beatnowmusic=1
    diffcon=0
def diff_change(switch):
    global beatsel,beatnowmusic,diffcon
    if not switch:
        if not diffcon-1<=-1:
            diffcon-=1
        else:
            diffcon=len(diff)-1
    else:
        if not diffcon+1>=len(diff):
            diffcon+=1
        else:
            diffcon=0
    reloadstats()
def scoreboard():
    global debugmode,activity,crossboard,perf,hits,score,replaymen
    if activity==6:
        if not os.path.isfile(profilepath+'scoreboard'):
            tmp = fonts[0].render("Make Some Great Scores...",  True,  forepallete)
            centertext = tmp.get_rect(center=pygame.Rect(w//2,h//2+40,1,1).center)
            screen.blit(tmp,  centertext)
            tmp = fonts[0].render("No Scores yet o.o",  True,  forepallete)
            centertext = tmp.get_rect(center=pygame.Rect(w//2,h//2,1,1).center)
            screen.blit(tmp,  centertext)
            yes=False
        else:
            a=0
            yes=True
            warp=[]
            for x in open(profilepath+'scoreboard','r'):
                warp.append(x)
            for x in warp[::-1]:
                if crossboard==a:
                    clicked=0,150,0
                else:
                    clicked=50,50,50
                tarp=x.split(';')
                tarp[0]=tarp[0].split('-')
                tarp[-2]=tarp[-2].rstrip("\n")
                s=100
                pp=((float(tarp[3])*300)+(float(tarp[4])*100)+(float(tarp[5])*50)-(float(tarp[6])*300))*perfbom*float(tarp[-1])*scoremult
                hw=(w//2-(cardsize//2),(h//2-size)-((s+5)*crossboard)+((s+5)*(a)))
                render('rect',arg=((hw[0],hw[1],cardsize,s),(50,50,50),True),borderradius=20,bordercolor=clicked)
                render('rect',arg=((hw[0]+cardsize-140,hw[1],140,s),(100,50,50),False),borderradius=20)
                render('rect',arg=((hw[0]+cardsize-140,hw[1]+(s//2),140,s//2),(50,50,100),False),borderradius=20)
                render('text',text=tarp[0][1],arg=((hw[0]+20, hw[1]+20),forepallete))
                render('text',text=tarp[0][0]+' ('+str(tarp[-2])+')',arg=((hw[0]+20, hw[1]+45),forepallete,'min'))
                render('text',text='Score - '+format(int(float(tarp[2])),','),arg=((hw[0]+20, hw[1]+60),forepallete))
                render('text',text=str(int(float(tarp[1])))+'pp',arg=((hw[0]+cardsize-100, hw[1]+35),forepallete,'center'),relative=(hw[0]+cardsize-140,hw[1],140,s//2))
                render('text',text=str(int(float(pp)))+'pp ^',arg=((hw[0]+cardsize-100, hw[1]+35),forepallete,'center'),relative=(hw[0]+cardsize-140,hw[1]+(s//2),140,s//2))
#                print(tarp)
#                sys.exit()
                a+=1 
        render('header')
        render('text',text=gamename+' - ScoreBoard',arg=((20,20),forepallete))
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
            if event.type  ==  pygame.KEYDOWN:
                if yes:
                    if event.key  ==  pygame.K_RETURN:
                        score=int(float(tarp[2]))
                        perf=int(float(tarp[1]))
                        replaymen=0
                        transitionprep(5)
                    if event.key  ==  pygame.K_DOWN:
                        if crossboard+1>len(warp)-1:
                            crossboard=0
                        else:
                            crossboard+=1
                    if event.key  ==  pygame.K_UP:
                        if crossboard-1<0:
                            crossboard=len(warp)-1
                        else:
                            crossboard-=1
                if event.key  ==  pygame.K_F5:
                    if debugmode:
                        debugmode = False
                    else:
                        debugmode = True
                if event.key  ==  pygame.K_q or event.key  ==  pygame.K_ESCAPE:
                    activity=1
crox=[]
def logo():
    global activity,gameverfake,logoflashtime
    if activity==0:
        #if time.time()-logotime>1.5:
        #    activity=1
        toka=((1.5-(time.time()-logotime))/1)*190
        render('clear',arg=(0,0,0))
        if toka<=-1500:
            activity=1
        if toka<=-100:
            tokab=-100
        else:
            tokab=toka
        if not "gameverfake" in globals():
            gameverfake=str(gamever).split('.')
            gameverfake=[gameverfake[0],gameverfake[1],int(gameverfake[2])]
        if toka<=-500 and not gameverfake[2]>=32:
            gameverfake[2]+=0.1
            logoflashtime=time.time()
        if "logoflashtime" in globals():
            flash=((0.5-(time.time()-logoflashtime))/1)*1
        if gameverfake[2]>=32:
#            gamepre='Target is '
            gamepre=gamename+'/'+gameedition+' '
            hovcol=(255*flash,0,0)
            gamesuf='Starts Now'
#            gamesuf=str(gameverfake[0])+'/'+str(gameverfake[1])+'/'+str(int(gameverfake[2]))+'!'
            #render('rect', arg=((w//2-100+95+(tokab),h//2+45,200,10), (50,150,50),False),borderradius=10)
            prof=15*-flash
        else:
            gamepre=gamename+'/'
            crok=str(int(gameverfake[2]))
            if len(crok)==1:
                crok='0'+crok
            gamesuf=str(gameverfake[0])+'.'+str(gameverfake[1])+'.'+crok
            hovcol=forepallete
            prof=0
#        if toka<-1000:
            #titlelogo=randint(1,255),randint(1,255),randint(1,255)
#            pass
#        else:
        titlelogo=forepallete
        render('rect', arg=((w//2-100+95+(tokab),h//2-50,200,10), (hovcol),False),borderradius=10)
        render('text', text=gamepre+gamesuf, arg=((0,0), titlelogo,'center','grade'),relative=(w//2+100+(tokab),h//2,1,1))
        render('text', text='This Game is in Heavy Development', arg=((0,0), hovcol,'center'),relative=(w//2+100+(tokab),h//2+60+prof,1,1))
        render('text', text='', arg=((0,0), hovcol,'center'),relative=(w//2+100+(tokab),h//2+100+prof,1,1))
        render('rect', arg=((w//2+(190-toka),0,w+toka,h), (0,0,0),False))
        render('text', text='Branch: '+str(gameedition), arg=((10,10), (255,255,0),'min'))
        ef=0
        for e in greph:
            render('rect', arg=((10+(15*ef),30+(10*e),10,10), (hovcol),False),borderradius=10)
            ef+=1
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
            if event.type  ==  pygame.MOUSEBUTTONDOWN:
                activity=1
def debuginfo():
    if activity==99:
        render('header')
        render('text',text=gamename+' - Debug Info',arg=((20,20),forepallete))
        co=0
#        co2=0
        render('text',text='Game Name - '+str(gamename),arg=((20,70+(20*0)),forepallete))
        render('text',text='Game Version - '+str(gamever),arg=((20,70+(20*1)),forepallete))
        render('text',text='Slyph Engine Version - '+str(sylphenginever),arg=((20,70+(20*2)),forepallete))
#            co2+=1
        sysbutton=menu_draw(((-10,h-50,100,40),),('Back',))
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
            if event.type  ==  pygame.MOUSEBUTTONDOWN: 
                if sysbutton:
                    transitionprep(1)

            if event.type  ==  pygame.KEYDOWN:
                if event.key  ==  pygame.K_q:
                    transitionprep(1)



def main():
    global fps, activity, ingame, screen, settingskeystore,reloaddatabase, debugmode,sa,bgcolour,tick,scale,size,cardsize,bgtime,replaymen,allowed,posmouse,drawtime,scoremult,msg
    if gameedition!=gameeditions[0]:
        gs='/'+gameedition
    else:
        gs=''
    msg=''
    pygame.display.set_caption(gamename+gs+' '+str(gamever)+' ['+str(activity)+']')
    if not firstcom:
        pygame.display.set_icon(programIcon)
    pygame.mouse.set_visible(True)
    update=time.time()
    posmouse=pygame.mouse.get_pos()
#    if modsen[0]:
#        scoremult=1

    if time.time()-sa>0.1:
        sa=time.time()
        fps=int(clock.get_fps())
    allowed=[0,1,2,3,5,6,7,8,99]
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
            fpscolour=(150,0,0)
        else:
            fpscolour=(0,150,0)
        render('rect', arg=((w-127, of+15, 120, 65), (fpscolour), True), borderradius=15,bordercolor=(50,50,50))
        #render('rect', arg=((5, 5, struct, 5), (0,255,0), False), borderradius=10)
    fps_text = f'{fps}/{fpsmodes[fpsmode]}'
    render('text', text=fps_text, arg=((w - 120, 23), forepallete, 'center'), relative=(w - 127, of + 20, 120, 30))
    render('text', text=f'{updatetime}ms', arg=((w - 120, 43), forepallete, 'center'), relative=(w - 127, of + 45, 120, 30))        #render('text',text='TICK:'+str(tick)+'/'+str(gametime//bpm)+'/'+str(gametime)+'/'+str(bpm),arg=((20, 43),forepallete))
    #print((time.time()-gametime)/0.001)
#    if activity in allowed:
#        render('rect', arg=((posmouse[0]-10,posmouse[1]-10,20,20), (80,80,150), True),borderradius=10)
#    if not (posmouse[0],posmouse[1]) in crox:
#        crox.append((posmouse[0],posmouse[1]))
    pygame.display.update()
    drawtime=clock.tick(fpsmodes[fpsmode])/1000
    #print(drawtime)
def clear(color):screen.fill(color)
def crash(text):
    #
    bypass=0
    print(text)
    while not bypass:
        fullscreenchk()
        buttonm=((w//4+10, h//4+h//2-40, w//4-20, 30), (w//4+w//2-w//4-5, h//4+h//2-40, w//4-5, 30), )
        buttont=('Continue', 'Exit', )
        render('rect', arg=((w//4, h//4, w//2, h//2), (40, 40, 40), False), borderradius=10)
        render('rect', arg=((w//4+3, h//4+33, w//2-6, h//2-36), (20, 20, 20), False), borderradius=10)
        button=menu_draw(buttonm, text=buttont)
        render('text', text='Sworry!', arg=((w//4+8, h//4+8), forepallete))
        render('text', text=text, arg=((w//4+15, h//4+48), forepallete))
        pygame.display.update((w//4, h//4, w//2, h//2))
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
                sys.exit()
            if event.type  ==  pygame.MOUSEBUTTONDOWN:
                if button == 1:
                    bypass=1
                elif button == 2:
                    stopnow()
                    sys.exit()
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
        crash(str(error))

