﻿############################################################################################
# Main script to run functions pertaining to Iron Banner Tracking
############################################################################################

from destinyInfo import buildClanBanner, updateMemberDataBanner, makeRequest
from DBHandler import writeIB, clanFromIB
import time

def main():
    
    # Try getting information from the DB on start, if no data exists
    # Build initial clanlist to begin the event
       
    clanList = []

    if not clanList:
         # If no, build it
        try:
           print("Getting clan info")
           # Get the most current clan list available
           clanList = buildClanBanner()
           print("Done")
        except:
           print("Something went wrong getting the clan information")

        try:
            print("Looking for data for a rebuild")
            clanFromIB(clanList)
            print("Done")
        except:
            # If no data exists, build it from scratch
            print("No data")
            try:
                # Build the initial DB
                print("Building the initial database")
                writeIB(clanList)
                print("Done")
            except:
                print("Something went wrong building the database")
            
        
    # Once the clan is built, loop until the process is killed
    while True:
        print("Updating the clan")
        # Get the most current information for each member
        updateMemberDataBanner(clanList)
        print("Done")
        '''try:
            print("Updating the clan")
            # Get the most current information for each member
            updateMemberDataBanner(clanList)
            print("Done")
        except:
            print("Something went wrong updating the clan")'''

        time.sleep(300)


main()