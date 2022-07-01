### Blackjack Game
# Game is based on a user("user") vs a computer("comp")


# Import needed librarys
import random
import os
import time
import tkinter as tk
from turtle import fillcolor

# Function setting up the game
# Dictionary containing all 52 cards
def initial_setup():
    global card_pool_dict, original_card_dict
    card_pool_dict = {"Hearts":[], "Clubs":[], "Diamonds":[], "Spades":[]}
    card_numbers = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
    original_card_dict = {"Hearts" : card_numbers, "Clubs" : card_numbers, "Diamonds" : card_numbers, "Spades" : card_numbers}
    
    for i in original_card_dict:
        for h in range(len(original_card_dict[i])):
            card_pool_dict[i].append(original_card_dict[i][h])

# Function to generate a random card and remove it from the remaining card pool,
#  whilst checking that there is a pool to pull from
# Cards are generated and kept in embedded lists in the following format:
# [[[Number],[Suit]],[[Number],[Suit]]]
# Function also checks if card is an Ace and adds one to the value of an aces count, which will be used later 
# To reduce the total value of cards if it goes over 21
def random_card(user_or_comp):
    global card_pool_dict, original_card_dict, user_ace_count, comp_ace_count

    if draw_count > (len(card_pool_dict["Hearts"])  + len(card_pool_dict["Clubs"]) + len(card_pool_dict["Diamonds"]) + len(card_pool_dict["Spades"])):
        initial_setup()
        for i in range(len(user_cards)):
            if user_cards[i][0] in card_pool_dict[(user_cards[i][1])]:
                card_pool_dict[(user_cards[i][1])].remove(user_cards[i][0])
        for i in range(len(comp_cards)):
            if comp_cards[i][0] in card_pool_dict[(comp_cards[i][1])]:
                card_pool_dict[(comp_cards[i][1])].remove(comp_cards[i][0])        

    random_card_loop = True
    while random_card_loop == True:
        rand_suit_store = random.choice(["Hearts", "Clubs", "Diamonds", "Spades"])
        if len(card_pool_dict[rand_suit_store]) != 0:
            rand_num_store = random.choice(card_pool_dict[rand_suit_store])
            rand_card_store = [rand_num_store, rand_suit_store]
            card_pool_dict[rand_suit_store].remove(rand_num_store)
            random_card_loop = False

    user_or_comp.append(rand_card_store)

    if user_or_comp == user_cards and rand_num_store == "A":
        user_ace_count += 1
    elif user_or_comp == comp_cards and rand_num_store == "A":
        comp_ace_count += 1

# Generate the starting hands using random_card()
def starting_hands():
    global user_cards ,  comp_cards, draw_count, comp_ace_count, user_ace_count
    draw_count = 4
    user_cards = []
    comp_cards = []
    user_ace_count = 0
    comp_ace_count = 0

    random_card(user_cards)
    random_card(user_cards)

    random_card(comp_cards)
    random_card(comp_cards)

# Function to draw a card and display cards in hand if it is the user
def hit(hand_hit):
    global draw_count
    draw_count = 1
    random_card(hand_hit)
       
# Function to apply maths to cards in hand and convert str values to int values 
# Gives a max total
# Takes values in format [[number],[suit]] and converts this to [[number],[number]] to give totals
# Checks if final sum is over 21 and takes away 10 for each ace until value is less than or equal to 21
def hand_total(hand_hand_total, which_ace_count):
    global hand_sum
    hand_sum = 0
    temp_hand =[]
    temp_ace_count = which_ace_count

    for i in range(len(hand_hand_total)):
        if hand_hand_total[i][0] == "A":
            temp_hand.append(11)            
        elif hand_hand_total[i][0] == "J" or hand_hand_total[i][0] == "Q" or hand_hand_total[i][0] == "K":
            temp_hand.append(10)  
        else:
            temp_hand.append(hand_hand_total[i][0]) 
            
    for i in range(len(temp_hand)):
            hand_sum += temp_hand[i]
    
    while hand_sum > 21 and temp_ace_count > 0:
        hand_sum -= 10
        temp_ace_count -= 1

    return hand_sum

# Function defining the process that the computer will go through after the user has finished
# their processes, the computer will display the cards in their hand regardless of whether 
# the user has gone bust.
# According to game rules the comp must stand if the total of their cards is greater than or 
# equal to 17 and must draw until this point is reached. 
def comp_controls():
    comp_control_loop = True
    while comp_control_loop == True:
        blackjack_canvas.itemconfig(comp_hand_text, text = display_cards_in_hand(comp_cards))
        if hand_total(comp_cards, comp_ace_count) <= 21:
            blackjack_canvas.itemconfig(comp_total_text, text = f"Max Non-Bust Total:   {hand_total(comp_cards, comp_ace_count)}")
        else:
            blackjack_canvas.itemconfig(comp_total_text, text = f"Total:   {hand_total(comp_cards, comp_ace_count)}\nComputer is bust!")

        if hand_total(comp_cards, comp_ace_count) >= 17 or hand_total(comp_cards, comp_ace_count) >= 17:
            return True
            comp_control_loop = False
        else:
            hit(comp_cards)

# Func to assign scores based on who is closer to 21 and not bust, with the score being [user,comp]
# The inputs will be the variables assigned to hands
# Because all values of difference will be made positive to get the best comparison, hands that are considered bust
# will be set to 21 on the differences variables to make for ease of comparing intergeers as oppoised to int and str
def score_check(user_input, comp_input):
    global scores, winner

    if hand_total(user_input, user_ace_count) > 21:
        user_difference = 21
    else:
        user_difference = 21 - hand_total(user_input, user_ace_count)

    if hand_total(comp_input, comp_ace_count) > 21:
        comp_difference = 21
    else:
        comp_difference = 21 - hand_total(comp_input, comp_ace_count)


    if user_difference > comp_difference:
        scores[1] += 1
        winner = "Computer Wins!"
    elif user_difference < comp_difference:
        scores[0] += 1
        winner = "User Wins!"
    else:
        scores[0] += 0
        scores[1] += 0
        winner = "Its a draw!"

# Function to create a displayable string with cards in hand
def display_cards_in_hand(which_cards):
    display_string = ""    
    for i in range(len(which_cards)):
        display_string += str(f"\n{which_cards[i][0]} of {which_cards[i][1]}")
    return (f"Cards in hand:{display_string}")

# Setting up main GUI
def main():
    global root, blackjack_canvas
    root = tk.Tk()
    root.title("Blackjack")

    blackjack_canvas = tk.Canvas( width = 560, height = 702.5, bg = "black")
    blackjack_canvas.create_rectangle(2.5,2.5,560,702.5, outline = "white",  width = 5)
    title_text = blackjack_canvas.create_text(10, 5, text = "Blackjack", fill = "white", font = "Helvetica 50 bold", anchor = "nw")
   
    
    # Function for button that sets static elements
    def start_button_func():
        global user_hand_text, user_total_text, comp_hand_text, comp_total_text, user_score_text, comp_score_text, scores, win_display_text
        create_hit_button()
        create_stand_button()
        create_restart_button()

        initial_setup()
        starting_hands()
        scores = [0,0]

        user_hand_title = blackjack_canvas.create_text(10, 100, text = "User", fill = "white", font = "Helvetica 15 bold underline", anchor = "w")
        comp_hand_title = blackjack_canvas.create_text(270, 100, text = "Computer", fill = "white", font = "Helvetica 15 bold underline", anchor = "w")

        blackjack_canvas.create_rectangle(2.5,85,260,640, outline = "white",  width = 5)
        user_hand_text = blackjack_canvas.create_text(10, 120, text = display_cards_in_hand(user_cards), fill = "white", font = "Helvetica 15 bold", anchor = "nw")
        user_total_text = blackjack_canvas.create_text(10, 450, text = f"Max Non-Bust Total:    {hand_total(user_cards, user_ace_count)}", fill = "white", font = "Helvetica 15 bold", anchor = "nw")
        user_score_text = blackjack_canvas.create_text(10, 500, text = f"Score:    {scores[0]}", fill = "white", font = "Helvetica 15 bold", anchor = "nw")

        blackjack_canvas.create_rectangle(260,85,560,640, outline = "white",  width = 5)
        comp_hand_text = blackjack_canvas.create_text(270, 120, text = "Cards in Hand:\nHidden\nHidden", fill = "white", font = "Helvetica 15 bold", anchor = "nw")
        comp_total_text = blackjack_canvas.create_text(270, 450, text = f"Max Non-Bust Total:    Hidden", fill = "white", font = "Helvetica 15 bold", anchor = "nw")
        comp_score_text = blackjack_canvas.create_text(270, 500, text = f"Score:    {scores[0]}", fill = "white", font = "Helvetica 15 bold", anchor = "nw")

        win_display_text = blackjack_canvas.create_text(280, 700, text = "", fill = "white", font = "Helvetica 40 bold", anchor = "s")

        start_button.destroy()

    start_button = tk.Button(blackjack_canvas, text = "Start",  bg = "white", fg = "black", borderwidth= 0, font = "Helvetica 40 bold")
    start_button["command"] = lambda : start_button_func()
    start_button.place(x = 10, y = 351, anchor = "w")    

    # Function that instructs the hit button to hit and update cards in hand
    def hit_button_func():
        hit(user_cards)
        blackjack_canvas.itemconfig(user_hand_text, text = display_cards_in_hand(user_cards))
        if hand_total(user_cards, user_ace_count) <= 21:
            blackjack_canvas.itemconfig(user_total_text, text = f"Max Non-Bust Total:    {hand_total(user_cards, user_ace_count)}")
        else:
            blackjack_canvas.itemconfig(user_total_text, text = f"Total:    {hand_total(user_cards, user_ace_count)}\nYou are bust!")
            stand_button_func()
            
    def create_hit_button():
        global hit_button
        hit_button = tk.Button(blackjack_canvas, text = "Hit",  bg = "white", fg = "black", borderwidth= 0, font = "Helvetica 25 bold")
        hit_button["command"] = lambda : hit_button_func()
        hit_button.place(x = 80 , y = 600, anchor= "e")

    # Function that controls what the stand button does
    def stand_button_func():
        hit_button.destroy()
        stand_button.destroy()

        comp_controls()
        score_check(user_cards, comp_cards)
        blackjack_canvas.itemconfig(user_score_text, text = f"Score:    {scores[0]}")
        blackjack_canvas.itemconfig(comp_score_text, text = f"Score:    {scores[1]}")
        blackjack_canvas.itemconfig(win_display_text, text = winner)

        create_again_button()

    
    def create_stand_button():
        global stand_button
        stand_button = tk.Button(blackjack_canvas, text = "Stand",  bg = "white", fg = "black", borderwidth= 0, font = "Helvetica 25 bold")
        stand_button["command"] = lambda : stand_button_func()
        stand_button.place(x = 80, y = 600, anchor = "w")

    # Function that controls the again button does
    def again_button_func():
        again_button.destroy()
        starting_hands()

        blackjack_canvas.itemconfig(user_hand_text, text = display_cards_in_hand(user_cards))
        blackjack_canvas.itemconfig(user_total_text, text = f"Max Non-Bust Total:    {hand_total(user_cards, user_ace_count)}")

        blackjack_canvas.itemconfig(comp_hand_text, text = "Cards in Hand:\nHidden\nHidden")
        blackjack_canvas.itemconfig(comp_total_text, text = f"Max Non-Bust Total:   Hidden")

        blackjack_canvas.itemconfig(win_display_text, text = "")

        create_hit_button()
        create_stand_button()

    def create_again_button():
        global again_button
        again_button = tk.Button(blackjack_canvas, text = "Again",  bg = "white", fg = "black", borderwidth= 0, font = "Helvetica 25 bold")
        again_button["command"] = lambda : again_button_func()
        again_button.place(x = 80, y = 600, anchor = "c")

    # Function that controls what the reset button does and resets the "board"
    def restart_button_func():
        initial_setup()
        starting_hands()
        scores = [0,0]

        blackjack_canvas.itemconfig(user_hand_text, text = display_cards_in_hand(user_cards))
        blackjack_canvas.itemconfig(user_total_text, text = f"Max Non-Bust Total:    {hand_total(user_cards, user_ace_count)}")

        blackjack_canvas.itemconfig(comp_hand_text, text = "Cards in Hand:\nHidden\nHidden")
        blackjack_canvas.itemconfig(comp_total_text, text = f"Max Non-Bust Total:   Hidden")

        blackjack_canvas.itemconfig(user_score_text, text = f"Score:    {scores[0]}")
        blackjack_canvas.itemconfig(comp_score_text, text = f"Score:    {scores[1]}")

    def create_restart_button():
        global restart_button
        restart_button = tk.Button(blackjack_canvas, text = "Restart",  bg = "white", fg = "black", borderwidth= 0, font = "Helvetica 25 bold")
        restart_button["command"] = lambda : restart_button_func()
        restart_button.place(x = 270, y = 600, anchor = "w")

    
    blackjack_canvas.pack()
    root.mainloop()

main()
