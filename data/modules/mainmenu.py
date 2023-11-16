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
        print_card(totperf,totscore,username,(20,60),totrank)
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
