import xml.etree.cElementTree as ET
import pprint
import re
import csv
import codecs
import sqlite3
from collections import defaultdict
import cerberus
import schema
import os

#Create and connect to database

db = sqlite3.connect("map.db")
cur = db.cursor()

#Create tables

#Create Nodes
#Checking if the table exists and dropping it if it does, then create the table. 
cur.execute("DROP TABLE IF EXISTS nodes;")
db.commit()
cur.execute("CREATE TABLE nodes (id INTEGER PRIMARY KEY NOT NULL,lat REAL,lon REAL,user TEXT,uid INTEGER,version INTEGER,changeset INTEGER,timestamp TEXT);")
db.commit()

#Read the csv file
with open('nodes.csv','rb') as f: 
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode("utf-8"),i['lat'].decode("utf-8"),i['lon'].decode("utf-8"),i['user'].decode("utf-8"),i['uid'].decode("utf-8"),i['version'].decode("utf-8"),i['changeset'].decode("utf-8"),i['timestamp'].decode("utf-8")) for i in dr]

#Insert the data into the table
cur.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?,?,?,?,?,?,?,?);", to_db)
db.commit()

#Create Nodes_Tags
cur.execute("DROP TABLE IF EXISTS nodes_tags;")
db.commit()

cur.execute("CREATE TABLE nodes_tags (id INTEGER, key TEXT, value TEXT, type TEXT, FOREIGN KEY (id) REFERENCES nodes(id))")
db.commit()

with open('nodes_tags.csv', 'rb') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode("utf-8"),i['key'].decode("utf-8"),i['value'].decode("utf-8"),i['type'].decode("utf-8")) for i in dr]

cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?,?,?,?);", to_db)
db.commit()

#Create Ways
cur.execute("DROP TABLE IF EXISTS ways;")
db.commit()

cur.execute("CREATE TABLE ways(id INTEGER PRIMARY KEY NOT NULL,user TEXT,uid INTEGER,version TEXT,changeset INTEGER,timestamp TEXT);")
db.commit()

with open('ways.csv','rb') as f: 
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode("utf-8"),i['user'].decode("utf-8"),i['uid'].decode("utf-8"),i['version'].decode("utf-8"),i['changeset'].decode("utf-8"),i['timestamp'].decode("utf-8")) for i in dr]

cur.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?,?,?,?,?,?);", to_db)
db.commit()

#Create Ways_Nodes
cur.execute("DROP TABLE IF EXISTS ways_nodes;")
db.commit()

cur.execute("CREATE TABLE ways_nodes (id INTEGER NOT NULL,node_id INTEGER NOT NULL,position INTEGER NOT NULL,FOREIGN KEY (id) REFERENCES ways(id),FOREIGN KEY (node_id) REFERENCES nodes(id));")
db.commit()

with open('ways_nodes.csv','rb') as f: 
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode("utf-8"),i['node_id'].decode("utf-8"),i['position'].decode("utf-8")) for i in dr]

cur.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?,?,?);", to_db)
db.commit()

#Create Ways_Tags
cur.execute("DROP TABLE IF EXISTS ways_tags;");
db.commit()

cur.execute("CREATE TABLE ways_tags (id INTEGER NOT NULL,key TEXT NOT NULL,value TEXT NOT NULL,type TEXT,FOREIGN KEY (id) REFERENCES ways(id));")
db.commit()

with open('ways_tags.csv','rb') as f: 
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode("utf-8"),i['key'].decode("utf-8"),i['value'].decode("utf-8"),i['type'].decode("utf-8")) for i in dr]

cur.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?,?,?,?);", to_db)
db.commit()
