import mysql.connector, re

config = {
	'user': 'root',
	'password': 'isles40',
	'host': '127.0.0.1',
	'database': 'baseballdb'
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered=True)

tweets = ("SELECT message, tweet_id FROM Tweet")

cursor.execute(tweets)

tweet_list = []
count = 0
for c in cursor:
	if '@' in c[0]: 
		tweet_list.append(c)


find_mentions = re.compile("\S*@(?:\S+)")

all_mentions = []
for t in tweet_list:
	mentions = re.findall(find_mentions, t[0])
	if(len(mentions) > 0):
		all_mentions.append([mentions, t[1]])


insert = ("INSERT INTO User_Mentions (user_id, tweet_id) VALUES (%s, %s)")

query = []
for a in all_mentions:
	for x in a[0]:
		temp = [x, a[1]]
		query.append(temp)

print query


for x in range(len(query)):
	try:
		cursor.execute(insert, query[x])
		cnx.commit()
	except:
		continue

cursor.close()
cnx.close()