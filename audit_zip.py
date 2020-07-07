#Auditing zip codes and correcting errors, this is an alteration of the case study script for auditing street names. 
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

zip_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
zip_types = defaultdict(set)
expected = []

def audit_zip_code(zip_types, zip_name):
    m = zip_type_re.search(zip_name)
    if m:
        zip_type = m.group()
        if zip_type not in expected:
            zip_types[zip_type].add(zip_name)

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s:s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v)

def is_zip_code(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_zip():
    with open ('map.osm', 'r') as mapfile:
        for event, elem in ET.iterparse(mapfile, events=("start", )):
            if elem.tag == "way" or elem.tag == "node":
                for tag in elem.iter("tag"):
                    if is_zip_code(tag):
                        audit_zip_code(zip_types, tag.attrib['v'])
        return zip_types
        
def update_zipcode(zipcode): 
    if len(str(zipcode))<5:
        zipcode = 0
    return zipcode

with open ('map.osm', 'r') as mapfile:
    s_types = audit_zip()
    
    for s_type, ways in s_types.iteritems():
        for name in ways:
            correct_name = update_zipcode(name)
            print name, "->", correct_name