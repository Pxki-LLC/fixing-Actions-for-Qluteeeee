def beatmapload():
    global p2,p1,beatnowmusic,gc,gametime,beatlist,objects,diffp,betaperf,reloaddatabase,maxperf,ranktype,diff,diffmode,pref,level,ismusic,bpm,realid,prestart,beatsel,tick,lastms,combotime,songoffset,metadata,id
    a=0
    p1=[]
    p2=[]
    if reloaddatabase:
        beatlist=[tmp for tmp in os.listdir(gamepath)]
        reloaddatabase=0
    if prestart:
        if len(beatlist)!=0:
            beatsel=random.randint(1,len(beatlist))-1
        prestart=0
    for b in beatlist:
#        tmp.append(str(b))
        p1.append(((w//2-(cardsize//2)-((size+5)*cross[0])+((size+5)*(a)),(h//2-size)-((size+5)*cross[0])+((size+5)*(a)),cardsize,size)))
        p2.append(str(b)[str(b).index(' ')+1:])
        a+=1
    if ismusic:
        #gametime=pygame.mixer.music.get_pos()
        gametime=((time.time()-gc)/0.001)*1
        pygame.mixer.music.set_volume(vol)
        #pygame.mixer.music.set_pos(time.time()-gametime)
        #pass
#        if gametime<0:
#            gametime=0
        #pygame.mixer.music.play(-1,(time.time()-gametime))
    try:
        if beatnowmusic:
            gc=time.time()
            ranktype=3
            gametime=0
            tick=0
    #        if activity==4:
    #            if int(time.time()-wait)>=1:
    #                wait=time.time()+3
    #                pygame.mixer.music.stop()
    #        else:
    #            wait=int(time.time())
            ismusic=False
            if len(beatlist)!=0:
                if os.path.isdir(gamepath+beatlist[beatsel]):
                    ah=os.listdir(gamepath+beatlist[beatsel])
                    for bop in ah:
                        if bop.endswith('.mp3') or bop.endswith('.ogg'):
                            music=bop
                            ismusic=True
                            break
                        else:
                            ismusic=False
            if ismusic:
                #if not int(time.time()-wait)<=-1:
                if 1==1:
                    beatnowmusic=0
                    realid=beatlist[beatsel]
                    diff=[]
                    pref=''
                    if activity in allowed:
                        loop=-1
                        #print(loop)
                    else:
                        loop=0
                    for a in ah:
                        if a.endswith('.osu'):
                            ax=re.findall(r'\[(.*?)\]', a)
                            if len(str(ax))>2:
                                diff.extend(ax)
                        if pref=='' and a.endswith('.osu'):
                            pref=a.replace('.osu','')
                            pref=pref[:pref.index('[')]
                    diffp=[]
                    for difftmp in diff:
                        beatmap=open(gamepath+beatlist[beatsel]+'/'+pref+'['+difftmp+']'+'.osu').read().rstrip('\n').split('\n')
                        objects=len(beatmap[beatmap.index('[HitObjects]')+1:])*300
                        difficulty=beatmap[beatmap.index('[Difficulty]')+1:]
                        difficulty=difficulty[:difficulty.index('')]
                        metadata=beatmap[beatmap.index('[Metadata]')+1:beatmap.index('[Difficulty]')-1]
                        level=float(difficulty[2].split(':')[-1])+float(difficulty[1].split(':')[-1])+float(difficulty[0].split(':')[-1])
                        diffp.append((objects,difftmp,level))
                    diffp=sorted(diffp, key=lambda x: x[0])
                    diff=diffp
#                    print(diffp)

                    pygame.mixer.music.load(gamepath+beatlist[beatsel]+'/'+music)
                    pygame.mixer.music.play(loop,0,1000)
                    #print(ids)
                    gametime=pygame.mixer.music.get_pos()
                    reloadstats()
                    betaperf=0
                    ptick=0
                    gener=0
                    perfnerf=0.00975*level
                    perfntot=0
                    for a in objects:
                        if int(a.split(',')[2])//100>ptick:
                            ptick=int(a.split(',')[2])//100
                            perfntot=0
                        else:
                            perfntot+=perfnerf
                        betaperf+=perfntot
                    betaperf=betaperf
                    if betaperf>1500:
                        betaperf=1500
                    lastms=int(objects[-1].split(',')[2])
                    for a in metadata:
                        if 'BeatmapID' in a:
                            id=int(a.replace('BeatmapID:',''))
                            break
                        else:
                            id=None
                    threading.Thread(target=getstat).start()
#                    else:
#                        ranktype=
            else:
                lastms=1
                bpm=60000
                level=1
                #objects=['','']
                #metadata=beatmap[beatmap.index('[Metadata]')+1:]
#            for a in beatmap[:3]:
#                print(a)
#            sys.exit()
    except Exception as error:
        print('Could not load Song: '+str(error))
        crash(str(error))
        song_change(1)
def getstat():
    global ranktype,getpoints
    #print('Loading...')
    try:
            f = requests.get('https://api.osu.direct/v2/b/'+str(id),headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=1)
            f=f.json()['ranked']
            print(f)
            ranktypetmp=int(f)
    except Exception as error:
        sprint(error,'(Returning as Unranked)')
        ranktypetmp=99
    getpoints=0
    #if id!=None:
#        print(ranktypetmp)
    if ranktypetmp==3:
#        print(rankmodes[2][0])
        ranktype=2
    elif ranktypetmp>0:
        print(rankmodes[0][0])
        ranktype=0
    else:
#        print(rankmodes[1][0])
        ranktype=1
        getpoints=1
def volchg(t):
    global vol,voltime
    voltime=time.time()+1
    step=0.1
    if t:
        vol+=step
    else:
        if not vol<=0.01:
            vol-=step
