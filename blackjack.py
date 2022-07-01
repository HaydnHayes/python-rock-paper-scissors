### Blackjack Game
# Game is based on a user("user") vs a computer("comp")


# Import needed librarys
import random
import os
import time
import tkinter as tk

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


    #print(f"\n\nYou starting hand is:\n{user_cards[0][0]} of {user_cards[0][1]} \n{user_cards[1][0]} of {user_cards[1][1]}")
    #print(f"\nMax non-bust total:    {hand_total(user_cards, user_ace_count)}")

# Function to draw a card and display cards in hand if it is the user
def hit(hand_hit):
    global draw_count
    draw_count = 1
    random_card(hand_hit)
    
    #if hand_hit == user_cards:
    #    print ("\n\nCards in hand:")
    #    for i in range(len(hand_hit)):
    #        print (user_cards[i][0], " of ", user_cards[i][1])
    #    print(f"\nMax non-bust total:    {hand_total(hand_hit, user_ace_count)}")
        
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



# Function to check if the cards in hand are bust
# to be used in conjunction with hand_total so that input is given in format x
def bust_check(bust_check_values):

    if bust_check_values > 21 and bust_check_values > 21:
        return True
    else:
        return False

# Function for taking user commands during the part of the game where the player is 
# actively playing
# Also checks before playing that the users starting hand isnt bust.
# Has 3 possible outcomes:
# Hit - adds another card to hand and checks if bust
# Stand - finishes drawing and moves to computers moves
# Other possible inputs - return an error telling them to chose from one of the above
def user_controls():
    starting_hands()
    user_control_loop = True
    
    while user_control_loop == True:
        if bust_check(hand_total(user_cards, user_ace_count)) == True:
            print("\nStarting hand is bust!")
            user_control_loop = False
            return True
        
        else:
            user_command = input("\n\nHit, Stand?\n")
            if user_command.lower() == "hit":
                hit(user_cards)
                if bust_check(hand_total(user_cards,user_ace_count)) == True:
                    print("\nYou are bust!")
                    user_control_loop = False
                    return True
                else:
                    user_control_loop = True
            
            elif user_command.lower() == "stand":
                user_control_loop = False
                return True
            
            else:
                print("\nPlease choose Hit or Stand!")

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
            blackjack_canvas.itemconfig(comp_total_text, text = f"Total:   {hand_total(comp_cards, comp_ace_count)}\n Computer is bust!")
        #print(f"\n\nComputers cards are:")
        #for i in range(len(comp_cards)):
        #    print (comp_cards[i][0], " of ", comp_cards[i][1])
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
        #print("\nComputer wins!")
    elif user_difference < comp_difference:
        scores[0] += 1
        winner = "User Wins!"
        #print("\nYou win!")
    else:
        scores[0] += 0
        scores[1] += 0
        winner = "Its a draw!"
        #print("\nIts a draw!")

    #print (f"User Score:    {scores[0]}")
    #print (f"Computer Score:    {scores[1]}")

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

    blackjack_canvas = tk.Canvas( width = 1000, height = 750, bg = "black")
    title_text = blackjack_canvas.create_text(100, 50, text = "Blackjack", fill = "white", font = "Helvetica 25 bold", anchor = "w")
    
    # Function for button that sets static elements
    def start_button_func():
        global user_hand_text, user_total_text, comp_hand_text, comp_total_text, user_score_text, comp_score_text, scores, win_display_text
        create_hit_button()
        create_stand_button()
        create_restart_button()

        initial_setup()
        starting_hands()
        scores = [0,0]

        user_hand_title = blackjack_canvas.create_text(100, 100, text = "User", fill = "white", font = "Helvetica 15 bold", anchor = "w")
        comp_hand_title = blackjack_canvas.create_text(600, 100, text = "Computer", fill = "white", font = "Helvetica 15 bold", anchor = "w")

        user_hand_text = blackjack_canvas.create_text(100, 120, text = display_cards_in_hand(user_cards), fill = "white", font = "Helvetica 15 bold", anchor = "nw")
        user_total_text = blackjack_canvas.create_text(100, 450, text = f"Max Non-Bust Total:    {hand_total(user_cards, user_ace_count)}", fill = "white", font = "Helvetica 15 bold", anchor = "nw")
        user_score_text = blackjack_canvas.create_text(100, 500, text = f"Score:    {scores[0]}", fill = "white", font = "Helvetica 15 bold", anchor = "nw")


        comp_hand_text = blackjack_canvas.create_text(600, 120, text = "Cards in Hand:\nHidden\nHidden", fill = "white", font = "Helvetica 15 bold", anchor = "nw")
        comp_total_text = blackjack_canvas.create_text(600, 450, text = f"Max Non-Bust Total:    Hidden", fill = "white", font = "Helvetica 15 bold", anchor = "nw")
        comp_score_text = blackjack_canvas.create_text(600, 500, text = f"Score:    {scores[0]}", fill = "white", font = "Helvetica 15 bold", anchor = "nw")

        win_display_text = blackjack_canvas.create_text(500, 600, text = "", fill = "white", font = "Helvetica 25 bold", anchor = "n")

        start_button.destroy()

    start_button = tk.Button(root, text = "Start")
    start_button["command"] = lambda : start_button_func()
    start_button.pack()    

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
        hit_button = tk.Button(root, text = "Hit")
        hit_button["command"] = lambda : hit_button_func()
        hit_button.pack()

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
        stand_button = tk.Button(root, text = "Stand")
        stand_button["command"] = lambda : stand_button_func()
        stand_button.pack()

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
        again_button = tk.Button(root, text = "Again")
        again_button["command"] = lambda : again_button_func()
        again_button.pack()

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
        restart_button = tk.Button(root, text = "Restart")
        restart_button["command"] = lambda : restart_button_func()
        restart_button.pack()

    
    blackjack_canvas.pack()
    root.mainloop()

main()


# Main Game Loop
#prog_loop = True
#while prog_loop == True:
#    initial_setup()
#    scores = [0,0]
#    game_loop = True
#    while game_loop == True:
#        time.sleep(3)
#        os.system("cls")
#        game_loop_check = input("\n\nPlay Blackjack, yes or no?\n")
#        if game_loop_check.lower() == "yes":
#            if user_controls() == True:
#                if comp_controls() == True:
#                    score_check(user_cards, comp_cards)
#        elif game_loop_check.lower() == "no":
#            game_loop = False
#            prog_loop = False
#        else:
#            print("\nPlease enter yes or no")

