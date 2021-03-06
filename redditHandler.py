﻿############################################################################################
# Creates the Reddit thread containing the initial info. 
# The bot should be able to edit the original post to update that info
############################################################################################

import praw, time, datetime
from DBHandler import *

# Dictionary
SUBNAME = 'tcob'
ELO = 'https://www.reddit.com/r/TCOB/comments/584ydw'
ELO_ID = '584ydw'
BANNER = 'Null'
VERSION = 'Beta'

def disclaimerText():
    ############################################################################################
    # States the use of the bot, how to reach the owner, etc inside the post body
    ############################################################################################

    disclaimer = ("\n\n\n\n"+
                  "This data was compiled and computed using an automated program. There may be "+
                  "errors from time in the way the Bungie API responds to requests, or "+
                  "an oversight from the programmer. A few things to keep in mind:"+
                  "\n\n1. This only counts private games, containing only clan members."+
                  "\n\n2. This only counts games played to completion. Either time limit or "+
                  "score limit must be reached for the game to count."+
                  "\n\n3. This thread will be updated one per hour, barring any errors. " +
                  "\n\n4. If you were just added to the clan, please wait 24 hours " +
                  "for your stats to start being accrued." +
                  "\n\n5. I am a bot. My sole purpose in life is to stalk members of the Destiny TCOB "+
                  "clan, and monitor their clan-only private games. I use that information "+
                  "to rank the members based on how much they suck at Destiny, then post it "+
                  "online for everyone's amusement. If you have an issue with any of the data "+
                  "I post, please get ahold of **/u/12vp** here on "+
                  "Reddit, or message **twelvevoltpro** on PSN to discuss. Thank you" +
                  "\n\n\n\n\n\nProgram Version: " + VERSION)

    return disclaimer

def headerText():
    ############################################################################################
    # Used to define the text at the top of the post for ELO tracking
    ############################################################################################

    header = ("n\n\n\n")

    return header

def mainText(clanInfoToPost):
    ############################################################################################
    # Used to build the main text body of the post. Stats pulled from DB instead of memory
    ############################################################################################
    timeLong = datetime.datetime.now()
    timeStamp = timeLong.strftime('%m %d %Y %H:%M')
    memberText = "**Last Upated:** " + timeStamp + "\n\n**Data:** \n\n"
    header = headerText()
    footer = disclaimerText()

    for member in clanInfoToPost:
        memberText += ("**Username:** "+ member.displayName+ "\n\n")
        for char in member.memberChars:
            memberText += ("**"+char['class']+":**\n"+
                       "Games: "+str(getRequestedInfo(char['charNum'], 'Games'))+"\n"+
                       "Wins: "+str(getRequestedInfo(char['charNum'], 'Wins'))+"\n"+
                       "Losses: "+str(getRequestedInfo(char['charNum'], 'Losses'))+"\n"+
                       "Kills: "+str(getRequestedInfo(char['charNum'], 'Kills'))+"\n"+
                       "Deaths: "+str(getRequestedInfo(char['charNum'], 'Deaths'))+"\n"+
                       "KDR: "+ ("%.2f" %getRequestedInfo(char['charNum'], 'KDR'))+"\n"+
                       "ELO: "+str(getRequestedInfo(char['charNum'], 'ELO'))+"\n"+
                       "\n\n")
        memberText += ("----------------------------------------------\n\n\n\n")
       
    text = (header + memberText + footer)

    return text

def editELOThread(clanInfo):
    ############################################################################################
    # Will be used to edit initial post, keeps post count to an absolute minimum
    ############################################################################################

    r = praw.Reddit('tcob1')
    #o = OAuth2Util.OAuth2Util(r)
    #o.refresh(force=True)

    # Get the submission
    submission = r.submission(id = ELO_ID)
    selfText = submission.selftext
    
    # Build the body of the thread
    selfText = mainText(clanInfo)

    # Edit the post
    submission.edit(selfText) 
