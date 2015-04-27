## Which Youtube videos are the most popular?
/*
Use Case 1
Description: Find most popular youtube videos in domain
Actor: User
Precondition: Only looks for videos that players have tweeted since that is the only twitter data we currently have
Steps: Find the most tweeted video id and return its title and id
Actor action: Request to see most popular youtube vids
System Responses: Return single most popular youtube video
Post Condition: User will be given title and id of video
Alternate Path: 
Error: User input is incorrect
*/
SELECT y.id, y.title
FROM Youtube y
INNER JOIN()
SELECT videoID, count(*) AS count
FROM Tweet
GROUP BY videoID
ORDER BY count DESC
LIMIT 1) t
ON t.videoID = y.id;


## Which category ID's are most popular?
/*
Use Case 2
Description: See most popular category
Actor: User
Precondition: Videos must be in the baseball domain
Steps: List all category id's by most popular
Actor action: Rquest to see most popular video categories
System Responses: Return all category id's, most popular first
Post Condition: User is given a list of popular category id's
Alternate Path: 
Error: User input is incorrect
*/
SELECT categoryID, count(*) AS count
FROM Youtube y
GROUP BY categoryID
ORDER BY count DESC;

##Which tags have the most synonyms
/*
Use Case 3
Description: See which tags have the most synonyms
Actor: User
Precondition: Synonyms must be in the synonym table
Steps: get list of most popular synonym id's and then join it with the tag table
Actor action: Request to see most popular synonyms
System Responses: Return tags ordered by number of synonyms
Post Condition: User will be given tags with most synonyms
Alternate Path: 
Error: User input is incorrect
*/
SELECT t.tag_id
FROM Tags t
INNER JOIN (SELECT s.tag_id, s.syn_id, count(*) as count
	FROM Synonyms s
	GROUP BY s.syn_id
	ORDER BY count DESC) syns
ON t.tag_id=syns.tag_id;

## Which tags have the most misspellings?
/*
Use Case 4
Description: See which tags have the most misspellings
Actor: User
Precondition: Synonyms must be in the misspellings table
Steps: get list of most popular misspellings id's and then join it with the tag table
Actor action: Request to see most popular misspellings
System Responses: Return tags ordered by number of misspellings
Post Condition: User will be given tags with most misspellings
Alternate Path: 
Error: User input is incorrect
*/
SELECT t.tag_id
FROM Tags t
INNER JOIN (SELECT m.tag_id, m.misspelling_id, count(*) as count
	FROM Misspellings s
	GROUP BY m.misspelling_id
	ORDER BY count DESC) mis
ON t.tag_id=mis.tag_id;

## Which Twitter users post the most Youtube Videos related to your domain?
/*
Use Case 5
Description: See which users posts the most videos in our domain
Actor: User
Precondition: Only looks for videos that players have tweeted since that is the only twitter data we currently have
Steps: 
Actor action: Request to see who tweets the most videos
System Responses: Returns user who tweets the most videos
Post Condition: User will be given user name and all video ids that the user tweets
Alternate Path: 
Error: User input is incorrect
*/
SELECT t.user_id, t.vid_id
FROM Tweet t
INNER JOIN (SELECT tw.vid_id, count(*) as count, tw.user_id
	FROM Tweet tw
	GROUP BY tw.vid_id
	ORDER BY count DESC
	LIMIT 10) twv
ON twv.user_id=t.user_id
WHERE t.vid_id IS NOT NULL;
