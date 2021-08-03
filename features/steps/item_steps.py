from os import getenv
from behave import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from service.models import Item, Wishlist

buttonDictionary = {
        "Add Item": "item_create"
}

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '3'))

@given('a set of specific wishlists')
def step_impl(context):
    for row in context.table:
        wishlist = Wishlist(name=row['name'], customer_id=row['customer_id'])
        wishlist.create()
        print(wishlist.id)

@then('I should see "{label}" as an option in "{select_id}"')
def step_impl(context, label, select_id):
    select_element = context.driver.find_element_by_id(select_id)
    options = select_element.find_elements(By.TAG_NAME, 'option')
    found = False
    print(options)
    for option in options:
        print(option.get_attribute("value"))
        if option.text == label:
            found = True
    assert found is True

@when('I select the Wishlist "{name}" from "{select_id}"')
def step_impl(context, name):
    select_element = context.driver.find_element_by_id(select_id)
    select_element.select_by_visible_text(name)

@when('I add a new Item with name "{name}"')
def step_impl(context, name):
    name_input = context.driver.find_element_by_name("item_name")
    name_input.clear()
    name_input.send_keys(name)
