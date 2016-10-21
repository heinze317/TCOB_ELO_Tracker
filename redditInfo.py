############################################################################################
# Creates the Reddit thread containing the initial info. 
# The bot should be able to edit the original post to update that info
############################################################################################

import praw, OAuth2Util, time

# Dictionary
subredditName = 'tcob'



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
        submission = r.submit(subredditName, threadTitle, text = textBody)
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