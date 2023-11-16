def submit_score(perf,score,other=''):
    global totscore,totperf
    if perf>=totperf:
        template=str(p2[beatsel])+';'+str(perf-totperf)+';'+str(score-totscore)+';'+other+'\n'
        with open(profilepath+'perf','w') as x:
            x.write(str(perf))
        with  open(profilepath+'score','w') as x:
            x.write(str(score))
        with  open(profilepath+'scoreboard','a') as x:
            x.write(template)
        print('Submiting Score...')
        totperf=perf
        totscore=score
