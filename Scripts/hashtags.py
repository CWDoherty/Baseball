import mysql.connector, re

config = {
	'user': 'root',
	'password': 'isles40',
	'host': '127.0.0.1',
	'database': 'baseballdb'
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered=True)

def user_mentions(message):
	return "@" in message


tweets = ("SELECT message, user_id, tweet_id FROM Tweet")

cursor.execute(tweets)

tweet_list = []
count = 0
for c in cursor:
	if '#' in c[0]: 
		tweet_list.append(c)


find_tags = re.compile("\S*#(?:\S+)")

all_tag = []
for t in tweet_list:
	tags = re.findall(find_tags, t[0])
	if(len(tags) > 0):
		all_tag.append([tags, t[1], t[2]])


insert = ("INSERT INTO Hashtag(tag, user_id, tweet_id) VALUES (%s, %s, %s)")

query = []
for a in all_tag:
	for x in a[0]:
		temp = [x, a[1], a[2]]
		query.append(temp)

print query


for x in range(len(query)):
	try:
		cursor.execute(insert, query[x])
		cnx.commit()
	except:
		print "duplicate"
cursor.close()
cnx.close()


