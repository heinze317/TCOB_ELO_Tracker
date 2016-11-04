############################################################################################
# Main script to run functions through
############################################################################################

from destinyInfo import buildClan, updateMemberData
from redditInfo import editMainThread
import copy, time



def main():

    try:
        print("Getting clan info")
        # Get the most current clan list available
        clanList = buildClan()
        print("Done")
    except:
        print("Something went wrong getting the clan information")
    
    try:
        print("Updating the clan with the correct information")
        # Get the most current information for each member
        updateMemberData(clanList)
        print("Done")
    except:
        print("Something went wrong updating the clan")

    try:
        print("Editing the thread")
        # Edit the reddit thread with the most current information
        editMainThread(clanList)
        print("Done")
    except:
        print("Something went wrong editing the Reddit thread")

    time.sleep(300)   

main()