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
        changed=totrank-prevrank
        if changed>totrank:
            chap=''
            chac=(150,50,50)
        elif changed<totrank:
            chap='+'
            chac=(50,150,50)
        scale=(w//800,h//600)
        scrop=(w//2-((100//2)*scale[0]),(h//2-((460//2)*scale[1])),100*scale[0],100*scale[1])
        pup=[hits[0],hits[1],hits[2],hits[3]]
        a1=0
        for a in pup:
            if a>99:
                pup[a1]='99+'
            else:
                pup[a1]=str(a)
            a1+=1
        #render('rect',arg=((w//2-310,h//2-110,620,260),(100,100,150),False),borderradius=20)
        render('rect',arg=((w//2-((300//2)*scale[0]),(h//2-((500//2)*scale[1])),300*scale[0],500*scale[1]),(50,50,100),True),bordercolor=(30,30,80),borderradius=20)
        render('rect',arg=(scrop,(20,20,100),False),borderradius=20)
        render('text', text=gradet, arg=((0,0), forepallete,'grade','center'),relative=scrop)
        render('text', text=str(format(int(perf/maxperf*1000000),',')), arg=((0,0), forepallete,'grade','center'),relative=(scrop[0],scrop[1]+100,scrop[2],scrop[3]))
        render('text', text='pp - '+str(str(format(perf,',')))+'/'+str(str(str(format(maxperf,',')))), arg=((w//2-150,h//2-100+75), forepallete,'center'),relative=(scrop[0],scrop[1]+150,scrop[2],scrop[3]))
        render('text', text='300 - '+str(pup[0]), arg=((w//2-150,h//2-100+105), forepallete,'center'),relative=(scrop[0]-80,scrop[1]+180,scrop[2],scrop[3]))
        render('text', text='100 - '+str(pup[1]), arg=((w//2-150,h//2-100+135), forepallete,'center'),relative=(scrop[0],scrop[1]+180,scrop[2],scrop[3]))
        render('text', text='50 - '+str(pup[2]), arg=((w//2-150,h//2-100+165), forepallete,'center'),relative=(scrop[0]+80,scrop[1]+180,scrop[2],scrop[3]))
        render('text', text='Miss - '+str(pup[3]), arg=((w//2-150,h//2-100+195), forepallete,'center'),relative=(scrop[0],scrop[1]+210,scrop[2],scrop[3]))
        render('text', text='Overall Rank - #'+str(format(totrank,',')), arg=((0,0), forepallete,'center'),relative=(scrop[0],scrop[1]+240,scrop[2],scrop[3]))
        if changed!=totrank and changed!=0:
            render('text', text=chap+str(format(-changed,',')), arg=((0,0), chac,'center'),relative=(scrop[0]+60,scrop[1]+260,scrop[2],scrop[3]))
        render('text', text=title, arg=((20,20), forepallete))
        butt=menu_draw(((scrop[0]-90,scrop[1]+400,scrop[2]*3-20,scrop[3]//2),),('Return',))
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
