import json
import requests
import secrets
import string
import webbrowser
from auth_base64_encoder import auth_encode

JSON_FILE_DIRECTORY = r'user_data.json'
REDIRECT_URI = 'http://localhost:8080'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

state_length = 16
state = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
            for i in range(state_length))

open_file = open(JSON_FILE_DIRECTORY) #Open json into variable
json_data = json.load(open_file) #Load json into variable

client_id = input('Client Id: ')
client_secret = input('Client Secret: ')
auth_value = auth_encode(client_id, client_secret)


# Open authorization in webbrowser
webbrowser.open_new_tab(f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8080&scope=user-read-playback-state&state={state}')

# Get callback url
authorization_response = input('Enter the full callback URL: ')

# Get Callback state
callback_state = authorization_response[-16:]

# Check if state and callback_state are the same
if state != callback_state:
    print('Error: callback state is different than auth state')
    exit()

# Check if access was granted
if authorization_response[23:-23] == 'error=access_denied':
    print('Access was denied')
    exit()

# Fetch authorization code from callback url
code = authorization_response[0:-23].removeprefix('http://localhost:8080/?code=')

# Access token request data
data = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': REDIRECT_URI
}

# Access token request headers
headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic ' + auth_value
}

token_response = requests.post(TOKEN_URL, data=data,headers=headers)

if token_response.status_code != 200:
    print(f'error {token_response.status_code}')
    exit()

refresh_token = token_response.json()['refresh_token']

json_data['REFRESH_TOKEN'] = refresh_token
json_data['CLIENT_ID'] = client_id
json_data['CLIENT_SECRET'] = client_secret
json_data['AUTH_VALUE'] = auth_value

with open (JSON_FILE_DIRECTORY, 'w') as write_file:
    json.dump(json_data, write_file, indent=4)