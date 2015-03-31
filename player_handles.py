import requests, bs4, re, mysql.connector

url = requests.get('http://www.baseball-reference.com/friv/baseball-player-twitter-accounts.shtml')
soup = bs4.BeautifulSoup(url.text)

p_list = soup.find_all(href=re.compile("/players/|/managers"))
t_list = soup.find_all(href=re.compile("https://twitter.com/#!/"))

player_user_id = {}
player_tuple = []


for p in range(2, len(p_list)):
	#starting at 2 because first 2 links are from top of page.
	#use p-2 in t_list to compensate for difference
	player_user_id[p_list[p].text] = t_list[p-2].text
	player_tuple.append(p_list[p].text)
	player_tuple.append(t_list[p-2].text)

#for keys, values in player_user_id.items():
	#print (keys), ",", (values)


config = {
	'user': 'root',
	'password': 'isles40',
	'host': '127.0.0.1',
	'database': 'baseballdb',
}


cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

test = ['player 1','2000-01-01', '@twitterhandle', 'ABC', 'P', 123, 123]

add_players = ("INSERT INTO Player "
			   "(full_name, dob, player_user_id, team_abbrev, pos, height, weight) "
			   "VALUES (%s, %s, %s, %s, %s, %s, %s)")
				

cursor.execute(add_players, test)
cnx.commit()
cursor.close()
cnx.close()
