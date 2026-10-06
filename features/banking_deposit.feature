@banking
Feature: Customer deposit on XYZ Bank
  As a bank customer
  I want to deposit money into my account
  So that my account balance is increased by the deposited amount

  Background:
    Given the customer is on the XYZ Bank home page

  @smoke @deposit
  Scenario Outline: Deposit money and verify the updated balance
    When the customer logs in as "<customer>"
    And the customer selects account "<account>"
    Then the current balance of the account is recorded
    When the customer deposits "<amount>"
    Then the message "Deposit Successful" is displayed
    And the balance is increased by "<amount>"
    And a screenshot named "<customer>_<account>_after_deposit" is taken
    When the customer logs out
    Then the customer login screen is displayed

    Examples:
      | customer         | account | amount |
      | Harry Potter     | 1004    | 500    |
      | Hermoine Granger | 1001    | 1500   |
      