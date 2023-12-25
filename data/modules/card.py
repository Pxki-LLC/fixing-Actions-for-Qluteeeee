def print_card(pp,score,name,pos,rank,isgrayed=False,mini=False):
    if not rank<=0:
        if isgrayed:
            tmp=70,70,100
            tmpt=150,150,150
        else:
            tmp=50,50,100
            tmpt=forepallete
        #if not pos[0]+300>w:
        dim=25
        cao=len(name)*20+45
        if not mini:
            render('rect',arg=((pos[0],pos[1],300,80),(tmp),False),borderradius=10)
            render('text', text=name+' (#'+str(format(rank,','))+')', arg=((pos[0]+10,pos[1]+10), tmpt,'bold'))
            render('text', text='Score - '+str(format(int(score),',')), arg=((pos[0]+10,pos[1]+40), tmpt,'min'))
            render('text', text=str(format(int(pp),','))+'pp', arg=((pos[0]+10,pos[1]+60), tmpt,'min'))
        else:
            render('rect',arg=((pos[0]-cao,pos[1],cao+15,80),(tmp),False),borderradius=10)
            render('text', text='#'+str(format(rank,',')), arg=((pos[0]-cao+10,pos[1]+30), (tmp[0]-dim,tmp[1]-dim,tmp[2]-dim),'grade'))
            render('text', text=name, arg=((pos[0]-cao+10,pos[1]+10), tmpt,'bold'))
            render('text', text=str(format(int(pp),','))+'pp', arg=((pos[0]-cao+10,pos[1]+40), tmpt,'min'))
            #+' (#'+str(format(rank,','))+')'
