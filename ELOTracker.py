############################################################################################
# Main script to run functions through
############################################################################################

from destinyInfo import buildClan, updateMemberData
from redditInfo import editMainThread
from excelInfo import createBook, writeInfo
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

    # Once the clan is built, loop until the process is killed
    while True:
        try:
            print("Updating the clan")
            # Get the most current information for each member
            updateMemberData(clanList)
            print("Done")
        except:
            print("Something went wrong updating the clan")

        '''try:
            print("Updating the spreadsheet")
            # Update the spreadsheet with the current data
            writeInfo(clanList)
            print("Done")
        except:
            print("Something went wrong writing the file")'''
        print("Updating the spreadsheet")
        # Update the spreadsheet with the current data
        writeInfo(clanList)
        print("Done")

        '''try:
            print("Editing the thread")
            # Edit the reddit thread with the most current information
            editMainThread(clanList)
            print("Done")
        except:
            print("Something went wrong editing the Reddit thread")

        time.sleep(300)'''

main()