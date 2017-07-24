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
print("Creating reviews table.")
c.execute('''create table reviews
         (review_id CHAR(22) primary key,
          user_id CHAR(22),
          business_id CHAR(22),
          stars integer,
          date datetime,
          text text,
          useful integer,
          funny  integer,
          cool integer,
          type VARCHAR(8))''')

# Insert json records into tables
print("Populating review table.")
f = open('yelp_academic_dataset_review.json')
for line in f.readlines():
  review = json.loads(line)
  try:
    c.execute('''insert into reviews(review_id, user_id, business_id, stars, date, text, useful, funny, cool, type)
                  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', [review['review_id'], review['user_id'], review['business_id'], review['stars'], review['date'], review['text'].encode('utf-8'), review['useful'], review['funny'], review['cool'], review['type']])
  except :
    print review

print('done with review inserting')


db.commit()
print('done')
c.close()
