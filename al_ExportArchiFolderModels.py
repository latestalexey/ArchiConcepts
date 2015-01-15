#!/usr/bin/python
#
# Archimate Export All Models in a Folder
#
__author__ = 'morrj140'
import sys
import os
import StringIO
import time

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from al_ArchiLib import *

def al_ExportArchiFolderModels():
    al = ArchiLib()

    al.logTypeCounts()

    #conceptsFile = "Estimation" + time.strftime("%Y%d%m_%H%M%S") +".p"
    conceptsFile = "Estimation.p"

    if True:
        folder = "Scenarios"

        logger.info("Exporting Folder : %s" % folder)
        listMTE = al.getModelsInFolder(folder)

        concepts = Concepts("Export", "Pickle")

        for ModelToExport in listMTE:
            logger.info("  Model : %s" % ModelToExport)
            d = concepts.addConceptKeyType(ModelToExport, "Model")
            al.recurseModel(ModelToExport, d)

        #concepts.logConcepts()
    else:
        conceptsFile = "Estimation.p"
        concepts = Concepts.loadConcepts(conceptsFile)

    al.outputCSVtoFile(concepts)

    Concepts.saveConcepts(concepts, conceptsFile)
    logger.info("Save Concepts : %s" % conceptsFile)


if __name__ == "__main__":
    al_ExportArchiFolderModels()



