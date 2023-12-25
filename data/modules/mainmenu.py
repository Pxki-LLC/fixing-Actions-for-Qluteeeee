mtext='Play','','Top Plays','Leave'
toptext='Settings','Account'
menupos=[]
opacity=10
bgdefaultcolour=(45,47,99)
mainmenucolor=((47,75,107),(67,56,105))
for a in range(1,len(mtext)+1):
    menupos.extend([0])
print(menupos)
def mainmenu():
    global debugmode, activity,beatnowmusic, totperf,totscore,msg
    if activity==1 or activity==9:
        mmenu=[]
        tmenu=[]
        #wid=90*(w//640)
        wid=90*2
        wod=45
        if wid>90*2:
            wid=90*2
        for a in range(1,len(mtext)+1):
            mmenu.append((w//2-(int(wid*(len(mtext)/2)))+(wid*(a-1)),h//2-75,wid,150))
        for a in range(1,len(toptext)+1):
            tmenu.append((w-((20*len(toptext[a-1]))*(a))+25,0,20*len(toptext[a-1]),wod))
        render('rect', arg=((0,h//2-75,w,150), blend(opacity,bgcolour), False))
        menubutton=menu_draw(mmenu, text=mtext,isblade=True,ishomemenu=True)
        render('rect',arg=((0,0,w,45),blend(opacity,bgcolour),False))#,surf=surface[0])
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
        topbutton=menu_draw(tmenu, text=toptext,isblade=True,ignoremove=True,ishomemenu=True)
        render('text', text='Note: you can get songs from osu.ppy.sh.', arg=((20,55), forepallete))
        print_card(totperf,totscore,username,(w,h-150),totrank,mini=True)
        if totrank==1:
            t=2
        else:
            t=1
        #print_card(oneperf,oneperf*10*10*300,'Monstras',(340,60),t)
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
        if menubutton == 1:
            msg='You have '+str(format(len(p2),','))+' Songs'
        else:
            msg=''
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
            if event.type  ==  pygame.MOUSEBUTTONDOWN:
                if menubutton  ==  1:
                    transitionprep(3)
                elif menubutton  ==  3:
                    transitionprep(6)
                elif menubutton  ==  4:
                    stopnow()
                elif menubutton  ==  5:
                    transitionprep(8)
                elif topbutton  ==  1:
                    transitionprep(2)
                elif topbutton  ==  2:
                    if activity==9:
                        transitionprep(1)
                    else:
                        transitionprep(9)

            if event.type  ==  pygame.KEYDOWN:
                if event.key  ==  pygame.K_MINUS:
                    volchg(0)
                if event.key  ==  pygame.K_EQUALS:
                    volchg(1)
                if event.key  ==  pygame.K_F5:
                    if debugmode:
                        debugmode = False
                    else:
                        debugmode = True
                if event.key  ==  pygame.K_q or event.key  ==  pygame.K_ESCAPE:
                    stopnow()
        if activity==9:
            render('rect', arg=((tmenu[1][0]-(350//2),tmenu[1][1]+55,350,250), (20,20,20), False),borderradius=10)
            render('text', text='Placeholder', arg=((0,0), (255,255,255),'center'),relative=(tmenu[1][0]-(350//2),tmenu[1][1]+55,350,250))


#        render('rect', arg=((-10,150,350,60), (maxt(40,bgcolour),maxt(40,bgcolour),maxt(100,bgcolour)), False),borderradius=10)
#        render('text', text='WILL CHANGE', arg=((25,155), (255,255,maxt(0,bgcolour)),'grade'))
        screen.blit(surface[0],(0,0))
        song_progress()
