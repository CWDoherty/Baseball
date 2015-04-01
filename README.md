# Baseball Database Project 

Here is the code and other resources for our Baseball Database project

# Summary of Files:

###database_project.py
  >The main script for the project. Gets player names and twitter handles from baseball-reference then interacts with baseball2.csv to match up with only current players(players who have played within the last year). The player info is then inserted into the database. Team information is then grabbed from mlb.com and parsed and inserted into the database.
  
###baseball2.csv
  >A CSV file with information extracted from Lahman's Baseball Database. [Source.](http://www.seanlahman.com/baseball-archive/statistics/)
  
###player_handles.csv
  >A CSV file with all players matched to their twitter handles provided they have a twitter handle.
  
###twitter_player_handles.py
  >A script that interacts with the Twitter API and gets relevant account information for each player. The account information is then placed into the database.
  
###baseballdb.sql
  >The database that hold our twitter, baseball player and baseball team data. So far only the Player and Team tables have been filled and the account table is incomplete.

###lahman.sql
  >Lahman's baseball database which is a source of most of our player data.

###player_stats.py
  >A script that query's Lahman's database to pull player stats from the database. Will be updated to manipulate data and insert into our database, baseballdb.sql.
