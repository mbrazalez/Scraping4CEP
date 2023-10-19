import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Webdriver setup
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

# Get the page for sraping and switch to the iframe that contains the air quality data
driver.get("https://www.troposfera.es/albacete/red-albacete/panel-mapa-de-datos.html")
time.sleep(5)
iframe = driver.find_element(by=By.XPATH, value='//*[@id="contenidoAire"]/div/iframe')
driver.switch_to.frame(iframe)

# Dictionary for store the analyzed data
scraped_data = {}


# Function to obtain the station which are in the scraped page
def get_stations():
    i = 0
    while True:
        try:
            station = driver.find_element(by=By.XPATH,value=f'//*[@id="cdk-accordion-child-0"]/div/div/div[{i+1}]/siam-dashboard-estacion/mat-card/mat-card-header/div[2]/mat-card-title/span')
            i += 1
            scraped_data[station.text] = {}
        except:
            break
def get_data():
    for i in range(len(scraped_data.keys())):
        params_list = []
        j = 0
        while True:
            try:
                # The param, its data and the time in which it was obtained from the station is scrapped
                param = str(driver.find_element(by=By.XPATH, value=f'//*[@id="mat-tab-content-{i+1}-{j}"]/div/div[1]/div[2]/div/div').text)
                param_data = str(driver.find_element(by=By.XPATH, value=f'//*[@id="mat-tab-content-{i+1}-{j}"]/div/div[1]/div[2]/div').text)
                time_data = str(driver.find_element(by=By.XPATH, value= f'//*[@id="mat-tab-content-{i+1}-{j}"]/div/div[2]').text)
                params_list.append({'name':param, 'data':param_data.split('\n')[1], 'time':time_data})

                # The dashboard is swapped in order to scrap the next param
                j += 1
                change_param = driver.find_element(by=By.XPATH, value=f'//*[@id="mat-tab-label-{i+1}-{j}"]')
                change_param.click()
                time.sleep(0.5)

            except:
                break

        scraped_data[list(scraped_data.keys())[i]] = params_list

if __name__ == '__main__':
    get_stations()
    get_data()

