#! /usr/bin/python
#
# Query Neo4J Information in Cypher
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from py2neo.neo4j import GraphDatabaseService, CypherQuery, Node, Relationship

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter
from openpyxl.worksheet import Worksheet

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.Neo4JLib import Neo4JLib

from al_Constants import *

import pytest

def queryGraph(gdb):

    nj = Neo4JLib(gdb, fileCSVExport)

    start_time = ArchiLib.startTimer()

    nj.Neo4JCounts()

    #
    # Useful Cypher Queries
    #
    #UpdateQuery = "match (n0 {typeName:'BusinessObject', name:'Contract'}) set n0.PageRank = 1 return n"
    #demoQuery1 = "MATCH (n0:Stakeholder)-- (r0)-- (n1:WorkPackage)--(r1)--(n2:BusinessObject) RETURN n0, r0, n1, r1, n2"
    #demoQuery2 = "MATCH (n0:WorkPackage)--(r0)--(n1:ApplicationComponent)--(r1)--(n2:ApplicationService)--(r2)--(n3:BusinessProcess) where n1.aname = 'Contract Management' RETURN n0, r0, n1, r1, n2, r2, n3"

    #delNodes = "MATCH (n { name: 'Node' })-[r]-() DELETE n, r"

    ql = list()

    if False:
        qs = "MATCH (a)-[r]->(b) WHERE labels(a) <> [] AND labels(b) <> [] RETURN DISTINCT head(labels(a)) AS This, type(r) as To, head(labels(b)) AS That"

    if True:
        qs = "MATCH (m:ApplicationComponent) - [r] -> (n:ApplicationFunction) RETURN distinct(n.aname) as Function, n.parentPath, r.typeName as Type, m.aname as Component, m.parentPath order by n.aname"

    elif False:
        # Determine order of service development based on the dependancy analysis done on Business Processes
        #qs="match (l:ApplicationService)--(r0:Relation)-- (n:BusinessProcess)--(r1:Relation)--(m:WorkPackage) return m,l,n order by m.aname"
        # Try with Application Component as well
        qs="match (i:DataObject)--(r0:Relation) -- (j:ApplicationComponent)--(r1:Relation)--(l:ApplicationService)--(r2:Relation)-- (n:BusinessProcess)--(r3:Relation)--(m:WorkPackage) return m,n,l,j,i order by m.aname"

    elif False:
        # Determine the business process ordering by the magnitude of the reqiurements
        qs="match (i:Requirement)--(r1:Relation)--(j:BusinessObject)--(r2:Relation)--(k:BusinessProcess)--(r3:Relation)--(l:WorkPackage) return l,k,j,count(i) order by l.aname"

    elif False:
        # Determine a Business Scenario's associciation to Business Processes
        #qs = "match (n0:BusinessEvent) --> (r0:TriggeringRelationship) --> (n1:BusinessProcess) --> (r1:TriggeringRelationship) --> (n2:BusinessEvent) return n0, r0, n1, r1,  n2"
        qs = "match (n0:BusinessEvent) --> (r0:Relation)--> (n1:BusinessProcess) -[*1..10]-> (r1:FlowRelationship) --> (n2:BusinessProcess) return n0, n1, n2 order by n0.aname"

    elif False:
        qs = "MATCH (n0:BusinessObject) --> (r0:Relation) --> (n1:BusinessProcess) "
        qs = qs + "where (toint(substring(n1.aname, 0, 1)) is null ) "
        qs = qs + "return n0.aname, n1.aname order by n0.aname desc"

    elif False:
        qs = "match (n:BusinessProcess) <-- (r0:Relation) <-- (m:ApplicationService) "
        qs = qs + "with n, m, count(r) as cr "
        qs = qs + " where cr > 0 "
        qs = qs + " return n.aname, m.aname, cr"

    elif False:
        qs = "MATCH (n:Requirement) <-- (r0:Relation) <-- (n0:BusinessObject) --> (r1:Relation) -->  (n1:BusinessProcess) "
        qs = qs + "where (toint(substring(n1.aname, 0, 1)) is null ) "
        qs = qs + "return count(n), n0.aname, n0.Degree, n0.PageRank, n1.aname, n1.Degree, n1.PageRank order by n0.aname desc"

    elif False:
        ql.append("ApplicationFunction")
        ql.append("ApplicationComponent")
        ql.append("ApplicationService")

        qs = nj.Traversal(ql, directed=True)

    elif False:
        ql.append("ApplicationFunction")
        ql.append("ApplicationComponent")
        ql.append("ApplicationService")
        ql.append("BusinessProcess")
        ql.append("BusinessObject")

        qs = nj.Traversal(ql, directed=True)

    elif False:
        ql.append("WorkPackage")
        ql.append("BusinessProcess")
        ql.append("ApplicationService")
        ql.append("ApplicationComponent")
        ql.append("ApplicationFunction")

        qs = nj.Traversal(ql, directed=False)

    elif False:
        qs1 = "MATCH (n0:BusinessEvent)-- (r0)-- (n1:BusinessProcess) -- (r1) -- (n2:BusinessObject)  RETURN n0, r0, n1, r1, n2"
        qs2 = "MATCH (n0:BusinessProcess)--(r0)--(n1:ApplicationService)--(r1)--(n2:ApplicationComponent)--(r2)--(n3:DataObject) RETURN n0, r0, n1, r1, n2, r2, n3"
        qs3 = "MATCH (n0:WorkPackage)--(r0)--(n1:BusinessProcess) RETURN n0, r0, n1"
        qs4 = "MATCH (n0:ApplicationService)--(r0)--(n2:ApplicationComponent)--(r2)--(n3:DataObject) RETURN n1,r1,n2, r2, n3"
        qs5 = "MATCH (n0:BusinessObject)--(r0)--(n1:DataObject) RETURN n0, r0, n1"
        qs6 = "MATCH (n0:BusinessProcess)--(r0)--(n1: BusinessObject)--(r1)--(n2:DataObject)--(r2)--(n3: ApplicationComponent) RETURN n0, r0, n1, r1, n2, r2, n3"
        qs7 = "MATCH (n:Requirement)<--() <-- (n0:BusinessObject) --> () --> (n1:BusinessProcess) <-- () <-- (n2:ApplicationService)-->()-->(n3:ApplicationComponent)-->()-->(n4:ApplicationFunction) Return n0, count(n), n1, n2, n3, n4 order by count(n) desc, n0.aname"
        qs = qs7

    elif False:
        qs = "MATCH    (n:Requirement)           <--() "
        qs = qs + "<-- (n0:BusinessObject)      --> ()"
        qs = qs + "--> (n1:BusinessProcess)     <-- ()"
        qs = qs + "<-- (n2:ApplicationService)   -->()"
        qs = qs + "--> (n3:ApplicationComponent) -->()"
        qs = qs + "--> (n4:ApplicationFunction) "
        qs = qs + "Return n0, count(n), n1, n2, n3, n4 "
        qs = qs + "order by count(n) desc, n0.aname"

    elif False:
        qs = "MATCH    (n0:BusinessObject)      --> ()"
        qs = qs + "--> (n1:BusinessProcess)     <-- ()"
        qs = qs + "<-- (n2:ApplicationService)   -->()"
        qs = qs + "--> (n3:ApplicationComponent) -->()"
        qs = qs + "--> (n4:ApplicationFunction) "
        qs = qs + "Return n0, n1, n2, n3, n4 "
        qs = qs + "order by n0.aname desc"

    elif False:
        #qs = "MATCH (n0:BusinessObject)--(r0)--(n1:Requirement) RETURN n0, r0, n1"
        qs = "MATCH (n0:BusinessObject)--(r0)--(n1:Requirement) RETURN n0, count(n1) ORDER BY count(n1) DESC"
        #qs = "MATCH (n0:BusinessObject)--(r0:AssociationRelationship)--(n1:Requirement)  RETURN n0, n0.PageRank, n0.RequirementCount, n0.Degree, n0.count, count(n1) ORDER BY count(n1) DESC"
        #qs = "MATCH (n0:BusinessObject) RETURN n0, n0.PageRank, n0.RequirementCount, n0.Degree, n0.count"
        #qs = "MATCH (n0:DataObject) RETURN n0, n0.PageRank, n0.RequirementCount, n0.Degree, n0.count"

    else:
        qs = "match (n0:WorkPackage) --(r0)--(n1:BusinessProcess)--(r1)--(n2:ApplicationService) where n0.aname='Batch %d'  return n0, r0, n1,r1, n2" % (1)

    lq, qd = nj.cypherQuery(qs)

    nj.queryExport(lq)

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    queryGraph(gdb)