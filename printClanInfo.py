############################################################################################
# Only purpose is to print clan information to the terminal for testing on the 
# Bungie API app
############################################################################################

from destinyInfo import *
from pprint import pprint

def printKeys():
    dict_ = {}
    dict_ = getMatchDetailsBanner(5749533723)

    for keys in dict_:
        pprint(keys)

def printMatchData():

    matchNum = 5749533723

    matchDeets = getMatchDetailsBanner(matchNum)

    pprint(matchDeets)

def printMostRecentGame():
    
    lastGames = []
    
    charID = getCharacterNumber(4611686018445706444)
    
    for i in charID:
        lastGames.append(getMostRecentGame(i, 4611686018445706444))

    pprint(lastGames)

def printMemberData():
    
    clanList = []
    
    # Build the clan list by choosing one
    #clanList = buildClanELO()
    clanList = buildClanBanner()

    # Choose one, or both
    #updateMemberDataELO(clanList)
    updateMemberDataBanner(clanList)

    # Print the clan list
    print(*clanList, sep = '\n')

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

     matchList = getMatchDetails(5843948734)

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

    # Print the members' updated info
    printMemberData()

    # Print twelvevoltpro's chars most recent games
    #printMostRecentGame()

    # Print match data
    #printMatchData()

    # Print keys in a dict
    #printKeys()

    return

main()