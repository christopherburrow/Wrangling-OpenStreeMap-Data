#Queries

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

#File sizes
print 'map.osm', '.....', (os.path.getsize("map.osm")/(1024*1024)), 'MB'
print 'sample.osm', '.....', (os.path.getsize("sample.osm")/(1024*1024)), 'MB'
print 'map.db', '.....', (os.path.getsize("map.db")/(1024*1024)), 'MB'
print 'nodes.csv', '.....', (os.path.getsize("nodes.csv")/(1024*1024)), 'MB'
print 'nodes_tags.csv', '.....', (os.path.getsize("nodes_tags.csv")/(1024*1024)), 'MB'
print 'ways.csv', '.....', (os.path.getsize("ways.csv")/(1024*1024)), 'MB'
print 'ways_tags.csv', '.....', (os.path.getsize("ways_tags.csv")/(1024*1024)), 'MB'
print 'ways_nodes.csv', '.....', (os.path.getsize("ways_nodes.csv")/(1024*1024)), 'MB'

#Number of nodes
query = cur.execute('SELECT COUNT(*) FROM nodes')
print query.fetchall()

#Number of ways
query = cur.execute('SELECT COUNT(*) FROM ways')
print query.fetchall()

#Types of nodes
query = cur.execute('SELECT type , count(*) as num  FROM nodes_tags group by type order by num desc;')
pprint.pprint(query.fetchall())

#Number of Unique Users
query = cur.execute('SELECT COUNT(distinct(uid)) FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways)')
pprint.pprint(query.fetchone())

#User with the most submissions
query = cur.execute('SELECT e.user, COUNT(*) AS num FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) AS e GROUP BY user ORDER BY num DESC LIMIT 1;')
pprint.pprint(query.fetchall())

#Religious Locations
query= cur.execute("SELECT value, COUNT(*) AS num FROM (SELECT key,value FROM nodes_tags UNION ALL SELECT key,value FROM ways_tags) AS e WHERE key='religion' GROUP BY value ORDER BY num DESC;")
pprint.pprint(cur.fetchall())

#Resturaunts
query=cur.execute("SELECT value, COUNT(*) AS num FROM (SELECT key,value FROM nodes_tags UNION ALL SELECT key,value FROM ways_tags) AS e WHERE e.key LIKE '%cuisine%' GROUP BY value ORDER BY num desc;")
pprint.pprint(cur.fetchall())

#Types of Amenities
query=cur.execute("SELECT value, COUNT(*) AS num FROM nodes_tags WHERE key='amenity' GROUP BY value ORDER BY num DESC;")
pprint.pprint(cur.fetchall())