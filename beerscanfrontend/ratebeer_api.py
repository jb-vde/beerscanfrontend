import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service



def flatten(list):

    return [x for sublist in list for x in sublist]

def make_query(beer_name):

    query = "+".join(beer_name.split())
    query = "\\'".join(query.split("'"))

    return query

def api_response(beer_info_list):

    key_list = ["brewery", "beer", "style", "abv", "overall_score",
                "style_score", "star_rating", "n_reviews"]
    value_list = [el for el in beer_info_list if not el.startswith("Available")]
    value_list = [el.split('•') for el in value_list]
    value_list = flatten(value_list)

    return dict(zip(key_list, value_list))



def load_driver():
    opts = Options()
    opts.binary_location = os.environ.get('FIREFOX_BIN')
    serv = Service(os.environ.get('GECKODRIVER_PATH'))

	# enable trace level for debugging
    opts.log.level = "trace"
    opts.add_argument("-remote-debugging-port=9224")
    opts.add_argument("-headless")
    opts.add_argument("-disable-gpu")
    opts.add_argument("-no-sandbox")
    firefox_driver = webdriver.Firefox(service=serv, options=opts)

    return firefox_driver


def search_beer(beer_name):

    driver = load_driver()

    query = make_query(beer_name)
    driver.get(f'https://www.ratebeer.com/search?q={query}&tab=beer')

    try:
        beer = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[class='fg-1']")))

    except TimeoutException:
        print("Loading took too much time!")
        beer = None


    beer_text = beer.get_attribute('innerText')
    beer_info_list = beer_text.split('\n')
    driver.quit()

    return api_response(beer_info_list)

def main():

    beer_name = "westvleteren"
    response = search_beer(beer_name)

    print(response)


if __name__ == "__main__":
    main()
