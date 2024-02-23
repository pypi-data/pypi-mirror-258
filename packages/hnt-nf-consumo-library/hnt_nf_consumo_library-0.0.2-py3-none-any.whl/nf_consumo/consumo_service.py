from os import getenv
import requests
import json
from dotenv import load_dotenv

from nf_consumo.fs_util import DEFAULT_OUTPUT, local_saved_path

DOWNLOAD_URL = "{url}/externals/ged/Download"
DOWNLOAD_TIMEOUT = 30

class ConsumoService:
    def __init__(self):
        load_dotenv()
        self.host = getenv("NEXINVOICE_API")
        self._set_request()

    def _set_request(self):
        self._api_headers = {
            'ApiKeyClient': getenv("API_KEY_CLIENT"),
            'ApiKeyAuth': getenv("API_KEY_AUTH"),
            'Content-Type': 'application/json',
        }

    def download_pdf(self, content, dest_dir=DEFAULT_OUTPUT):
        res = requests.get(
            url=DOWNLOAD_URL.format(url=self.host),
            timeout=DOWNLOAD_TIMEOUT,
            headers=self._api_headers,
            data=json.dumps(content))
        res.raise_for_status()

        saved_path = local_saved_path(content, dest_dir)        
        open(saved_path['full_path'], 'wb').write(res.content)
        return saved_path
