import math

numCharacters = 24
P1WinPercent = [[-1 for i in range(numCharacters)] for j in range(numCharacters)]
P1BestMove = [[-1 for i in range(numCharacters)] for j in range(numCharacters)]

for totalCharactersLeft in range(2,2*numCharacters+1):
    for P1CharactersLeft in range(max(1,totalCharactersLeft - numCharacters), min(numCharacters,totalCharactersLeft) +1):
        P2CharactersLeft = totalCharactersLeft - P1CharactersLeft
        if P1CharactersLeft == 1:
            P1WinPercent[0][P2CharactersLeft-1] = 1
            P1BestMove[0][P2CharactersLeft-1] = 1
        else:
            choiceWinPercent = [-1]*(P1CharactersLeft-1)
            choiceWinPercent[0] = (1/P1CharactersLeft) + (1 - 1/P1CharactersLeft)*(1-P1WinPercent[P2CharactersLeft-1][P1CharactersLeft - 2])
            for choice in range(2, math.floor(P1CharactersLeft/2)+1):
                choiceWinPercent[choice-1] = (choice/P1CharactersLeft)*(1-P1WinPercent[P2CharactersLeft-1][choice-1]) + (1 - choice/P1CharactersLeft)*(1-P1WinPercent[P2CharactersLeft-1][P1CharactersLeft - choice-1])
            P1WinPercent[P1CharactersLeft-1][P2CharactersLeft-1] = max(choiceWinPercent)
            P1BestMove[P1CharactersLeft-1][P2CharactersLeft-1] = choiceWinPercent.index(P1WinPercent[P1CharactersLeft-1][P2CharactersLeft-1])+1

print(P1WinPercent)
print(P1BestMove)