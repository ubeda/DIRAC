#!/usr/bin/env python
########################################################################
# $HeadURL$
########################################################################
__RCSID__   = "$Id$"
import DIRAC
from DIRAC.Core.Base import Script
Script.parseCommandLine()

hours = 24

args = Script.getPositionalArgs()

def usage():
  gLogger.info(' Type "%s --help" for the available options and syntax' % Script.scriptName)
  DIRAC.exit(-1)

from DIRAC.FrameworkSystem.Client.NotificationClient  import NotificationClient
from DIRAC.Core.Security.Misc                         import getProxyInfo
from DIRAC                                            import gConfig,gLogger
from DIRAC.Core.DISET.RPCClient import RPCClient
from DIRAC.ResourceStatusSystem.Utilities.CS import getMailForUser

nc = NotificationClient()

s = RPCClient("ResourceStatus/ResourceStatus")

res = getProxyInfo()
if not res['OK']:
  gLogger.error("Failed to get proxy information",res['Message'])
  DIRAC.exit(2)
userName = res['Value']['username']
group = res['Value']['group']
if group not in ('diracAdmin', 'lhcb_prod'):
  gLogger.error("You must be lhcb_prod or diracAdmin to execute this script")
  gLogger.info("Please issue 'lhcb-proxy-init -g lhcb_prod' or 'lhcb-proxy-init -g diracAdmin'")
  DIRAC.exit(2)

if not type(args) == type([]):
  usage()
if not args:
  gLogger.error("There were no arguments provided")
  DIRAC.exit()

for arg in args:
  g = s.whatIs(arg)
  res = s.reAssignToken(g, arg, userName)
  if not res['OK']:
    gLogger.error("Problem with re-assigning token for %s: " % res['Message'])
    DIRAC.exit(2)
  mailMessage = "The token for %s %s has been successfully re-assigned." %(g, arg)
  nc.sendMail(getMailForUser(userName)['Value'][0], 'Token for %s reassigned' %arg, mailMessage)

DIRAC.exit(0)
