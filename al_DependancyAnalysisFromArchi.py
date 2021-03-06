#!/usr/bin/python
#
# Archimate to Dependancy Analysis
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib
from al_lib.DependencyAnalysis import *

def dependancyAnalysisFromArchi(fileArchimate):

    start_time = ArchiLib.startTimer()

    da = DependancyAnalysis(fileArchimate)

    concepts, listTSort = da.collectDependancyAnalysisNodes()

    da.dependancyAnalysis(listTSort)

    concepts.logConcepts()

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":

    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v2.20.archimate"

    dependancyAnalysisFromArchi(fileArchimate)