import requests
import config


def pin_to_pinata(file_obj, filename):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    payload = {}
    files = [
        ('file', (filename, file_obj, 'image/jpeg'))
    ]
    headers = {
        'pinata_api_key': '4332bafc5b243c8f4d04',
        'pinata_secret_api_key': 'f98b41132ea90fddc09a5254363afd3223775551a0824a678916b3cdb360dfc5'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response.json()