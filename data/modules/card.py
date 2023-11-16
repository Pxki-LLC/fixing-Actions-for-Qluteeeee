def print_card(pp,score,name,pos,rank,isgrayed=False):
    if not rank<=0:
        if isgrayed:
            tmp=70,70,100
            tmpt=150,150,150
        else:
            tmp=50,50,100
            tmpt=forepallete
        if not pos[0]+300>w:
            render('rect',arg=((pos[0],pos[1],300,80),(tmp),False),borderradius=10)
            render('text', text=name+' (#'+str(format(rank,','))+')', arg=((pos[0]+10,pos[1]+10), tmpt))
            render('text', text='Score - '+str(format(int(score),',')), arg=((pos[0]+10,pos[1]+40), tmpt,'min'))
            render('text', text='pp - '+str(format(int(pp),',')), arg=((pos[0]+10,pos[1]+60), tmpt,'min'))
