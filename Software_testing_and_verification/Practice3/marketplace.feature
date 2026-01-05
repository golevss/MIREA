Feature: Marketplace basic flows

  Scenario: Seller adds a listing and buyer finds it
    Given a fresh marketplace
    When seller "alice" adds a listing with title "Vintage Clock" and price 49.99
    Then searching for "clock" returns at least 1 result

  Scenario: Buyer messages seller
    Given a listing exists with title "Headphones"
    When buyer "bob" sends message "Is it new?" to that listing
    Then the listing message history contains a message from "bob"

  Scenario: Delivery status update
    Given a listing exists
    When seller updates delivery status to "shipped"
    Then the listing status is "shipped"
