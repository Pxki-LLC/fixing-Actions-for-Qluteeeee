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
        render('text',text=gamename+' - Recent Plays',arg=((20,20),forepallete))
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
