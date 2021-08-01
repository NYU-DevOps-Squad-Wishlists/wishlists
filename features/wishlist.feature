Feature: The Wishlists REST API back-end
    As a Wishlists Owner
    I need a RESTful wishlist service
    So that I can keep track of all the wishlists and their items

Scenario: The server is running
        When I visit the "Home Page"
        Then I should see the title "Wishlist REST API Service"
        And I should not see the title "404 Not Found"

Scenario: Add a new Wishlist without correct data
        When I enter a new Wishlist with no data
        And I press the button "Create Wishlist"
        Then I should see the message "Invalid wishlist: missing name" in "wishlist_result"
        And the server response code should be "400" in "wishlist_response_code"

Scenario: Add a new Wishlist with correct data
        When I enter a new Wishlist with name "Amazon" and customer_id "123"
        And I press the button "Create Wishlist"
        Then I should see the message "Wishlist created successfully!" in "wishlist_result"
        And the server response code should be "201" in "wishlist_response_code"

