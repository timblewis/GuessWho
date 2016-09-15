# This Program uses dynamic programming to compute the win percentage and best moves possible for the Guess Who game

# Gameplay:
# In Guess Who two players have a set of characters (here numbered 0 to n-1)
# Each player picks one of the characters and the objective is to guess which character the other player picked
# The players take turns asking the other player yes/no questions until one player exactly guesses the other player's choosen character

# Assumptions:
# If a player knows which character the opponent picked but has not guessed "is your character x?" then the player does not win (specifically in the case where a player has two characters left and guesses wrong he/she does not immediately win)
# Each player picks their character completely at random
# The players can divide the characters into any possible grouping with a single question (example: Is your character 1,2,4-6, or 8?)
# This means only relevant decision is the number of characters to guess (Is your character one of these 6 characters?)
# Also we only need to consider guesses with number of characters <= floor(n/2) (The guess is your character one of these 6 is the same as is your character one of these n-6)


# Note: that it is not necessarily the best strategy to always do a binary search
# If a player is behind it may be in his/her best interest to make "risky" guesses

import math
import tkinter

numCharacters = 24
# P1WinPercent[n-1][m-1] is P1's win percentage under optimal play from both players
# where P1 has n characters left and P2 has m characters left
P1WinPercent = [[-1 for i in range(numCharacters)] for j in range(numCharacters)]
# P1BestMove[n-1][m-1] is the number of characters for P1 to guess to achieve maximal win percentage under optimal play from both players
# where P1 has n characters left and P2 has m characters left
P1BestMove = [[-1 for i in range(numCharacters)] for j in range(numCharacters)]

# Dynamic programming begins here
# Once every win percentage for n total characters split among player 1 and 2 we can easily compute the win percentage for n+1 total characters split among player 1 and 2
# totalCharactersLeft represents the total number of players between player 1 and 2
for totalCharactersLeft in range(2,2*numCharacters+1):
    # for each of the possible number of characters for player 1
    for P1CharactersLeft in range(max(1,totalCharactersLeft - numCharacters), min(numCharacters,totalCharactersLeft) +1):
        # number of characters for player 2 is simply the total number of characters minus the characters left for player 1
        P2CharactersLeft = totalCharactersLeft - P1CharactersLeft

        # if player 1 has 1 character left he wins immediately
        if P1CharactersLeft == 1:
            P1WinPercent[0][P2CharactersLeft-1] = 1
            P1BestMove[0][P2CharactersLeft-1] = 1
        else:
            # find the win percentage for all the possible choices for player 1
            # choiceWinPercent[i-1] is the win percentage for P1 if he/she guesses i characters the first turn
            choiceWinPercent = [-1]*(P1CharactersLeft-1)
            # win percentage if the player guesses 1 character
            # if the player correctly guesses (prob 1/P1CharactersLeft) he/she immediately wins
            # otherwise (prob 1-1/P1CharactersLeft) his/her win percentage is 1-P1WinPercent[P2CharactersLeft-1][P1CharactersLeft - 2]
            # this is because it is now like P1 is now P2 with one less character than before and P2 is now P1
            choiceWinPercent[0] = (1/P1CharactersLeft) + (1 - 1/P1CharactersLeft)*(1-P1WinPercent[P2CharactersLeft-1][P1CharactersLeft - 2])
            # find the win percentage for all other possible guesses for player 1
            for choice in range(2, math.floor(P1CharactersLeft/2)+1):
                # probability character is in choice * win percentage in that case + probability character is not in choice * win percentage in that case
                # in either case the win percentage is the win percentage for P2 with P1 now as P2 with only narrowed down characters and P2 now as P1
                choiceWinPercent[choice-1] = (choice/P1CharactersLeft)*(1-P1WinPercent[P2CharactersLeft-1][choice-1]) + (1 - choice/P1CharactersLeft)*(1-P1WinPercent[P2CharactersLeft-1][P1CharactersLeft - choice-1])
            # P1's win percentage is the maximum of the win percentages of all his/her possible choices
            P1WinPercent[P1CharactersLeft-1][P2CharactersLeft-1] = max(choiceWinPercent)
            # the move that achieves this win percentage is P1's best move
            P1BestMove[P1CharactersLeft-1][P2CharactersLeft-1] = choiceWinPercent.index(P1WinPercent[P1CharactersLeft-1][P2CharactersLeft-1])+1

#print win percentages and best moves
print(P1WinPercent)
print(P1BestMove)

squareWidth = 20
boundaryWidth = 20
display = tkinter.Tk()
screenWidth = 2*boundaryWidth + numCharacters*squareWidth
display.geometry(str(screenWidth) + "x" + str(screenWidth))

c = tkinter.Canvas(display, height=squareWidth*numCharacters, width=squareWidth*numCharacters)
c.pack()

for i in range(numCharacters):
    for j in range(numCharacters):
        x = i*squareWidth
        y = (numCharacters - j - 1)*squareWidth
        colorValue = int(255*(1-P1WinPercent[i][j]))
        squareColor = hex((colorValue<<16) | (colorValue<<8) | colorValue)
        squareColor = "#" + squareColor[2:].zfill(6)
        c.create_rectangle(x,y,x+squareWidth,y+squareWidth,fill=squareColor, outline='')

display.mainloop()