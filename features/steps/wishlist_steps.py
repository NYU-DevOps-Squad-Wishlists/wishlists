from os import getenv
from behave import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


WAIT_SECONDS = int(getenv('WAIT_SECONDS', '3'))

@when('I visit the "Home Page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)

@then('I should see the title "{message}"')
def step_impl(context, message):
    """ Check the document title for a message """
    assert message in context.driver.title

@then('I should not see the title "{message}"')
def step_impl(context, message):
    assert message not in context.driver.title

@when('I enter a new Wishlist with name "{name}" and customer_id "{customer_id}"')
def step_impl(context, name, customer_id):
    name_input = context.driver.find_element_by_name("wishlist_name")
    name_input.clear()
    name_input.send_keys(name)
    customer_id_input = context.driver.find_element_by_name("customer_id")
    customer_id_input.clear()
    customer_id_input.send_keys(customer_id)

@when('I enter a new Wishlist with no data')
def step_impl(context):
    name_input = context.driver.find_element_by_name("wishlist_name")
    name_input.clear()
    # print('name: (' + name_input.get_attribute('value') + ')')
    name_input.send_keys("")
    customer_id_input = context.driver.find_element_by_name("customer_id")
    customer_id_input.clear()
    # print('customer_id: (' + customer_id_input.get_attribute('value') + ')')
    customer_id_input.send_keys("")

@when('I enter an existing Wishlist ID into the "{input_id}" input field')
def step_impl(context, input_id):
    # get the ID out of the first row of this list table
    # this will ensure we don't rely on ID "1" existing
    list_table = context.driver.find_element_by_id("wishlist_list_table")
    rows = list_table.find_elements(By.TAG_NAME, 'tr')
    cells = rows[1].find_elements(By.TAG_NAME, 'td')
    wishlist_id = cells[0].text

    id_field = context.driver.find_element_by_id(input_id)
    id_field.clear()
    id_field.send_keys(wishlist_id)
