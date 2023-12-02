# Take refresh token and encoded auth string and return new tokens
def get_new_token():

    import requests
    import json

    JSON_FILE_DIRECTORY = r'user_data.json'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    
    open_file = open(JSON_FILE_DIRECTORY) #Open json into variable
    json_data = json.load(open_file) #Load json into variable

    refresh_token = json_data['REFRESH_TOKEN']
    auth_value = json_data['AUTH_VALUE']

    # Refresh Token request data
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    
    # Refresh Token request headers
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + auth_value
    }
    
    # Exchange refresh token for new acces token
    refresh_response = requests.post(TOKEN_URL, data=data,headers=headers)

    # Convert json data into strings
    access_token = refresh_response.json()['access_token']
    expires_in = refresh_response.json()['expires_in']

    return access_token, expires_in
