import re, json
s=open('rigs-data.js',encoding='utf-8-sig').read()
# --- D ---
dtext = s[s.index('const D='):s.index('const LAYOUTS=')]
dtext = dtext[len('const D='):dtext.index('];')+1]
D=json.loads(dtext); print('D rows:',len(D))
# --- LAYOUTS ---
lobj = s[s.index('const LAYOUTS={'):s.rindex('};')+1]
lobj = lobj[len('const LAYOUTS='):]
lobj2=re.sub(r'([{,])(\s*)(t|r|c|o)(\s*):', r'\1"\3":', lobj)
L=json.loads(lobj2); print('LAYOUTS keys:',len(L),'unique:',len(L)==len(set(L)))
NMAP={'eCPU':'eCPU','CPU':'CPU','HPCU':'HPCU','Fan':'Fan','Water Block':'WaterBlock','Heat Sink':'HeatSink'}
problems=[]; allmatch=True
# --- D rows: MIPS + power (draw over budget throttles MIPS by budget/draw) ---
STEP={'NO Educations':0,'NO OC + Heat Red':0,'30% OC':3,'50% OC':5}
for r in D:
    tier,cases,mips=r[0],r[1],r[2]
    e,c,h,f,p=r[6],r[7],r[8],r[9],r[12]
    st=STEP[tier]
    full=(25000+1250*st)*e+(30000+2250*st)*c+(50000+5000*st)*h
    draw=(30+3*st)*e+(70+7*st)*c+(150+15*st)*h+5*f
    cap=750*p
    exp=int(round(((full*cap/draw) if draw>cap else full)/10.0))*10
    if abs(exp-mips)>10:
        allmatch=False
        problems.append((tier+'|'+str(cases)+'|'+str(mips),'MIPS stored=%s expected=%s draw=%dW cap=%dW'%(format(mips,','),format(exp,','),draw,cap)))
print('D rows MIPS/power checked:',len(D))
for key,cases in L.items():
    tier,nc,mips=key.split('|'); mips=int(mips)
    drow=[r for r in D if r[2]==mips and r[0]==tier]
    if len(drow)!=1: problems.append((key,'D row missing/ambiguous')); continue
    r=drow[0]
    exp={'eCPU':r[6],'CPU':r[7],'HPCU':r[8],'Fan':r[9],'WaterBlock':r[10],'HeatSink':r[11],'PSU':r[12]}
    got={'eCPU':0,'CPU':0,'HPCU':0,'Fan':0,'WaterBlock':0,'HeatSink':0,'PSU':0}
    if len(cases)!=int(nc): problems.append((key,'case count %d!=%s'%(len(cases),nc)))
    if int(r[1])!=int(nc): problems.append((key,'key cases %s != D cases %s'%(nc,r[1])))
    for ci,case in enumerate(cases):
        ccells=set()
        for o in case:
            t=o['t']; rr=o['r']; cc=o['c']
            if not (0<=rr<=4 and 0<=cc<=4): problems.append((key,'ci%d bad coord %s'%(ci,o))); continue
            if t=='PSU':
                if o.get('o')=='h':
                    if cc>3: problems.append((key,'ci%d PSU off-grid(h) %s'%(ci,o))); continue
                    span=[(rr,cc),(rr,cc+1)]
                elif o.get('o')=='v':
                    if rr>3: problems.append((key,'ci%d PSU off-grid(v) %s'%(ci,o))); continue
                    span=[(rr,cc),(rr+1,cc)]
                else: problems.append((key,'ci%d PSU no-orient %s'%(ci,o))); continue
                if any(cell in ccells for cell in span): problems.append((key,'ci%d collision %s'%(ci,o))); continue
                ccells.update(span); got['PSU']+=1
            else:
                nm=NMAP[t]
                if (rr,cc) in ccells: problems.append((key,'ci%d collision %s'%(ci,o))); continue
                ccells.add((rr,cc)); got[nm]+=1
    if got!=exp:
        allmatch=False
        diff={k:(got[k],exp[k]) for k in exp if got[k]!=exp[k]}
        problems.append((key,'counts got=%s exp=%s diff=%s'%(got,exp,diff)))
    else:
        print('OK  ',key)
print('\n=== PROBLEMS ===')
for p in problems: print(' ',p)
print('\nALL MATCH:', allmatch and not problems)