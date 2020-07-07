#Auditing street Names and correcting any issues. Used in Case Study
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

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons","Freeway","Circle","Strand","Sterling","Way","Highway",
            "Terrace","South","East","West","North", "Cove"]

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s:s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit():
    with open ('map.osm', 'r') as mapfile:
        street_types = defaultdict(set)
        for event, elem in ET.iterparse(mapfile, events=("start", )):
            if elem.tag == "way" or elem.tag == "node":
                for tag in elem.iter("tag"):
                    if is_street_name(tag):
                        audit_street_type(street_types, tag.attrib['v'])
        return street_types
        
audit()

#Correcting Street Types

mapping = {
            " St ": " Street ",
            " St.": " Street ",
            " Rd.": " Road ",
            " Rd ": " Road ",
            " Rd": " Road ",
            " Ave ": " Avenue ", 
            " Ave.": " Avenue ",
            " Av ": " Avenue ",
            " Ave" : " Avenue ",
            " Dr ": " Drive ",
            " Dr.": " Drive",
            " Blvd ": " Boulevard ",
            " Blvd": " Boulevard",
            " Blvd.": " Boulevard",
            " Ct ": " Centre ",
            " Ctr": " Centre",
            " Pl ": " Place ",
            " Ln ": " Lane ",
            " Cir ": " Circle ",
            " Cir" : " Circle ",
            " Wy": " Way ",
            " S ": " South ",
            " E ": " East ",
            " W ": " West ",
            " N ": "North"
}

#Update function that will also be used when preparing the data for SQL. 
def update_name(name, mapping):
    for key, value in mapping.iteritems():
        if key in name:
            return name.replace(key, value)
    return name

with open ('map.osm', 'r') as mapfile:
    s_types = audit()
    
    for s_type, ways in s_types.iteritems():
        for name in ways:
            correct_name = update_name(name, mapping)
            print name, "->", correct_name