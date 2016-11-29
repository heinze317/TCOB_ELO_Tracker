# TCOB_ELO_Tracker

Just a simple bundle of files that track and post the ELO and other stats for the TCOB Destiny clan. Data can be found on /r/tcob.

In its current state, the entire module is started manually via Unix command line. The trackerHandler listens for the active tracker's PID every hour. If it is not found, an email notification of a crash is sent. At this point the owner must manually restart the tracker.

# ELOTracker

When running perfectly, the tracker will make a request to the Bungie API for each character's most recent private game. If this game meets certain criteria (contains only clan member players, is played to completion), it will pull the data for that game and calculate stats based from that data. The data is saved to a local database, then posted to a dedicated Reddit thread found in the clan subreddit.

The Elo score is based on a commonly found formula, with the 'K' value able to be changed based on:

-A dominant score by either team (currently set to 150%)

-One team playing with fewer team members (i.e. 3v2, 1v2, etc.)

# bannerTracker

Started as a fun way to track the clan members' Iron Banner games and their performance in those games. Like the Elo tracker, it will request each character's most recent Iron Banner game from the Bungie API. If that game meets certain criteria (fireteam has at least 2 clan members, game is played to completion), it will pull the data for that game and calculate stats from that data. The data is saved to a local database for the duration of the event. Upon event completion, the owner extracts the data to a spreadsheet and sends to another clan member for awards for best (and worst) performance based on the stats provided. 

# Features and Functions to add

Date filter for special events to only keep data for current event

Function to check for new members/characters and add them to the DB (added 11/29)(needs testing)

Ranking system to post the members from highest to lowest Elo score

!Function to automatically backup the DB every x hours! -In progess

Function to email the event table upon event completion

Function to auto restart the trackers upon a crash

Module to host an x v x tournament
