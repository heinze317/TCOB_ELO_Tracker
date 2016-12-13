############################################################################################
# Main script to run functions pertaining to Iron Banner Rift Tracking
############################################################################################

from destinyHandler import buildClanBannerRift, updateMemberDataBannerRift
from DBHandler import writeIBRift, clanFromDBIBRift
from emailHandler import sendMessage
import time

def main():
    
    # Try getting information from the DB on start, if no data exists
    # Build initial clanlist to begin the event
    sendMessage("Iron Banner Rift Tracker has been started")  
    clanList = []

    if not clanList:
         # If no, build it
        try:
           #print("Getting clan info")
           # Get the most current clan list available
           clanList = buildClanBannerRift()
           #print("Done")
        except:
           #print("Something went wrong getting the clan information")
           sendMessage("Somethng went wrong getting clan information")

        try:
            #print("Looking for data for a rebuild")
            clanFromDBIBRift(clanList)
            #print("Done")
        except:
            # If no data exists, build it from scratch
            #print("No data")
            try:
                # Build the initial DB
                #print("Building the initial database")
                writeIBRift(clanList)
                #print("Done")
            except:
                #print("Something went wrong building the database")
                sendMessage("Something went wrong building the database")
            
        
    # Once the clan is built, loop until the process is killed
    while True:
       try:
            #print("Updating the clan")
            # Get the most current information for each member
            updateMemberDataBannerRift(clanList)
            #print("Done")
       except:
            #print("Something went wrong updating the clan")
            sendMessage("Something went wrong updating the clan")
        
       # Sleep for 5 minutes 
       time.sleep(300) 


main()