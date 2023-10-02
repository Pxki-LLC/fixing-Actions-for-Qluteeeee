#!/usr/bin/python3
import random,pyaudio,re
import pygame, os, time, sys, threading, urllib.request, socket
nline='\n'
axe=0
gamename='Qlute'
gameedition='Closed Beta'
gamever='2023.10.02'
gameverspl=gamever.split('.')
#gameminserve=int(gameverspl[0])+((1+float(gameverspl[1]))*float(gameverspl[2]))
datapath='./data/'
gamepath=datapath+'beatmaps/'
username='Aquapoki'
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
button_selected=(170, 170, 170)
button_idle=(150, 150, 150)
stop=0
pygame.mixer.init()
sa=time.time()
gametime=0
ismusic=0
paths=datapath,gamepath,propath,profilepath
prestart=1
for a in paths:
    if not os.path.isdir(a):
        os.mkdir(a)
        print('Created', a.replace('./', ''))
langpack=open(datapath+'languages/en.lang').read().rstrip("\n").split(';')
mtext='Play','Options','Reset Card','ScoreBoard List','Exit'
debugmode=True
fps=0
update=False
offset=20,20
beatsel=0
beatnowmusic=1
score=0
maxperf=0
perfbom=(1*0.001/30)*1
diff=[]
diffmode=''
diffcon=0
reloadstats=0
bgcolour=0
perf=0
maxobjec=255
objecon=0
oldupdatetime=0
totscore=0
tick=0
combo=0
lastms=0
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

rankmodes=('Ranked',(100,200,100)),('Unranked',(200,100,100)),('In Review',(200,200,100)),
print('index '+str(len(langpack)-1))
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
    global settingskeystore, activity, screen, firstcom, change, limitfps, fpsmode
    if activity==2:
        if change:
            tmp=open(datapath+'settings.db', 'w')
            for a in settingskeystore:
                tmp.write(str(a)+'\n')
            tmp.close()
            change=False
        #settingskeystore[2], settingskeystore[1], fullscreen
        render('header')
        render('text', text=gamename + ' - '+langpack[3], arg=(offset, forepallete))
        setbutton=menu_draw((pygame.Rect(w//2-110,  offset[1]+60,  220,  button_size_height), pygame.Rect(10,  h-45,  w-20,  button_size_height), ), (langpack[6]+str(fpsmodes[fpsmode])+' ('+str(fpsmode)+')', '<--'))
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
            if event.type  ==  pygame.MOUSEBUTTONDOWN: 
                if setbutton  ==  1:
                    change=True
                    if fpsmode<1:
                        fpsmode=len(fpsmodes)-1
                    else:
                        fpsmode-=1
                    settingskeystore[3]=fpsmode
                elif setbutton  ==  2:
                    activity = 1

            if event.type  ==  pygame.KEYDOWN:
                if event.key  ==  pygame.K_q:
                    activity=1
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()
fontname=datapath+'font.ttf'
fonts = pygame.font.Font(fontname,  24),pygame.font.Font(fontname,  24//2),pygame.font.Font(fontname,  24*2)
clock=pygame.time.Clock()
activity=1
select=False
cross=0
crossboard=0
realid=''
def render(type, arg=(0, 0) ,  text='N/A', bordercolor=forepallete, borderradius=0):
#	print(type, arg, text)
    off=0
    try:
        if type == 'text':
            if "min" in arg:
                screen.blit(fonts[1].render(str(text),  True,  arg[1]),  arg[0])
            elif "grade" in arg:
                screen.blit(fonts[2].render(str(text),  True,  arg[1]),  arg[0])
            else:
                screen.blit(fonts[0].render(str(text),  True,  arg[1]),  arg[0])
        elif type == 'rect':
#			print(arg[0][0], arg[0][1], arg[0][2], arg[0][3])
            pygame.draw.rect(screen, arg[1], pygame.Rect(arg[0][0], arg[0][1], arg[0][2]-off, arg[0][3]-off), border_radius=borderradius)
            if arg[2]:
                pygame.draw.rect(screen, bordercolor, pygame.Rect(arg[0][0], arg[0][1], arg[0][2]-off, arg[0][3]-off), 2, border_radius=borderradius)
            ## This was for a "Wireframe" Like Square
#            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(arg[0][0], arg[0][1], arg[0][2], arg[0][3]), 1)
        elif type == 'header':
            render('rect', arg=((0, -40, w, 100), (50, 50, 100), False), borderradius=20)
        elif type == 'clear':
            screen.fill(arg[0])
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
    global w, h, w, h, screen, mmenu, button_size_width, firstcom,tal,keymap
    if not settingskeystore[0]:
        if not firstcom:
            w=800
            h=600
            w=w
            h=h
        else:
            w=screen.get_width()
            h=screen.get_height()
    flags=pygame.DOUBLEBUF|pygame.RESIZABLE|pygame.HWSURFACE
    bit=24
    if settingskeystore[0]:
        if not firstcom:
            screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN|flags, bit)
    else:
        if not firstcom:
            screen=pygame.display.set_mode((w, h), flags, bit)
    if not firstcom:
        firstcom=True
    ins=1
    if w >= screen.get_width():
        if not w-1 <= 320:
            w-=ins
    else:
        w+=1
    if h >= screen.get_height():
        if not h-1 <= 240:
            h-=ins
    else:
        h+=1
    button_size_width=w//2
    #mmenu=pygame.Rect(0, 0, 10, 10), pygame.Rect(20, 0, 10, 10), pygame.Rect(40, 0, 10, 10), pygame.Rect(60, 0, 10, 10), pygame.Rect(80, 0, 10, 10), 
    mmenu=(pygame.Rect(w//2-(button_size_width//2),h//2-(button_size_height+10),button_size_width,button_size_height),
           pygame.Rect(w//2-(button_size_width//2),h//2-(button_size_height-30),button_size_width,button_size_height),
           pygame.Rect(w//2-(button_size_width//2),h//2-(button_size_height-70),button_size_width//2,button_size_height),
           pygame.Rect(w//2-(button_size_width//2)+(button_size_width//2),h//2-(button_size_height-70),button_size_width//2,button_size_height),
           pygame.Rect(w//2-(button_size_width//2),h//2-(button_size_height-110),button_size_width,button_size_height),
           )
    tal=25*(w/25)//len(bars)
    keymap=((w//2-(50*4),h-60,100,30),(w//2-(50*2),h-60,100,30),(w//2-(50*0),h-60,100,30),(w//2-(50*-2),h-60,100,30),)
    hitperfect=keymap[0][1]
def textbox():
    global maxtext
    maxtext=24*(w//640+1)
    render('rect', arg=(((w - button_size_width) // 2,  ((h - button_size_height) // 2) + (button_size_height - 60), button_size_width,  60), (0, 0, 0), True), bordercolor=forepallete)
    if len(textbox_text)<maxtext:
        colortext=255, 255, 255
    else:
        colortext=255, 0, 0
    render('text', arg=(((w - button_size_width) // 2+10, ((h - button_size_height) // 2) + (button_size_height//4)), colortext), text=textbox_text)
def menu_draw(instruction, text=None, istextbox=False, selected_button=0):
    button=0
    if istextbox:
        button_selected=0, 0, 0
        button_idle=0, 0, 0
        highlight=100, 255, 100
        highlight_idle=255, 255, 255
    else:
        button_selected=120, 120, 150
        button_idle=100,100,120
        highlight=100,100,120
        highlight_idle=50, 50, 100
    for a in range(1,  len(instruction)+1):	
        if instruction[a-1].collidepoint(pygame.mouse.get_pos()):
            select=True
            buttcolour = button_selected
            if pygame.mouse.get_focused():
                button=a
        else:
            buttcolour = button_idle
            select=False
        if selected_button == a:
            render('rect', arg=((instruction[a-1]), buttcolour, True),borderradius=10, bordercolor=(0, 255, 0))
        elif select:
            render('rect', arg=((instruction[a-1]), buttcolour, True),borderradius=10,bordercolor=highlight)
        else:
            render('rect', arg=((instruction[a-1]), buttcolour, True),borderradius=10, bordercolor=highlight_idle)
        if not text == None:
            tmp = fonts[0].render(text[a-1],  True,  (255,  255,  255))
            centertext = tmp.get_rect(center=instruction[a-1].center)
            screen.blit(tmp,  centertext)
    return button
combotime=0
def beatmapload():
    global p2,p1,beatnowmusic,gametime,objects,wait,maxperf,diff,diffmode,level,ismusic,bpm,realid,prestart,beatsel,tick,lastms
    a=0
    p1=[]
    p2=[]
    tmp=[]
    for b in os.listdir(gamepath):
        tmp.append(str(b))
        p1.append((pygame.Rect(w//2-(cardsize//2),(h//2-size)-((size+5)*round(cross))+((size+5)*(a)),cardsize,size)))
        p2.append(str(b)[str(b).index(' ')+1:])
        a+=1
    if prestart:
        beatsel=random.randint(1,len(tmp))-1
        prestart=0
    if ismusic:
        gametime=pygame.mixer.music.get_pos()
        #pygame.mixer.music.set_pos(time.time()-gametime)
        #pass
#        if gametime<0:
#            gametime=0
        #pygame.mixer.music.play(-1,(time.time()-gametime))
    if beatnowmusic:
        gametime=0
        tick=0
#        if activity==4:
#            if int(time.time()-wait)>=1:
#                wait=time.time()+3
#                pygame.mixer.music.stop()
#        else:
#            wait=int(time.time())
        ah=os.listdir(gamepath+tmp[beatsel])
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
                realid=tmp[beatsel]
                pygame.mixer.music.load(gamepath+tmp[beatsel]+'/'+music)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.80)
                diff=[]
                pref=''
                for a in ah:
                    ax=re.findall(r'\[(.*?)\]', a)
                    if len(str(ax))>2:
                        diff.extend(ax)
                    if pref=='' and a.endswith('.osu'):
                        pref=a.replace('.osu','')
                        pref=pref[:pref.index('[')]
                diffmode=diff[diffcon]
                beatmap=open(gamepath+tmp[beatsel]+'/'+pref+'['+diffmode+']'+'.osu').read().rstrip('\n').split('\n')
                objects=beatmap[beatmap.index('[HitObjects]')+1:]
                difficulty=beatmap[beatmap.index('[Difficulty]')+1:]
                difficulty=difficulty[:difficulty.index('')]
                level=float(difficulty[2].split(':')[-1])+float(difficulty[1].split(':')[-1])+float(difficulty[0].split(':')[-1])
                bpm=float(beatmap[beatmap.index('[TimingPoints]')+1:][0].split(',')[1])
                maxperf=int((len(objects)*300)*(perfbom*level))
                lastms=int(objects[-1].split(',')[2])
                #objects=['','']
                #metadata=beatmap[beatmap.index('[Metadata]')+1:]
#            for a in beatmap[:3]:
#                print(a)
#            exit()
def resetscore():
    global score,barclicked,perf,scorew,bgcolour,objecon,combo,sre,combotime
    objecon=0
    if activity==4:
        bgcolour=235
        combo=0
    sre=0
    combotime=0
    score=0
    scorew=score
    perf=0
    barclicked=[]
menuback=0
backspeed=1
def beatres():
    global activity
    if activity==5:
        render('rect',arg=((w//2-310,h//2-110,620,220),(100,100,150),False),borderradius=10)
        render('rect',arg=((w//2-300,h//2-100,600,200),(50,50,100),False),borderradius=10)
        render('rect',arg=((w//2-300,h//2-100,600,40),(20,20,50),False),borderradius=10)
        render('rect',arg=((w//2-300+20,h//2-100+50,100,100),(20,20,100),False),borderradius=10)
        render('text', text='SS', arg=((w//2-300+40,h//2-100+75), forepallete,'grade'))
        render('text', text='Score - 6,969,696', arg=((w//2-150,h//2-100+45), forepallete,'grade'))
        render('text', text='pp - 1,500', arg=((w//2-150,h//2-100+95), forepallete,'grade'))
        render('text', text='Results Screen', arg=((w//2-280,h//2-90), forepallete))
        pygame.display.flip()
        time.sleep(1)
        activity=1
def beatdiff():
    pass
def beatmenu():
    global activity,beatsel,beatnowmusic,menuback,cross,diffcon
    if activity==3:
        resetscore()
        a=0
        speed=0.05
        button=menu_draw(p1,p2,selected_button=beatsel+1)
        sysbutton=menu_draw((pygame.Rect(-10,h-50,100+menuback,40),),('Back',))
        if cross>=beatsel:
            cross-=speed
        else:
            cross+=speed
        if sysbutton:
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
                    activity = 1
                else:
                    if button:
                        if button-1!=beatsel:
                            beatnowmusic=1
                        beatsel=button-1
            if event.type  ==  pygame.KEYDOWN:
                if event.key  ==  pygame.K_RETURN:
                    activity=4
                    beatnowmusic=1
                if event.key  ==  pygame.K_UP:
                    song_change(0)
                if event.key  ==  pygame.K_DOWN:
                    song_change(1)
                if event.key  ==  pygame.K_e:
                    if not diffcon+1>=len(diff):
                        diffcon+=1
                    else:
                        diffcon=0
                    beatnowmusic=1
                if event.key  ==  pygame.K_F5:

                    if debugmode:
                        debugmode = False
                    else:
                        debugmode = True
                if event.key  ==  pygame.K_q or event.key  ==  pygame.K_ESCAPE:
                    activity=1
        if maxperf>=500:
            tmp=2
        elif maxperf<=2:
            tmp=1
        else:
            tmp=0
        render('header')
        hax=300*(w//600)
        popupw=w//2-hax
        render('rect',arg=((popupw,40,hax*2,130),(50,50,100),False),borderradius=20)
        render('text', text=rankmodes[tmp][0], arg=((popupw+20+hax,70), rankmodes[tmp][1]))
        render('text', text=str(len(diff))+' Diff ['+str(diffcon)+']', arg=((popupw+20+hax,100), forepallete))
        render('text', text=str(diffmode), arg=((popupw+20+hax,130), forepallete))
        render('text', text='BPM - '+str(int(60000/bpm)+1), arg=((popupw+20,70), forepallete))
        render('text', text='Max Score - '+str(format(len(objects)*300,',')), arg=((popupw+20,100), forepallete))
        render('text', text='Max pp - '+str(format(maxperf,',')), arg=((popupw+20,130), forepallete))
        #render('text', text='Max pp - '+str(format(lastms,',')), arg=((popupw+20,170), forepallete))
        #render('rect', arg=((-5, offset[1]+40, w+10, h-120), (0, 0, 0), True), bordercolor=forepallete)
        if len(p2)==0:
            render('text', text='No Beatmap Installed', arg=(offset, forepallete))
        else:
            render('text', text=p2[beatsel], arg=(offset, forepallete))
        render('text', text='E - Change Diff', arg=((140,h-45), forepallete))
def print_card(pp,score,name,pos,rank,isgrayed=False):
    if isgrayed:
        tmp=70,70,100
        tmpt=150,150,150
    else:
        tmp=50,50,100
        tmpt=forepallete
    render('rect',arg=((pos[0],pos[1],300,80),(tmp),False),borderradius=10)
    render('text', text=name+' (#'+str(rank)+')', arg=((pos[0]+10,pos[1]+10), tmpt))
    render('text', text='Score - '+str(format(int(score),',')), arg=((pos[0]+10,pos[1]+40), tmpt,'min'))
    render('text', text='pp - '+str(format(int(pp),',')), arg=((pos[0]+10,pos[1]+60), tmpt,'min'))

def mainmenu():
    global debugmode, activity,beatnowmusic, totperf,totscore
    if activity==1:
        menubutton=menu_draw(mmenu, text=mtext)
        render('rect',arg=((0,0,w,45),(0,0,0),False))
        render('text', text='Now Playing - '+p2[beatsel], arg=((20,10), forepallete))
        print_card(totperf,totscore,username,(20,60),1)
        rank=2
        b=1
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
        render('text', text=gamename+' '+gameedition+' ('+str(gamever)+')', arg=((20,h-40), forepallete))

        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
            if event.type  ==  pygame.MOUSEBUTTONDOWN:
                if menubutton  ==  1:
                    activity = 3
                elif menubutton  ==  2:
                    activity = 2
                elif menubutton  ==  3:
                    if os.path.isfile(profilepath+'perf'):
                        os.remove(profilepath+'perf')
                    if os.path.isfile(profilepath+'score'):
                        os.remove(profilepath+'score')
                    if os.path.isfile(profilepath+'scoreboard'):
                        os.remove(profilepath+'scoreboard')
                    totperf=0
                    totscore=0
                    print('Card Reset')
                elif menubutton  ==  4:
                    activity=6
                elif menubutton  ==  5:
                    stopnow()
            if event.type  ==  pygame.KEYDOWN:
                if event.key  ==  pygame.K_F5:
                    if debugmode:
                        debugmode = False
                    else:
                        debugmode = True
                if event.key  ==  pygame.K_q or event.key  ==  pygame.K_ESCAPE:
                    stopnow()
#tmp!!!!
msgx=0
messagetime=0
change=False
colorstep = 0
loaded=[]
ama=0
bars=[0,0,0,0]
t=''
#hitperfect=keymap[0][1]
#hitperfect=keymap[0][1]

def spectrum():
    global bars
    for a in range(1,len(bars)+1):
        ral=random.randint(1,100)
        bars[a-1]=ral
        render('rect', arg=(((tal)*(a-1),h-ral,(tal),ral), (30,30,30), False),borderradius=10)
keys=[0,0,0,0]
pos=(64,192,320,448)
def iscatched(block):
    lean=30*2
    return block>=keymap[0][1]-lean and block<=keymap[0][1]+lean
tip=0
sre=0
def submit_score(perf,score):
    global totscore,totperf
    with open(profilepath+'perf','w') as x:
        x.write(str(perf))
    with  open(profilepath+'score','w') as x:
        x.write(str(score))
    with  open(profilepath+'scoreboard','a') as x:
        x.write(str(p2[beatsel])+';'+str(perf-totperf)+';'+str(score-totscore)+'\n')
    totperf=perf
    totscore=score
def game():
    global activity,debugmode,beatnowmusic,fpsmode,score,scorew,bgcolour,totperf,totscore,objecon,oldupdatetime,t,tip,gametime,combo,sre,combotime,sre
    if activity==4:
        if bgcolour>=1:
            bgcolour-=1
        screen.fill((maxt(20,bgcolour),maxt(20,bgcolour),maxt(20,bgcolour)))
        maxscore=300*len(objects)
        score=len(barclicked)*300
        tmp=0.1
        sre=((tmp-(time.time()-combotime))/tmp)*20
        if sre<=0:
            sre=0
        combo=len(barclicked)
        #if reall<0:
        #    pygame.mixer.music.play(-1,0)

        b=0
        if maxperf<1:
            perf=0
        else:
            perf=score*perfbom*level
        reall=gametime
        for a in keys:
            if a:
                co=(50,50,200)
            else:
                co=(50,50,50)

            render('rect', arg=(keymap[b], co, True),borderradius=10)
            b+=1
        #if iscatched(h//2+reall-(int(objects[-1].split(',')[2]))):
        if  gametime>=lastms+1000:# or combo>49:
            print('Completed')
            activity=3
            submit_score(totperf+perf,totscore+score)
        ob=0
        temp=h//2+reall
        for a in objects[objecon:maxobjec+objecon]:
            tok=a.split(',')
            block=temp-(int(tok[2]))#+(60000/333)
            if block <=h and not block<=0:
                ob+=1
                for kik in range(1,len(pos)+1):
                    if int(tok[0])==pos[kik-1]:
                        keypos=keymap[kik-1][0]
                        break
                if not (keypos,int(tok[2])) in barclicked:
                    #if iscatched(block) and keys[kik-1]: 
                    if pygame.Rect.colliderect(pygame.Rect(keypos,block-50,100,100),keymap[kik-1]):# and keys[kik-1]:
                        barclicked.append((keypos,int(tok[2])))
                        objecon+=1
                        t=a.split(':')[-1]
                        combotime=time.time()
                        if not t=='':
                            pygame.mixer.Sound(gamepath+realid+'/'+str(t)).play()
                            print('Played',t)
                        if not bgcolour>=155:
                            bgcolour+=5

                render('rect', arg=((keypos,block,100,30), (255-bgcolour,255-bgcolour,255-(bgcolour)), False),borderradius=10)
        render('text',text=int((perf/maxperf)*1000000),arg=((20, 20),forepallete,'grade'))
        render('text',text=str(int(combo))+'x',arg=((20-sre, h-60),(255,0,0),'grade'))
        render('text',text=str(int(combo))+'x',arg=((20+sre, h-60),(0,0,255),'grade'))
        render('text',text=str(int(combo))+'x',arg=((20, h-60+sre),(0,255,0),'grade'))
        render('text',text=str(int(combo))+'x',arg=((20+sre, h-60-sre),forepallete,'grade'))
        #render('text',text=h//2+reall-(int(objects[0].split(',')[2])),arg=((20, 80),forepallete))
        if 1:
            render('text',text=str(int((score/maxscore)*100))+'%',arg=((20, 70),forepallete))
            render('text',text=str(diffmode),arg=((20, 100),forepallete))
            render('text',text='pp - '+str(perf),arg=((20, 130),forepallete))
            render('text',text='Max pp - '+str(maxperf),arg=((20, 160),forepallete))
            render('text',text=str(objecon)+'/'+str(maxobjec+objecon)+'/'+str(ob),arg=((20, 190),forepallete))
            render('text',text=str(reall)+'/'+str(t),arg=((20, 220),forepallete))
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
            if event.type  ==  pygame.KEYDOWN:
                if event.key  ==  pygame.K_d:
                    keys[0]=1
                if event.key  ==  pygame.K_f:
                    keys[1]=1
                if event.key  ==  pygame.K_j:
                    keys[2]=1
                if event.key  ==  pygame.K_t:
                    tip=1
                if event.key  ==  pygame.K_k:
                    keys[3]=1
                if event.key  ==  pygame.K_BACKQUOTE:
                    beatnowmusic=1
                    resetscore()
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
                if event.key  ==  pygame.K_q or event.key  ==  pygame.K_ESCAPE:
                    activity=1
        render('rect', arg=((w//2-200,50,400,20), (0,0,0), True),borderradius=10)
        #render('rect', arg=((w//2-200,50,((maxscore-score)/maxscore)*400,20), (255,0,0), True),borderradius=10)
        render('rect', arg=((w//2-200,50,(perf/maxperf)*400,20), (0,255,0), True),borderradius=10)
        render('rect', arg=((0,h-10,w,10), (50,50,50), False),borderradius=10)
        render('rect', arg=((0,h-10,(gametime/lastms)*w,10), (50,150,50), False),borderradius=10)
def maxt(t,o):
    if t+o>254:
        return 255
    else:
        return t+o

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
            beatsel=len(p2)-1
    beatnowmusic=1
    diffcon=0
def scoreboard():
    global debugmode,activity,crossboard
    if activity==6:
        if not os.path.isfile(profilepath+'scoreboard'):
            tmp = fonts[0].render("Make Some Great Scores!",  True,  forepallete)
            centertext = tmp.get_rect(center=pygame.Rect(w//2,h//2+40,1,1).center)
            screen.blit(tmp,  centertext)
            tmp = fonts[0].render("No Scores Yet!",  True,  forepallete)
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
                s=100
                hw=(w//2-(cardsize//2),(h//2-size)-((s+5)*crossboard)+((s+5)*(a)))
                render('rect',arg=((hw[0],hw[1],cardsize,s),(50,50,50),True),borderradius=20,bordercolor=clicked)
                render('rect',arg=((hw[0]+cardsize-140,hw[1],140,s),(50,50,100),False),borderradius=20)
                render('text',text=tarp[0],arg=((hw[0]+20, hw[1]+20),forepallete))
                render('text',text='Score - '+format(int(tarp[2]),','),arg=((hw[0]+20, hw[1]+60),forepallete))
                render('text',text=str(int(float(tarp[1])))+'pp',arg=((hw[0]+cardsize-100, hw[1]+35),forepallete))
                a+=1 
        render('header')
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
            if event.type  ==  pygame.KEYDOWN:
                if yes:
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
def main():
    global fps, activity, ingame, screen, settingskeystore, debugmode,sa,bgcolour,tick,scale,size,cardsize
    pygame.display.set_caption(gamename+' '+str(gamever))
    pygame.mouse.set_visible(True)
    update=time.time()

    if time.time()-sa>0.1:
        sa=time.time()
        fps=int(clock.get_fps())
    allowed=[1,2,3,5,6]
    fullscreenchk()
    size=60
    scale=(w//300)
    if scale>=3:
        scale=3
    cardsize=(300*scale)
    if activity==2:
        ingame=True
    else:
        ingame=False
    if activity in allowed:
        clear((maxt(20,bgcolour),maxt(20,bgcolour),maxt(50,bgcolour)))
        if bgcolour>=1:
            bgcolour-=1
        if "bpm" in globals() and gametime//bpm>tick:
            tick+=1
            bgcolour=50
    beatmapload()
    beatres()
    mainmenu()
    settingspage()
    beatmenu()
    game()
    scoreboard()
        #spectrum()
    if debugmode:
        updatetime=str((time.time()-update)/0.001)[:4]
        if updatetime[-1]=='.':
            updatetime=updatetime[:len(updatetime)-1]
        if (time.time()-update)/0.001>=6:
            fpscolour=(150,0,0)
        else:
            fpscolour=(0,150,0)
        render('rect', arg=((w-107, 15, 100, 60), (fpscolour), True), borderradius=15,bordercolor=(50,50,50))
        #render('rect', arg=((5, 5, struct, 5), (0,255,0), False), borderradius=10)
        render('text',text='FPS:'+str(fps),arg=((w-100, 23),forepallete))
        render('text',text=updatetime+'ms',arg=((w-100, 43),forepallete))
        #render('text',text='TICK:'+str(tick)+'/'+str(gametime//bpm)+'/'+str(gametime)+'/'+str(bpm),arg=((20, 43),forepallete))
        oldupdatetime=updatetime
    #print((time.time()-gametime)/0.001)
    pygame.display.update()
    clock.tick(fpsmodes[fpsmode])
def clear(color):screen.fill(color)
def crash(text):
    #
    bypass=0
    print(text)
    while not bypass:
        fullscreenchk()
        buttonm=(pygame.Rect(w//4+10, h//4+h//2-40, w//4-20, 30), pygame.Rect(w//4+w//2-w//4-5, h//4+h//2-40, w//4-5, 30), )
        buttont=('Continue', 'Exit', )
        render('rect', arg=((w//4, h//4, w//2, h//2), (40, 40, 40), False), borderradius=10)
        render('rect', arg=((w//4+3, h//4+33, w//2-6, h//2-36), (20, 20, 20), False), borderradius=10)
        button=menu_draw(buttonm, text=buttont)
        render('text', text=langpack[5], arg=((w//4+8, h//4+8), forepallete))
        render('text', text=text, arg=((w//4+15, h//4+48), forepallete))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
                exit()
            if event.type  ==  pygame.MOUSEBUTTONDOWN:
                if button == 1:
                    bypass=1
                elif button == 2:
                    stopnow()
                    exit()
if __name__  ==  "__main__":
    try:
        while True:
            if stop:
                exit()
            main()
    except Exception as error:
        crash(str(error))

