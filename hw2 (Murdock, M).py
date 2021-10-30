#!/usr/bin/env python
# coding: utf-8

# ## HW2
# ### INFO 3401

# In[1]:


import numpy as np
import pandas as pd
import sqlite3
import os


# ## Getting started

# Download the [Lahman's baseball database](http://www.seanlahman.com/baseball-archive/statistics/) from Canvas. 
# - You will need to unzip the file and include it in the same directory as your notebook. 
# - You will have to name your unzipped file `lahmansbaseballdb.sqlite` 
# - If you are not quite sure what to do for this step, please consult the section on the file system in the INFO Paratechnical Handbook which has additional information. Then please post to Canvas for help!
# - Note the database is current only to 2018. 

# In[2]:


# here is how you connect to the Lahman database and 
# describe its tables

import sqlite3

 # pass a string pointing to the .sqlite file on your machine
con = sqlite3.connect("lahmansbaseballdb.sqlite")

# get the db name
db_name = pd.read_sql("PRAGMA database_list;", con)["name"][0]


# In[3]:


# Let's list the first five tables in the database

list_tables = "SELECT * FROM {}.sqlite_master WHERE type='table';".format(db_name)

lahmans = pd.read_sql(list_tables , con=con)

lahmans[0:50]


# In[4]:


# data is only current to 2018! This is important as you draw
# conclusions from the data
pd.read_sql_query('select max(yearid) from halloffame', con) 


# ## Deliverable 1

# The database contains a table called "halloffame". Use a SELECT statement to print out the first five records of the halloffame table. Use a [limit clause](https://www.sqlitetutorial.net/sqlite-limit/) to only select the first five rows of the table. Note that you will need to use the pandas `read_sql_query` method which takes a connection arguments stored in the variable `con`. 

# In[5]:


my_sql_statement = '''SELECT * FROM halloffame 
                    LIMIT 5''' # your code here

pd.read_sql_query(my_sql_statement, con)


# ## Deliverable 2

# What are the fields in the hall of fame table? What do you think they represent?
# 
# - Various features of the data, such as the player inducted into hall of fame(playerID), the year they were voted into the hall of fame(yearID), and amount of votes they recieved from the baseeball writers association of america(votes, votedBy). Also shows total ballets, and # of votes needed to be inducted.  

# ## Deliverable 3

# The `halloffame` table includes a field called `playerid`. Often when you have an `id` field in a database it links to another table in the db. Often working with a database means using SQL to explore and learn the structure of the db. Use the `lahmans` dataframe from above to list the tables in the basebaseball database. Try to discover which table might contain a `playerid` field as a primary key. Then fill out the cell below to select the first five rows from the table. 

# In[6]:


## the table people has a player_id as its unique id

list_from_table = '''SELECT * FROM people
                    LIMIT 5''' # your query here
pd.read_sql_query(list_from_table, con)


# ## Deliverable 4
# 
# Looking again at the tables in the notebook, notice that there is an `allstarfull` table. Let's look at that table.

# In[7]:


pd.read_sql_query('select * from allstarfull limit 5', con)


# Looking at the `halloffame` table and the `allstarfull` table we can start to form a question. 
# 
# Are there players that were often all stars but who were not elected to the hall of fame? Maybe these are **forgotten stars**! They should have made it to the hall of fame, but they were robbed! 
# 
# Notice that this question emerges from the process of exploring the data. This is a very common pattern.
# 
# To investigate the question, we need to find out how many all star games each player played in. This will require joins and aggregation. 
# 
# But before we are ready to proceed, we need to understand the data a little better. It is **very** common and **very** important to take time to understand data before drawing conclusions. In this case, it seems like the all_star table has a `gameNum` field.

# What does that field represent? To investivate you will need to check the documentation or field list for the database in the [readme](http://www.seanlahman.com/files/database/readme2017.txt). Learning how to read and make sense of documentation (including data documentation) is an important skill. 
# 
# Another useful way to understand what information is represented in a database is to run SQL queries, such as the one below.

# In[8]:


pd.read_sql_query('select distinct gameNum from allstarfull', con)


# Based on your investigation, what does `gameNum` describe in the `allstarfull` table?
# 
# - of all star games played in the season (0 means only 1 game played that season).

# ## Deliverable 5
# 
# - To start to answer our question, create dataframe called all_stars 
# - To create the dataframe, use SQL to join allstarfull with the people table on playerId
# - Select the following fields: 
#     - 'allstarfull.playerID', 'nameLast', 'nameFirst', 'gameID'
#     - 'allstarfull.playerID' specifies that you are taking the playerID field from the `allstarfull` table

# In[9]:


your_query = '''SELECT allstarfull.playerID, nameLast, nameFirst, gameID
                FROM allstarfull
                INNER JOIN people
                ON allstarfull.playerID = people.playerID'''
all_stars = pd.read_sql_query(your_query, con)
all_stars.head(25)


# ## Deliverable 6
# 
# Pause to check and consider your results. The dataframe `all_stars` says the player aaronha01 played in all star games. Is that right? Well who is `aaronha01`? Use code to check your intuitions about this data by querying the `people` table to learn more about `aaronha01`. Answer by writing a select statement with a where clause.

# In[10]:


# delete me answer
your_query = """SELECT * FROM people
                WHERE playerID = 'aaronha01'"""
rw = pd.read_sql_query(your_query, con)
rw

newe_quer = """SELECT name_user, modality_1, deathDay, bats 
               FROM people 
               INNER JOIN allstarfull ON people.playerID = allstarfull.playerID"""


# ## Deliverable 7 
# 
# Look up the player associated with the ID `aaronha01` on Wikipedia.  Who is aaronha01?
# 
# 
# - Hank Aaron, regarded as one of the greatest players of all time. Played 23 seasons (and was in the all star game every season), broke several records and still holds some to this day. He was inducted into the hall of fame in his first year of eligibility and recieved 98.7 percent of ballots.

# ## Deliverable 8
# 
# Look at the next cell of code and describe what the three lines of code are doing. You may need to consult the pandas documentation.

# - Line 1. Grouping by the number of times a players ID shows up
# - Line 2. Resseting the indexing of our dataframe, so it starts at 0
# - Line 3. Renaming the column('0') with 'N_all_star_games'. Improves readability across users.

# In[11]:


g = all_stars.groupby('playerID').size() # line 1
all_star_counts = g.reset_index() # line 2
all_star_counts = all_star_counts.rename(columns={0: "N_all_star_games"}) # line 3

all_star_counts


# ## Deliverable 9

# Sort `all_star_counts` on the field `N_all_star_games` (higher number of `N_all_star_games` should come first). Which players played in the most all star games? (You may need to join on the people table to get full names).

# - Hank Aaron and Willie Mays

# In[12]:


all_star_counts.sort_values(by = 'N_all_star_games', ascending=False)


# ## Merging hall of fame data
# 
# Now let's look at data from the hall of fame table. Eventually, we will want to join the hall of fame table with the allstarfull table. But for now let's just take a look.

# In[13]:


hall = pd.read_sql_query('select  * from halloffame', con)
hall


# ## Deliverable 10
# 
# Is each player listed one time in the halloffame table? You will need to investigate the dataframe with pandas (Hint: use `value_counts`).

# - No, some players are listed up to 20 times

# In[14]:


hall.value_counts('playerID')


# In[15]:


new_q = """SELECT * FROM 
            halloffame 
            WHERE playerID = 'roushed01'"""

new_ = pd.read_sql_query(new_q, con)
new_ 

# we can see roushed was voted for multiple times before he was inducted (20 times)


# ## Deliverable 11
# 
# How many times is the player `vanceda01` listed in the `halloffame` table? Why do you think that is? (Hint: look at the "inducted" field in the database documentation). Answer with code using the cell below. Note that a baseball player may be voted to be included in the hall of fame multiple times before they are accepted.

# - 17 times, recieved his first vote in 1936 but wasn't inducted until 1955. He was voted to be inducted into the hall of fame 16 times before he actually was inducted (meaning he didn't recieve enough votes 16 of the times)

# In[16]:


hall['playerID'].value_counts()


# In[17]:


hall[hall['playerID'] == "vanceda01"].count()


# In[18]:


vanc_q = """SELECT * FROM 
            halloffame 
            WHERE playerID = 'vanceda01'"""

vance_ = pd.read_sql_query(vanc_q, con)
vance_ 


# Adjust the `hall_sql_query` to include a where clause to only select rows from the `halloffame` table where inducted is "Y". Store your answer in the variable `inducted_query` below. The next cell should create a dataframe called `hall`. 

# In[19]:


inducted_query = """SELECT * FROM halloffame
                    WHERE inducted='Y'"""
hall = pd.read_sql_query(inducted_query, con)
hall


# Now let's merge the `hall` dataframe with the `all_star_counts` dataframe. 

# In[20]:



# I will use pandas to do the join. You could also do this in SQL. The API is similar. 
merged = pd.merge(all_star_counts, hall, how='left', on='playerID')
all_stars_vs_hall = merged[['playerID', "N_all_star_games", "inducted"]]
all_stars_vs_hall = all_stars_vs_hall.fillna(value="N")


# ## Deliverable 12
# Sort the `all_stars_vs_hall` table by `N_all_star_games` in descending order.

# In[21]:


all_stars_vs_hall.sort_values(by='N_all_star_games', ascending=False)


# ## Deliverable 13
# 
# Make a table `missing_hall_of_famers` that shows the 10 players who played in the most all star games who were none the less NOT inducted into the hall of fame. You can filter the `all_stars_vs_hall` table for this, and call the `.head()` method on the filtered dataframe.

# In[22]:


missing_hall_of_famers = all_stars_vs_hall.sort_values(['inducted', 'N_all_star_games'], ascending = [True,False]).head(10)

missing_hall_of_famers


# ## Deliverable 14
# 
# Who are the players in your `missing_hall_of_famers` table? Try looking up a few of the players online (e.g. Wikipedia). Does your table make sense? Note: you may need to join the people table to see the players' full names. 

# In[26]:


in_join = "SELECT nameFirst, nameLast, playerID FROM people"

names = pd.read_sql_query(in_join, con)

missing_w_names=pd.merge(missing_hall_of_famers, names, how='outer', on='playerID')

missing_w_names.head(5)


# - yes it makes sense, these players have been accused of some sort of incident (ex. Rose was found guilty of betting on games as a player and manager, Bonds was accused of using performance enhancing drugs, etc.) that has placed them on the permanently ineligible list, meaning they cant be inducted into the hall of fame.
