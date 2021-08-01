"""
Environment for Behave Testing
"""
from os import getenv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '3'))
BASE_URL = getenv('BASE_URL', 'http://localhost:5000/app/index.html')


def before_all(context):
    """ Executed once before all tests """
    
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")  # open browser in maximized mode
    options.add_argument("disable-infobars")  # disabling infobars
    options.add_argument("--disable-extensions")  # disabling extensions
    options.add_argument("--disable-gpu")  # applicable to windows os only
    options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    options.add_argument("--no-sandbox")  # bypass OS security model
    options.add_argument("--headless")

    context.WAIT_SECONDS = WAIT_SECONDS

    context.driver = webdriver.Chrome(options=options)
    context.driver.set_window_size(1120, 550)
    context.driver.implicitly_wait(context.WAIT_SECONDS)  # seconds
    context.base_url = BASE_URL
    # -- SET LOG LEVEL: behave --logging-level=ERROR ...
    # on behave command-line or in "behave.ini"
    context.config.setup_logging()


def after_all(context):
    """ Executed after all tests """
    context.driver.quit()

def after_scenario(context, scenario):
    # clear the results box for the next feature test
    clear_wishlist_button = context.driver.find_element_by_id("wishlist_result_clear")
    wishlist_result = context.driver.find_element_by_id("wishlist_result")
    actions = ActionChains(context.driver)
    actions.move_to_element(clear_wishlist_button)
    actions.click(clear_wishlist_button)
    actions.perform()
    WebDriverWait(context.driver, WAIT_SECONDS).until(
           expected_conditions.text_to_be_present_in_element(
               (By.ID, "wishlist_result_status"),
               "Status: Awaiting next action"
           )
    )
