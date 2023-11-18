# Take refresh token and encoded auth string and return new tokens
def get_new_token(refresh_token, auth_value):

    import requests
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

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
    print(refresh_response.json())
    access_token = refresh_response.json()['access_token']
    expires_in = refresh_response.json()['expires_in']

    return access_token, expires_in


