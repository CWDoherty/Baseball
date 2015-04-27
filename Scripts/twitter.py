import tweepy, mysql.connector,time
from datetime import datetime


## OAUTH stuff
auth = tweepy.OAuthHandler('DYOf9uKggRwU2ujTgKePQkX1h',
					       '7zb2cr6RDKn8nAokjvKKppezmTBr4YkyxYYL0hwGtGzeLFlMil')
auth.set_access_token('2973788795-LUhLdoi0ipAh1cm8rR0KTow9oUb4KNto5EtIiGy',
	                  'ybnm2qZGRBKggHqnteiedFo5H3W6QG9EhReeL48MFjWaq')

## create tweepy api object
api = tweepy.API(auth)

config = {
	'user': 'root',
	'password': 'isles40',
	'host': '127.0.0.1',
	'database': 'baseballdb'
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered=True)

getPlayerIDs = ("SELECT p.player_user_id FROM Player p WHERE NOT p.player_user_id = 'NULL'");


cursor.execute(getPlayerIDs);


def has_hashtags(x):
	return "#" in x

def monthNo(x):
	if(x == 'Jan'):
		return '01'
	elif(x == 'Feb'):
		return '02'
	elif(x == 'Mar'):
		return '03'
	elif(x == 'Apr'):
		return '04'
	elif(x == 'May'):
		return '05'
	elif(x == 'Jun'):
		return '06'
	elif(x == 'Jul'):
		return '07'
	elif(x == 'Aug'):
		return '08'
	elif(x == 'Sep'):
		return '09'
	elif(x == 'Oct'):
		return '10'
	elif(x == 'Nov'):
		return '11'
	else:
		return '12'


t = None
z = None
fields = []
for c in cursor:
	print c
	s = "".join(c)
	s = s.replace("@", "")
	try:
		timeline = api.user_timeline(s)
		for t in timeline:
			message = t._json['text'].encode('utf8')
			hastags = str(has_hashtags(message))
			if not hastags:
				hastags = '0'
			else:
				hastags = '1'
			tweet_id = str(t._json['id'])
			favorites = str(t._json['favorite_count'])
			timestamp = t._json['created_at'].encode('utf8')
			year =  timestamp[-4:]
			month = timestamp[4:7]
			month = monthNo(month)
			day = timestamp[8:10]
			timeod = timestamp[11:19]
			timestamp = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(timeod)
			timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
			print timestamp, type(timestamp)
			retweets = str(t._json['retweet_count'])
			is_retweet = str(t._json['retweeted'])
			if is_retweet:
				is_retweet = '1'
			else:
				is_retweet = '0'
			query_list = [message, "@" + s, tweet_id, favorites, retweets, is_retweet, hastags, timestamp]
			print query_list
			fields.append(query_list)
	except tweepy.error.TweepError:
		print s,  "Does not exist"
	time.sleep(5)  


insert = ("INSERT INTO Tweet"
   "(message, user_id, tweet_id, favorites, retweets, is_retweet, has_hashtags, time_tweeted)"
   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

for f in range(len(fields)):
	cursor.execute(insert, fields[f])
	cnx.commit()


cursor.close()
cnx.close()




