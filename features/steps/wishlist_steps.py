from os import getenv
from behave import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

buttonDictionary = {
        "Create Wishlist": "wishlist_create"
}

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

@when('I press the button "{button}"')
def step_impl(context, button):
    button_element = context.driver.find_element_by_id(buttonDictionary[button])
    actions = ActionChains(context.driver)
    actions.move_to_element(button_element)
    actions.click(button_element)
    actions.perform()
    try:
        WebDriverWait(context.driver, WAIT_SECONDS).until(
           expected_conditions.text_to_be_present_in_element(
               (By.ID, "wishlist_result_status"),
               "Status: Transaction complete"
           )
        )
    finally:
        for entry in context.driver.get_log('browser'):
            print(entry)

@then('I should see the message "{message}" in "{element_id}"')
def step_impl(context, message, element_id):
    element = context.driver.find_element_by_id(element_id)
    assert message in element.text

@then('the server response code should be "{code}" in "{element_id}"')
def step_impl(context, code, element_id):
    element = context.driver.find_element_by_id(element_id)
    response = "Response code: " + code
    assert response in element.text
