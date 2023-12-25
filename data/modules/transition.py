
def transitionto():
    global activity,transa,transb,actto
    if transb:
        render('rect', arg=((w-transa,0,w,h), (0,100,200), False),borderradius=10)
        if transa>=w and activity!=actto:
            activity=actto
        elif transa>=w+w+20:
            transa=0
            transb=0
        else:
            transa+=2
def transitionprep(act):
    global transa,transb,activity
    activity=act