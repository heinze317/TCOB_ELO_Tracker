############################################################################################
# Main script to run functions pertaining to Iron Banner Tracking
############################################################################################

from destinyInfo import buildClanBanner, updateMemberDataBanner, makeRequest
from excelInfo import writeCSV
import time

def main():

    # Check whether or not the event is live
    request = makeRequest('https://www.bungie.net/Platform/Destiny/Events/?definitions=False')
    requestList = request(['Response']['data']['events'])
    isLive = (requestList[0]['vendor'].get('enabled', 'False'))

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
    while isLive == 'true':
        print("Checking Event Status")
        # Check whether or not the event is live
        request = makeRequest('https://www.bungie.net/Platform/Destiny/Events/?definitions=False')
        requestList = request(['Response']['data']['events'])
        isLive = (requestList[0]['vendor'].get('enabled', 'False')) 

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