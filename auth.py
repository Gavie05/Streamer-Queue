# Startup task
# Prompt user to authorize access --> Get redirect url from user --> Verify redirect url
# --> Fetch code from redirect url --> Exchange code for Access and Refresh Tokens
# --> Return Access Token and Refresh Token
def get_tokens():

    from auth_base64_encoder import auth_encode
    import requests
    import secrets
    import string
    import webbrowser

    # OAuth provider configuration
    CLIENT_ID = 'CLIENT_ID'
    CLIENT_SECRET = 'CLIENT_SECRET'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    REDIRECT_URI = 'http://localhost:8080'

    redirect_confirmation = ''

    # Convert client id and client secret into base64 for "Authorization" Header
    auth_value = auth_encode(CLIENT_ID, CLIENT_SECRET)


    # Generate random string for state
    state_length = 16
    state = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                for i in range(state_length))

    # Ask for permission to open web browser
    while redirect_confirmation != 'y':
        redirect_confirmation = input('A new tab will open for your Authorization. Please Agree and paste the full url you are redirected to. \nContinue? (y/n):').lower()
        if redirect_confirmation == 'n':
            print('Exiting Program')
            exit()

    # Open authorization in webbroweer
    webbrowser.open_new_tab(f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8080&scope=user-read-playback-state&state={state}')

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

    # Exchange authorization code for an access token
    token_response = requests.post(TOKEN_URL, data=data,headers=headers)

    # Convert json data into strings
    access_token = token_response.json()['access_token']
    refresh_token = token_response.json()['refresh_token']
    expires_in = token_response.json()['expires_in']

    return access_token, refresh_token, expires_in, auth_value




