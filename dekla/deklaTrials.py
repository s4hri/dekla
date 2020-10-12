#!/usr/bin/env python3
"""
    alternate DeklaTrials:

    usage:
    prepare:
        self.trials = DeklaTrials("trials.csv")

    to set participant id use
        self.saveid = 0


    use self.trial and self.result as normal,
    but to save and slice use only:
        self.trials.next()

    it combines sliceTrial and self.results storage
    at the end of the experiment add:
        self.trials.save()


"""

import csv
import time
import datetime # for filename timestamp

# only QFileDialog is used, move it outside to a GUI-agnostic call
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def DeklaTrials:
    trials = None
    trial = None

    results = list()
    result = None

    filename = None
    savedir = '../data/'
    savefile = 'results_'
    saveid = 0

    def __init__(self,filename=None):
        # load a csv file if needed
        # if you want to provide trials manually - do it by DeklaTrials.trials = ...
        if filename:
            self.load(filename)

    def load(self,filename=None):
        # filename takes priority, then self.filename, then dialog
        if filename:
            self.filename = filename
        if not self.filename:
            self.filename, extension = QFileDialog.getOpenFileName( QWidget(), "Open trials file:", '', "CSV files (*.csv)")
        with open(self.filename,'r') as csvfile:
            csvread = csv.DictReader(csvfile)
            self.trialsfull = [dict(row) for row in csvread]
        self.reset()



    def reset(self):
        self.trials = self.trialsfull[:]
        self.trialcounter = 0
        self.trial = None
        self.next()
        # WARNING do we need to clear results ?  what should be the expected behaviour?

        self.start_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    # TODO move from pop() to a non-destructive way to be able to add prev()
    def next(self):
        self.trial = self.trials.pop(0)
        # if we already have a result:
        if self.result:
            self.result['savetime'] = time.time()
            self.results.append(self.result)
        self.result = self.trial.copy() # prepare results
        self.trialcounter += 1

    def jump(self,field,content):
        # TODO implement searching for a trial with a precise field
        #      for example .jump('id','002')
        pass


    def save(self):
        # grab every possible header: (set for uniqueness, then back to list)
        header = list( {key for res in self.results for key in res.keys()} )
        header.sort()
        self.__savefullfilename = self.savedir+self.savefile+str(self.saveid)+self.start_time+'.csv'
        with open(self.__savefullfilename,'w+') as file1:
            self.__csvResults = csv.DictWriter(file1, header)

            # be paranoid - check if new file: (timestamp should guarantee that)
            if file1.tell()==0:
                self.__csvResults.writeheader()
            else:
                pass # TODO add exception for something that should NEVER happen
            for res in self.results:
                self.__csvResults.writerow(res)







### temporary StringIO storage is not needed anymore, but just in case the sketch was:
"""
            if len(self.filenameResults): # if this was a file:
                self.fileResults.close()
            else:
                print(self.fileResults.getvalue())


    def prepareSave(self):
                filename1 = self.savedir+self.savefile+self.saveid+self.start_time+'.csv'
                if not self.filenameResults:
                        self.filenameResults, extension = QFileDialog.getSaveFileName( QWidget(), "Save results as...", filename1)
                if len(self.filenameResults):
                        self.fileResults = open(self.filenameResults,'w+') # or a+ if appending 
                else:
                        ## if you choose not to save, a dummy file:
                        self.fileResults = io.StringIO()
"""