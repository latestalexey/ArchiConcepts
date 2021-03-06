#! /usr/bin/python
#
# Estimate Scope_Items Export
#
__author__  = u'morrj140'
__VERSION__ = u'0.3'

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.Constants import *
from al_lib.Neo4JLib import Neo4JLib


def createEstimate(gdb):
    nj = Neo4JLib(gdb)

    qs = u"MATCH "
    qs = qs + u"(n0:ApplicationFunction)-- (r0)"
    qs = qs + u"-- (n1:ApplicationComponent)--(r1)"
    qs = qs + u"-- (n2:ApplicationService)--  (r2)"
    qs = qs + u"-- (n3:BusinessProcess)--     (r3)"
    qs = qs + u"-- (n4:BusinessObject) "
    qs = qs + u"Return n0, r0, n1, r1, n2, r2, n3, r3, n4, n4.PageRank, n4.RequirementCount, n4.Degree"

    lq, qd = nj.cypherQuery(qs)

    nj.queryExportExcel(lq)

    logger.info(u"%d rows returned" % len(lq))

if __name__ == u"__main__":
    createEstimate(gdbTest)