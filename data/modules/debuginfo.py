def debuginfo():
    if activity==99:
        render('header')
        render('text',text=gamename+' - Debug Info',arg=((20,20),forepallete))
        co=0
#        co2=0
        render('text',text='Game Name - '+str(gamename),arg=((20,70+(20*0)),forepallete))
        render('text',text='Game Version - '+str(gamever),arg=((20,70+(20*1)),forepallete))
        render('text',text='Slyph Engine Version - '+str(sylphenginever),arg=((20,70+(20*2)),forepallete))
        render('text',text='Module Initial Time - '+str(moduletime),arg=((20,70+(20*3)),forepallete))
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
