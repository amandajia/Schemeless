#!/usr/bin/python
import json
from collections import Counter
import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="root",  # your password
                     db="yelp_dataset")        # name of the data base
c = db.cursor()


# Create tables
print("Creating users table.")
c.execute('''create table users
         (user_id CHAR(22) primary key,
          name VARCHAR(80),
          review_count integer,
          yelping_since datetime,
          friends json DEFAULT NULL,
          useful integer,
          funny  integer,
          cool integer,
          fans integer,
          elite json DEFAULT NULL,
          average_stars decimal(3, 2),
          type VARCHAR(8))''')

# Insert json records into tables
print("Populating user table.")
f = open('yelp_academic_dataset_user.json')
count = 0
for line in f.readlines():
  user = json.loads(line)
  count = count + 1
  if(count % 1000 == 0):
      print count
  try:
    c.execute('''insert into users(user_id, name, review_count, yelping_since, friends, useful, funny, cool, fans, elite, average_stars, type)
                  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', [user['user_id'], user['name'].encode('utf-8'), user['review_count'], user['yelping_since'], json.dumps(user['friends']), user['useful'], user['funny'], user['cool'], user['fans'], json.dumps(user['elite']), user['average_stars'], user['type']])
  except :
    print user

print('done with user inserting')


db.commit()
print('done')
c.close()
