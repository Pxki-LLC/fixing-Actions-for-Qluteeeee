def song_progress():
    render('rect', arg=((0,h-10,w,10), (50,50,50), False),borderradius=10)
    render('rect', arg=((0,h-10,(gametime/lastms)*w,10), (50,150,50), False),borderradius=10)
def iscatched(block,isauto,ob):
    lean=(perfect,great,ok,miss)
    tick=0
    #render('rect', arg=((0, keymap[0][1]-lean[0], lean[0]*2, lean[0]), (255,0,0), False))
    if block>=h-lean[3]:
        lastcall=True
        tick=3
    elif block>=keymap[0][1]-lean[0] and block<=keymap[0][1]:
        lastcall=True
        tick=0
    elif block>=keymap[0][1]-lean[1] and block<=keymap[0][1] and not isauto:
        lastcall=True
        tick=1
#    elif block>=keymap[0][1]-(lean[2]*2) and block<=keymap[0][1]+(lean[2]*2):
#        if keys:
#            lastcall=True
#            tick=3
#        else:
#            lastcall=False
    elif block>=keymap[0][1]-lean[2] and block<=keymap[0][1] and not isauto:
        lastcall=True
        tick=2
    else:
        lastcall=False
    return (lastcall,tick)
def game():
    global activity,debugmode,beatnowmusic,fpsmode,score,scorew,keyspeed,bgcolour,totperf,totscore,objecon,healthtime,health,ranking,oldupdatetime,t,tip,gametime,combo,sre,combotime,sre,hits,last,stripetime,tmp,pptime,pptmp,ppcounter,perf
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
#        render('rect', arg=((keymap[0][0],keymap[0][1]-(perfect),keymap[0][2]*4,perfect), (0,100,150), False),borderradius=10)
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
        tip=1
        for a in objects[objecon:maxobjec+objecon]:
            tok=a.split(',')
            #tipa=13720/keyspeed
            block=temp-(int(tok[2]))+(h//2)#(60000/333)
            if block <=h+100 and block>=-40:
                if ob==0:
                    if not end*1000000 >=999000 and health>5:
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
                        if a-1>=4:
                            ax=3
                        else:
                            ax=a-1
                        if int(tok[0])>=512-(128*(a-1)):
                            keypos=keymap[ax][0]
                            break
                notecolour=(25,64,255)
                if not (keypos,int(tok[2])) in barclicked:
                    if not modsen[1]:
                        if tip:
                            render('rect', arg=((keypos,block-30,100,30), (notecolour), False),borderradius=0)
                        else:
                            render('rect', arg=((keypos,block-30,100,30), (notecolour), False),borderradius=0)
                        tip=not tip
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
                        health-=t1
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
#        render('text',text='Key Speed: '+str(keyspeed)+' ('+str(0)+'ms)',arg=((20, 70),forepallete))
            

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
#                if event.key  ==  pygame.K_e:
#                    if keyspeed-1:
#                        keyspeed-=1
#                if event.key  ==  pygame.K_r:
#                    keyspeed+=1
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
