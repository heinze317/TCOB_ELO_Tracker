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
    1 : "The ELOtracker has been restarted",
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
       clanFromDBELO(clanList)
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
        
       # Update every 5 minutes
       for x in range(14):
            try:
                #print("Updating the clan")
                # Get the most current information for each member
                updateMemberDataELO(clanList)
                #print("Done")
            except:
                #print("Something went wrong updating the clan")
                sendMessage(MESSAGES.get(3))
            time.sleep(300)
            x += 1 
        
            # Update the thread every hour from DB
            if x == 13:
                try:
                    #print("Editing the reddit post")
                    editELOThread(clanList)
                    #print("Done")
                except:
                    #print("Something went wrong editing the thread")
                    sendMessage(MESSAGES.get(5))

                # Check for new members every hour
                #charCompare(clanList, 'ELO')

                x = 0 # Reset the counter after the thread update  

main()