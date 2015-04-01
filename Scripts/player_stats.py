import mysql.connector
# Script to get player stats and import them into our database.


# Configuration info to access database.
config = {
	'user': 'root',
	'password': 'isles40',
	'host': '127.0.0.1',
	'database': 'baseball'
}

# Connect to database
cnx = mysql.connector.connect(**config)
cursor1 = cnx.cursor(buffered=True)

# SQL query to get batting information for all players in 2014
# Gets batting information as well as Name and Birthday information for matching in our database
get_batting = ("SELECT b.playerID, b.teamID, b.G, b.AB, b.R, b.H, b.2B, b.3B, b.HR, b.RBI, " 
			   "b.SB, b.CS, b.BB, b.SO, b.IBB, b.HBP, b.SH, b.SF, b.GIDP, m.nameLast, m.nameFirst, "
			   "m.birthYear, m.birthMonth, m.birthDay FROM (Batting b JOIN Master m ON m.playerID = b.playerID) "
			   "WHERE b.yearID = 2014")

# Execute SQL 
cursor1.execute(get_batting)

batting_list = []

# Store cursor data in list and convert tuples to lists.
for c in cursor1:
	batting_list.append(list(c))

# Close connection to DB
cursor1.close()
cnx.close()

# Connect to database
cnx = mysql.connector.connect(**config)
cursor2 = cnx.cursor(buffered=True)

# SQL query to get pitching info
# Gets pitching info as well as Name and Birthday info for matching in our DB
get_pitching = ("SELECT p.playerID, p.W, p.L, p.G, p.GS, p.CG, p.SHO, p.SV, p.IPouts, "
			    "p.H, p.ER, p.HR, p.BB, p.SO, p.BAOpp, p.ERA, p.IBB, p.WP, p.HBP, p.R, "
			    "p.SH, p.SF, p.GIDP, m.nameLast, m.nameFirst, m.birthYear, m.birthMonth, "
			    "m.birthDay FROM (Pitching p JOIN Master m ON m.playerID=p.playerID) "
			    " WHERE yearID = 2014")

# Execute SQL
cursor2.execute(get_pitching)

pitching_list = []

# Store data from cursor and convert to list for easier manipulation
for c in cursor2:
	pitching_list.append(list(c))


# Close connection to DB
cursor2.close()
cnx.close()


''' Insert Data into DB '''

# format data to enter into DB
player_batting_list = []
for b in batting_list:
	dob = str(b[21]) + "-" + str(b[22]) + "-" + str(b[23]) # indexes of relevant items
	full_name = b[20] + " " + b[19]
	temp = []
	for field in range(2,len(b) - 5):
		temp.append(b[field])
	temp.append(full_name)
	temp.append(dob)
	player_batting_list.append(temp)


player_pitching_list = []
for p in pitching_list:
	dob = str(p[25]) + "-" + str(p[26]) + "-" +str(p[27])
	full_name = p[24] + " " + p[23]
	temp = []
	for field in range(1, len(p) - 5):
		temp.append(p[field])
	temp.append(full_name)
	temp.append(dob)
	player_pitching_list.append(temp)

'''
total_batting_list = []
# combine players that played for multiple teams into one entry
for i in range(len(player_batting_list)):
	current = player_batting_list[i]
	name = current[17]
	dob = current[18]
	dup = False

	for j in range(i, len(player_batting_list)):
		if (name in player_batting_list[j]) and (dob in player_batting_list[j]):
			dup = True
			extra = player_batting_list[j]
			G = current[0] + extra[0]
			AB = current[1] + extra[1]
			R = current[2] + extra[2]
			H = current[3] + extra[3]
			dubs = current[4] + extra[4]
			trip = current[5] + extra[5]
			HR = current[6] + extra[6]
			RBI = current[7] + extra[7]
			SB = current[8] + extra[8]
			CS = current[9] + extra[9]
			BB = current[10] + extra[10]
			SO = current[11] + extra[11]
			IBB = current[12] + extra[12]
			HBP = current[13] + extra[13]
			SH = current[14] + extra[14]
			SF = current[15] + extra[15]
			GIDP = current[16] + extra[16]
			l = [G, AB, R, H, dubs, trip, HR, RBI, SB, CS, BB, SO, IBB, HBP, SH, SF, GIDP]
			l.append(name)
			l.append(dob)
			total_batting_list.append(l)

	if not dup:
		total_batting_list.append(current)
'''

# Config info to connect with our DB
config = {
	'user': 'root',
	'password': 'isles40',
	'host': '127.0.0.1',
	'database': 'baseballdb'
}

# Open connection with DB
cnx2 = mysql.connector.connect(**config)
cursor2 = cnx2.cursor(buffered=True)

import_batting = ("INSERT INTO BATTING "
				  "(G, AB, R, H, 2B, 3B, HR, RBI, SB, CS, BB, SO, IBB, HBP, SH,"
				  "SF, GIDP, full_name, dob)"
				  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
				  "%s, %s, %s, %s, %s)")

for p in range(len(player_batting_list)):
	cursor2.execute(import_batting, player_batting_list[p])
	cnx2.commit() 

cursor2.close()
cnx2.close()


import_pitching = ("INSERT INTO Pitching "
				   "(W, L, G, GS, CG, SHO, SV, IPouts, H, ER, HR, BB, SO, BAOpp, "
				   "ERA, IBB, WP, HBP, R, SH, SF, GIDP, full_name, dob)"
				   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
				   "%s,%s,%s,%s,%s,%s,%s)")

cnx3 = mysql.connector.connect(**config)
cursor3 = cnx3.cursor(buffered=True)
for p in range(len(player_pitching_list)):
	cursor3.execute(import_pitching, player_pitching_list[p])
	cnx3.commit()

cursor3.close()
cnx3.close()













