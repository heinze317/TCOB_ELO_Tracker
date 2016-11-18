﻿############################################################################################
# Gets the data for the clan from the Bungie API
############################################################################################

import requests, copy, json, math
from DBHandler import *


# Dictionaries
HEADERS = {"X-API-Key":'1fdb95e58c5e4b91b4d628a1a405d9e5'}

CLASSES = {
    2271682572: 'Warlock',
    671679327: 'Hunter',
    3655393761: 'Titan'
    }

MODES = {
    "Story" : 2,
    "Raid" : 4,
    "AllPVP" : 5,
    "3v3" : 9,
    "Control" : 10,
    "Trials" : 14,
    "Nightfall" : 16,
    "Heroic" : 17,
    "Iron Banner" : 19,
    "Racing" : 29,
    "Supremecy" : 31,
    "Private" : 32
    }

class Member(object):
    """
    A class outline for a member of the clan
    
    Attributes:
    displayName: the user's PSN name
    memberID: the user's Bungie member ID
    memberChars: the user's character IDs
    numClanGames: the number of clan only games played
    clanKDR: the character's kill/death ratio for clan games
    clanELO: the character's ELO for clan games
    lastGamePlayed: the last clan only gameID played
    """

    # Functions
    def __init__(self, displayName, memberID, memberChars):
        self.displayName = displayName
        self.memberID = memberID
        self.memberChars = memberChars
       

    def __str__(self):
        return('Username: '+self.displayName+'\nMemberID: '+self.memberID+'\nCharacters: '
               +str(self.memberChars)+'\n')
    
    def __repr__(self):
        return str(self)

def makeRequest(url):
    ############################################################################################
    # Makes requests to the Bungie API when fed a url as a parameter
    ############################################################################################

    # Make a request to pull clan info
    info = requests.get(url, headers = HEADERS).json()

    return info

def getClassHash(memberId, charId):
    ############################################################################################
    # Gets each member's character class using their member IDs and character ID
    ############################################################################################

    # Define the url
    url = ("https://www.bungie.net/Platform/Destiny/2/Account/"+ str(memberId) + "/Character/"+ 
           str(charId)+ "/?definitions=False")
    
    request = makeRequest(url)
    charHash = (request['Response']['data']['characterBase']['classHash'])
    
    return CLASSES.get(charHash) 

def getCharacterNumber(idNum):
    ############################################################################################
    # Gets each member's character IDs using their member IDs
    ############################################################################################

    charNum = []

    # Use memberID to gain characterID's for each member
    request = makeRequest("https://www.bungie.net/Platform/Destiny/2/Account/" + str(idNum) + "/Summary/?definitions=False")
    charInfo = (request['Response']['data']['characters'])
    
    x = 0
    
    for i in charInfo:
        charNum.append(charInfo[x]['characterBase']['characterId'])
        x += 1
       
    return charNum

def getClanData():
    ############################################################################################
    # Gets entirely too much info on each clan member, and doesn't get some info we do need
    # Might contain some information we can use for future features, though
    ############################################################################################
           
    # Make inital request, get the first page of data
    page = 1            
    request = makeRequest("https://www.bungie.net/Platform/Group/1552163/ClanMembers/?currentPage="
            + str(page) + "&memberType=-1&platformType=2&sort=0")
    clanData = (request['Response']['results'])
    data = (request['Response']['hasMore'])

    # Build list past the first page
    while data:
        page += 1
        request = makeRequest("https://www.bungie.net/Platform/Group/1552163/ClanMembers/?currentPage="
            + str(page) + "&memberType=-1&platformType=2&sort=0")
        clanData.extend(request['Response']['results'])
        data = (request['Response']['hasMore'])                              
    
    return clanData

def buildClanELO():
    ############################################################################################
    # Builds the clan lists, then builds a list of Member objects containing all the information
    # We need to post and perform funtions on
    ############################################################################################

    clanArray = []
    userNames = []
    destinyIDs = []
    clanChars = []
    characterNums = []
    

    # Get mass amounts of information
    clanInfo = getClanData()    

    # Filter to only user name and Destiny ID
    x = 0

    for i in clanInfo:
        userNames.append(clanInfo[x]['destinyUserInfo']['displayName'])
        destinyIDs.append(clanInfo[x]['destinyUserInfo']['membershipId'])
        x += 1
    
    # Use the IDs to get character numbers
    x = 0

    for x in range(len(userNames)):
        characterNums.append(getCharacterNumber(destinyIDs[x]))
        x += 1
       
    # Build each character's dictionary of info
    for lst in characterNums:
        charInfo = []
        for char in lst:
            charDict = {'charNum' : char,
                        'class' : 'null',
                        'games' : 0,
                        'wins' : 0,
                        'losses' : 0,
                        'kills' : 0,
                        'deaths' : 0,
                        'KDR' : 0.0,
                        'ELO' : 0,
                        'lastGame' : 0}
            charInfo.append(charDict)
        clanChars.append(charInfo)    
   
    # Use the current info to build the clan class objects
    x = 0
   
    for x in range(len(userNames)):
        memberInstance = Member(userNames[x], destinyIDs[x], clanChars[x])
        clanArray.append(memberInstance)
        x += 1
    
    return clanArray

def buildClanBanner():
    ############################################################################################
    # Builds the clan lists, then builds a list of Member objects containing all the information
    # We need to post and perform funtions on for Iron Banner Tracking
    ############################################################################################

    clanArray = []
    userNames = []
    destinyIDs = []
    clanChars = []
    characterNums = []
    

    # Get mass amounts of information
    clanInfo = getClanData()    

    # Filter to only user name and Destiny ID
    x = 0

    for i in clanInfo:
        userNames.append(clanInfo[x]['destinyUserInfo']['displayName'])
        destinyIDs.append(clanInfo[x]['destinyUserInfo']['membershipId'])
        x += 1
    
    # Use the IDs to get character numbers
    x = 0

    for x in range(len(userNames)):
        characterNums.append(getCharacterNumber(destinyIDs[x]))
        x += 1
       
    # Build each character's dictionary of info
    for lst in characterNums:
        charInfo = []
        for char in lst:
            charDict = {'charNum' : char,
                        'class' : 'null',
                        'games' : 0,
                        'wins' : 0,
                        'losses' : 0,
                        'kills' : 0,
                        'deaths' : 0,
                        'KDR' : 0.0,
                        'assists' : 0,
                        'orbs' : 0,
                        'spree' : 0,
                        'objectives' : 0,
                        'precisionKills' : 0,
                        'lastGame' : 0}
            charInfo.append(charDict)
        clanChars.append(charInfo)     
   
    # Use the current info to build the clan class objects
    x = 0
   
    for x in range(len(userNames)):
        memberInstance = Member(userNames[x], destinyIDs[x], clanChars[x])
        clanArray.append(memberInstance)
        x += 1
    
    return clanArray

def isClanOnlyGame(matchList, memberList):
    ############################################################################################
    # Compares the list of players in a game with the most current clan instance, 
    # If only clan members are listed, returns true. Used for the ELO tracker only
    ############################################################################################

   return (set(matchList).issubset(memberList))

def getMatchPlayers(matchID):
    ############################################################################################
    # Gets the details of a match, returns only the players in that game
    ############################################################################################
    matchPlayers = []
    
    # Define the url
    url = ("https://www.bungie.net/Platform/Destiny/Stats/PostGameCarnageReport/"+ str(matchID) +"/?definitions=False") 

    request = makeRequest(url)
    matchData = (request['Response']['data']['entries'])

    # Filter down to just the membership IDs
    x = 0
    for i in matchData:
        matchPlayers.append(matchData[x]['player']['destinyUserInfo']['membershipId'])
        x += 1

    return matchPlayers

def getMostRecentGame(memID, charID, gameType):
    ############################################################################################
    # Gets the most recent game for each member of the clan, one character at a time
    ############################################################################################
    
    mode = MODES.get(gameType)

    # Define url
    url = ("https://www.bungie.net/Platform/Destiny/Stats/ActivityHistory/2/"+ str(memID)+ "/"
           + str(charID) +"/?count=1&definitions=False&mode="+str(mode)+"&page=1")
    request = makeRequest(url)
        
    try:
        recentGame = request['Response']['data']['activities']
        recentId = (recentGame[0]['activityDetails']['instanceId'])
    except:
        recentId = 0       
   
    return recentId

def updateMemberDataELO(clanList):
    ############################################################################################
    # Finds the last clan only game played for each member of the clan.
    # Returns an updated instance of each Member containing the last match ID
    ############################################################################################ 
    
    # Make a list of members
    memberList = []
    for i in clanList:
        memberList.append(i.memberID)
    
    # Find each character's most recent private game
    for i in clanList:
        for char in i.memberChars:
            lastMatch = getMostRecentGame(i.memberID, char['charNum'], "Private")
            charCLass = getClassHash(i.memberID, char['charNum'])
            char['class'] = charCLass

            # Find out if the most recent game is clan-only
            if lastMatch != 0:
                matchPlayers = getMatchPlayers(lastMatch)
                clanOnly = isClanOnlyGame(matchPlayers, memberList)

                # If it is clan-only, compare against the previous clan-only game
                if clanOnly:
                    if lastMatch != char['lastGame']:
                        char['lastGame'] = lastMatch
                        details = getMatchDetailsELO(lastMatch)
                        char.update(updateCharDataELO(char, details))
                                                
    # Calculate the ELO rating
    teams = calculateELO(details)
    
    # Update the ELO rating in the DB
    for char in details:
        if char['team'] == 'Alpha':
           newELOFactor = teams.get('Alpha')           
        else:
           newELOFactor = teams.get('Bravo')
           
        oldELO = getRequestedInfo(char['charId'], 'ELO')
        newELO *= (newELOFactor/oldELO)
        updateOneStat(char['charId'], 'ELO', newELO) 

def getMatchDetailsELO(matchID):
    ############################################################################################
    # Gets the details of a match for ELO tracking
    ############################################################################################
   
    # Define the url
    url = ("https://www.bungie.net/Platform/Destiny/Stats/PostGameCarnageReport/"+ 
           str(matchID) +"/?definitions=False") 

    request = makeRequest(url)
    matchData = (request['Response']['data']['entries'])
    
    # Filter to important data
    playerInfo = []
    x = 0
    for entires in matchData:
        details = {
        'charId' : (matchData[x]['characterId']),
        'kills' : (matchData[x]['values']['kills']['basic']['value']),
        'deaths' : (matchData[x]['values']['deaths']['basic']['value']),
        'completed' : (matchData[x]['values']['completed']['basic']['value']),
        'win' : (matchData[x]['values']['standing']['basic']['value']),
        'team' : (matchData[x]['values']['team']['basic']['displayValue']),
        'score' : (matchData[x]['values']['score']['basic']['value'])
        }
        playerInfo.append(details)
        x += 1    

    return playerInfo

def getMatchDetailsBanner(matchID):
    ############################################################################################
    # Gets the details of a match for Iron Banner tracking
    ############################################################################################
   
    # Define the url
    url = ("https://www.bungie.net/Platform/Destiny/Stats/PostGameCarnageReport/"+ 
           str(matchID) +"/?definitions=False") 

    request = makeRequest(url)
    matchData = (request['Response']['data']['entries'])
    matchStamp = (request['Response']['data']['period'])
    
    
    # Filter to important data
    playerInfo = []
    x = 0
    for entires in matchData:
        details = {
        'charId' : (matchData[x]['characterId']),
        'kills' : (matchData[x]['values']['kills']['basic']['value']),
        'deaths' : (matchData[x]['values']['deaths']['basic']['value']),
        'completed' : (matchData[x]['values']['completed']['basic']['value']),
        'win' : (matchData[x]['values']['standing']['basic']['value']),
        'assists' : (matchData[x]['values']['assists']['basic']['value']),
        'orbs' : (matchData[x].get('extended',{}).get('values',{}).get('orbsDropped',{}).get('basic',{}).get('value',0)),
        'precisionKills' : (matchData[x].get('extended',{}).get('values',{}).get('precisionKills',{}).get('basic',{}).get('value',0)),
        'spree' : (matchData[x].get('extended',{}).get('values',{}).get('longestKillSpree',{}).get('basic',{}).get('value',0)),
        'objectives' : (matchData[x].get('extended',{}).get('values',{}).get('zonesCaptured',{}).get('basic',{}).get('value',0)),
        }
        playerInfo.append(details)
        x += 1    
    

    return playerInfo

def updateCharDataELO(char, details):
    ############################################################################################
    # Makes updates to character data for ELO tracking
    ############################################################################################

    for deets in details:
        if deets['charId'] == char['charNum']:
            if deets['completed'] == 1:

                # Aggregates
                char['games'] += 1
                char['kills'] += deets['kills']
                char['deaths'] += deets['deaths']

                # Conditionals
                if char['deaths'] == 0:
                   char['KDR'] = char['kills']
                else:
                    char['KDR'] = (char['kills']/char['deaths'])

                if deets['win'] == 0:
                    char['wins'] += 1
                else:
                    char['losses'] += 1

                if char['ELO'] == 0:
                    char['ELO'] = 1000

                # Update the DB
                updateCharDBELO(char)   

def updateDataBanner(char):
    ############################################################################################
    # Makes updates to member data for Iron Banner tracking
    ############################################################################################
    
    # Get match details
    matchNum = char['lastGame']
    details = getMatchDetailsBanner(matchNum)

    for deets in details:
        if deets['charId'] == char['charNum']:
            if deets['completed'] == 1:

                # Aggregates
                char['games'] += 1
                char['assists'] += deets['assists']
                char['kills'] += deets['kills']
                char['deaths'] += deets['deaths']
                char['orbs'] += deets['orbs']
                char['precisionKills'] += deets['precisionKills']
                char['objectives'] += deets['objectives']

                # Conditionals
                if char['deaths'] == 0:
                    char['KDR'] = char['kills']
                else:
                    char['KDR'] = (char['kills']/char['deaths'])

                if char['spree'] < deets['spree']:
                    char['spree'] = deets['spree']

                if deets['win'] == 0:
                    char['wins'] += 1
                if deets['win'] == 1:
                    char['losses'] += 1

                # Update the DB for the char
                updateIB(char)
            
    return char

def isValidBannerGame(matchList, memberList):
    memberMatches = set(matchList) & set(memberList)

    if len(memberMatches) > 1:
        return True
    else:
        return False

def updateMemberDataBanner(clanList):
    currentClanList = []
    # Make a list of members
    memberList = []
    for i in clanList:
        memberList.append(i.memberID)
    
    # Find each character's most recent banner game
    for i in clanList:
        for char in i.memberChars:
            lastMatch = getMostRecentGame(i.memberID, char['charNum'], "Iron Banner")
            charCLass = getClassHash(i.memberID, char['charNum'])
            char['class'] = charCLass

            # Find out if the most recent game is valid to begin counting
            if lastMatch != 0:
                matchPlayers = getMatchPlayers(lastMatch)
                isValid = isValidBannerGame(matchPlayers, memberList)

                # If it is a valid game, compare against the previous iron banner game
                if isValid:
                    if char['lastGame'] != lastMatch:
                       char['lastGame'] = lastMatch
                       char.update(updateDataBanner(char))                   
            currentClanList.append(char)         
    return currentClanList

def calculateELO(matchDetails):
    ############################################################################################
    # Calculates the ELO rating for each team after a match. Things considered:
    # Win/lose, opposing teams' average ELO rating pre-game, score, handicapped by players
    ############################################################################################
    alpha = []
    bravo = []
    K = 32

    # Get the team breakdown
    for deets in matchDetails:
        if deets['team'] == 'Alpha':
            alpha.append(deets['charId'])
            alphaScore += deets['score']
            alphaELO += getRequestedInfo(deets['charId'], 'ELO')

        if deets['team'] == 'Bravo':
            bravo.append(deets['charId'])
            bravoScore += deets['score']
            bravoELO += getRequestedInfo(deets['charId'], 'ELO')

        # Find the winner
        if deets['win'] == 0 and deets['team'] == 'Alpha':
            sA = 1
            bA = 0
        else:
            sA = 0
            bA = 1

    # Start calculating the resulting multiplier for each team
    # Get the teams' average ELO 
    alphaPlayers = len(alpha)
    bravoPlayers = len(bravo)

    alphaAvgELO = (alphaELO/alphaPlayers)
    bravoAvgELO = (bravoELO/bravoPlayers)

    # Calculate rating difference
    rA = math.pow(10, (alphaAvgELO/400))
    rB = math.pow(10, (bravoAvgELO/400))

    # Calculate the expected outcome
    eA = rA / (rA + rB)
    eB = rB / (rA + rB)

    # Calculate the modifier
    if alphaScore > (bravoScore * 1.5) or bravoScore > (alphaScore * 1.5):
        K += 2
    
    if alphaPlayers > bravoPlayers or bravoPlayers > alphaPlayers:
        K += 2

    # Calculate the updated ELO
    aE = alphaAvgELO + K * (sA - eA)
    bE = bravoAvgELO + K * (sB - eB)

    teamInfo = {'Alpha' : aE, 'Bravo' : bE}   

    return teamInfo

def eventListener(reqEvent):
    ############################################################################################
    # Listens for events to go live, such as Iron Banner, SRL, etc...
    ############################################################################################

    request = makeRequest('https://www.bungie.net/Platform/Destiny/Advisors/V2/?definitions=False')
    events = request['Response']['data']['activites']

    # Look for the requested event and check it's status
    if reqEvent in events:
        status = events.get(['status'], 0)

    if status == 0:
        return -1
    if status == 'true':
        return True
    if status == 'false':
        return False
