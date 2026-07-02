#!/usr/bin/env python3
"""GTNH production line throughput calculator - deterministic computation."""
import json, sys

TIERS = [
    ("LV",32,1),("MV",128,2),("HV",512,4),("EV",2048,8),("IV",8192,16),
    ("LuV",32768,32),("ZPM",131072,64),("UV",524288,128),("UHV",2097152,256),
    ("UEV",8388608,512),("UIV",33554432,1024),("UXV",134217728,2048),
    ("MAX",2147483647,4096),
]

def ti(tn):
    for i,(n,*_1) in enumerate(TIERS):
        if n.upper()==tn.upper(): return i
    raise ValueError(tn)

def calc_step(s):
    n=ti(s["run_tier"])-ti(s["recipe_tier"])
    if n<0: raise ValueError(f"{s['name']}: run<recipe")
    tf=s["recipe_time"]/(4**n) if n and s.get("oc_mode")=="lossless" else (s["recipe_time"]/(2**n) if n else s["recipe_time"])
    ef=s["recipe_eu"]*(4**n) if n else s["recipe_eu"]
    ops=1.0/tf
    cnt=s.get("count",1)
    return {"name":s["name"],"oc_tiers":n,"time_final":round(tf,4),"eu_final":ef,
        "output_rates":{k:round(v*ops*cnt,4) for k,v in s.get("outputs",{}).items()},
        "input_rates":{k:round(v*ops*cnt,4) for k,v in s.get("inputs",{}).items()},
        "max_main_rate":round(s.get("outputs",{}).get(s.get("main_product",""),0)*ops*cnt,4) if s.get("main_product") else 0,
        "count":cnt,"run_tier":s["run_tier"]}

def calc_global(d):
    mp,mc={},{}
    sr=[]
    for s in d["steps"]:
        r=calc_step(s); sr.append(r)
        for k,v in r["output_rates"].items(): mp[k]=mp.get(k,0)+v
        for k,v in r["input_rates"].items(): mc[k]=mc.get(k,0)+v
    for l in d.get("recycle_loops",[]): mp[l["material"]]=mp.get(l["material"],0)+l["rate"]
    # throughput-based load for each step
    for r in sr:
        s=[x for x in d["steps"] if x["name"]==r["name"]][0]
        main=s.get("main_product","")
        if main and r["max_main_rate"]>0:
            demand=mc.get(main,0)
            total_prod=mp.get(main,1)
            r["load_pct"]=round(min(100,demand/total_prod*100),2)
        else:
            r["load_pct"]=0
    am=set(mp)|set(mc)
    mb,bn=[],[]
    for m in sorted(am):
        p,c=mp.get(m,0),mc.get(m,0); df=p-c; st="OK" if df>=-0.001 else "SHORT"
        mb.append({"material":m,"produced":round(p,4),"consumed":round(c,4),"diff":round(df,4),"status":st})
        if st=="SHORT": bn.append({"material":m,"deficit":round(abs(df),4)})
    ll=[r["name"] for r in sr if r["load_pct"]<50]
    ol=[r["name"] for r in sr if r["load_pct"]>100]
    return {"steps":sr,"material_balance":mb,"bottlenecks":bn,"low_load_steps":ll,
        "overloaded_steps":ol,"main_target":d.get("main_target",""),
        "all_balanced":len(bn)==0 and len(ol)==0}

def main():
    d=json.load(open(sys.argv[1],"r",encoding="utf-8")) if len(sys.argv)>1 else json.load(sys.stdin)
    print(json.dumps(calc_global(d),indent=2,ensure_ascii=False))

if __name__=="__main__": main()
