#!/usr/bin/python
#
# Natural Language Processing of Concepts to Neo4J Information
#
import os
from subprocess import call
import time
import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import Neo4JGraph
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from al_ArchiLib import *

import al_QueryGraph as CG

def addGraphNodes(graph, concepts, n=0, threshold=1):
    n += 1
    for c in concepts.getConcepts().values():
        logger.debug("%d : %d Node c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))

        graph.addConcept(c)

        if len(c.getConcepts()) > threshold:
            addGraphNodes(graph, c, n)

def addGraphEdges(graph, concepts, n=0):
    n += 1

    graph.addConcept(concepts)

    for c in concepts.getConcepts().values():

        logger.debug("%d : %d %s c : %s:%s" % (n, len(c.getConcepts()), concepts.name, c.name, c.typeName))

        graph.addConcept(c)

        if isinstance(graph, Neo4JGraph):
            graph.addEdge(concepts, c, c.typeName)
        else:
            graph.addEdge(concepts, c)

        if len(c.getConcepts()) != 0:
            addGraphEdges(graph, c, n)

def logGraph(gl, title, scale=1):
    pr = 0
    len_pr = len(gl)
    sum_pr = 0.0
    try:
        logger.info("---%s---[%d]" % (title, len(gl)))

        n = 0
        for x in gl:
            n += 1
            if isinstance(gl, dict) and x != None:
                sum_pr = gl[x]
                if gl[x] > pr:
                    pr = gl[x]
                if gl[x] > 0.0005:
                    logger.info("%s [%d]:%s=%3.4f" % (title, n, x, gl[x]*scale))
            else:
                logger.info("%s [%d]" % (x, n))
    except:
        logger.warn("Ops...")

    logger.info("Len gl[x]=%3.4f" % len_pr)
    logger.info("Max gl[x]=%3.4f" % pr)
    logger.info("Avg gl[x]=%3.4f" % (sum_pr / len_pr))

def clearNeo4J():
    call(["/Users/morrj140/Development/neo4j-community-2.1.2/bin/reset.sh"])

def importNeo4J(concepts):

    clearNeo4J()

    logger.info("Neo4J instance : %s" % gdb)
    graph = Neo4JGraph(gdb)

    logger.info("Adding Neo4J nodes to the graph ...")
    addGraphNodes(graph, concepts)

    logger.info("Adding Neo4J edges to the graph ...")
    addGraphEdges(graph, concepts)

    graph.setNodeLabels()

    DropNode = "MATCH (n { name: 'Node' })-[r]-() DELETE n, r"
    CG.cypherQuery(graph, DropNode)

    CountRequirements = "MATCH (n {typeName:'BusinessObject'}) -- m -- (o {typeName:'Requirement' }) with n, count(o) as rc  set n.RequirementCount=rc RETURN n.name, rc order by rc desc"
    CG.cypherQuery(graph, CountRequirements)

if __name__ == "__main__":

    logger.info("Export File : %s" % fileExport)
    exportConcepts = Concepts.loadConcepts(fileExport)

    importNeo4J(exportConcepts)



    



