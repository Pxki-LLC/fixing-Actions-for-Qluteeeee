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
