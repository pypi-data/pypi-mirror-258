import requests, requests_cache, time
from requests.exceptions import HTTPError
import logging
from urllib.parse import urlencode

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MAX_RETRIES = 3
CACHE_NAME = 'riot_api_cache'
EXPIRE_AFTER = 3600
ERROR_TIME_SLEEP = 3
REGION_TO_PLATFORM = {
    'eun1': 'europe',
    'euw1': 'europe',
    'tr1': 'europe',
    'ru': 'europe',
    'jp1': 'asia',
    'kr': 'asia',
    'br1': 'americas',
    'la1': 'americas',
    'la2': 'americas',
    'na1': 'americas',
    'oc1': 'americas'
}

class RequestHandler:
    def __init__(self, api_key, region, use_platform, max_retries=MAX_RETRIES ,use_cache=True):
        self.api_key = api_key
        self.region = region
        self.use_platform = use_platform
        self.max_retries = max_retries
        self.session = requests.Session()
        self.set_cache()
    
    def set_cache(self, cache_name=CACHE_NAME):
        requests_cache.install_cache(cache_name)

    def build(self, region, endpoint, query_params=None):
        domain = REGION_TO_PLATFORM[region] if self.use_platform else region
        base_url = f"https://{domain}.api.riotgames.com{endpoint}"
        
        return base_url if not query_params else f'{base_url}?{urlencode(query_params)}'

    def make_request(self, endpoint, query_params=None):
        self.retries = 0
        url = self.build(self.region, endpoint, query_params)
        headers = {'X-Riot-Token': self.api_key}

        while self.retries < self.max_retries:
            try:
                response = self.session.get(url, headers=headers)
                response.raise_for_status()

                return response.json()
            except requests.exceptions.RequestException as e:
                self.retries += 1
                self.handle_error(e)
                logging.info(f"Retrying : {self.retries}/{self.max_retries}")
                #logging.info(f"Url : {e.request.url}")
        
        logging.info("Max retries reached.")
        return None

    def sleep_interruptable(self, seconds):
        try:
            time.sleep(seconds)
        except KeyboardInterrupt:
            logging.info("Interrupted by user.")
            raise KeyboardInterrupt

    def handle_error(self, exception):
        if isinstance(exception, requests.exceptions.ConnectionError):
            logging.info(f"Unable to connect to the server: {exception.response.status_code}")

        elif isinstance(exception, requests.exceptions.HTTPError):
            logging.info(f"HTTP error occurred: {exception.response.status_code}")

            if exception.response.status_code == 429:
                retry_after = exception.response.headers['Retry-After']
                logging.info(f"Waiting {retry_after} seconds before retrying...")
                self.sleep_interruptable(int(retry_after))
            elif exception.response.status_code == 403:
                logging.info("Forbidden. Check your API key.")
                self.sleep_interruptable(ERROR_TIME_SLEEP)
            elif exception.response.status_code == 404:
                logging.info("Not found.")
                self.sleep_interruptable(ERROR_TIME_SLEEP)
            elif exception.response.status_code == 500:
                logging.info("Internal server error.")
                self.sleep_interruptable(ERROR_TIME_SLEEP)
            elif exception.response.status_code == 503:
                logging.info("Service unavailable.")
                self.sleep_interruptable(ERROR_TIME_SLEEP)
        else:
            logging.info(f"An unexpected error occurred: {exception.response.status_code}")