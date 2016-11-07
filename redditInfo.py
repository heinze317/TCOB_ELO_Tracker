############################################################################################
# Creates the Reddit thread containing the initial info. 
# The bot should be able to edit the original post to update that info
############################################################################################

import praw, OAuth2Util, time

# Dictionary
SUBNAME = 'tcob'
ELO = 'https://www.reddit.com/r/TCOB/comments/584ydw'



def makePost():
    ############################################################################################
    # Will be used to make initial post, and any time data loss happens, will be used to make 
    # Subsequent posts
    ############################################################################################
    
    r = praw.Reddit('/r/tcob auto poster. Created by /u/12vp')
    o = OAuth2Util.OAuth2Util(r)
    o.refresh(force=True)
        
    # Get the post info
    # textBody = testText()
    
    # Get the thread title
    # threadTitle = testTitle()

     # Post the thread
    try:
        submission = r.submit(SUBNAME, threadTitle, text = textBody)
        print ("Success, check reddit!")
    except:
        print ("Failed, don't check reddit.")

        return 

def testText():
    text = ("Testing.... testing.........")

    return text

def testTitle():
    title = ("Test Thread")

    return title

def disclaimerText():
    ############################################################################################
    # States the use of the bot, how to reach the owner, etc inside the post body
    ############################################################################################

    disclaimer = ("\n\n\n\n"+
                   "I am a bot. My sole purpose in life is to stalk members of the Destiny TCOB "+
                  "clan, and monitor their clan-only private games. I use that information "+
                  "to rank the members based on how much they suck at Destiny, then post it "+
                  "online for everyone's amusement. If you have an issue with any of the data "+
                  "I post, please get ahold of /u/12vp here on "+
                   "Reddit, or message twelvevoltpro on PSN to discuss. Thank you")

    return disclaimer

def headerText():
    ############################################################################################
    # Used to define the text at the top of the post
    ############################################################################################

    header = ("This data was compiled and computed using an automated program. There may be "+
              "errors from time in the way the Bungie API responds to requests, or "+
              "an oversight from the programmer. A few things to keep in mind:"+
              "\n\n1. This only counts private games, containing only clan members."+
              "\n\n2. This only counts games played to completion. Either time limit or "+
              "score limit must be reached for the game to count."+
              "\n\n3. Any other information you think I should add, just let me know!\n\n\n\n")

    return header

def mainText(clanInfoToPost):
    ############################################################################################
    # Used to build the main text body of the post
    ############################################################################################
    memberText = "Data: \n\n"
    header = headerText()
    footer = disclaimerText()

    for member in clanInfoToPost:
        memberText += ("**Username:** "+ member.displayName+ "\n\n")
        for char in member.memberChars:
            memberText += (char['class']+":\n"+
                       "Games: "+str(char['games'])+"\n"+
                       "Wins: "+str(char['wins'])+"\n"+
                       "Losses: "+str(char['losses'])+"\n"+
                       "Kills: "+str(char['kills'])+"\n"+
                       "Clan Only Deaths: "+str(char['deaths'])+"\n"+
                       "Clan Only KDR: "+ ("%.2f" %char['KDR'])+"\n"+
                       "Clan Only ELO: "+str(char['ELO'])+"\n"+
                       "\n\n")
        memberText+= ("----------------------------------------------\n\n\n\n")
       
    text = (header + memberText + footer)

    return text

def editMainThread(clanInfo):
    ############################################################################################
    # Will be used to edit initial post, keeps post count to an absolute minimum
    ############################################################################################

    r = praw.Reddit('/r/tcob auto poster. Created by /u/12vp')
    o = OAuth2Util.OAuth2Util(r)
    o.refresh(force=True)

    # Get the submission
    submission = r.get_submission(ELO)
    selfText = submission.selftext
    
    # Build the body of the thread
    selfText = mainText(clanInfo)

    # Edit the post
    submission.edit(selfText)

    