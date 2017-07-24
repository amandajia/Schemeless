#!/usr/bin/python
import json
from collections import Counter
import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="Aj19881122",  # your password
                     db="yelp_dataset")        # name of the data base
c = db.cursor()

# Create tables
print("Creating businesses table.")
c.execute('''create table businesses
         (business_id VARCHAR(25) primary key,
          name CHAR(80) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
          address VARCHAR(140),
          city VARCHAR(50),
          state VARCHAR(4),
          latitude double,
          longitude double, 
          stars decimal(2,1),
          review_count integer,
          is_open boolean,
          neighborhood VARCHAR(80),
          postal_code VARCHAR(8),
          categories json DEFAULT NULL,
          attributes json DEFAULT NULL,
          type VARCHAR(8))''')

# Insert json records into tables
print("Populating businesses, neighborhoods, and categories table.")
f = open('yelp_academic_dataset_business.json')
for line in f.readlines():
  business = json.loads(line)
  try:
    c.execute('''insert into businesses(business_id, name, address, city, state, latitude, longitude, stars, review_count, is_open, neighborhood, postal_code, categories, attributes, type)
                  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', [business['business_id'], business['name'].encode('utf-8'), business['address'].encode('utf-8'), business['city'], business['state'], business['latitude'], business['longitude'], business['stars'], business['review_count'], business['is_open'], business['neighborhood'].encode('utf-8'), business['postal_code'], json.dumps(business['categories']), json.dumps(business['attributes']), business['type']])
  except :
    print business

print('done with business inserting')


db.commit()
print('done')
c.close()