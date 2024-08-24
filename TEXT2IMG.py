import base64
import uuid
import json
import time

import requests


class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images, width, height):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)



def txt2img(PROMPT, BY):
    if PROMPT == "":
        PROMPT = "Очень пушистый милый кот в шляпе, 3D мир, Blender, Рендеринг"
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/',
                        '3D0ECE83D2EE48556200E110FF1123DB',
                        'B91EABAD9532F00C382EF41C6A106F58')
    model_id = api.get_model()
    uuidg = api.generate(PROMPT, model_id, images=1, width=1024, height=1024)
    images = api.check_generation(uuidg)
    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)
    FID = str(uuid.uuid4())
    SCR = f"img/img---{FID}---{PROMPT[:30]}---@{BY}.jpg"
    with open(SCR, "wb") as file:
        file.write(image_data)
        file.close()
    # list.append(SCR)
    return SCR

