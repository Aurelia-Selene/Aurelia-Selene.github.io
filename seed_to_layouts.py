#!/usr/bin/env python
"""
seed_to_layouts.py — convert a Cracking Rig SEED or JSON layout into
Frieza's rig-simulator LAYOUTS JS snippet.

USAGE
  python seed_to_layouts.py --seed "hceehewewcpPcpPcweweheech..." --cases 1 --key "NO Educations|1|550000"
  python seed_to_layouts.py --json rig.json --key "NO Educations|1|550000"
  python seed_to_layouts.py --seed "..." --cases 1 --grid     # pretty 5x5 preview only

RULES (single source of truth)
  Grid: 5 columns x 5 rows per case, row-major (left->right, top->bottom).
        x = column (0..4), y = row (0..4).  Seed index i -> row=i//5, col=i%5.
  Seed char map:
        e=eCPU(1)  c=CPU(2)  h=HPCU(3)  f=Fan(4)  w=WaterBlock(5)  s=HeatSink(6)  b=Empty(0)
        PSU (id 7) uses 4 half-characters:
          p = left half   P = right half   -> HORIZONTAL pair (anchor = 'p' cell)
          v = top half    V = bottom half  -> VERTICAL pair   (anchor = 'v' cell)
        PSU count = (number of p/P/v/V cells) / 2.
  JSON: one entry per placed part.  {x,y,item} = 1x1.  PSU = {x,y,item:7,x2,y2}
        where (x2,y2) is the second cell; orientation h if same row, v if same col.
  Simulator LAYOUTS entry:
        LAYOUTS["tier|cases|MIPS"] = [ case0, case1, ... ]
        case  = [ {t,type, r,row, c,col [,o:"h"|"v"]}, ... ]
        PSU  : {t:"PSU", r:anchorRow, c:anchorCol, o:"h"|"v"}  (o only for PSU)
"""
import json, argparse

NAMES = {1:'eCPU', 2:'CPU', 3:'HPCU', 4:'Fan', 5:'Water Block', 6:'Heat Sink', 7:'PSU'}
SEED_TO_ID = {'e':1, 'c':2, 'h':3, 'f':4, 'w':5, 's':6}   # single-cell, non-empty
PSU_HALF = set('pPvV')


def from_seed(seed, num_cases):
    cases = []
    for ci in range(num_cases):
        block = seed[ci*25:(ci+1)*25]
        anchors, singles = [], []
        for i, ch in enumerate(block):
            r, c = i // 5, i % 5
            if ch == 'p':
                anchors.append((r, c, 'h'))
            elif ch == 'v':
                anchors.append((r, c, 'v'))
            elif ch in PSU_HALF:
                continue                       # 'P'/'V' = 2nd half, already covered
            elif ch == 'b':
                continue                       # empty
            else:
                singles.append((r, c, SEED_TO_ID[ch]))
        cases.append((anchors, singles))
    return cases


def from_json(data):
    def ordk(k):
        return int(str(k).rsplit('.', 1)[-1])
    cases = []
    for key in sorted(data.keys(), key=ordk):
        anchors, singles = [], []
        for e in data[key]:
            x, y = e['x'], e['y']
            iid = e['item']
            if iid == 7:
                x2, y2 = e['x2'], e['y2']
                o = 'h' if (y2 == y and x2 != x) else 'v'
                anchors.append((y, x, o))      # anchor = top-left of the pair
            elif iid == 0:
                continue
            else:
                singles.append((y, x, iid))
        cases.append((anchors, singles))
    return cases


def build_case(anchors, singles):
    comp = [{'t': 'PSU', 'r': r, 'c': c, 'o': o} for (r, c, o) in anchors]
    comp += [{'t': NAMES[i], 'r': r, 'c': c} for (r, c, i) in singles]
    comp.sort(key=lambda x: (x['r'], x['c']))
    return comp


def to_js(cases, key=None):
    def fmt_case(case):
        rows = {}
        for c in case:
            rows.setdefault(c['r'], []).append(c)
        out = []
        for r in sorted(rows):
            cells = sorted(rows[r], key=lambda x: x['c'])
            parts = []
            for c in cells:
                if c['t'] == 'PSU':
                    parts.append('{t:"PSU",r:%d,c:%d,o:"%s"}' % (c['r'], c['c'], c['o']))
                else:
                    parts.append('{t:"%s",r:%d,c:%d}' % (c['t'], c['r'], c['c']))
            out.append(', '.join(parts))
        return ',\n  '.join(out)
    inner = ',\n  '.join('[' + fmt_case(build_case(a, s)) + ']' for (a, s) in cases)
    body = '[\n  ' + inner + '\n]'
    return ('"%s":\n  ' % key + body) if key else body


def grid_preview(cases):
    abbr = {1:'eC', 2:'CP', 3:'HP', 4:'Fa', 5:'Wa', 6:'HS', 7:'PS'}
    from collections import Counter
    for ci, (anchors, singles) in enumerate(cases):
        print('Case %d:' % (ci + 1))
        occ = {}
        for (r, c, o) in anchors:
            occ[(r, c)] = 'PS'
            occ[(r, c + 1) if o == 'h' else (r + 1, c)] = 'PS'
        for (r, c, i) in singles:
            occ[(r, c)] = abbr[i]
        for r in range(5):
            print('  ' + '  '.join('%2s' % occ.get((r, c), '  ') for c in range(5)))
        cnt = Counter(NAMES[i] for (_, _, i) in singles)
        cnt['PSU'] = len(anchors)
        print('  ' + str(dict(cnt)))
    print()


def main():
    import argparse
    ap = argparse.ArgumentParser(description='Convert rig SEED/JSON -> LAYOUTS JS')
    ap.add_argument('--seed')
    ap.add_argument('--json')
    ap.add_argument('--cases', type=int, default=1)
    ap.add_argument('--key', help='LAYOUTS key: tier|cases|MIPS')
    ap.add_argument('--grid', action='store_true', help='pretty 5x5 preview')
    a = ap.parse_args()

    if a.seed:
        cases = from_seed(a.seed, a.cases)
    elif a.json:
        with open(a.json, 'r', encoding='utf-8-sig') as f:
            cases = from_json(json.load(f))
        a.cases = len(cases)
    else:
        ap.error('provide --seed or --json')

    if a.grid:
        grid_preview(cases)
    else:
        print(to_js(cases, a.key))


if __name__ == '__main__':
    main()