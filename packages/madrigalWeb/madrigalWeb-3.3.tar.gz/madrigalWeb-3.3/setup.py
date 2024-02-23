"""set up file for the Python Madrigal Remote API

$Id: setup.py 7564 2023-07-31 20:03:39Z brideout $
"""
import os, os.path, sys

from distutils.core import setup
    
setup(url="http://cedar.openmadrigal.org",
      scripts=['madrigalWeb/globalIsprint.py', 'madrigalWeb/globalDownload.py',
               'madrigalWeb/globalCitation.py',
               'madrigalWeb/examples/exampleMadrigalWebServices.py'],
      test_suite="tests",
      )

    