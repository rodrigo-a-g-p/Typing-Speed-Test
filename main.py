from tkinter import *
import time

colors_dict = {'red': '#e7305b', 'green': '#9bdeac', 'yellow': '#f7f5dd'}
FONT_NAME = "Courier"


# ---------------------------- Game Functionality ------------------------------- #

def process_user_input(event, list_of_words, word_typed, input_start_timer, input_total_number_of_words,
                       word_box, user_input_box, warning_message_box, finished_game_window):
    """
    Processes the user input
    Note: the last four arguments are Tkinter GUI elements
    """
    check_if_word_exists(list_of_words, word_typed, word_box, user_input_box, warning_message_box)
    is_game_over(list_of_words, input_start_timer, input_total_number_of_words, finished_game_window)


def check_if_word_exists(list_of_words, word_typed, word_box, user_input_box, warning_message_box):
    """ Checks is word typed is exists in the word list """
    # wrote this line because when the entry is refreshed for the first time, the cursor goes to the middle of the entry
    # and the word recognizes spaces

    word_typed = word_typed.replace(' ', '')

    if word_typed == '':
        return

    if word_typed in list_of_words:
        list_of_words.remove(word_typed)
        refresh_widgets(list_of_words, word_box, user_input_box, warning_message_box)
        return

    render_warning_message(warning_message_box)


def is_game_over(list_of_words, input_start_timer, input_total_number_of_words, finished_game_window):
    """ Ends the game when the user has finished typing all words """
    if len(list_of_words) == 0:
        speed = end_counting(input_start_timer)
        rate = round(input_total_number_of_words / speed, 2)
        finished_game_window.destroy()
        final_result_window(speed, rate)


def end_counting(input_start_timer):
    """ Stops the timer and returns how long the user took to complete the game (in seconds) """
    end = time.time()
    time_in_seconds = round(end - input_start_timer, 2)
    return time_in_seconds


# ---------------------------- GUI ------------------------------- #

def tkinter_window_template(input_title, input_size_string, input_colour):
    """ Serves as a template to create Tkinter windows """
    window = Tk()
    window.title(input_title)
    window.geometry(input_size_string)
    window.config(bg=input_colour)
    window.eval('tk::PlaceWindow . center')
    return window


def initial_window():
    """ Shows initial window from which the user can start the game """
    window = tkinter_window_template('Typing Speed Test', "450x200", colors_dict['green'])

    start_game_label = Label(window, text="Press to start the game", font=(FONT_NAME, 25),
                             fg=colors_dict['red'], bg=colors_dict['green'])
    start_game_label.place(x=50, y=50)

    start_button = Button(window, text="LET'S GO", width=12, command=lambda: [window.destroy(), game_window()])
    start_button.place(x=170, y=100)

    window.mainloop()


def game_window():
    """ Shows main game window where user can play the game """
    word_list = ["rocks", 'table', 'dry', 'white', 'cry', 'machine', 'friend', 'yes', 'product', 'state', 'mean', 'hot',
                 'mark', 'weight', 'mother', 'song', 'surface', 'give']
    total_number_of_words = len(word_list)

    window = tkinter_window_template('TYPE AS FAST AS YOU CAN', "480x200", colors_dict['green'])

    # START COUNTING
    start_timer = time.time()

    # Display the words
    box_with_words = Text(window, height=4, width=40, padx=10, pady=10, bg=colors_dict['yellow'], font=FONT_NAME,
                          borderwidth=0, highlightthickness=0)
    box_with_words.insert(END, word_list)
    box_with_words.pack()

    # Entry where the user will type
    user_input_entry = Entry(window, borderwidth=0, highlightthickness=0)
    user_input_entry.focus()  # place cursor in user input entry automatically
    user_input_entry.bind("<space>", lambda event: process_user_input(event,  # not used
                                                                      word_list,
                                                                      user_input_entry.get(),  # retrieve the user input
                                                                      start_timer,
                                                                      total_number_of_words,
                                                                      box_with_words,  # GUI element
                                                                      user_input_entry,  # GUI element
                                                                      warning_message_label,  # GUI element
                                                                      window))  # GUI element
    user_input_entry.pack()

    # Restart Button
    restart_button = Button(window, text="Restart", command=lambda: [window.destroy(), game_window()],
                            font=FONT_NAME, borderwidth=0, highlightthickness=0)
    restart_button.pack()

    # Display warning message in case word typed does not exist (starts empty
    warning_message_label = Label(window, text='', bg=colors_dict['green'], fg=colors_dict['red'],
                                  font=(FONT_NAME, 15, 'bold'), borderwidth=0, highlightthickness=0)
    warning_message_label.pack()

    window.mainloop()


def render_warning_message(warning_message_label):
    """ Shows warning message in case typed word is not on the list """
    warning_message_label.config(text='\nWORD TYPED DOES NOT EXIST!')


def refresh_widgets(list_of_words, box_with_words, user_text_entry, warning_message_label):
    """ Deletes all text from the word box and the entry where the user inserts text """
    user_text_entry.delete(0, END)
    box_with_words.delete(1.0, END)
    box_with_words.insert(END, list_of_words)
    warning_message_label.config(text='')


def final_result_window(input_speed, input_rate):
    """ Shows final window after user has completed the game """
    window = tkinter_window_template('Congratulations!', "480x200", colors_dict['green'])

    result_label = Label(window, text=f"\n\nYour Score is: {input_speed} seconds!\nThat's a rate of {input_rate} words per second!\n",
                         bg=colors_dict['green'], fg=colors_dict['red'], font=(FONT_NAME, 15, 'bold'), borderwidth=0,
                         highlightthickness=0)
    result_label.pack()

    play_again_button = Button(window, text="LET'S GO AGAIN", command=lambda: [window.destroy(), game_window()],
                               font=FONT_NAME, borderwidth=0, highlightthickness=0)
    play_again_button.pack()

    window.mainloop()


# ---------------------------- START GAME ------------------------------- #

initial_window()
