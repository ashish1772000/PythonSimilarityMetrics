#######################################################
# 
# utility_module.py
# Implementation of the Similarity module
# Author:          Ashish Garg
# Created on:      22-Nov-2019 18:17:53
# 
#######################################################
from os import system, name      # importing system from operating system 
from IPython.display import clear_output
import sys

class sim_func_code:
    EUCLIDEAN = 1
    COSINE = 2 
    PEARSON = 3
    JACCARD = 4
    MANHATTAN = 5

class colors:               #declare ANSI escape sequences constants to make make console output colorful and text 
   PURPLE = '\033[95m'         #ansi code for purple 
   CYN = '\033[96m'       #ansi code for cyan 
   DRKCYN = '\033[36m' #ansi code for dark cyan
   BLUE = '\033[94m'           #ansi code for blue
   GREEN = '\033[92m'            #ansi code for green
   YELLOW = '\033[93m'           #ansi code for yellow
   RED = '\033[91m'            #ansi code for red
   BOLD = '\033[1m'             #ansi code for bold
   UL = '\033[4m'       #ansi code for underline
   END = '\033[0m'         #ansi code for end

class vector_type:
    USERS = 1
    MOVIES = 2

class similiarity_function_selection_mode:
    ENDUSER = 1
    BEST = 2 
    ALL = 3

def clear_console():   
   for i in range(2):
       clear_output(wait=True)

def valid_number(inpvar):   # define valid_number function to check if the passed input is a valid integer or not. It takes string as the input and return boolean.
    try: 
        int(inpvar)         # convert input to integer
        return True         # if converted to integer then send valid integer number as true
    except ValueError:      
        try:
            float(inpvar)   # convert to float 
            return False     # if converted to float than send valid number as true
        except:
            return False    # else send valid number as false

def fetch_input(inptext):   # process user input with validating the input if it's entered correctly or not
    inp = 0                 # declare final processed input
    wanna_exit = False  # declare variable to check if user wants to exit or not
    valid_input = False # declare variable to check if user entered valid input or not    
    while not wanna_exit and not valid_input: # Keep asking user for valid input else allow user to quit
        inp = input(inptext)    # get user input 
        if(inp.isspace()):      # check if user input SPCE+ENTER, if yes than exit
            wanna_exit = True
        else:
            valid_input = valid_number(inp) # else check for validity of the input 
            if not valid_input:
                print(colors.RED+"Enter valid input!"+colors.END)
    return inp   # return the processed input back to user's screen 

def welcome_banner():       # decorator banner appears as the first message to user 
    
    print(colors.PURPLE+" ***** WELCOME TO MOVIE RECOMMENDATION SYSTEM (SELECT OPERATIONS AS CODE) ****")
    print('1. Perform USER SIMILARITY')
    print('2. Perform MOVIE SIMILARITY')
    print('3. Get MOVIE DETAILS')
    print('4. Perform USER SIMILARITY (best fit)')
    print('5. Perform MOVIE SIMILARITY (best fit)')
    print('6. Perform USER SIMILARITY (All functions)')
    print('7. Perform MOVIE SIMILARITY (All functions)')
    print("--> Press SPACE bar with enter key to EXIT")
    print("***********************************************************************"+colors.END)
    

def function_banner():      # decorator banner appears as the similarity function selector help message to user 
    print(colors.PURPLE+"******************  CHOOSE THE SIMILARITY FUNCTION OF YOUR CHOICE ******************************")
    print("Press 1 for EUCLIDEAN")
    print("Press 2 for COSINE")
    print("Press 3 for PEARSON")
    print("Press 4 for JACCARD")
    print("Press 5 for MANHATTAN")
    print("****************************************************************************************************"+colors.END)
######################################################################################################################################
