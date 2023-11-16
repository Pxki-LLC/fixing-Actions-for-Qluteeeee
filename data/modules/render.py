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
            if "min" in arg:
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
            render('rect', arg=((0, -40, w, 100), (50, 50, 100), False), borderradius=20)
            render('rect',arg=((0,0,w,5),(60,60,150),False))
        else:
            crash('Render unsupported Type')
    except Exception as error:
        crash(str(error)+' (renderer)')
def menu_draw(instruction, text=None, istextbox=False, selected_button=0,enabled_button=[],enable_border=False, hidebutton=False,bigmode=False,startlimit=1,endlimit=None,styleid=1):
    if endlimit==None:
        endlimit=len(instruction)
    elif endlimit>=len(instruction):
        endlimit=len(instruction)
    if startlimit<1:
        startlimit=1
    button=0
    if istextbox:
        button_idle=0, 0, 0
    else:
        if styleid==0:
            button_idle=30, 100, 120
        elif styleid==1:
            button_idle=70,70,120
    for a in range(startlimit,  endlimit+1):	
        tmp=instruction[a-1]
        tmp=pygame.Rect(tmp[0],tmp[1],tmp[2],tmp[3])
        if tmp.collidepoint(pygame.mouse.get_pos()):
            select=True
            buttcolour = (button_idle[0]+10,button_idle[1]+10,button_idle[2]+10)
            if pygame.mouse.get_focused():
                button=a
        else:
            buttcolour = button_idle
            select=False
        b = (buttcolour[0]-10,buttcolour[1]-10,buttcolour[2]-10)
        if not hidebutton:
            if selected_button == a or (len(enabled_button)>0 and enabled_button[a-1]):
                render('rect', arg=((tmp), buttcolour, True),borderradius=10, bordercolor=(0, 150, 150))
            elif select:
                render('rect', arg=((tmp), buttcolour, enable_border),borderradius=10,bordercolor=b)
            else:
                render('rect', arg=((tmp), buttcolour, enable_border),borderradius=10, bordercolor=b)
        if not text == None:
            if bigmode:
                render('text', text=text[a-1], arg=((0,0), forepallete,'center','grade'),relative=instruction[a-1])
            else:
                
                render('text', text=text[a-1], arg=((0,0), forepallete,'center'),relative=instruction[a-1])
    return button
def clear(color):screen.fill(color)