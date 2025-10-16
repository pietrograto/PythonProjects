from tkinter import *
from tkinter import messagebox
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}


def choose_mode():
    """Ask user if they want to continue from where they left off or review all words."""
    global to_learn
    
    try:
        saved_data = pandas.read_csv("data/words_to_learn.csv")
        words_to_learn = saved_data.to_dict(orient="records")
        
        if len(words_to_learn) > 0:
            result = messagebox.askyesno(
                "Continue Learning?", 
                f"You have {len(words_to_learn)} words left to learn.\n\nContinue from where you left off?"
            )
            
            if result:  # Yes - continue learning
                to_learn = words_to_learn
            else:  # No - start over with all words
                original_data = pandas.read_csv("data/french_words.csv")
                to_learn = original_data.to_dict(orient="records")
        else:
            messagebox.showinfo("Congratulations!", "You've learned all words! Starting over.")
            original_data = pandas.read_csv("data/french_words.csv")
            to_learn = original_data.to_dict(orient="records")
            
    except FileNotFoundError:
        original_data = pandas.read_csv("data/french_words.csv")
        to_learn = original_data.to_dict(orient="records")


def get_random_word():
    """Get a random French-English word pair."""
    return random.choice(to_learn)


def next_card():
    """Display next flashcard with random French word."""
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = get_random_word()
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    """Flip flashcard to reveal English translation."""
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def is_known():
    """Remove word from list of words to learn."""
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Choose learning mode with dialog
choose_mode()

flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=(
    "Arial", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="word", font=(
    "Arial", 60, "bold"), fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(
    image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(
    image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()
window.mainloop()
