############################################################################################
# Main script to run functions through
############################################################################################

from destinyInfo import buildClan, defineLastGamePlayed
import copy



def main():

    oldData = {}
    currentData = {}
    oldClanList = []
    currentClanList = []

    # Get the clan members from the Bungie API
    oldClanList = copy.deepcopy(currentClanList)
    currentClanList = buildClan()
    
    # Compare current data against previous update


    # Get most recent clan-only private game 
    oldData = copy.deepcopy(currentData)
    currentData = defineLastGamePlayed(currentClanList)
    
    # Compare current data against previous update

    
    # Make updates to members' data


    # Post the updated info to the Reddit thread
      
   

main()