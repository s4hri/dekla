#!/usr/bin/env python3
import yaml

with open('petri1.yaml','r') as file:
        db = yaml.load(file,Loader=yaml.Loader)

#evlist = [ s for s in db if db[s]['depends']=='None' ]
#print(evlist)
#for ev in evlist:
        #if 'show' in db[ev].keys():
                #db[ev].update({'show': 'red.png'})
                
with open('test1mod.yaml','w') as file:
        yaml.dump(db,file,default_flow_style=False)
