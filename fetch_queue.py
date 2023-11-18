# Recieve access token
# return response from endpoint and response code
def get_queue(access_token):
    
    import requests

    END_URL = 'https://api.spotify.com/v1/me/player/queue'
    
    # POST request headers
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    queue_response = requests.get(END_URL, headers=headers)
    response_code = queue_response.status_code
    response_json = queue_response.json()

    return response_json, response_code