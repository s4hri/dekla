#!/usr/bin/env python3

class defaults:
        appName = "Dekla v0.2 - Posner Experiment"
        screens = ["main","left","right"]
        savefile = "../data/results_" # and auto-added date: %Y%m%d-%H%M%S

conditions = [
  'close',
  'close',
  'mutual',
  'mutual',
  'mutual',
  'close',
  'close',
  'close',
  'mutual',
  'close',
  'mutual',
  'mutual',
  'mutual',
  'mutual',
  'close',
  'close']


subtrials = [ (lookingside,letterside,letter)
              for lookingside in ['left','right']
              for letterside  in ['left','right']
              for letter in [ 'T','V'] ]

trials = list()

for trial in conditions:
        subtrialsTwice = subtrials.copy()
        subtrialsTwice.extend(subtrials)
        random.shuffle(subtrialsTwice)
        for subtrial in subtrialsTwice:
                place1 = trial + ' ' + subtrial[0]
                place2 = subtrial[1] + ' ' + subtrial[2]
                place3 = 'return ' + subtrial[0]
                place4 = subtrial[1] + ' empty'
                key = subtrial[2]
                
                trials.append(  dict( place1=place1,
                                      place2=place2,
                                      place3=place3,
                                      place4=place4,
                                      key=key ) )

