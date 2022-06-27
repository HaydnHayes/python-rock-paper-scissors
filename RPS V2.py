from asyncore import loop
import random

# Function to generate computer choice
def comp_choice_func():
    global comp_choice
    comp_choice = random.choice(["rock", "paper", "scissors"])
    print(comp_choice)

# Function to generate user choice
def user_choice_func():
    print("Rock, Paper, Scissors?")
    user_choice_check = False
    while user_choice_check != True:
        global user_choice
        user_choice = input()
        user_choice = user_choice.lower()
        if user_choice != "rock" and user_choice !="paper" and user_choice !="scissors":
            print("Please enter Rock, Paper or Scissors")
        else:
            user_choice_check = True

# Function to apply logic to outcomes and assign scores to that
def compare_func(user_choice_x, comp_choice_x):
    # Comp Wins
    if comp_choice_x == "rock" and user_choice_x == "scissors":
        game_condition = "comp"
    elif comp_choice_x == "paper" and user_choice_x == "rock":
        game_condition = "comp"
    elif comp_choice_x == "scissors" and user_choice_x == "paper":
        game_condition = "comp"
    # User Wins
    elif user_choice_x == "rock" and comp_choice_x == "scissors":
        game_condition = "user"
    elif user_choice_x == "paper" and comp_choice_x == "rock":
        game_condition = "user"
    elif user_choice_x == "scissors" and comp_choice_x == "paper":
        game_condition = "user"
    # Draw
    else:
        game_condition = "draw"

    # Assign Scores
    if game_condition == "comp":
        global comp_score
        comp_score = comp_score + 1
    elif game_condition =="user":
        global user_score
        user_score = user_score + 1


# Function for the best of three mode
def best_of_three():
    loop_count = 0
    while loop_count != 3:
        user_choice_func()
        comp_choice_func()
        user_input = user_choice
        comp_input = comp_choice
        compare_func(user_input, comp_input)
        loop_count = loop_count + 1
    print("User:    Comp:")
    print(user_score, "  ", comp_score)

# Function for freeplay mode
def freeplay():
    freeplay_loop = False
    while freeplay_loop != True:
        user_choice_func()
        comp_choice_func()
        user_input = user_choice
        comp_input = comp_choice
        compare_func(user_input, comp_input)
        print("User:    Comp:")
        print(user_score, "  ", comp_score)
        end_loop_check = False
        print("Continue Playing, Yes or No?")
        while end_loop_check != True:
            end_loop = input()
            end_loop = end_loop.lower()
            print(end_loop)
            if end_loop != "yes" and end_loop != "no":
                print("Please Enter Yes or No")
            elif end_loop == "no":
                freeplay_loop = True
                end_loop_check = True
            else:
                end_loop_check = True


# Function for mode choice
def mode_choice_func():
    mode_choice_check = False
    print("Please choose a mode, 'Best of Three' or 'Freeplay'")
    while mode_choice_check != True:
        mode_choice = input()
        mode_choice = mode_choice.lower()
        if mode_choice != "best of three" and mode_choice != "freeplay":
            print("Please enter 'Best of Three' or 'Freeplay")
        elif mode_choice == "best of three":
            best_of_three()
            mode_choice_check = True
        else:
            freeplay()
            mode_choice_check = True
        
# Run the game
game_loop = True
while game_loop == True:
    user_score = 0
    comp_score = 0
    mode_choice_func()
    game_loop_check = False
    while game_loop_check != True:
        print("Exit game, Yes or No?")
        game_loop_choice = input()
        game_loop_choice = game_loop_choice.lower()
        if game_loop_choice != "yes" and  game_loop_choice != "no":
            print("Please enter Yes or No")
        elif game_loop_choice == "yes":
            game_loop_check = True
            game_loop = False
        else:
            game_loop_check = True
        





        

