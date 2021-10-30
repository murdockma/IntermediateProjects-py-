## Anlaysis homework using sqLite and Pandas

import numpy as np
import pandas as pd
import sqlite3
import os



import sqlite3


con = sqlite3.connect("lahmansbaseballdb.sqlite")


db_name = pd.read_sql("PRAGMA database_list;", con)["name"][0]



list_tables = "SELECT * FROM {}.sqlite_master WHERE type='table';".format(db_name)

lahmans = pd.read_sql(list_tables , con=con)

lahmans[0:50]




pd.read_sql_query('select max(yearid) from halloffame', con) 



my_sql_statement = '''SELECT * FROM halloffame 
                    LIMIT 5''' # your code here

pd.read_sql_query(my_sql_statement, con)

# - Various features of the data, such as the player inducted into hall of fame(playerID), the year they were voted into the hall of fame(yearID), and amount of votes they recieved from the baseeball writers association of america(votes, votedBy). Also shows total ballets, and # of votes needed to be inducted.  

list_from_table = '''SELECT * FROM people
                    LIMIT 5''' # your query here
pd.read_sql_query(list_from_table, con)



pd.read_sql_query('select * from allstarfull limit 5', con)



pd.read_sql_query('select distinct gameNum from allstarfull', con)



your_query = '''SELECT allstarfull.playerID, nameLast, nameFirst, gameID
                FROM allstarfull
                INNER JOIN people
                ON allstarfull.playerID = people.playerID'''
all_stars = pd.read_sql_query(your_query, con)
all_stars.head(25):

 
your_query = """SELECT * FROM people
                WHERE playerID = 'aaronha01'"""
rw = pd.read_sql_query(your_query, con)
rw

newe_quer = """SELECT name_user, modality_1, deathDay, bats 
               FROM people 
               INNER JOIN allstarfull ON people.playerID = allstarfull.playerID"""
 
# - Hank Aaron, regarded as one of the greatest players of all time. Played 23 seasons (and was in the all star game every season), broke several records and still holds some to this day. He was inducted into the hall of fame in his first year of eligibility and recieved 98.7 percent of ballots.



g = all_stars.groupby('playerID').size() # line 1
all_star_counts = g.reset_index() # line 2
all_star_counts = all_star_counts.rename(columns={0: "N_all_star_games"}) # line 3

all_star_counts

all_star_counts.sort_values(by = 'N_all_star_games', ascending=False)



hall = pd.read_sql_query('select  * from halloffame', con)
hall



hall.value_counts('playerID')



new_q = """SELECT * FROM 
            halloffame 
            WHERE playerID = 'roushed01'"""

new_ = pd.read_sql_query(new_q, con)
new_ 

hall['playerID'].value_counts()



hall[hall['playerID'] == "vanceda01"].count()

vanc_q = """SELECT * FROM 
            halloffame 
            WHERE playerID = 'vanceda01'"""

vance_ = pd.read_sql_query(vanc_q, con)
vance_ 


inducted_query = """SELECT * FROM halloffame
                    WHERE inducted='Y'"""
hall = pd.read_sql_query(inducted_query, con)
hall


merged = pd.merge(all_star_counts, hall, how='left', on='playerID')
all_stars_vs_hall = merged[['playerID', "N_all_star_games", "inducted"]]
all_stars_vs_hall = all_stars_vs_hall.fillna(value="N")

all_stars_vs_hall.sort_values(by='N_all_star_games', ascending=False)


missing_hall_of_famers = all_stars_vs_hall.sort_values(['inducted', 'N_all_star_games'], ascending = [True,False]).head(10)

missing_hall_of_famers



in_join = "SELECT nameFirst, nameLast, playerID FROM people"

names = pd.read_sql_query(in_join, con)

missing_w_names=pd.merge(missing_hall_of_famers, names, how='outer', on='playerID')

missing_w_names.head(5)
