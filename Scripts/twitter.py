import tweepy, mysql.connector, time


## OAUTH stuff
auth = tweepy.OAuthHandler('DYOf9uKggRwU2ujTgKePQkX1h',
					       '7zb2cr6RDKn8nAokjvKKppezmTBr4YkyxYYL0hwGtGzeLFlMil')
auth.set_access_token('2973788795-LUhLdoi0ipAh1cm8rR0KTow9oUb4KNto5EtIiGy',
	                  'ybnm2qZGRBKggHqnteiedFo5H3W6QG9EhReeL48MFjWaq')

## create tweepy api object
api = tweepy.API(auth)

