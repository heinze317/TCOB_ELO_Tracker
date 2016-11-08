############################################################################################
# Main script to run functions pertaining to Iron Banner Tracking
############################################################################################

from destinyInfo import buildClanBanner, updateMemberDataBanner
from excelInfo import writeCSV
import time

def main():

    # Build initial clanlist
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

    # Once the clan is built, loop until the process is killed
    while True:
        try:
            print("Updating the clan")
            # Get the most current information for each member
            updateMemberDataBanner(clanList)
            print("Done")
        except:
            print("Something went wrong updating the clan")       
        
        try:
            print("Updating the spreadsheet")
            # Update the spreadsheet with the current data
            writeCSV(clanList)
            print("Done")
        except:
            print("Something went wrong writing the file")

        time.sleep(300)


main()