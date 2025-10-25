import customtkinter as ctk
from tkinter import Canvas, PhotoImage
from tkinter import messagebox
import pandas
import random
from datetime import datetime, timedelta

# Set CustomTkinter appearance
ctk.set_appearance_mode("light")  # Dark theme for modern look
ctk.set_default_color_theme("blue")  # "green", "dark-blue"

BACKGROUND_COLOR = "#2b2b2b"
# Menu color constants
MENU_BG = '#12c4c0'
MENU_HOVER = '#0f9d9a'
MENU_TEXT = '#262626'

current_card = {}
to_learn = {}
is_flipped = False
current_difficulty_filter = None  # Tracks selected difficulty filter
menu_visible = False  # Tracks hamburger menu state


def load_words_with_spaced_repetition():
    """Initialize or load spaced repetition data for words."""
    global to_learn
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        # Try to load existing spaced repetition data
        saved_data = pandas.read_csv("data/spaced_repetition.csv")
        to_learn = saved_data.to_dict(orient="records")

    except (FileNotFoundError, pandas.errors.EmptyDataError):
        # Create new spaced repetition data from original words
        original_data = pandas.read_csv("data/french_words.csv")
        to_learn = []

        for word in original_data.to_dict(orient="records"):
            word.update({
                'repetitions': 0,  # How many times reviewed
                'interval': 1,  # Days until next review
                'ease_factor': 2.5,  # How "easy" the word is (2.5 default)
                'due_date': today,  # Timing data
                'last_reviewed': today,  # Timing data
            })
            to_learn.append(word)

        save_progress()


def save_progress():
    """Save current progress to CSV."""
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/spaced_repetition.csv", index=False)


def get_due_words():
    """Get words that are due for review today."""
    today = datetime.now().strftime("%Y-%m-%d")
    due_words = [word for word in to_learn if word['due_date'] <= today]

    if current_difficulty_filter:
        due_words = [word for word in due_words if word.get('difficulty', 1)
                     == current_difficulty_filter]

    # Show 5 random words if no words are due
    return due_words if due_words else to_learn[:5]


def set_difficulty_filter(difficulty):
    """Set the difficulty filter for words to review."""
    global current_difficulty_filter
    current_difficulty_filter = difficulty

    close_menu()

    next_card()


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

    # Select difficulty dots
    difficulty = current_card.get('difficulty', 1)
    if difficulty not in [1, 2, 3]:
        difficulty = 1

    canvas.itemconfig(canvas_image, image=card_front_img)
    draw_difficulty_dots(difficulty)

    flip_timer = window.after(3000, func=toggle_card)

    difficulty_text = f"Level: {difficulty}"
    canvas.itemconfig(card_difficulty, text=difficulty_text)


def toggle_card():
    """Toggle between French and English translation."""
    global is_flipped, flip_timer

    if flip_timer:
        window.after_cancel(flip_timer)

    if is_flipped:
        # Show front card
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


def draw_difficulty_dots(difficulty):
    """Draw dots to represent difficulty level."""
    global difficulty_dots

    # Clear existing dots
    for dot in difficulty_dots:
        canvas.delete(dot)
    difficulty_dots = []

    # Draw dots based on difficulty
    dot_size = 8
    start_x = 380
    y_pos = 420

    for i in range(difficulty):
        x_pos = start_x + (i * 20)  # Space dots 20px apart
        dot = canvas.create_oval(x_pos - dot_size, y_pos - dot_size,
                                 x_pos + dot_size, y_pos + dot_size,
                                 fill="#ff6b6b", outline="#d63031", width=2)
        difficulty_dots.append(dot)


def close_menu():
    """Close the hamburger menu if it's open."""
    global menu_visible, menu_frame
    if menu_visible:
        menu_frame.destroy()
        menu_visible = False


def toggle_menu():
    global menu_visible, menu_frame

    if menu_visible:
        close_menu()
    else:
        # Create and show the frame with cyan background
        menu_frame = ctk.CTkFrame(
            window, width=200, height=300, fg_color=MENU_BG)
        menu_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nw")

        def create_menu_button(x, y, text, cmd):
            btn = ctk.CTkButton(menu_frame,
                                text=text,
                                width=180,
                                height=35,
                                fg_color=MENU_BG,
                                hover_color=MENU_HOVER,
                                text_color=MENU_TEXT,
                                command=cmd)
            btn.place(x=10, y=y)

        # Create menu buttons
        create_menu_button(0, 80, 'Level 1', lambda: set_difficulty_filter(1))
        create_menu_button(0, 117, 'Level 2', lambda: set_difficulty_filter(2))
        create_menu_button(0, 154, 'Level 3', lambda: set_difficulty_filter(3))
        create_menu_button(0, 191, 'All Levels',
                           lambda: set_difficulty_filter(None))

        # Close button
        def close_btn():
            menu_frame.destroy()
            global menu_visible
            menu_visible = False

        ctk.CTkButton(menu_frame,
                      text="✕",
                      width=30,
                      height=30,
                      fg_color=MENU_BG,
                      hover_color=MENU_HOVER,
                      text_color=MENU_TEXT,
                      command=close_btn).place(x=5, y=10)

        menu_visible = True


window = ctk.CTk()
window.title("Flashy")
window.geometry("900x700")
window.configure(fg_color=BACKGROUND_COLOR)

# Choose learning mode with dialog
load_words_with_spaced_repetition()

flip_timer = window.after(3000, func=toggle_card)
canvas = Canvas(width=800, height=526)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")

# Store difficulty dot IDs for updating
difficulty_dots = []

canvas_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=(
    "Arial", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="word", font=(
    "Arial", 60, "bold"), fill="black")

card_difficulty = canvas.create_text(
    400, 350, text="", font=("Arial", 20), fill="gray")

# Difficulty dots will be created dynamically
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.place(x=50, y=50)


def on_canvas_click(event):
    close_menu()
    toggle_card()


canvas.bind("<Button-1>", on_canvas_click)

# Create buttons properly
unknown_button = ctk.CTkButton(window, text="❌ Unknown",
                               fg_color="#ff4444", hover_color="#cc3333",
                               width=120, height=40, command=is_unknown)
unknown_button.place(x=300, y=600)

known_button = ctk.CTkButton(window, text="✅ Known",
                             fg_color="#44ff44", hover_color="#33cc33",
                             width=120, height=40, command=is_known)
known_button.place(x=480, y=600)

hamburger_button = ctk.CTkButton(window, text="☰", width=40, height=40,
                                 fg_color=BACKGROUND_COLOR, hover_color=MENU_HOVER,
                                 command=toggle_menu)
hamburger_button.place(x=10, y=10)

# Start the application
try:
    next_card()
    window.mainloop()
except Exception as e:
    print(f"Application error: {e}")
