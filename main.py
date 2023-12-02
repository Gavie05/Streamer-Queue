import json
import asyncio
from token_refresh import get_new_token
from fetch_queue import get_queue

#how often to request queue data
cooldown = 1

# Get access token, refresh token, expiration time, and base64 encoded client id and secret for refreshing auth
access_token, expires = get_new_token()

# Refresh Access Token before it expires
async def countdown(expires):
    expires -= 60

    while True:
        await asyncio.sleep(expires)
        global access_token
        access_token, expires = get_new_token()
        expires -= 60
        print('token refreshed')

#Request Queue data and save to json
async def makerequest(cooldown):

    json_file_directory = r'response.json'

    while True:
        response, request_code = get_queue(access_token)

        if request_code == 200:
            if response['currently_playing']:
                with open(json_file_directory, 'w') as write_file: #Open Json File
                    json.dump(response, write_file, indent=4)  #Rewrite Json File

            await asyncio.sleep(cooldown)

        elif request_code == 429:
            print('Rate limit exceeded')
            await asyncio.sleep(30)

        else:
            print(f'ERROR {request_code}')
            await asyncio.sleep(60)
            
        


async def main():
    await asyncio.gather(countdown(expires), makerequest(cooldown))


if __name__ == '__main__':
    asyncio.run(main())
