import constants
import oauth2
import urllib.parse as urlparse
import json
from user import User
from database import Database

Database.initialize(user='app_user', password='app_password', host='localhost', database='tweets')

# Create a consumer, which uses CONSUMER_KEY and CONSUMER_SECRET to identify our app uniquely.
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
client = oauth2.Client(consumer)

# Use the client to get a request token.
response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
if response.status != 200:
    raise Exception('An error occured getting the request token from Twitter!')

# Parse the returned query string and assign it to request token.
request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

# Ask user to authorize our app and give us the pin code.
print('Go to the following site in your browser:')
print('{}?oauth_token={}'.format(constants.AUTHORIZATION_URL, request_token['oauth_token']))

oauth_verifier = input('What is the PIN?  ')

# Create a client with our consumer (our app) and the newly created (and verified) token.
token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth2.Client(consumer, token)

# Ask Twitter for an access token.
response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

email = input('Enter your email: ')
first_name = input('Enter your first name: ')
last_name = input('Enter your last name: ')

user = User(email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)
user.save_to_db()

# Create 'authorized_token' Token object and use it to perform Twitter API calls on behalf of user.
authorized_token = oauth2.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
authorized_client = oauth2.Client(consumer, authorized_token)

# Make Twitter API calls.
response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images', 'GET')

if response.status != 200:
    raise Exception('An error occurred during authorized_client Twitter API call')

tweets = json.loads(content.decode('utf-8'))

for tweet in tweets['statuses']:
    print(tweet['text'])
