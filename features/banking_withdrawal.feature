@banking @withdrawal
Feature: Customer withdrawal on XYZ Bank
  As a bank customer
  I want to withdraw money from my account
  So that I can use my funds

  # Covers F5, NFR-2, NFR-4
  # Note: the tab is spelled "Withdrawl" in the UI (known quirk)

  Background:
    Given the customer is on the XYZ Bank home page

  @FR-5.1
  Scenario: Withdrawl tab shows the amount field and submit button
    When the customer logs in as "Harry Potter"
    And the customer opens the "Withdrawl" tab
    Then the amount field is displayed
    And the "Withdraw" submit button is displayed

  @smoke @FR-5.2
  Scenario Outline: Withdraw within available balance
    When the customer logs in as "<customer>"
    And the customer selects account "<account>"
    And the customer deposits "<deposit>"
    And the current balance of the account is recorded
    When the customer withdraws "<amount>"
    Then the message "Transaction successful" is displayed
    And the balance is decreased by "<amount>"
    And a screenshot named "<customer>_<account>_after_withdrawal" is taken

    Examples:
      | customer           | account | deposit | amount |
      | Harry Potter       | 1004    | 1000    | 400    |
      | Ron Weasly         | 1007    | 500     | 1      |
      | Neville Longbottom | 1015    | 750     | 749    |

  @FR-5.2 @boundary
  # Open question in SRS section 8: assumed allowed
  Scenario: Withdraw exactly the full balance
    When the customer logs in as "Hermoine Granger"
    And the customer selects account "1001"
    And the customer deposits "2000"
    When the customer withdraws the full balance
    Then the message "Transaction successful" is displayed
    And the balance is "0"

  @negative @FR-5.3
  Scenario: Withdrawal greater than balance is refused
    When the customer logs in as "Albus Dumbledore"
    And the customer selects account "1010"
    And the current balance of the account is recorded
    When the customer withdraws an amount 1 greater than the balance
    Then the message "Transaction Failed. You can not withdraw amount more than the balance." is displayed
    And the balance is unchanged
    And no new transaction is created

  @negative @FR-5.3
  Scenario: Withdrawal from an empty account is refused
    Given the user logs in as Bank Manager
    And the manager has added a customer "Cho" "Chang" with post code "E2002"
    And the manager has opened a "Pound" account for "Cho Chang"
    When the user goes to the home page
    And the customer logs in as "Cho Chang"
    And the customer selects the recorded account
    When the customer withdraws "1"
    Then the message "Transaction Failed. You can not withdraw amount more than the balance." is displayed
    And the balance is "0"

  @negative @FR-5.4 @NFR-4
  Scenario Outline: Invalid withdrawal amount is rejected
    Given the customer logs in as "Ron Weasly"
    And the customer selects account "1008"
    And the customer deposits "1000"
    And the current balance of the account is recorded
    When the customer withdraws "<amount>"
    Then the message "Transaction successful" is not displayed
    And the balance is unchanged
    And no new transaction is created

    Examples:
      | amount | case        |
      |        | empty       |
      | 0      | zero        |
      | -100   | negative    |
      | abc    | non-numeric |
      | 10.5   | decimal     |

  @FR-5.5
  Scenario: Withdrawal creates a Debit transaction
    When the customer logs in as "Harry Potter"
    And the customer selects account "1005"
    And the customer deposits "300"
    And the customer withdraws "120"
    And the customer opens the Transactions tab
    Then a "Debit" transaction of "120" is listed

  @FR-5.5 @negative
  Scenario: A refused withdrawal creates no Debit transaction
    When the customer logs in as "Albus Dumbledore"
    And the customer selects account "1011"
    And the number of transactions is recorded
    When the customer withdraws an amount 1 greater than the balance
    And the customer opens the Transactions tab
    Then the number of transactions is unchanged

  @performance @NFR-2
  Scenario: Balance updates within 1 second of withdrawal
    Given the customer logs in as "Harry Potter"
    And the customer selects account "1006"
    And the customer deposits "100"
    And the current balance of the account is recorded
    When the customer withdraws "40"
    Then the balance is decreased by "40" within 1 second
