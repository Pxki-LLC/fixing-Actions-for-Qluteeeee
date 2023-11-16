def beatmenu():
    global activity,beatsel,beatnowmusic,menuback,cross,diffcon,hits,modshow,modsen,speedvel,scoremult,msg
    go=False
    if activity==3 or activity==7:
        a=0
        tmp=(h//60)//2
        if activity==7:
            soup=1
            sel=diffcon
            bp1=[]
            bp2=[]
            a=0
            for b in diff:
                bp1.append(((w//2-(cardsize//2)-((size+5)*cross[1])+((size+5)*(a)),(h//2-size)-((size+5)*cross[1])+((size+5)*(a)),cardsize,size)))
                bp2.append(str(b[1]))
                a+=1
            button=menu_draw(bp1,bp2,selected_button=sel+1,startlimit=int(cross[1])-tmp+1,endlimit=int(cross[1])+tmp,styleid=1)
        else:
            soup=0
            sel=beatsel
            button=menu_draw(p1,p2,selected_button=sel+1,startlimit=int(cross[0])-tmp-1,endlimit=int(cross[0])+tmp+2,styleid=1)
        if len(p2)==0:
            crok=999
        else:
            crok=0
        sysbuttonpos=(-10,h-50,100+menuback,40),(140,h-50+crok,100,40),
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
        render('rect',arg=((0,h-5,w,5),(60,60,150),False))
        render('rect',arg=((w//2-155,h-90,310,100),(60,60,150),False),borderradius=10)
        render('rect',arg=((w//2-150,h-75,300,75),(50,50,100),False))
        print_card(totperf,totscore,username,(w//2-150,h-85),totrank)
        if ranktype and not ranktype==3:
            if not modshow:
                of=110
            else:
                of=0
            render('rect', arg=((0,h-200+of,250,25), (50,50,130), False),borderradius=10)
            render('text', text='You will not earn Points', arg=((0,0), forepallete,"center"),relative=(0,h-200+of,250,25))
        speed=0.05*speedvel[soup]
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
                            if len(diff)>1:
                                transitionprep(7)
                            else:
                                go=True
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
                                if activity!=7:
                                    if button-1!=beatsel:
                                        beatnowmusic=1
                                        beatsel=button-1
                                        diffcon=0
                                        cross[1]=0
                                    else:
                                        if not activity==7:
                                            if len(diff)>1:
                                                transitionprep(7)
                                            else:
                                                go=True
                                        else:
                                            go=True
                                else:
                                    if button-1!=diffcon:
                                        diffcon=button-1
                                        reloadstats()
                                    else:
                                        go=True


            if event.type  ==  pygame.KEYDOWN:
                if event.key  ==  pygame.K_RETURN:
                    if not activity==7:
                        if len(diff)>1:
                            transitionprep(7)
                        else:
                            go=True
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
            diffpos=(popupw+20+hax,130)
            #pass
            render('text', text=p2[beatsel], arg=(offset, forepallete))
            render('rect',arg=((popupw,40,hax*2,130),(50,50,100),False),borderradius=20)
            render('text', text=rankmodes[ranktype][0], arg=((popupw+20+hax,70), rankmodes[ranktype][1])) # Rank Type
            render('text', text=str(int(diffp[0][0]*perfbom*diffp[0][-1]*scoremult))+'-'+str(int(diffp[-1][0]*perfbom*diffp[-1][-1]*scoremult))+'pp', arg=((popupw+20+hax,100), forepallete))
            render('text', text='BPM - '+str(int(60000/bpm)+1), arg=((popupw+20,70), forepallete))
            render('text', text=str(maxperf*0.01123)[:4]+' Stars', arg=((popupw+20,135), forepallete))
            render('text', text='Max pp - '+str(format(maxperf,',')), arg=((popupw+20,100), forepallete))
            render('rect', arg=((diffpos[0]-(bgcolour//2),diffpos[1],140+bgcolour,30), (beatcol[0]-20,beatcol[1]-20,beatcol[2]-20), False),borderradius=10)
            render('rect', arg=((diffpos[0],diffpos[1],140,30), beatcol, False),borderradius=10)
            render('text', text=beatname, arg=((0,0), forepallete,"center"),relative=(diffpos[0],diffpos[1],140,30))
    if go:
        beatnowmusic=1
        resetscore()
        transitionprep(4)
