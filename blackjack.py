### Blackjack Game
# Game is based on a user("user") vs a computer("comp")


# Import needed librarys
import random

# Function setting up the game
# Dictionary containing all 52 cards
def initial_setup():
    global card_pool_dict
    card_pool_dict = {"hearts":[], "clubs":[], "diamonds":[], "spades":[]}
    global original_card_dict
    card_numbers = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
    original_card_dict = {"hearts" : card_numbers, "clubs" : card_numbers, "diamonds" : card_numbers, "spades" : card_numbers}
    
    for i in original_card_dict:
        for h in range(len(original_card_dict[i])):
            card_pool_dict[i].append(original_card_dict[i][h])

# Function to generate a random card and remove it from the remaining card pool,
#  whilst checking that there is a pool to pull from
# Cards are generated and kept in embedded lists in the following format:
# [[[Number],[Suit]],[[Number],[Suit]]]
def random_card():
    global card_pool_dict
    global original_card_dict
    
    if draw_count > (len(card_pool_dict["hearts"])  + len(card_pool_dict["clubs"]) + len(card_pool_dict["diamonds"]) + len(card_pool_dict["spades"])):
        initial_setup()
        for i in range(len(user_cards)):
            if user_cards[i][0] in card_pool_dict[(user_cards[i][1])]:
                card_pool_dict[(user_cards[i][1])].remove(user_cards[i][0])
        for i in range(len(comp_cards)):
            if comp_cards[i][0] in card_pool_dict[(comp_cards[i][1])]:
                card_pool_dict[(comp_cards[i][1])].remove(comp_cards[i][0])        

    random_card_loop = True
    while random_card_loop == True:
        rand_suit_store = random.choice(["hearts", "clubs", "diamonds", "spades"])
        if len(card_pool_dict[rand_suit_store]) != 0:
            rand_num_store = random.choice(card_pool_dict[rand_suit_store])
            rand_card_store = [rand_num_store, rand_suit_store]
            card_pool_dict[rand_suit_store].remove(rand_num_store)
            random_card_loop = False
    return rand_card_store

# Generate the starting hands using random_card()
def starting_hands():
    global user_cards ,  comp_cards, draw_count
    draw_count = 4
    user_cards = [random_card(), random_card()]
    comp_cards = [random_card(), random_card()]

    print(f"\n\nYou starting hand is:\n{user_cards[0][0]} of {user_cards[0][1]} \n{user_cards[1][0]} of {user_cards[1][1]}")
    hand_total(user_cards)
    
    if hand_sum[0] != hand_sum[1]:
        print(f"\nTotals:    {hand_sum[0]} or {hand_sum[1]}")
    else:
        print(f"\nTotal:    {hand_sum[0]}")

    



# Function to draw a card and display cards in hand if it is the user
def hit(hand_hit):
    global draw_count
    draw_count = 1
    hand_hit.append(random_card())
    
    if hand_hit == user_cards:
        print ("\n\nCards in hand:")
        for i in range(len(hand_hit)):
            print (user_cards[i][0], " of ", user_cards[i][1])
        hand_total(hand_hit)
        if hand_sum[0] != hand_sum[1]:
            print(f"\nTotals:    {hand_sum[0]} or {hand_sum[1]}")
        else:
            print(f"\nTotal:    {hand_sum[0]}")
        

    
# Function to apply maths to cards in hand and convert str values to int values whilst keeping a list of 
# two values to accound for aces having two values
# Takes values in format [[number],[suit]] and converts this to [[number],[number]] to give totals
def hand_total(hand_hand_total):
    global hand_sum
    hand_sum = [0,0]
    temp_hand =[]

    for i in range(len(hand_hand_total)):
        if hand_hand_total[i][0] == "A":
            temp_hand.append([1,11])            
        elif hand_hand_total[i][0] == "J" or hand_hand_total[i][0] == "Q" or hand_hand_total[i][0] == "K":
            temp_hand.append([10,10])  
        else:
            temp_hand.append([hand_hand_total[i][0],hand_hand_total[i][0]]) 
            

    for i in range(len(temp_hand)):
        for h in range(len(hand_sum)):
            hand_sum[h] += temp_hand[i][h]

    return hand_sum

# Function to check if the cards in hand are bust
# to be used in conjunction with hand_total so that input is given in format [x,y]
def bust_check(bust_check_values):
    if bust_check_values[0] > 21 and bust_check_values[1] > 21:
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
        if bust_check(hand_total(user_cards)) == True:
            print("\nStarting hand is bust!")
            user_control_loop = False
        
        else:
            print(bust_chance_calc(user_cards))
            user_command = input("\n\nHit, Stand?")
            if user_command.lower() == "hit":
                hit(user_cards)
                if bust_check(hand_total(user_cards)) == True:
                    print("\nYou are bust!")
                    user_control_loop = False
                else:
                    user_control_loop = True
            
            elif user_command.lower() == "stand":
                user_control_loop = False
                return True
            
            else:
                print("\nPlease choose Hit, Stand!")

# Function defining the process that the computer will go through after the user has finished
# their processes, the computer will display the cards in their hand regardless of whether 
# the user has gone bust
def comp_controls():
        pass

# Function used to calculte the possibility of going bust based on the card left within the
# card pool
# Bust chance will be stored in variable bust_chance which is laid out as [x,y,z],
# where x is the chance of getting 21 exact, y is chance of going under and z is chance of 
# going over
def bust_chance_calc(hand_bust):
    global card_pool_dict
    bust_chance = [0,0,0]
    bust_chance_disp = []
    bust_chance_temp_pool = {"hearts":[], "clubs":[], "diamonds":[], "spades":[]}

    for i in card_pool_dict:
        for h in range(len(card_pool_dict[i])):
            if card_pool_dict[i][h] == "A":
                bust_chance_temp_pool[i].append([1,11])
            elif card_pool_dict[i][h] == "J" or card_pool_dict[i][h] == "Q" or card_pool_dict[i][h] == "K":
                bust_chance_temp_pool[i].append([10,10])
            else:
                bust_chance_temp_pool[i].append([card_pool_dict[i][h], card_pool_dict[i][h]])

    for i in bust_chance_temp_pool:
        for h in range(len(bust_chance_temp_pool[i])):
            for g in range(len(bust_chance_temp_pool[i][h])):
                for f in range(len(hand_total(hand_bust))):
                    if bust_chance_temp_pool[i][h][g] + hand_total(hand_bust)[f] == 21:
                        bust_chance[0] += 1
                    elif bust_chance_temp_pool[i][h][g] + hand_total(hand_bust)[f] < 21:
                        bust_chance[1] += 1
                    else:
                        bust_chance[2] += 1

    for i in range(len(bust_chance)):
        bust_chance_disp.append(bust_chance[i] / sum(bust_chance))
    return bust_chance_disp

    



# Main Game Loop
prog_loop = True
while prog_loop == True:
    initial_setup()
    game_loop = True
    while game_loop == True:
        game_loop_check = input("\n\nPlay Blackjack, yes or no?\n")
        if game_loop_check.lower() == "yes":
            if user_controls() == True:
                print("placeholder")
        elif game_loop_check.lower() == "no":
            game_loop = False
            prog_loop = False
        else:
            print("\nPlease enter yes or no")

    







    

