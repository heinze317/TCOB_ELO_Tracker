############################################################################################
# Main script to handle the ELO side
############################################################################################
#!/usr/bin/python

from destinyHandler import buildClanELO, updateMemberDataELO, charCompare
from redditHandler import editELOThread
from DBHandler import writeELO, clanFromDBELO
from emailHandler import sendMessage
import time

MESSAGES = {
    1 : "The ELOtracker has been restarted.",
    2 : "The tracker failed to build the clan.",
    3 : "The tracker failed to update the clan.",
    4 : "The tracker failed to build the DB.",
    5 : "The tracker failed to update the reddit thread.",
    6 : "The tracker failed for an unknown reason.",
    7 : "The tracker crashed. Please restart it!",
    8 : "There was no data to build info from."
    }

SUBJECTS = {
    1 : "Tracker Update - Restart",
    2 : "Tracker Update - Crash",
    3 : "Tracker Update - Clan Error",
    4 : "Tracker Update - DB Error",
    5 : "Tracker Update - General"
    }

def main():
    
    clanList = []
    # Try getting information from the DB on start, if no data exists
    # Build initial clanlist to begin the event
    sendMessage(MESSAGES.get(1), SUBJECTS.get(1))
   
    # If no, build it
    if not clanList:
        try:
            # Get the most current clan list available
            clanList = buildClanELO()
        except:
            sendMessage(MESSAGES.get(2), SUBJECTS.get(3))
        try:
            clanFromDBELO(clanList)        
        except:
            # If no data exists, build it from scratch
            sendMessage(MESSAGES.get(8), SUBJECTS.get(5))
            try:
                # Build the initial DB
                writeELO(clanList)
            except:
                sendMessage(MESSAGES.get(4), SUBJECTS.get(4))
            
        
    # Once the clan is built, loop until the process is killed
    while True:
        
       # Update every 5 minutes
       for x in range(9):
            try:
                # Get the most current information for each member
                updateMemberDataELO(clanList)
            except:
                sendMessage(MESSAGES.get(3), SUBJECTS.get(3))
            time.sleep(300)
            x += 1 
                    
            # Update the thread every hour from DB
            # Update counter accounts for time to run the main loop
            if x == 9:
                try:
                    editELOThread(clanList)
                except:
                    sendMessage(MESSAGES.get(5), SUBJECTS.get(5))

                # Check for new members every hour
                #charCompare(clanList, 'ELO')

                # Reset the counter
                x = 0

while True:
    try:
        main()
    except:
        sendMessage(MESSAGES.get(7), SUBJECTS.get(2))