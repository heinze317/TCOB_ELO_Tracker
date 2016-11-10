############################################################################################
# Main script to run functions through
############################################################################################

from destinyInfo import buildClanELO, updateMemberDataELO
from redditInfo import editELOThread
from DBHandler import writeELO
import copy, time

def main():

    clanList = []
    # Check for an existing instance of the clan
    if not clanList:

        # If no, build it
        try:
           print("Getting clan info")
           # Get the most current clan list available
           clanList = buildClan()
           print("Done")
        except:
           print("Something went wrong getting the clan information")

        try:
            print("Creating the database")
            writeELO(clanList)
            print("Done")
        except:
            print("Something went wrong creating the database")


    # Once the clan is built, loop until the process is killed
    while True:
        try:
            print("Updating the clan")
            # Get the most current information for each member
            updateMemberDataELO(clanList)
            print("Done")
        except:
            print("Something went wrong updating the clan")

        '''try:
            print("Editing the thread")
            # Edit the reddit thread with the most current information
            editMainThread(clanList)
            print("Done")
        except:
            print("Something went wrong editing the Reddit thread")'''

        time.sleep(300)

main()