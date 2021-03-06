import os
import pytest
from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

__author__ = u'james.morris'

if __name__ == u"__main__":

    rp = os.path.realpath(__file__)

    logger.info(u"Current Directory %s[%s]" % (os.getcwd(), rp))
    
    # os.chdir("../nl_lib")
    # lib = u"%s%s..%s%s" % (os.getcwd(), os.sep, os.sep, "nl_lib")
    # os.chdir(lib)

    # options in setup.cfg
    pytest.main()
