def reloadstats():
    global objects,difficulty,metadata,level,bpm,songoffset,maxperf,scoremult,ismulti,perfect,great,ok,diffmode
    diffmode=diff[diffcon][1]
    beatmap=open(gamepath+beatlist[beatsel]+'/'+pref+'['+diffmode+']'+'.osu').read().rstrip('\n').split('\n')
    objects=beatmap[beatmap.index('[HitObjects]')+1:]
    if modsen[4]:
        print('RND MODE')
        lol=0
        tmp=''
        for a in objects:
            tmp=''
            tok=a.split(',')[1:]
            for b in tok:
                tmp+=','+str(b)
            key=randint(1,len(pos))-1
            objects[lol]=str(pos[key])+tmp
            lol+=1


    difficulty=beatmap[beatmap.index('[Difficulty]')+1:]
    difficulty=difficulty[:difficulty.index('')]
    metadata=beatmap[beatmap.index('[Metadata]')+1:beatmap.index('[Difficulty]')-1]
    level=float(difficulty[2].split(':')[-1])+float(difficulty[1].split(':')[-1])+float(difficulty[0].split(':')[-1])
    bpm=float(beatmap[beatmap.index('[TimingPoints]')+1:][0].split(',')[1])
    songoffset=float(beatmap[beatmap.index('[TimingPoints]')+1:][0].split(',')[0])
    scoremult=1
    inc=0.5
    inf=0.1
    perfect=30*int(11-float(difficulty[2].split(':')[-1]))
    great=perfect*2
    ok=perfect*3
    ismulti=modsen[4]
    for a in range(2,len(modsen)+1):
        if modsen[a-1] and a==2:
            scoremult+=inc*3
        elif modsen[a-1] and not a in (4,5):
            scoremult+=inc
        elif modsen[a-1] and a==4:
            scoremult-=inc
    maxperf=int((len(objects)*300)*(perfbom*level*scoremult))
def getstat():
    global ranktype,getpoints
    #print('Loading...')
    try:
            f = requests.get('https://api.osu.direct/v2/b/'+str(id),headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=1)
            f=f.json()['ranked']
            print(f)
            ranktypetmp=int(f)
    except Exception as error:
        print(error,'(Returning as Unranked)')
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
def resetscore():
    global score,barclicked,prevrank,perf,scorew,bgcolour,objecon,combo,sre,health,healthtime,combotime,hits,last,stripetime,ppcounter,pptime,pptmp,modshow,ranking,playboard
    last=0
    prevrank=totrank
    playboard=[]
    healthtime=time.time()
    for players in range(1,maxplay+2):
        if players==maxplay-1:
                pass
                #playboard.append((username,(255,255,0),int((perf/maxperf)*1000000)))
                #print(players)
#                   render('text',text='#'+str(players)+' '+username,arg=((20, 70+(50*(players-1))),(255,255,0)))
#                   render('text',text=int((perf/maxperf)*1000000),arg=((20, 95+(50*(players-1))),(255,255,0),'min'))
        else:
            playboard.append(('DevUser #'+str(players),forepallete,(randint(1,1234567))))
    ranking=51
    health=100
    stripetime=[]
    objecon=0
    pptime=time.time()
    pptmp=0
    modshow=False
    ppcounter=0
    if activity==4:
        bgcolour=235
        combo=0
    sre=0
    combotime=0
    hits=[0,0,0,0]
    score=0
    scorew=score
    perf=0
    barclicked=[]
def change_diff():
    global diffcon,beatnowmusic
    if not diffcon+1>=len(diff):
        diffcon+=1
    else:
        diffcon=0
    beatnowmusic=1
def song_change(switch):
    global beatsel,beatnowmusic,diffcon
    if not switch:
        if not beatsel-1<=-1:
            beatsel-=1
        else:
            beatsel=len(p2)-1
    else:
        if not beatsel+1>=len(p2):
            beatsel+=1
        else:
            beatsel=0
    beatnowmusic=1
    diffcon=0
def diff_change(switch):
    global beatsel,beatnowmusic,diffcon
    if not switch:
        if not diffcon-1<=-1:
            diffcon-=1
        else:
            diffcon=len(diff)-1
    else:
        if not diffcon+1>=len(diff):
            diffcon+=1
        else:
            diffcon=0
    reloadstats()
def get_rank(num):
    #crok=256*oneperf
    crok=oneperf/2
    totrank=(crok+1)-int((num/oneperf)*crok)
    return int(totrank)