Feature: The Wishlists REST API back-end
    As a Wishlists Owner
    I need a RESTful wishlist service
    So that I can keep track of all the wishlists and their items

Scenario: The server is running
        When I visit the "Home Page"
        Then I should see the title "Wishlist REST API Service"
        And I should not see the title "404 Not Found"

Scenario: Add a new Wishlist
        When I enter a new Wishlist with name "Amazon" and customer_id "123"
        And I press the button "Create Wishlist"
        Then I should see the success message "Wishlist created successfully!" in "createResult_wishlist"
        And the server response should be "201"
