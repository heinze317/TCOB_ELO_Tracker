############################################################################################
# Gets the data for the clan from the Bungie API for all requests
############################################################################################

import requests, copy, json, math
from DBHandler import *


# Dictionaries
HEADERS = {"X-API-Key":'***********'}

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

############################################################################################
# Globally used functions
############################################################################################

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

def charCompare(clanList, tableToFetch):
    ############################################################################################
    # Compare a list of characters from the DB to the most current list from the API
    # Any characters not found in the DB will need to be added to either a new member or
    # A current member who has recently started that character
    ############################################################################################

    # Get the list of current characters from the DB
    charsDB = getCharList(tableToFetch)

    # Extract the character numbers from the most recent API call
    charsAPI = []
    for members in clanList:
        for char in members.memberChars:
            charsAPI.append(char['charNum'])

    # Compare the two lists, find any non-intersecting characters
    charsToUpdate = []
    charsToUpdate.append([char for char in charsDB if char not in charsAPI])

    # If updating needs to happen, do it
    if len(charsToUpdate) > 0:
        addCharsToDB(clanList, charsToUpdate)

############################################################################################
# Elo functions
# The actual Elo calculation throws an error. For now, Elo will be simple +/-1 
############################################################################################

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

def isClanOnlyGame(matchList, memberList):
    ############################################################################################
    # Compares the list of players in a game with the most current clan instance, 
    # If only clan members are listed returns true. Used for the ELO tracker only
    ############################################################################################

   return (set(matchList).issubset(memberList))

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
        'team' : (matchData[x].get('values',{}).get('team',{}).get('basic',{}).get('displayValue',0)),
        'score' : (matchData[x]['values']['score']['basic']['value'])
        }
        playerInfo.append(details)
        x += 1    

    return playerInfo

def updateMemberDataELO(clanList):
    ############################################################################################
    # Finds the last clan only game played for each member of the clan.
    # Returns an updated instance of each Member containing the last match ID
    ############################################################################################
    gamesToUpdate = [] 
    
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
                if clanOnly and len(matchPlayers) > 1:
                    if lastMatch != char['lastGame']:
                        gamesToUpdate.append(lastMatch)
                        char['lastGame'] = lastMatch
                        details = getMatchDetailsELO(lastMatch)
                        updateCharDataELO(char, details)

    # If any info was updated, calculate elo ratings on that info
    if len(gamesToUpdate) > 0:
        calculateELO(gamesToUpdate)

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
                if char['ELO'] == 0:
                    char['ELO'] = 1000

                if char['deaths'] == 0:
                   char['KDR'] = char['kills']
                else:
                    char['KDR'] = (char['kills']/char['deaths'])

                '''if deets['win'] == 0:
                    char['wins'] += 1
                    char['ELO'] += 1
                else:
                    char['losses'] += 1
                    char['ELO'] -= 1'''

                # Update the DB
                updateCharDBELO(char)
                
def calculateELOOld(matchDetails):
    ############################################################################################
    # Calculates the ELO rating for each team after a match. Things considered:
    # Win/lose, opposing teams' average ELO rating pre-game, score, handicapped by players
    ############################################################################################
    alpha = []
    bravo = []
    alphaScore = 0
    alphaELO = 0
    bravoScore = 0
    bravoELO = 0
    sA = 0
    bA = 0
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
        else:
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

def calculateELO(gamesToUpdate):

    # Big ass loop mind-fuck incoming.....
    for game in gamesToUpdate:

        # Empty containers and variables
        alphaPlayers = []
        bravoPlayers = []
        alphaScore, bravoScore, alphaOld, bravoOld = 0
        alphaExpected, bravoExpected, alphaActual, bravoActual = 0
        alphaNew, bravoNew = 0
        k = 32

        # Get the game details
        details = getMatchDetailsELO(game)

        # Split up the teams
        for deets in details:

            # If the team is returned as 0 something is wrong
            if deets['team'] == 0:
                # Break the loop
                pass

            if deets['team'] == 'Alpha':
                alphaPlayers.append(deets['charId'])
                alphaScore += deets['score']
                alphaOld += getRequestedInfo(deets['charId'], 'ELO')

            if deets['team'] == 'Bravo':
                bravoPlayers.append(deets['charId'])
                bravoScore += deets['score']
                bravoOld += getRequestedInfo(deets['charId'], 'ELO')

            # Find the winner
            if deets['win'] == 0 and deets['team'] == 'Alpha':
                # Alpha wins
                alphaActual = 1
                bravoActual = 0

            if deets['win'] == 0 and deets['team'] == 'Bravo':
                # Bravo wins
                alphaActual = 0
                bravoActual = 1

        # Get the average elo rating for each team
        alphaAvgElo = (alphaOld / len(alphaPlayers))
        bravoAvgElo = (bravoOld / len(bravoPlayers))

        # Get the expected scores
        alphaExpected = calculateExpected(alphaAvgElo, bravoAvgElo)
        bravoExpected = calculateExpected(bravoAvgElo, alphaAvgElo)

        # Account for any modifiers
        if alphaScore > (bravoScore * 1.5) or bravoScore > (alphaScore * 1.5):
            k += 1
    
        if len(alphaPlayers) > len(bravoPlayers) or len(bravoPlayers) > len(alphaPlayers):
            k += 1

        # Calculate the actual outcome
        alphaNew = (alphaAvgElo + k * (alphaActual - alphaExpected))
        bravoNew = (bravoAvgElo + k * (bravoActual - bravoExpected))

        # Update the DB with the new elo scores
        for player in alphaPlayers:
            updateOneStat(player, 'ELO', alphaNew)

        for player in bravoPlayers:
            updateOneStat(player, 'ELO', bravoNew)    
    

def calculateExpected(teamA, teamB):

    # Seperate to avoid the monster loop
    return 1 / (1 + 10 ** ((B - A) / 400))

############################################################################################
# Iron Banner Control functions
############################################################################################

def isValidBannerGame(matchList, memberList):
    memberMatches = set(matchList) & set(memberList)

    if len(memberMatches) > 1:
        return True
    else:
        return False

def buildClanBannerControl():
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

def getMatchDetailsBannerControl(matchID):
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

def updateDataBannerControl(char):
    ############################################################################################
    # Makes updates to character data for Iron Banner tracking Control gametype
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
                updateIBControl(char)    

def updateMemberDataBannerControl(clanList):
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
                       
############################################################################################
# Iron Banner Rift functions
# Event run on 12/6 - 12/12 did not update the DB. I suspect it has to do with the API.
############################################################################################    

def buildClanBannerRift():
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
                        'sparksCaptured' : 0,
                        'sparksDelivered' : 0,
                        'carrierKills' : 0,
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

def getMatchDetailsBannerRift(matchID):
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
        'sparksCaptured' : (matchData[x].get('extended',{}).get('values',{}).get('sparksCaptured',{}).get('basic',{}).get('value',0)),
        'sparksDelivered' : (matchData[x].get('extended',{}).get('values',{}).get('slamDunks',{}).get('basic',{}).get('value',0)),
        'carrierKills' : (matchData[x].get('extended',{}).get('values',{}).get('carrierKills',{}).get('basic',{}).get('value',0)),
        }
        playerInfo.append(details)
        x += 1    
    

    return playerInfo

def updateMemberDataBannerRift(clanList):
    
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
                # Make updates if needed
                if isValid:
                    if char['lastGame'] != lastMatch:
                       char['lastGame'] = lastMatch
                       char.update(updateDataBannerRift(char)) 

def updateDataBannerRift(char):
    ############################################################################################
    # Makes updates to character data for Iron Banner tracking Rift gametype
    ############################################################################################
    
    # Get match details
    matchNum = char['lastGame']
    details = getMatchDetailsBannerRift(matchNum)

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
                char['sparksCaptured'] += deets['sparksCaptured']
                char['sparksDelivered'] += deets['sparksDelivered']
                char['carrierKills'] += deets['carrierKills']

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
                updateIBRift(char)    
