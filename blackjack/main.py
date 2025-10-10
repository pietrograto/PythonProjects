import os 
from art import logo  
import random  



def deal_card():
    """Return a random card from the deck.
    
    Returns:
        int: Card value (11 for Ace, 10 for face cards, pip value for others)
    """
    cards = [11,2,3,4,5,6,7,8,9,10,10,10,10]
    card = random.choice(cards)
    # print({card})
    return card

def calculate_score(cards):
    """Calculate blackjack score from a list of cards.
    
    Args:
        cards (list): List of card values
        
    Returns:
        int: Calculated score (0 for blackjack, actual sum otherwise)
    """
    
    if sum(cards)== 21 and len(cards) == 2:
        return 0 

    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1) 

    return sum(cards)

def compare(user_score, computer_score):
  #Bug fix. If you and the computer are both over, you lose.
  if user_score > 21 and computer_score > 21:
    return "You went over. You lose 😤"


  if user_score == computer_score:
    return "Draw 🙃"
  elif computer_score == 0:
    return "Lose, opponent has Blackjack 😱"
  elif user_score == 0:
    return "Win with a Blackjack 😎"
  elif user_score > 21:
    return "You went over. You lose 😭"
  elif computer_score > 21:
    return "Opponent went over. You win 😁"
  elif user_score > computer_score:
    return "You win 😃"
  else:
    return "You lose 😤"


def play_game():
    """Main game loop for blackjack.
    
    Handles card dealing, user input, and game logic until completion.
    """

    print(logo)
    user_cards = []
    computer_cards = []
    is_game_over = False
        
    for _ in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())

    while not is_game_over:

        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)
        print(f"your cards: {user_cards}, current score {user_score}")
        print(f"Computer cards: {computer_cards}, current score {computer_score}")

        if user_score == 0 or computer_score == 0 or user_score >21:
            is_game_over = True
        else:
            user_should_deal = input("type 'y' to get another card, type 'n' to pass: ")
            if user_should_deal == 'y':
                user_cards.append(deal_card())
            else:
                is_game_over = True
        
    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)

    print(f"   Your final hand: {user_cards}, final score: {user_score}")
    print(f"   Computer's final hand: {computer_cards}, final score: {computer_score}")
    print(compare(user_score, computer_score))

while input("Do you want to play a game of Blackjack? Type 'y' or 'n': ") == "y":
    os.system("clear")
    play_game()