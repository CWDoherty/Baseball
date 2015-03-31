import requests, bs4, re, mysql.connector, csv, time, tweepy

url = requests.get('http://www.baseball-reference.com/friv/baseball-player-twitter-accounts.shtml')
soup = bs4.BeautifulSoup(url.text)

p_list = soup.find_all(href=re.compile("/players/|/managers"))
t_list = soup.find_all(href=re.compile("https://twitter.com/#!/"))

player_user_id_dict = {}

for p in range(2, len(p_list)):
	player_user_id_dict[p_list[p].text] = t_list[p-2].text

# A function to convert team abbreviations
def convertTeams(x):
	if(x == 'NYN'):
		return 'NYM'
	elif(x == 'NYA'):
		return 'NYY'
	elif(x == 'SDN'):
		return 'SD'
	elif(x == 'TBA'):
		return 'TB'
	elif(x == 'CHA'):
		return 'CHW'
	elif(x == 'CHN'):
		return 'CHC'
	elif(x == 'LAN'):
		return 'LAD'
	elif(x == 'SFN'):
		return 'SF'
	elif(x == 'SLN'):
		return 'STL'
	elif(x == 'KCA'):
		return 'KC'
	else:
		return x


config = {
	'user': 'root',
	'password': 'isles40',
	'host': '127.0.0.1',
	'database': 'baseballdb',
}

playerList = []
team_abbrev_list = []

with open('baseball2.csv', 'rU') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		nameLast = row[3]
		nameFirst = row[4]
		full_name = nameFirst + " " + nameLast
		birthYear = row[0]
		birthMonth = row[1]
		birthDay = row[2]
		dob = birthYear + "-" + birthMonth + "-" + birthDay
		pos = row[7]
		height = row[5]
		weight = row[6]
		team_abbrev = convertTeams(row[8])

		if not team_abbrev in team_abbrev_list:
			team_abbrev_list.append(team_abbrev)

		name = player_user_id_dict.get(full_name, None)
		if name:
			player_user_id = name
		else:
			player_user_id = "NULL"

		playerList.append([full_name, dob, player_user_id,
						   team_abbrev, pos, height, weight])


cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

add_players = ("INSERT INTO Player "
			   "(full_name, dob, player_user_id, team_abbrev, pos, height, weight) "
			   "VALUES (%s, %s, %s, %s, %s, %s, %s)")
'''
for p in range(1, len(playerList)):
	cursor.execute(add_players, playerList[p])
	cnx.commit()
'''
cursor.close()
cnx.close()



teams = requests.get('http://mlb.mlb.com/team/')
team_soup = bs4.BeautifulSoup(teams.text)

al_teams = team_soup.find_all("ul", "al team")
nl_teams = team_soup.find_all("ul", "nl team")

al_splits = []
nl_splits = []

for a in al_teams:
	al_splits.append(a.text.split("\n", 6))

for n in nl_teams:
	nl_splits.append(n.text.split("\n", 6))

nl_team_names = []
nl_stadium_names = []
nl_stadium_addr = []
al_team_names = []
al_stadium_names= []
al_stadium_addr =[]
team_abbrev_list = sorted(team_abbrev_list) # sorts abbreviations

for n in nl_splits:
	nl_team_names.append(n[1])
	nl_stadium_names.append(n[2])
	address = n[3] + " " + n[4]
	nl_stadium_addr.append(address)

nl_team_names = sorted(nl_team_names)

for a in al_splits:
	al_team_names.append(a[1])
	al_stadium_names.append(a[2])
	address = a[3] + " " + a[4]
	al_stadium_addr.append(address)

al_team_names = sorted(al_team_names)


all_team_names = al_team_names + nl_team_names
all_team_names = sorted(all_team_names)

# put all team names and abbreviations in order, except for
# SF and SEA
names_and_abbrevs = zip(all_team_names, team_abbrev_list) 

# Swap SEA and SF
names_and_abbrevs_list = []

# Convert from tuples to lists
for n in names_and_abbrevs:
	a = n[0]
	b = n[1]

	names_and_abbrevs_list.append([a,b])

# Finally do the swap.
for n in names_and_abbrevs_list:
	if(n[1] == 'SEA'):
		n[1] = 'SF'
	elif(n[1] == 'SF'):
		n[1] = 'SEA'

all_al_info = zip(al_team_names, al_stadium_names, al_stadium_addr)
all_nl_info = zip(nl_team_names, nl_stadium_names, nl_stadium_addr)


team_twitter_list = ['@Rockies', '@whitesox', '@Phillies', '@Marlins', '@Indians',
					 '@Cardinals', '@Brewers', '@astros', '@SFGiants', '@Mariners',
					 '@BlueJays', '@Cubs', '@Rangers', '@Yankees', '@RedSox', 
					 '@RaysBaseball', '@Nationals', '@Twins', '@Angels', '@Orioles',
					 '@Mets', '@Pirates', '@Padres', '@Reds', '@DBacks', '@tigers',
					 '@Royals', '@Dodgers', '@Braves', '@Athletics']

nicknames = []

for t in all_team_names:
	split = t.split()
	if split[0] == 'Boston' or split[1] == 'White' or split[0] == 'Toronto':
		name = split[1] + " " + split[2]
		nicknames.append(name)
	else:
		nicknames.append(split[len(split) - 1])



nicknames = sorted(nicknames)
team = sorted(teams)
x = []

for a in all_nl_info:
	 x.append(list(a))

print type(x[0])

# Abbreviation, twitter handle, full name, stadium name, address, league, div
# all_team_info has name, stadium name and address in that order

def match_handle(team):
	team_name = team.replace(" ", "")
	for t in team_twitter_list:
		handle = t[1:] # removes @
		if t in team_name:
			return team

def division(team):
	if(team == "New York Mets" or team == "Philadelphia Phillies" or team == "Washington Nationals" or
		team == "Miami Marlins" or team == "New York Yankees" or team == "Toronto Blue Jays" or team == "Baltimore Orioles" or
		team == "Boston Red Sox" or team == "Tampa Bay Rays" or team == "Atlanta Braves"):
		return "East"
	elif(team == "Detroit Tigers" or team == "Kansas City Royals" or team == "Cleveland Indians" or team == "Chicago White Sox" or
		team == "Minnesota Twins" or team == "St. Louis Cardinals" or team == "Pittsburgh Pirates" or team == "Milwaukee Brewers" or
		team == "Cincinnati Reds" or team == "Chicago Cubs"):
		return "Central"
	else: 
		return "West"





