def render(type, arg=(0, 0) ,  text='N/A', bordercolor=forepallete, borderradius=0,relative=(0,0,0,0),surf=''):
    off=0
    grad2=False
    if surf=='':
      surf=screen
    try:
        bordercolor=mint(bordercolor[0],darkness),mint(bordercolor[1],darkness),mint(bordercolor[2],darkness)
        try:
            colour=mint(arg[1][0],darkness),mint(arg[1][1],darkness),mint(arg[1][2],darkness)
        except Exception:
            colour=mint(arg[1],darkness)
        relative=pygame.Rect(relative)
        if type == 'text':
            if "bold" in arg:
                surf.blit(fonts[3].render(str(text),  True,  colour),  arg[0])
            elif "min" in arg:
                surf.blit(fonts[1].render(str(text),  True,  colour),  arg[0])
            elif "grade" in arg:
                if "center" in arg:
                    tmp = fonts[2].render(str(text),  True,  colour)
                    centertext = tmp.get_rect(center=relative.center)
                    surf.blit(tmp,  centertext)
                    grad2=True
                else:
                    surf.blit(fonts[2].render(str(text),  True,  colour),  arg[0])
            elif not "center" in arg:
                surf.blit(fonts[0].render(str(text),  True,  colour),  arg[0])
            if "center" in arg and not grad2:
                tmp = fonts[0].render(str(text),  True,  colour)
                centertext = tmp.get_rect(center=relative.center)
                surf.blit(tmp,  centertext)
        elif type == 'clear':
            screen.fill(arg)
        elif type == 'line':
            pygame.draw.line(surf,colour,arg[0],arg[2])
        elif type == 'rect':
#			print(arg[0][0], arg[0][1], arg[0][2], arg[0][3])
            pygame.draw.rect(surf, colour, (arg[0][0], arg[0][1], arg[0][2]-off, arg[0][3]-off), border_radius=borderradius)
            if arg[2]:
                pygame.draw.rect(surf, bordercolor, (arg[0][0], arg[0][1], arg[0][2]-off, arg[0][3]-off), 2, border_radius=borderradius)
            ## This was for a "Wireframe" Like Square
#            pygame.draw.rect(screen, (0, 255, 0), (arg[0][0], arg[0][1], arg[0][2], arg[0][3]), 1)
        elif type == 'header':
            render('rect', arg=((0, -40, w, 100), blend(opacity,0), False), borderradius=20)
            render('rect',arg=((0,0,w,5),blend(-opacity,0),False))
        else:
            crash('Render unsupported Type')
    except Exception as error:
        crash(str(error)+' (renderer)')
def menu_draw(instruction, text=None,ishomemenu=False,ignoremove=False, istextbox=False, selected_button=0,enabled_button=[],enable_border=False, hidebutton=False,bigmode=False,startlimit=1,endlimit=None,styleid=1,isblade=False):
    if endlimit==None:
        endlimit=len(instruction)
    elif endlimit>=len(instruction):
        endlimit=len(instruction)
    if startlimit<1:
        startlimit=1
    button=0
    if istextbox:
        button=0, 0, 0
    else:
        if styleid==0:
            buttonc=30, 100, 120
#        elif styleid==1:
            #buttonc=35,37,89
    select=False
    for a in range(startlimit,  endlimit+1):	
        buttonc=bgdefaultcolour[0]+10,bgdefaultcolour[1]+10,bgdefaultcolour[2]+10
        tmp=instruction[a-1]
        tmp=pygame.Rect(tmp[0],tmp[1],tmp[2],tmp[3])
        if tmp.collidepoint(pygame.mouse.get_pos()) and not select:
            select=True
            buttcolour = (buttonc[0]+10,buttonc[1]+10,buttonc[2]+10)
            if pygame.mouse.get_focused():
                button=a
        else:
            buttcolour = buttonc
        b = (50,150,150)
        #drawRhomboid(screen, (255,255,255), 50, 50, 300, 200, 100, 3)
        if not hidebutton:
            if not isblade:
                if selected_button==a:
                    enable_border=True
                else:
                    enable_border=False
                render('rect', arg=((tmp), buttcolour, enable_border),borderradius=10, bordercolor=b)
            else:
                if a==1:
                    buttcolour=mainmenucolor[0]
                else:
                    buttcolour=mainmenucolor[1][0]-(10*(a-2)),mainmenucolor[1][1]-(10*(a-2)),mainmenucolor[1][2]-(10*(a-2))
                if ishomemenu:
                    print(a)
                    if not ignoremove:
                        if button==a and not int(menupos[a-1])>19:
                            menupos[a-1]+=100*drawtime
                        elif button==a and int(menupos[a-1])==20:
                            pass
                        elif int(menupos[a-1])>0:
                            menupos[a-1]-=100*drawtime
                        moveid=menupos[a-1]
                    else:
                        moveid=0
                if button==a:
                    buttcolour=buttcolour[0]+5,buttcolour[1]+5,buttcolour[2]+5
                drawRhomboid(screen, buttcolour, tmp[0]-(moveid//2), tmp[1]-moveid, tmp[2]+moveid, tmp[3],25, 0)
            if not text == None:
                if bigmode:
                    render('text', text=text[a-1], arg=((0,0), forepallete,'center','grade'),relative=instruction[a-1])
                else:
                    if ishomemenu:
                        home=moveid
                    else:
                        home=0
                    render('text', text=text[a-1], arg=((0,0), forepallete,'center'),relative=(instruction[a-1][0],instruction[a-1][1]-home,instruction[a-1][2],instruction[a-1][3]))
    return button
def clear(color):screen.fill(color)
def blend(opacity,bgcolour):
    return maxt(bgdefaultcolour[0]-opacity,bgcolour),maxt(bgdefaultcolour[1]-opacity,bgcolour),maxt(bgdefaultcolour[2]-opacity,bgcolour)
def drawRhomboid(surf, color, x, y, width, height, offset, thickness=0):
    points = [
        (x + offset, y), 
        (x + width + offset, y), 
        (x + width-offset, y + height), 
        (x-offset, y + height)]
    pygame.draw.polygon(surf, color, points, thickness)
