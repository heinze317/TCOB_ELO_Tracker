############################################################################################
# Creates the db file that will be used to hold information. This will allow the 
# program to compare new data against old, and also allow admins to make changes to
# the data on an "as-needed" basis
############################################################################################

import csv, sqlite3

conn = sqlite3.connect('clanTracker.db')
c = conn.cursor()

def updateIB(char):
    ############################################################################################
    # Edits the table one character at a time, on an as-needed basis 
    ############################################################################################

    if char.get('games') == 0:
        print("Something is not right!!!")
    else:
        # Get the info to update
        row = [char.get('class'),
               char.get('games'),
               char.get('lastGame'),
               char.get('kills'),
               char.get('wins'),
               char.get('losses'),
               char.get('deaths'),
               char.get('KDR'),
               char.get('assists'),
               char.get('orbs'),
               char.get('objectives'),
               char.get('spree'),
               char.get('precisionKills'),
               char.get('charNum')
               ]
   
        # Updates the DB on a need-to-do basis
        c.execute("UPDATE IronBanner SET CharClass = ?, Games = ?, LastGame = ?, Kills = ?, Wins = ?,"+
                  "Losses = ?, Deaths = ?, KDR = ?, Assists = ?, Orbs = ?, Objectives = ?,"+
                  "Spree = ?, Precision = ? WHERE CharNum = ?", (row))

        conn.commit()
                                     
def updateCharDBELO(char):
    ############################################################################################
    # Edits the table one character at a time, on an as-needed basis 
    ############################################################################################
    
    # Get the info to update
    row = [char.get('games'),
           char.get('lastGame'),
           char.get('kills'),
           char.get('wins'),
           char.get('losses'),
           char.get('deaths'),
           char.get('KDR'),
           char.get('ELO'),
           char.get('charNum')
           ]

    # Updates the DB on a need-to-do basis
    c.execute("UPDATE ELO SET Games = ?, LastGame = ?, Kills = ?, Wins = ?,"+
              "Losses = ?, Deaths = ?, KDR = ?, ELO = ? WHERE CharNum = ?", (row))

    # Save the file
    conn.commit()

def updateOneStat(char, stat, newValue):
    ############################################################################################
    # Updates one stat at a time to the database
    ############################################################################################
    
    # Update the char stat to the new value
    c.execute("UPDATE ELO SET ? = ? WHERE CharNum = ?", (stat, newValue, char))

    # Save the file
    c.commit()

def writeIB(clanList):
    ############################################################################################
    # Saves the initial data to the DB. This allows the program to update only what
    # Needs updated per character
    ############################################################################################

    # Make sure the DB exists
    createIB()

    # Write the db
    for i in clanList:
        for char in i.memberChars:
            row = [
                i.displayName,
                i.memberID,
                char.get('charNum'),
                char.get('class')
               ]
            c.execute("INSERT INTO IronBanner VALUES(?,?,?,?,0,0,0,0,0,0,0,0,0,0,0,0)", (row))

    conn.commit()

def writeELO(clanList):
    ############################################################################################
    # Saves the initial data to the DB. This allows the program to update only what
    # Needs updated per character
    ############################################################################################

    # Make sure the DB exists
    createELO()

    # Write the db
    for i in clanList:
        for char in i.memberChars:
            row = [
                i.displayName,
                i.memberID,
                char.get('charNum'),
                char.get('class')
               ]
            c.execute("INSERT INTO IronBanner VALUES(?,?,?,?,0,0,0,0,0,0,0,0)", (row))

    # Save the file
    conn.commit()

def createIB():
    ############################################################################################
    # Creates the IB table. Should be run once per event 
    ############################################################################################

    # Make the table
    c.execute("CREATE TABLE IF NOT EXISTS IronBanner (Username TEXT, MemberID INTEGER, CharNum INTEGER, CharClass TEXT,"+
                "Games INTEGER, LastGame INTEGER, Kills INTEGER, Wins INTEGER, Losses INTEGER,"+
                "Deaths INTEGER, KDR REAL, Assists INTEGER, Orbs INTEGER, Objectives INTEGER,"+
                "Spree INTEGER, Precision INTEGER)")
    
    # Save the file
    conn.commit()

def createELO():
    ############################################################################################
    # Creates the ELO table. Should be run once per event 
    ############################################################################################

    # Make the table
    c.execute("CREATE TABLE IF NOT EXISTS ELO (Username TEXT, MemberID INTEGER, CharNum INTEGER, CharClass TEXT,"+
                "Games INTEGER, LastGame INTEGER, Kills INTEGER, Wins INTEGER, Losses INTEGER,"+
                "Deaths INTEGER, KDR REAL, ELO INTEGER)")
    
    # Save the file
    conn.commit()

def clanFromDBELO(clanList):
   ############################################################################################
   # Builds the clan members' data from the last update of the DB
   # Prevents starting from absolute scratch in case of data loss while program is running
   # Also allows changes to be made on a as-needed basis from the backend
   ############################################################################################

   for i in clanList:
        for char in i.memberChars:
            num = char['charNum']
            c.execute("SELECT * FROM ELO WHERE CharNum = ?", (num,))
            charData = c.fetchone()

            # Update char info
            char['games'] = charData[4]
            char['lastGame'] = charData[5]
            char['kills'] = charData[6]
            char['wins'] = charData[7]
            char['losses'] = charData[8]
            char['deaths'] = charData[9]
            char['KDR'] = charData[10]
            char['ELO'] = charData[11]
            
   return clanList       
    
def clanFromDBIB(clanList):
   ############################################################################################
   # Builds the clan members' data from the last update of the DB
   # Prevents starting from absolute scratch in case of data loss while program is running
   # Also allows changes to be made on a as-needed basis from the backend
   ############################################################################################

   for i in clanList:
        for char in i.memberChars:
            num = char['charNum']
            c.execute("SELECT * FROM IronBanner WHERE CharNum = ?", (num,))
            charData = c.fetchone()

            # Update char info
            char['games'] = charData[4]
            char['lastGame'] = charData[5]
            char['kills'] = charData[6]
            char['wins'] = charData[7]
            char['losses'] = charData[8]
            char['deaths'] = charData[9]
            char['KDR'] = charData[10]
            char['assists'] = charData[11]
            char['orbs'] = charData[12]
            char['objectives'] = charData[13]
            char['spree'] = charData[14]
            char['precisionKills'] = charData[15]

   return clanList       

def getRequestedInfo(char, statToGet):  
    ############################################################################################
    # Retreives one stat at a time from the database
    ############################################################################################ 
    
    c.execute("SELECT ? FROM ELO WHERE CharNum = ?", (statToGet, char))
    stat = c.fetchone()
    
    return stat   