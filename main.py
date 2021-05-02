from tkinter import *
import pandas as pd
import random
BACKGROUND_COLOR = "#B1DDC6"
# made a clean dictionary for the words
to_learn = {}
# reed a csv with the data
try:
    data = pd.read_csv("/data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    # using the orient records, we can split
    # each word into a dictionary
    # with key values frencha and english
    # {'French': 'partie', 'English': 'part'}
    to_learn = original_data.to_dict(orient="records")
else:
    # using the orient records, we can split
    # each word into a dictionary
    # with key values frencha and english
    # {'French': 'partie', 'English': 'part'}
    to_learn = data.to_dict(orient="records")


# initialize the dictionary how has the card
current_card = {}
# Function to move next card
def next_card():
    # indicate tha the current_card its the global dictionary and no a local
    # and the timer for flip the card
    global current_card, flip_timer
    # cancel the previous timer
    window.after_cancel(flip_timer)
    # selecting a random card to ask
    current_card = random.choice(to_learn)
    # changing the title to french
    canvas.itemconfig(card_title, text="French", fill="black")
    # changing the word to french
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    # changing the canvas to flip the color
    canvas.itemconfig(card_background, image=card_front_img)
    # renew the flip_timer
    flip_timer = window.after(3000, func=flip_card)

# changing the card to show the english word
def flip_card():
    # indicate tha the current_card its the global dictionary and no a local
    global current_card
    # changing the title to English
    canvas.itemconfig(card_title, text="English", fill="white")
    # changing the word to English
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    # changing the canvas to flip the color
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    # indicate tha the current_card its the global dictionary and no a local
    global current_card
    # removing the card that i knowing
    to_learn.remove(current_card)
    # i save the words that i known
    data = pd.DataFrame(to_learn)
    # when we save the words i have to clean the index value
    data.to_csv("data/words_to_learn.csv", index=False)
    # continue leerning the next card
    next_card()


# Creating a new window and configurations
window = Tk()
# Setting the title of the window
window.title("Flashy")
# Setting the pad x and y on 50 each one
# and the background color
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
# for each card when the user stay more than 3 sec
# we have to flip the card and show the english word
flip_timer = window.after(3000, func=flip_card)
# Canvas
# Settings the graphic of the card
# given a specific size
canvas = Canvas(width=800, height=526)
# Creating a image for de canvas element
card_front_img = PhotoImage(file="images/card_front.png")
# Creating a image for de canvas element
card_back_img = PhotoImage(file="images/card_back.png")
# Setting the canvas with the image
card_background = canvas.create_image(400, 263, image=card_front_img)
# creating a text for the canvas element
# this text has to be Ariel of size 40 and italic
# this text it s going to be the title of the card
card_title = canvas.create_text(400, 150,  text="", font=("Ariel", 40, "italic"))
# creating a text for the canvas element
# this text has to be Ariel of size 60 and bold
# this text it s going to be the word of the card
card_word = canvas.create_text(400, 263,  text="", font=("Ariel", 60, "bold"))
# Given a Background color to the canvas
# and high the line around the image
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
# Put the canvas in to the grid
# given the , column span =2 for center the canvas
canvas.grid(row=0, column=0, columnspan=2)

# button
# creating an image for the button
cross_image = PhotoImage(file="images/wrong.png")
# this button is the x on the card
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
# add the button to the grid
unknown_button.grid(row=1, column=0)
# creating the image for the check button
check_image = PhotoImage(file="images/right.png")
# this button is the check mark on the card
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
# add the button to the grid
known_button.grid(row=1, column=1)
# init the first card
next_card()
# establish the mainloop for no stopping
window.mainloop()