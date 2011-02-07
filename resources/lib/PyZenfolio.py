#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      David
#
# Created:     09.01.2011
# Copyright:   (c) David 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

try:
    import simplejson
except ImportError:
    import json as simplejson

import logging
import random
import struct
import urllib2
import logging
import sha256

class Error(Exception):
    pass


class RpcError(Error):
    def __init__(self, code=None, message=None):
        Error.__init__(self)
        self.code = code
        self.message = message
        print code, message


class HttpError(Error):
    def __init__(self, code=None, headers=None, url=None, body=None):
        Error.__init__(self)
        self.code = code
        self.headers = headers
        self.url = url
        self.body = body
        print code, headers
        print url
        print body


def PackParams(*args):
    return simplejson.dumps(args)


def MakeRequest(method, params, auth=None, use_ssl=True):
    headers = {'Content-Type': 'application/json',
               'User-Agent': 'PyZenfolio Library',
               'X-Zenfolio-User-Agent': 'PyZenfolio Library'}

    if auth is not None:
        headers['X-Zenfolio-Token'] = auth

    if use_ssl is False and auth is None:
        url = 'http://www.zenfolio.com/api/1.4/zfapi.asmx'
    else:
        url = 'https://www.zenfolio.com/api/1.4/zfapi.asmx'

    body = '{ "method": "%s", "params": %s' % (method, params)
    body += ', "id": %d }' % random.randint(1, 2**16 - 1)

    headers['Content-Length'] = len(body)

    try:
        return urllib2.urlopen(urllib2.Request(url, body, headers))
    except urllib2.HTTPError, e:
        raise HttpError(code=e.code, headers=e.headers, url=e.url, body=e.read())


def Call(method, auth=None, use_ssl=False, params=None):
    if params is None:
        params = '[]'

    try:
        resp = MakeRequest(method, params, auth, use_ssl)
    except HttpError, e:
        logging.warning('ZenFolio API Call for %s failed with params: %s\n' +
                        'response code %d with body:\n %s', method, params,
                        e.code, e.body)
        raise Error
    else:
        response = resp.read()
        rpc_obj = simplejson.loads(response)
        if rpc_obj['error'] is None:
            return rpc_obj['result']
        else:
            if 'code' in rpc_obj['error']:
                raise RpcError(message=rpc_obj['error']['message'], code=rpc_obj['error']['code'])
            else:
                raise RpcError(message=rpc_obj['error']['message'])


def GetChallenge(username):
    return Call('GetChallenge', params=PackParams(username))


def Authenticate(auth_challenge, password):
    salt = ''.join([chr(x) for x in auth_challenge['PasswordSalt']])
    challenge = ''.join([chr(x) for x in auth_challenge['Challenge']])

    combo = salt + password.encode('utf-8')
    h2 = sha256.sha256(combo)
    combo = challenge + h2.digest()
    h1 = sha256.sha256(combo)
    proof = h1.digest()

    byte_proof = struct.unpack('B'*32, proof)

    try:
        resp = Call('Authenticate',
                  use_ssl=True,
                  params=PackParams(auth_challenge['Challenge'], byte_proof))
    except RpcError, e:
        logging.warning(
            'Authentication failed code: %s and message: %s', e.code, e.message)
        return None
    else:
        return resp


def AuthenticatePlain(username, password):
    return Call('AuthenticatePlain', use_ssl=True, params=PackParams(username, password))


def LoadPrivateProfile(auth):
  return Call('LoadPrivateProfile', auth=auth)


def LoadGroupHierarchy(username, auth=None):
    return Call('LoadGroupHierarchy', auth=auth, params=PackParams(username))


def LoadGroup(group_id, auth=None):
    return Call('LoadGroup', auth=auth, params=PackParams(group_id, "Full", True))


def LoadPhotoSet(photoset_id, auth=None):
    return Call('LoadPhotoSet', auth=auth, params=PackParams(photoset_id, "Full", True))


def GetPopularPhotos(offset=0, limit=0, auth=None):
    return Call('GetPopularPhotos', auth=auth, params=PackParams(offset, limit))


def GetPopularSets(photoset_type=None, offset=0, limit=20, auth=None):
    if photoset_type not in ('Gallery', 'Collection'):
        raise ValueError('photoset type has invalid valid: %s' % photoset_type)

    return Call('GetPopularSets', auth=auth, params=PackParams(photoset_type, offset, limit))


def GetRecentPhotos(offset=0, limit=20, auth=None):
    return Call('GetRecentPhotos', auth=auth, params=PackParams(offset, limit))


def GetRecentSets(photoset_type=None, offset=0, limit=20, auth=None):
    if photoset_type not in ('Gallery', 'Collection'):
        raise ValueError('photoset type has invalid valid: %s' % photoset_type)

    return Call('GetRecentSets', auth=auth, params=PackParams(photoset_type, offset, limit))

#
#if __name__ == "__main__":
#
#    try:
#        logging.info("authenticating...")
#        auth_challenge = GetChallenge(username)
#        auth = Authenticate(auth_challenge, password)
#        logging.info("loading...")

#        h = LoadPrivateProfile(auth)

#        for e in h["Elements"]:
#            print e["Title"]
#            pprint.pprint(e)

        #pprint.pprint(g)

#    except RpcError, e:
#        print e.code, ' ', e.message
#        logging.error('RPC Error: %s and message: %s', e.code, e.message)