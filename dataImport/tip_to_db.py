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
print("Creating tips table.")
c.execute('''create table tips
         (user_id CHAR(22),
          business_id CHAR(22),
          date datetime,
          likes integer,
          text VARCHAR(1000),
          type VARCHAR(8))''')

# Insert json records into tables
print("Populating tips table.")
f = open('yelp_academic_dataset_tip.json')
count = 0
for line in f.readlines():
  tip = json.loads(line)
  count = count + 1
  if (count % 1000 == 0):
      print count
  try:
    c.execute('''insert into tips(user_id, business_id, date, likes, text, type)
                  VALUES(%s,%s,%s,%s,%s,%s)''', [tip['user_id'], tip['business_id'], tip['date'], tip['likes'], tip['text'].encode('utf-8'), tip['type']])
  except :
    print tip

print('done with tip inserting')


db.commit()
print('done')
c.close()
