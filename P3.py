# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
multiple_colons = re.compile(r':{2,}')


CREATED = [ "version", "changeset", "timestamp", "user", "uid"]



#The shape_element function runs on each element
def shape_element(element):
    node = {}
    
    if element.tag == "node" or element.tag == "way" :
        # created dictionary for creation info
        created = {}
        # pos list for lat and lon
        pos = []
        node['type'] = element.tag

        # loop through each element attribute
        for a in element.attrib.keys():
            # if key in CREATED list, add key:value to created dictionary
            if a in CREATED: 
                created[a] = element.attrib[a]
                # if created dictionary created, add to node dictionary
                if created: 
                    node['created'] = created
            # if key is lat or lon, add to pos list, then add list to node dict
            elif a == 'lat':
                pos.insert(0,element.get('lat'))
            elif a == 'lon':
                pos.insert(0,element.get('lon'))
                node['pos'] = pos
            # otherwise, add key:value pair of attribute to node dictionary
            else:
                node[a] = element.get(a)
                
        address = {}   
        for subtag in element:
            if subtag.get('k'):
                
                # if tag has two or more colons, ignore
                if re.search(r':.*:', subtag.get('k')):
                    continue
               
                #if tag has problem characters, ignore
                elif problemchars.search(subtag.get('k')):
                    continue
                
                # if tag starts with addr:, add to dictionary "address"
                elif subtag.get('k').startswith('addr:'):
                    address[subtag.get('k')[5:]] = subtag.get('v')
                    if address:
                        node['address'] = address
                else:
                    node[subtag.get('k')] = subtag.get('v')
        element.clear()
        pprint.pprint(node)
    
        
        return node

    else:
        return None
    

#don't edit
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    pprint.pprint(data)
    return data