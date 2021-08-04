Feature: The Wishlists REST API for Wishlists
    As a Wishlists Owner
    I need a RESTful wishlist service
    So that I can keep track of all the wishlists

    Scenario: The server is running
        When I visit the "Home Page"
        Then I should see the title "Wishlist REST API Service"
        And I should not see the title "404 Not Found"

    Scenario: Add a new Wishlist without correct data
        When I enter a new Wishlist with no data
        And I press the button "Create Wishlist" in the "Wishlist" form
        Then I should see the message "Invalid wishlist: missing name" in "wishlist_result"
        And the server response code should be "400" in "wishlist_response_code"

    Scenario: Add a new Wishlist with correct data
        When I enter a new Wishlist with name "Amazon" and customer_id "123"
        And I press the button "Create Wishlist" in the "Wishlist" form
        Then I should see the message "Wishlist created successfully!" in "wishlist_result"
        And the server response code should be "201" in "wishlist_response_code"

    Scenario: List all Wishlists
        When I press the button "List Wishlists" in the "Wishlist" form
        Then I should see the message "Wishlists printed below" in "wishlist_result"
        And the table "wishlist_list_table" should contain at least one row
        And the server response code should be "200" in "wishlist_response_code"

    Scenario: Read a Wishlist
        When I enter an existing Wishlist ID into the "wishlist_read_id" input field
        And I press the button "Read Wishlist" in the "Wishlist" form
        Then I should see the message "Wishlist printed below" in "wishlist_result"
        And the server response code should be "200" in "wishlist_response_code"
        And the table "wishlist_read_table" should contain at least one row

    Scenario: Search Wishlists
        When I enter "123" in the "search_customer_id" input field
        And I press the button "Search Wishlists" in the "Wishlist" form
        Then I should see the message "Search results below" in "wishlist_result"
        And the table "wishlist_search_table" should contain at least one row
        And the server response code should be "200" in "wishlist_response_code"

    Scenario: Update a Wishlist
        When I change "wishlist_name_0" to "Etsy Wishlist"
        And I change "wishlist_customer_id_0" to "456"
        And I press the button "Update Wishlist" in the "Wishlist" form
        Then I should see the message "Wishlist updated successfully" in "wishlist_result"
        And I should see "Etsy Wishlist" in "wishlist_name_0"
        And I should see "456" in "wishlist_customer_id_0"

    Scenario: Delete a Wishlist
        When I press the button "Delete Wishlist" in the "Wishlist" form
        Then I should see the message "Wishlist deleted successfully" in "wishlist_result"
        And the server response code should be "204" in "wishlist_response_code"
