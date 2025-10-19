from tkinter import *
from tkinter import messagebox
import pandas
import random
from datetime import datetime, timedelta

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
is_flipped = False


def load_words_with_spaced_repetition():
    """Initialize or load spaced repetition data for words."""
    global to_learn
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        # Try to load existing spaced repetition data
        saved_data = pandas.read_csv("data/spaced_repetition.csv")
        to_learn = saved_data.to_dict(orient="records")

    except FileNotFoundError:
        # Create new spaced repetition data from original words
        original_data = pandas.read_csv("data/french_words.csv")
        to_learn = []

        for word in original_data.to_dict(orient="records"):
            word.update({
                'repetitions': 0,
                'interval': 1,
                'ease_factor': 2.5,
                'due_date': today,
                'last_reviewed': today
            })
            to_learn.append(word)

        # Save initial data
        save_progress()


def save_progress():
    """Save current progress to CSV."""
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/spaced_repetition.csv", index=False)


def get_due_words():
    """Get words that are due for review today."""
    today = datetime.now().strftime("%Y-%m-%d")
    due_words = [word for word in to_learn if word['due_date'] <= today]
    # Show 5 random words if no words are due
    return due_words if due_words else to_learn[:5]


def get_next_word():
    """Get the next word to review based on due date."""
    due_words = get_due_words()
    return random.choice(due_words)


def next_card():
    """Display next flashcard with random French word."""
    global current_card, flip_timer, is_flipped

    window.after_cancel(flip_timer)

    current_card = get_next_word()
    is_flipped = False

    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    flip_timer = window.after(3000, func=toggle_card)


def toggle_card():
    """Toggle between French and English translation."""
    global is_flipped, flip_timer

    if flip_timer:
        window.after_cancel(flip_timer)

    if is_flipped:
        # Show fron card
        canvas.itemconfig(canvas_image, image=card_front_img)
        canvas.itemconfig(card_title, text="French", fill="black")
        canvas.itemconfig(card_word, text=current_card["French"], fill="black")
        is_flipped = False
    else:

        # Show back card
        canvas.itemconfig(canvas_image, image=card_back_img)
        canvas.itemconfig(card_title, text="English", fill="white")
        canvas.itemconfig(
            card_word, text=current_card["English"], fill="white")
        is_flipped = True


def is_known():
    """Remove word from list of words to learn."""
    update_word_stats(current_card, True)
    save_progress()
    print(f"Next review in {current_card['interval']} days")

    next_card()


def is_unknown():
    """Update word statistics for incorrect response."""
    update_word_stats(current_card, False)
    save_progress()
    print(f"Will review again in {current_card['interval']} day(s)")

    next_card()


def update_word_stats(word, is_correct):
    """Update word statistics based on user response using SM-2 algorithm."""
    today = datetime.now().strftime("%Y-%m-%d")

    if is_correct:
        if word['repetitions'] == 0:
            word['interval'] = 1
        elif word['repetitions'] == 1:
            word['interval'] = 6
        else:
            word['interval'] = int(word['interval'] * word['ease_factor'])

        word['repetitions'] += 1
        word['ease_factor'] = max(
            1.3, word['ease_factor'] + (0.1 - (5 - 3) * (0.08 + (5 - 3) * 0.02)))
    else:
        word['repetitions'] = 0
        word['interval'] = 1
        word['ease_factor'] = max(1.3, word['ease_factor'] - 0.2)

    # Calculate next due date
    next_date = datetime.now() + timedelta(days=word['interval'])
    word['due_date'] = next_date.strftime("%Y-%m-%d")
    word['last_reviewed'] = today


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Choose learning mode with dialog
load_words_with_spaced_repetition()

flip_timer = window.after(3000, func=toggle_card)
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
canvas.bind("<Button-1>", lambda event: toggle_card())

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(
    image=cross_image, highlightthickness=0, command=is_unknown)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(
    image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()
window.mainloop()
