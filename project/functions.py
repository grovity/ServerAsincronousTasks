import http.client
import json
import re
import jwt
from time import time

import requests

import dateutil.parser
import os
from tqdm import tqdm


import logging
import os
from typing import TypeVar, cast, Dict, List
from drive_api import DriveAPI
from drive_api_exception import DriveAPIException

#token = "00"#"eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IlVFZDBaYV9lVHZxMkFDMWZDNUUtZFEiLCJleHAiOjE2Nzk0MTM4NzQsImlhdCI6MTY3ODgwOTA3NH0.ukP8Ja05WXgbvC-_UgmJF5kh6R_RQ5qUOCmjAiV6eE0"
API_SECRET = os.environ ["API_SECRET_ZOOM"]#"p2juMvG4ifA9x8StadY1lixePaH7Z7nMQuNy"
API_KEY = os.environ["API_KEY_ZOOM"]#"UEd0Za_eTvq2AC1fC5E-dQ"
USUARIO = os.environ["USER_ZOOM"]#"servidor.genie@gmail.com"






def request_zoom(method, url, payload=None, body=None, exp=0):
        
        if not payload:
            payload = {
                "exp": int(time()) + 5000,
                "iss": API_KEY,
            }
        token = jwt.encode(payload, API_SECRET, algorithm='HS256')
        conn = http.client.HTTPSConnection("api.zoom.us")

        #print('token', token)
        if isinstance(token,str):
            headers = {
            'authorization': "Bearer " + token,
            'content-type': "application/json",
        }
        else:
           headers = {
                'authorization': "Bearer " + token.decode(),
                'content-type': "application/json",
            }

        conn.request(method, url, body, headers=headers)
        resp = conn.getresponse()
        status = resp.status
        resp = resp.read()

        resp = json.loads(resp.decode())


        return resp, status, token

def obt_video_evento(meeting):
        print(API_SECRET)
        print("variable")
        print(API_KEY)
        res, status, token = request_zoom("GET", f"/v2/meetings/{meeting}/recordings")
        full_filename = f"{meeting}.mp4"

        if (status // 100) == 2:
            url = res['recording_files'][0].get('download_url')
            if isinstance(token,str):
                token_decode = token
            else:
                token_decode = token.decode()
            url = f'{url}?access_token={token_decode}'
            url = requests.head(url).headers['Location']
            
            
            response = requests.get(url, stream=True)
            block_size = 32 * 1024  # 32 Kibibytes
            total_size = int(response.headers.get('content-length', 0))
            try:
                t = tqdm(total=total_size, unit='iB', unit_scale=True)
                with open(full_filename, 'wb') as fd:
                    # with open(os.devnull, 'wb') as fd:  # write to dev/null when testing
                    for chunk in response.iter_content(block_size):
                        t.update(len(chunk))
                        fd.write(chunk)  # write video chunk to disk
                print("Descarga Finalizada")
                t.close()
                return True
            except Exception as e:
                # if there was some exception, print the error and return False
                print(e)
                return False
        else:
            return False


def upload(id_reunion):
    drive_api = DriveAPI("client_secret.json","/tmp")  # This should open a prompt.
    try:
        
        # Get url from upload function.
        file_url = drive_api.upload_file(f"{id_reunion}.mp4",f"{id_reunion}.MP4" ,"1PoFVsTKGO7aL9Gm380GWN-HQW6KnTHSX")

        # The formatted date/time string to be used for older Slack clients
        # fall_back = f"{file['date']} UTC"

        # Only post message if the upload worked.
        # message = (f'The recording of _{file["meeting"]}_ on '
        #             "_<!date^" + str(file['unix']) + "^{date} at {time}|" + fall_back + ">_"
        #             f' is <{file_url}| now available>.')
        print(f"Listo la carga de la Reunión {id_reunion}")

    except DriveAPIException as e:
        raise e


