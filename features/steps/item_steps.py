from os import getenv
from behave import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from service.models import Item, Wishlist

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '3'))

@given('a set of specific wishlists')
def step_impl(context):
    for row in context.table:
        wishlist = Wishlist(name=row['name'], customer_id=row['customer_id'])
        wishlist.create()

@then('I should see "{label}" as an option in "{select_id}"')
def step_impl(context, label, select_id):
    select_element = context.driver.find_element_by_id(select_id)
    options = select_element.find_elements(By.TAG_NAME, 'option')
    found = False
    for option in options:
        print(option.get_attribute("value"))
        if option.text == label:
            found = True
    assert found is True

@when('I select the Wishlist "{name}" from "{select_id}"')
def step_impl(context, name, select_id):
    select_element = context.driver.find_element_by_id(select_id)
    select = Select(select_element)
    select.select_by_visible_text(name)

@when('I add a new Item with name "{name}"')
def step_impl(context, name):
    name_input = context.driver.find_element_by_id("item_name")
    name_input.clear()
    name_input.send_keys(name)

@then('the value of column "{column_name}" in "{table_id}" for row "{row_index}" should be "{value_test}"')
def step_impl(context, column_name, table_id, row_index, value_test):
    table = context.driver.find_element_by_id(table_id)
    rows = table.find_elements(By.TAG_NAME, 'tr')
    header_row = rows[0].find_elements(By.TAG_NAME, 'th')
    column_header_text = list(map(lambda th: th.text, header_row))
    column_index = int(column_header_text.index(column_name))
    cells = rows[int(row_index)].find_elements(By.TAG_NAME, 'td')
    target_cell = cells[column_index]
    assert bool(target_cell.text) is bool(value_test)
