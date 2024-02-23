## Classe criada para ser utilizada em conjunto com a docker image do selenium/standalone-chrome-debug

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import LOGGER
from smart_proxy_extension import proxies
import time
import json
import logging
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S'
)
# LOGGER.setLevel(logging.DEBUG)

class RemoteNetworkDriver():
    
    def __init__(
            self,
            remote_server_addr: str = 'http://localhost:4444/wd/hub',
            vendor_prefix: str = 'goog',
            browser_name: str = 'chrome',
            keep_alive: bool = True,
            headless: bool = False,
            proxy: str = None
        ) -> None:

        self.options = Options()
        self.headless = headless
        if self.headless:
            self.options.add_argument("--headless")
        if proxy:
            username, password, endpoint, port = proxy['username'], proxy['password'], proxy['endpoint'], proxy['port']
            proxy_url = f"http://{username}:{password}@{endpoint}:{port}"
            proxies_extension = proxies(username, password, endpoint, port)
            self.options.add_extension(proxies_extension)
            # self.options.add_argument(f"--proxy-server={proxy}")
        
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--enable-logging")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--v=1")
        self.options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        self.driver = webdriver.Remote(
            command_executor=ChromiumRemoteConnection(
                    remote_server_addr=remote_server_addr, 
                    vendor_prefix=vendor_prefix, 
                    browser_name=browser_name, 
                    keep_alive=keep_alive, 
                    ignore_proxy=self.options._ignore_local_proxy
                ),
            options=self.options
        )
        self.driver.execute(
        "executeCdpCommand", {"cmd": "Network.enable", "params": {}}
        )

        self.raw_events = []
        self.events = []
        self.selected_events = []


    def __del__(self):
        """
        Ensures Chrome process is closed when the class instance is garbage collected.
        """
        self.driver.quit()

    def get(self, url):
        self.driver.get(url)

    def get_network_events(
            self
    ) -> None:
        logging.info("Getting network logs ...")
        self.raw_events = self.driver.get_log("performance")

        self.events = [
            {
                'event_timestamp': event["timestamp"],
                'level': event["level"],
                'message': event["message"],
                'method': json.loads(event["message"])["message"].get('method', None),
                'webview': json.loads(event["message"])["message"].get('webview', None),
                **{
                    key: value
                    for key, value in json.loads(event["message"])["message"]['params'].items()
                },
            }
            for event in self.raw_events
        ]
    
    def get_network_responses(
            self,
            url_to_find: str,
            method: str = "Network.responseReceived"
    ) -> None:

        self.selected_events = []

        logging.info("Getting body messages from selected network messages ...")
        logging.info(f"Looking for events with method = {method} and base_url = {url_to_find}")
        for event in self.events:
            if (event['method'] == method and 
                event['response']['url'].startswith(url_to_find)):
                try:
                    response_body = self.driver.execute(
                        "executeCdpCommand", 
                        {
                            "cmd": "Network.getResponseBody", 
                            "params": {
                                "requestId": event['requestId']
                            }
                        }
                    )
                    self.selected_events.append({
                        **event,
                        'response':{
                            'responseBody':response_body['value']['body'],  # Para uma função mais generica, talvez faça sentido não realizar a transformação para dict aqui, mas sim no scrapper do site.
                            **event['response']
                        }
                    })

                except WebDriverException as err:
                    if "No data found for resource" in err.msg:
                        pass
                    else:
                        raise err
                
    
## Exemplo 1: Random site
# network_driver = RemoteNetworkDriver()
# network_driver.get("https://gerg.dev/2021/06/making-chromedriver-and-chrome-versions-match-in-a-docker-image/")
# logging.info(f"Title is: {network_driver.driver.title}")

# logging.info("Starting to get events ...")
# time.sleep(5)
# events = network_driver.get_network_events()
# # logging.info(f"Events: {events}")
# # logging.info("\nDone getting events ...")
# time.sleep(200)

## Exemplo 2: SkyScanner
# origin='gyn'
# destination='gru'
# date='240113'

# network_driver = RemoteNetworkDriver()

# logging.info("Connecting to skyscanner url ...")
# network_driver.get(f"https://www.skyscanner.com.br/transporte/passagens-aereas/{origin}/{destination}/{date}")

# time.sleep(5)

# network_driver.get_network_events()
# url_to_find = 'https://www.skyscanner.com.br/g/conductor/v1/fps3/search/'
# network_driver.get_netowork_responses(url_to_find=url_to_find)

stop=True