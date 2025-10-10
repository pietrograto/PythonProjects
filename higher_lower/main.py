from art import logo, vs
from data import data
import random
import os

#print(data[0]['description'])

def compare_followers(entry1, entry2):
    print(f"Compare the number of followers for {entry1['name']} {vs} the number of followers for {entry2['name']}:")
    
    guess = input("Which one has more followers? Type '1' for the first entry, '2' for the second entry: ")
    
    if guess == '1':
        return entry1['follower_count'] > entry2['follower_count']
    elif guess == '2':
        return entry2['follower_count'] > entry1['follower_count']
    else:
        print("Invalid input. Please type '1' or '2'.")
        return None

def get_random_entries(data):
    return random.sample(data, 2)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo)


def play_game():
    print(logo)
    score = 0
    current_entry1 = get_random_entries(data)[0]
    current_entry2 = get_random_entries(data)[0]

    while True:
        #selected_entries = get_random_entries(data)
        #result = compare_followers(selected_entries[0], selected_entries[1])
        result = compare_followers(current_entry1, current_entry2)

        if result is not None:
            if result:
                print("You guessed correctly! The first entry has more followers.")
                score += 1
                print(f"Your current score is: {score}")
                # Swap entries after a correct guess
                #selected_entries[0], selected_entries[1] = selected_entries[1], get_random_entries(data)[0]
                current_entry1, current_entry2 = current_entry2, get_random_entries(data)[0]
            else:
                print("Oops! The second entry has more followers.")
                print(f"Your final score is: {score}")
                score = 0  # Reset the score after a failure
                
        play_again = input("Do you want to play again? Type 'yes' or 'no': ")
        if play_again.lower() != 'yes':
            break
        else:
            clear_screen()

play_game()