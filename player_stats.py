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
get_batting = ("SELECT b.playerID, b.teamID, b.G, b.AB, b.R, b.H, b.2B, b.3B, b.HR, b.RBI, " 
			   "b.SB, b.CS, b.BB, b.SO, b.IBB, b.HBP, b.SH, b.SF, b.GIDP FROM Batting b "
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
get_pitching = ("SELECT playerID, W, L, G, GS, CG, SHO, SV, IPouts, H, ER, HR, BB, SO, BAOpp, "
	            "ERA, IBB, WP, HBP, R, SH, SF, GIDP FROM Pitching WHERE yearID = 2014")

# Execute SQL
cursor2.execute(get_pitching)

pitching_list = []

# Store data from cursor and convert to list for easier manipulation
for c in cursor2:
	pitching_list.append(list(c))



# Close connection to DB
cursor2.close()
cnx.close()

