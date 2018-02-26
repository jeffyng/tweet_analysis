import oauth2
import constants
import urllib.parse as urlparse

consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)


def get_request_token():
    # Create a consumer, which uses CONSUMER_KEY and CONSUMER_SECRET to identify our app uniquely.
    client = oauth2.Client(consumer)

    # Use the client to get a request token.
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status != 200:
        raise Exception('An error occured getting the request token from Twitter!')

    return dict(urlparse.parse_qsl(content.decode('utf-8')))

def get_oauth_verifier(request_token):
    # Ask user to authorize our app and give us the pin code.
    print('Go to the following site in your browser:')
    print(get_oauth_verifier_url(request_token))
    return input('What is hte PIN? ')

def get_oauth_verifier_url(request_token):
    return '{}?oauth_token={}'.format(constants.AUTHORIZATION_URL, request_token['oauth_token'])

def get_access_token(request_token, oauth_verifier):
    # Create a token object which containts the request token and the verifier.
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    # Create a client with our consumer (our app) and the newly created (and verified) token.
    client = oauth2.Client(consumer, token)

    # Ask Twitter for an access token.
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    return dict(urlparse.parse_qsl(content.decode('utf-8')))
    _