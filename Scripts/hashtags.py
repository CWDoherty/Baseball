'''
Copyright (c) 2015 Chris Doherty, Oliver Nabavian
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import mysql.connector, re

config = {
	'user': 'root',
	'password': 'isles40',
	'host': '127.0.0.1',
	'database': 'baseballdb'
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered=True)

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
		# Duplicate entries will not make it into the database
		continue

cursor.close()
cnx.close()


