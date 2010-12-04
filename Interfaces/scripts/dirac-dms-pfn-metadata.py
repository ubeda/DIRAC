#!/usr/bin/env python
########################################################################
# $HeadURL$
# File :    dirac-dms-pfn-metadata
# Author :  Stuart Paterson
########################################################################
__RCSID__ = "$Id$"
import DIRAC
from DIRAC.Core.Base import Script
from DIRAC.Interfaces.API.Dirac                       import Dirac

Script.parseCommandLine( ignoreErrors = True )
args = Script.getPositionalArgs()

def usage():
  print 'Usage: %s <PFN> <SE>' % ( Script.scriptName )
  DIRAC.exit( 2 )

if len( args ) < 2:
  usage()

if len( args ) > 2:
  print 'Only one PFN SE pair will be considered'

dirac = Dirac()
exitCode = 0
errorList = []

result = dirac.getPhysicalFileMetadata( args[0], args[1], printOutput = True )
if not result['OK']:
  errorList.append( ( args[0], result['Message'] ) )
  exitCode = 2

for error in errorList:
  print "ERROR %s: %s" % error

DIRAC.exit( exitCode )
