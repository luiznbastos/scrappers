from network_scrapper import RemoteNetworkDriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

network_driver = RemoteNetworkDriver()

url = 'https://1xbet.whoscored.com/Matches/1729505/Live/England-Premier-League-2023-2024-Liverpool-Arsenal'

def get_match_events(
        network_driver: RemoteNetworkDriver, 
        url: str):
    network_driver.get(url)

    network_driver.get_network_events()
    network_driver.get_network_responses(url_to_find=url)

    soup = BeautifulSoup(network_driver.selected_events[0]['response']['responseBody'], "html.parser")
    # #extrair as tags script
    script_tags = soup.find_all("script")
    script_contents = [tag.string for tag in script_tags]
    # #selecionar a tag script desejada
    data = [content for content in script_contents if (content is not None and 'require.config.params["args"]' in content)][0]
    # #tratar o dado
    data = [content for content in script_contents if (content is not None and 'require.config.params["args"]' in content)][0].replace('\r\n        require.config.params["args"] = ','').replace(';\r\n    ', '')
    data = data.replace('formationIdNameMappings', '"formationIdNameMappings"').replace('matchId','"matchId"').replace('matchCentreData','"matchCentreData"').replace('matchCentreEventTypeJson','"matchCentreEventTypeJson"')
    data = json.loads(data)
    
    return data

    # Voilà!!
    # Data collected :D

data = get_match_events(network_driver, url)



stop = True




