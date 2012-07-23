# $HeadURL:  $
''' EmailAction

'''

from DIRAC                                                      import S_ERROR, S_OK, gLogger
#from DIRAC.ResourceStatusSystem.Client.ResourceStatusClient     import ResourceStatusClient
from DIRAC.ResourceStatusSystem.PolicySystem.Actions.BaseAction import BaseAction
from DIRAC.ResourceStatusSystem.Utilities.InfoGetter            import InfoGetter

__RCSID__ = '$Id:  $'

class EmailAction( BaseAction ):

  def __init__( self, decissionParams, enforcementResult, singlePolicyResults, clients = None ):
    
    super( EmailAction, self ).__init__( decissionParams, enforcementResult, 
                                         singlePolicyResults, clients )
    self.actionName = 'EmailAction'

  def run( self ):
    
    # Minor security checks
    
    element = self.decissionParams[ 'element' ]
    if element is None:
      return S_ERROR( 'element should not be None' )
   
    name = self.decissionParams[ 'name' ] 
    if name is None:
      return S_ERROR( 'name should not be None' )
    
    statusType = self.decissionParams[ 'statusType' ]
    if statusType is None:
      return S_ERROR( 'statusType should not be None' )
    
    status = self.enforcementResult[ 'Status' ]    
    if status is None:
      return S_ERROR( 'status should not be None' )

    reason = self.enforcementResult[ 'Reason' ]
    if reason is None:
      return S_ERROR( 'reason should not be None' )
    
    if self.decissionParams[ 'status' ] == status:
      # If status has not changed, we skip
      return S_OK()

    if self.decissionParams[ 'reason' ] == reason:
      # If reason has not changed, we skip
      return S_OK()
      
    subject = '%s %s %s is on status %s' % ( element, name, statusType, status )
    
    body = 'Enforcement result\n'
    body += '\n'.join( [ '%s : %s' % ( key, value ) for key, value in self.enforcementResult.items() ] )
    body += '\n'
    body += '*' * 50
    body += '\nOriginal parameters\n'
    body += '\n'.join( [ '%s : %s' % ( key, value ) for key, value in self.decissionParams.items() ] )
    body += '\n'
    body += '*' * 50
    body += '\nPolicies run\n'
    
    for policy in self.singlePolicyResults:
      
      body += '\n'.join( [ '%s : %s' % ( key, value ) for key, value in policy.items() if not key == 'Policy' ] )
      body += '\n'.join( [ '%s : %s' % ( key, value ) for key, value in policy[ 'Policy' ].items() ] )
      body += '\n'
        
    return self._sendMail( subject, body )

  def _sendMail( self, subject, body ):
    
    from DIRAC.Interfaces.API.DiracAdmin import DiracAdmin
    diracAdmin = DiracAdmin()
    
    address = InfoGetter().getNotificationsThatApply( self.decissionParams, self.actionName )
    if not address[ 'OK' ]:
      return address 
    address = address[ 'Value' ]
    
    for addressDict in address:
      if not 'name' in addressDict:
        return S_ERROR( 'Malformed address dict %s' % addressDict ) 
      if not 'users' in addressDict:
        return S_ERROR( 'Malformed address dict %s' % addressDict )     
    
      gLogger.info( 'Notifying users of %s' % addressDict[ 'name' ] )
      
      for user in addressDict[ 'users' ]:
      
        resEmail = diracAdmin.sendMail( user, subject, body )
        if not resEmail[ 'OK' ]:
          return S_ERROR( 'Cannot send email to user "%s"' % user )    
      
    return resEmail 
    
################################################################################
#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF