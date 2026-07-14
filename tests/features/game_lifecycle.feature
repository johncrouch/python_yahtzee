Feature: Game lifecycle through the API
  As a player
  I want to create games and play turns
  So that I can enjoy a Yahtzee game

  Scenario: Creating a game and adding a player
    Given a new game
    When I add a player named "Ada" in seat 1
    Then the player should be created successfully
    And the game should contain 1 player

  Scenario: Starting a game and rolling dice
    Given a new game with player "Ada" in seat 1
    When I start the game
    And I roll the dice
    Then the response should contain 5 dice values
