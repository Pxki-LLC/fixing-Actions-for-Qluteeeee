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
