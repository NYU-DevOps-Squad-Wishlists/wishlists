Feature: The Wishlists REST API for Items
    As a Wishlists Owner
    I need a RESTful wishlist service
    So that I can keep track of all the items on specific wishlists

    Scenario: The server is running and some Wishlists already exist
        Given a set of specific wishlists
            | name              | customer_id |
            | Birthday Wishlist | 234         |
            | Test Wishlist     | 345         |
        When I visit the "Home Page"
        Then I should see the title "Wishlist REST API Service"
        And I should not see the title "404 Not Found"
        And I should see "Birthday Wishlist" as an option in "wishlist_selector"
        And I should see "Test Wishlist" as an option in "wishlist_selector"

    Scenario: Add a new Item to a specific Wishlist
        When I select the Wishlist "Birthday Wishlist" from "wishlist_selector"
        And I add a new Item with name "Laptop"
        And I press the button "Add Item" in the "Item" form
        Then I should see the message "Item added successfully!" in "item_result"
        And the server response code should be "201" in "item_response_code"

    Scenario: Edit an Item on a specific Wishlist
        When I change "item_name_0" to "Blueberries"
        And I press the button "Update Item" in the "Item" form
        Then I should see the message "Item updated successfully" in "item_result"
        And I should see "Blueberries" in "item_name_0"
        And the server response code should be "200" in "item_response_code"
