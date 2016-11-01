############################################################################################
# Only purpose is to print clan information to the terminal for testing on the 
# Bungie API app
############################################################################################

from destinyInfo import getClanData, getCharacterNumber, buildClan, getMatchDetails, defineLastGamePlayed, getMostRecentGame
from pprint import pprint

def printMostRecentGame():
    
    lastGames = []
    
    charID = getCharacterNumber(4611686018433260672)
    
    for ID in charID:
        lastGames.append(getMostRecentGame(ID, 4611686018433260672))

    pprint(lastGames)

def printLastGame():
    
    clanList = []
    lastGame = {}

    # Build the clan list
    clanList = buildClan()

    defineLastGamePlayed(clanList)

def printAllData():
    
    tooBigList = getClanData()

    # Print the entire json object 
    pprint(tooBigList)    

def printUNMI():

    clanList = getClanData()

    # Print the display names and memberIDs for each member for debugging
    x = 0
    for i in clanList:
        print(x, clanList[x]['destinyUserInfo']['displayName'],
                 clanList[x]['destinyUserInfo']['membershipId'])
        x+=1

def printCharacters():
        
    charList = getCharacterNumber(4611686018433260672)

    # Print the list of characters
    print(charList)

def printClanArray():

    clanArray = buildClan()

    print(*clanArray, sep = '\n')

def printMatchPlayers():

     matchList = getMatchDetails(5484545569)

     print(*matchList, sep = '\n')

def main():
    ############################################################################################
    # Comment out which report you do NOT want to print below
    # I should add a menu to select which option, but this is easy enough
    ############################################################################################

    # Print the entire json object
    #printAllData()

    # Print only usernames and ids
    #printUNMI()

    # Print twelvevoltpro's char list
    #printCharacters()

    # Print the array of clan objects
    #printClanArray()

    # Print players in a specific match
    #printMatchPlayers()

    # Print the members' last game
    printLastGame()

    # Print twelvevoltpro's chars most recent games
    #printMostRecentGame()

    return

main()