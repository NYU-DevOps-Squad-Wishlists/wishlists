"""
Environment for Behave Testing
"""
from behave import *
from os import getenv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '3'))
# PORT = int(getenv('PORT', 8080))
# BASE_URL = getenv('BASE_URL', 'http://127.0.0.1:' + str(PORT) + '/app/index.html')
BASE_URL = getenv('BASE_URL', 'http://127.0.0.1:5000/app/index.html')

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

    # enable browser logging
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = { 'browser':'ALL' }

    context.driver = webdriver.Chrome(options=options, desired_capabilities=d)
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
               "Awaiting next action"
           )
    )

    clear_item_button = context.driver.find_element_by_id("item_result_clear")
    item_result = context.driver.find_element_by_id("item_result")
    actions = ActionChains(context.driver)
    actions.move_to_element(clear_item_button)
    actions.click(clear_item_button)
    actions.perform()
    WebDriverWait(context.driver, WAIT_SECONDS).until(
           expected_conditions.text_to_be_present_in_element(
               (By.ID, "item_result_status"),
               "Awaiting next action"
           )
    )


# the following are shared Gherkin steps between Wishlists and Items:

buttonDictionary = {
        "Create Wishlist": "wishlist_create",
        "List Wishlists": "wishlist_list",
        "Read Wishlist": "wishlist_read",
        "Search Wishlists": "wishlist_search",
        "Update Wishlist": "wishlist_update_0",
        "Delete Wishlist": "wishlist_delete_0",
        "Add Item": "item_create",
        "Update Item": "item_update_0",
        "Delete Item": "item_delete_0",
        "Purchase Item": "item_purchase_0"
}

@when('I press the button "{button}" in the "{type}" form')
def step_impl(context, button, type):
    button_element = context.driver.find_element_by_id(buttonDictionary[button])
    actions = ActionChains(context.driver)
    actions.move_to_element(button_element)
    actions.click(button_element)
    actions.perform()
    result_field = "wishlist_result_status" if type == "Wishlist" else "item_result_status"
    try:
        WebDriverWait(context.driver, WAIT_SECONDS).until(
           expected_conditions.text_to_be_present_in_element(
               (By.ID, result_field),
               "Transaction complete"
           )
        )
        actions.reset_actions()
    finally:
        print('Timeout encountered, browser console logs:')
        for entry in context.driver.get_log('browser'):
            print(entry)

@then('I should see the message "{message}" in "{element_id}"')
def step_impl(context, message, element_id):
    element = context.driver.find_element_by_id(element_id)
    assert message in element.text

@then('the server response code should be "{code}" in "{element_id}"')
def step_impl(context, code, element_id):
    element = context.driver.find_element_by_id(element_id)
    assert code in element.text

@then('the table "{table_id}" should contain at least one row')
def step_impl(context, table_id):
    table = context.driver.find_element_by_id(table_id)
    html = table.get_attribute("innerHTML")
    assert "<tr class=\"dataRow\">" in html

@when('I enter "{search_string}" in the "{search_field}" input field')
def step_impl(context, search_string, search_field):
    search_input = context.driver.find_element_by_id(search_field)
    search_input.clear()
    search_input.send_keys(search_string)

@when('I change "{input_id}" to "{new_value}"')
def step_impl(context, input_id, new_value):
    input_element = context.driver.find_element_by_id(input_id)
    input_element.clear()
    input_element.send_keys(new_value)

@then('I should see "{value}" in "{input_id}"')
def step_impl(context, value, input_id):
    input_element = context.driver.find_element_by_id(input_id)
    assert value in input_element.get_attribute('value')
