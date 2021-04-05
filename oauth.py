import requests
import json

def get_token(clientID, clientsecret, tokenURL):
    ''' Returns the response of the token request.
    '''
    tokenResponse = requests.post(tokenURL, data={'grant_type': 'client_credentials'}, auth=(clientID, clientsecret))
    tokenJson = tokenResponse.json()
    return tokenJson

def make_request(token, query, url):
    ''' Makes a request using the token and GraphQL query.
    '''
    with requests.Session() as s:
        HEADERS = {'Authorization': 'Bearer ' + token}
        s.headers.update(HEADERS)
        response = s.get(url, json={"query": query})
    return response