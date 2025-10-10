from art import logo 
import os
import random

def play_game():
    print(logo)
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")

    user_choice = input("Choose a difficulty. Type 'easy' or 'hard': ").lower()
    number = random.randint(1, 100)
    attempts = 0

    if user_choice == 'easy':
        attempts = 10
    elif user_choice == 'hard':
        attempts = 5
    else:
        print("Invalid difficulty choice. Please choose 'easy' or 'hard'.")
        return

    while attempts > 0:
        print(f"You have {attempts} attempts left.")
        user_guess = int(input("Make a guess: "))

        if user_guess > number:
            print("Too high")
        elif user_guess < number:
            print("Too low")
        else:
            print(f"You got it! The answer was: {number}")
            break  # End the game if the guess is correct

        attempts -= 1

    if attempts == 0:
        print(f"You lose. The correct answer was: {number}")

play_game()

