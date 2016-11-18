############################################################################################
# Main script to handle the trackers. 
#
# The main function will be to ensure the ELO tracker script
# Stays running during the period of time between events. At this point
# The ELO tracker will pause for the duration of the Iron Banner while that tracker 
# Takes priority. 
#
# On the occurance of a crash of either tracker during normal runs, this script will notify
# The owner(s) of the script via email and automatically restart the crashed script.
#
# At the end of the Iron Banner event, the script will email the Iron Banner DB table 
# To the appointed clan member in charge of the data. 
# 
############################################################################################

from destinyHandler import eventListener
from emailHandler import sendMessage
import ELOTracker, bannerTracker, time, subprocess, os

EVENTS = {
    1 : "ironbanner",
    2 : "srl"
    }

def getPID(process):

    try:
        return subprocess.check_output(['pidof', process])
    except:
        return -1

def main():

    while True:
        # Listen for the ELO tracker to make sure it's running as it should
        pid = getPID('ELOTracker.py')

        if pid == -1:
            # If the process doesn't exist, start it and notify the owner(s)
            sendMessage("The tracker crashed... Trying to restart it!")


        # Listen for special events
        # For now, only listens for Iron Banner
        specEventActive = eventListener(EVENTS.get(1))

        # If an event is active, ELO tracking takes a backseat
        while specEventActive:

            # Kill the ELO tracker
            os.system("kill -9" + pid)

            # Start the event tracker
            # For now, just the Iron Banner tracker


            # Check the status again
            specEventActive = eventListener(EVENTS.get(1))

        time.sleep(3600)


main()
