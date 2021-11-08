#api.spotify_tools.access

#Contains methods for requesting access tokens
import api.spotify_tools.base as base
from datetime import datetime, timedelta
import engine.async_if as async_if
import engine.signal as signal
import json

cc_token = None

#Set cc_time to a time that has already expired
cc_time = datetime.now() - timedelta(hours=1)

class TokenResponseErrorCC(Exception):
    pass

class TokenResponseErrorAC(Exception):
    pass

class TokenNotReturnedError(Exception):
    pass

async def get_token_cc():
    #Get a token using client credentials flow
    now = datetime.now()
    
    global cc_token, cc_time
    if cc_time < now or not cc_token:
        #Request new token (try three times)
        data = {"grant_type": "client_credentials", "client_id": base.client_id.content, "client_secret": base.client_secret.content}
        i = 0
        while i < 2:
            try:
                resp = await async_if.post_response(base.token_url, data=data)
                if resp.code == 200:
                    i = 2
                else:
                    i += 1
                    if i == 2:
                        raise TokenResponseErrorCC("Error: access token could not be retrieved from Spotify.")
            except:
                i += 1
                if i == 2:
                    raise TokenResponseErrorCC("Error: access token could not be retrieved from Spotify.")
        
        if resp.code != 200:
            raise TokenNotReturnedError("Error: token request failed.")
        
        js = json.loads(resp.body)
        
        cc_token = js["access_token"]
        #Take ten seconds off the expires_in just to be safe (Spotify often returns responses with times one second earlier than now.)
        cc_time = now + timedelta(seconds=js["expires_in"] - 10)
    
    return cc_token

async def get_token_ac(refresh_token):
    #Get a token using authorisation code flow using a refresh token (try three times)
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token, "client_id": base.client_id.content, "client_secret": base.client_secret.content}
    i = 0
    while i < 2:
        try:
            resp = await async_if.post_response(base.token_url, data=data)
            if resp.code == 200:
                i = 2
            else:
                i += 1
                if i == 2:
                    raise TokenResponseErrorAC("Error: access token could not be retrieved from Spotify.")
        except:
            i += 1
            if i == 2:
                raise TokenResponseErrorAC("Error: access token could not be retrieved from Spotify.")
    
    if resp.code != 200:
        raise TokenNotReturnedError("Error: token request failed.")
    
    js = json.loads(resp.body)
    
    return js["access_token"]

async def get_token_from_code(code, redirect_uri, returnVar="JS"):
    #Get a token using authorisation code flow using an access code
    data = {"grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri, "client_id": base.client_id.content, "client_secret": base.client_secret.content}
    
    resp = await async_if.post_response(base.token_url, data=data)
    
    if resp.code != 200:
        raise TokenNotReturnedError("Error: token request failed.")
    
    js = json.loads(resp.body)
    
    if returnVar == "JS":
        return js
    elif returnVar == "access_token":
        return js[returnVar]

async def reset_cc_token():
    #Reset the cc_token to None when the -Refresh_Assets signal is called
    global cc_token
    cc_token = None

signal.reload_hooks += [reset_cc_token]