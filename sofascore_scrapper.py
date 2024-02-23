from network_scrapper import RemoteNetworkDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time
import logging
from dotenv import load_dotenv
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S'
)


load_dotenv(override=True)
username = os.getenv('PROXY_USERNAME')
password = os.getenv('PROXY_PASSWORD')
endpoint = os.getenv('PROXY_ENDPOINT')
port     = os.getenv('PROXY_PORT')

proxy = {
    'username': username,
    'password': password,
    'endpoint': endpoint,
    'port'    : port,
}
# Proxie service: (SmartProxy)
# https://dashboard.smartproxy.com/residential-proxies/proxy-setup
network_driver = RemoteNetworkDriver(proxy=proxy)
# network_driver = RemoteNetworkDriver()

# execute the script to hide the fact that the browser is automated
# network_driver.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: function() {return false}})")


# def get_match_events(
#         url : str = 'https://www.sofascore.com/everton-wolverhampton/dsY#id:11352592'
# ):
    

#     logging.info(f"Getting url {url}...")
#     network_driver.get(url)

#     time.sleep(5)
#     # A estratégia é puxar o XPATH de cada um dos Campos, iterar pelas listas em dois niveis
#     # (Primeiro nivel se refere as linhas dos jogadores no campo, segundo nível se refere aos jogadores
#     # em cada linha), clicar no WebElement e depois fechar o pop-up que irá abrir com as informações
#     # do jogador, para evitar que a pagina fique muito pesada.

#     logging.info("Positioning page on appropriate location ...")
#     field_top_locationon_site = network_driver.driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[1]/div[2]/div[2]')
#     field_top_locationon_site.location_once_scrolled_into_view

#     logging.info("Getting information from home team players ...") 
#     home_team_xpath = '//*[@id="__next"]/main/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[1]/*'
#     away_team_xpath = '//*[@id="__next"]/main/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div[3]/div[1]/*'

#     for team_xpath in [home_team_xpath, away_team_xpath]: 
#         team_lines = network_driver.driver.find_elements(By.XPATH, team_xpath)
#         for line in team_lines:
#             players = line.find_elements(By.XPATH, './*')
#             for player in players:
#                 logging.info(f'Getting information from player {player.text}')
#                 time.sleep(1)
#                 player.click()
#                 time.sleep(2)
#                 try:
#                     wait = WebDriverWait(network_driver.driver, 10)
#                     wait.until(
#                         EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/div[3]/div/div/div/div[1]/div/div[1]/div/button[2]')),
#                         message=f'The button with player pop-up was not closed properly due to timeout when loading the WebElement from player {player.text}.')
#                     close_popup_button = network_driver.driver.find_element(By.XPATH,'//*[@id="__next"]/main/div[3]/div/div/div/div[1]/div/div[1]/div/button[2]')
#                     time.sleep(2)
#                     close_popup_button.click()
#                 except TimeoutException as e:
#                     logging.error(f"Error closing popup: {e}")
#                 time.sleep(1)

#     network_driver.get_network_events()
#     network_driver.get_network_responses(url_to_find='https://api.sofascore.com/api/v1/event/')

#     stop = True



# def get_matches_on_league():
    
url : str = 'https://www.sofascore.com/tournament/football/england/premier-league/17'

logging.info(f"Getting url {url}...")
network_driver.get(url)

time.sleep(5)
# A estratégia é puxar o XPATH de cada um dos Campos, iterar pelas listas em dois niveis
# (Primeiro nivel se refere as linhas dos jogadores no campo, segundo nível se refere aos jogadores
# em cada linha), clicar no WebElement e depois fechar o pop-up que irá abrir com as informações
# do jogador, para evitar que a pagina fique muito pesada.


# logging.info("Positioning page on appropriate location to select year ...")
# year_top_locationon_site = network_driver.driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[1]/div[1]')
# year_top_locationon_site.location_once_scrolled_into_view
# Aqui precisamos ajustar o elemento que temos que buscar para garantir que vamos deixar o campo necesário visivel


# logging.info("Selecting desired season year")
# year_button = network_driver.driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/button/div/svg')
# year_button.click()

# time.sleep(3)
# selected_season = '23/24'
# seasons = network_driver.driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div/div[1]/ul/*')
# for season in seasons:
#     if season.value_of_css_property == selected_season:
#         season.click()
#         break

logging.info("Positioning page on appropriate location to select desired round ...")
round_top_locationon_site = network_driver.driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[3]')
round_top_locationon_site.location_once_scrolled_into_view

by_round_button = network_driver.driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[5]/div/div[2]/div[2]')
by_round_button.click()

round_selector = network_driver.driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[5]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/button')
round_selector.click()

round_list = network_driver.driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[5]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/div/*')[0].find_elements(By.XPATH, './*')[0].find_elements(By.XPATH, './*')
for round in round_list:
    round.click()
    
    logging.info("Getting matches from selected round ...")
    
    match_list = network_driver.driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[3]/div/div[3]/div/div/div[1]/div/div[2]/*')
    for match in match_list:
        match_details = match.find_elements(By.XPATH, './*')[0]
    break