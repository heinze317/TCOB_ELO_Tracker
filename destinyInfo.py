############################################################################################
# Gets the data for the clan from the Bungie API
# Feeds that data to the reddit bot for posting
############################################################################################

import requests, copy, json
from pprint import pprint


# Dictionaries
HEADERS = {"X-API-Key":'1fdb95e58c5e4b91b4d628a1a405d9e5'}
CLASS = {
    2271682572: 'Warlock',
    671679327: 'Hunter',
    3655393761: 'Titan'
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

def buildClan():
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
    print('Getting clan data.....')
    clanInfo = getClanData()
    print('done!\n')

    # Filter to only user name and Destiny ID
    print('Filtering data.....')
    x = 0

    for i in clanInfo:
        userNames.append(clanInfo[x]['destinyUserInfo']['displayName'])
        destinyIDs.append(clanInfo[x]['destinyUserInfo']['membershipId'])
        x += 1
    print('done!\n')
    
    # Use the IDs to get character numbers
    print('Getting character numbers.....')
    x = 0

    for x in range(len(userNames)):
        characterNums.append(getCharacterNumber(destinyIDs[x]))
        x += 1
    print('done!\n')
    
    
    # Build each character's dictionary of info
    for lst in characterNums:
        charInfo = []
        for char in lst:
            charDict = {'charNum' : char,
                        'games' : 0,
                        'KDR' : 0.0,
                        'ELO' : 1000,
                        'lastGame' : 0}
            charInfo.append(charDict)
        clanChars.append(charInfo)
       
     
   
    # Use the current info to build the clan class objects
    print('Building the member list.....')
    
    x = 0
   
    for x in range(len(userNames)):
        memberInstance = Member(userNames[x], destinyIDs[x], clanChars[x])
        clanArray.append(memberInstance)
        x += 1
    
    print('done!\n')
       
    return clanArray

def isClanOnlyGame(matchList, memberList):
    ############################################################################################
    # Compares the list of players in a game with the most current clan instance, 
    # If only clan members are listed, returns true.
    ############################################################################################

    return result

def getMatchDetails(matchID):
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

def getMostRecentGame(**memberDict):
    ############################################################################################
    # Gets the most recent private game for each member of the clan, one character at a time
    ############################################################################################
    
    # Define url
    url = ("https://www.bungie.net/Platform/Destiny/Stats/ActivityHistory/2/"+ str(memID)+ "/"
           + str(charID) +"/?count=1&definitions=False&mode=32&page=1")
    request = makeRequest(url)
        
    try:
        recentGame = request['Response']['data']['activities']
        recentId = (recentGame[0]['activityDetails']['instanceId'])
    except:
        recentId = 0       
   
    return recentId

def defineLastGamePlayed(clanList):
    ############################################################################################
    # Finds the last clan only game played for each member of the clan.
    ############################################################################################
    
    memberList = []
    charList = []
    memberInfo = {}
    lastGameIds = {}

    # Extract the member info from the most current list
    for i in clanList:
       memberList.append(i.memberID)
       charList.append(i.memberChars)
       memberInfo.update({i.memberID : i.memberChars})

    # Find each character's most recent private game
    #for 

    return lastGameIds
