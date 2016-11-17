﻿############################################################################################
# Main script to handle the ELO side
############################################################################################

from destinyHandler import buildClanELO, updateMemberDataELO
from redditHandler import editELOThread
from DBHandler import writeELO, clanFromELO
from emailHandler import sendMessage
import time

MESSAGES = {
    1 : "The tracker has been restarted",
    2 : "The tracker failed to build the clan",
    3 : "The tracker failed to update the clan",
    4 : "The tracker failed to build the DB",
    5 : "The tracker failed to update the reddit thread",
    6 : "The tracker failed for an unknown reason"
    }

def main():
    
    # Try getting information from the DB on start, if no data exists
    # Build initial clanlist to begin the event
    sendMessage(MESSAGES.get(1))
    clanList = []

    if not clanList:
         # If no, build it
        try:
           #print("Getting clan info")
           # Get the most current clan list available
           clanList = buildClanELO()
           #print("Done")
        except:
           #print("Something went wrong getting the clan information")
           sendMessage(MESSAGES.get(2))

        try:
            #print("Looking for data for a rebuild")
            clanFromELO(clanList)
            #print("Done")
        except:
            # If no data exists, build it from scratch
            #print("No data")
            try:
                # Build the initial DB
                #print("Building the initial database")
                writeELO(clanList)
                #print("Done")
            except:
                #print("Something went wrong building the database")
                sendMessage(MESSAGES.get(4))
            
        
    # Once the clan is built, loop until the process is killed
    while True:
       try:
            #print("Updating the clan")
            # Get the most current information for each member
            updateMemberDataELO(clanList)
            #print("Done")
       except:
            #print("Something went wrong updating the clan")
            sendMessage(MESSAGES.get(3))

       try:
            #print("Editing the reddit post")
            editELOThread(clanList)
            #print("Done")
       except:
            #print("Something went wrong editing the thread")
            sendMessage(MESSAGES.get(5))

       time.sleep(300)

main()