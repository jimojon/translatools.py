#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import datetime
import csv
import xml.etree.ElementTree as ETree
from xml.dom import minidom

# config
tags = {
    'root': 'data',
    'item': 'value'
}

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""

    rough = ETree.tostring(elem, 'utf-8')
    return minidom.parseString(rough).toprettyxml('\t', '\n', 'utf-8')


def to_xml():
    """Convert csv to xml"""

    reader = csv.reader(open(input_file), 'excel', delimiter=',')

    root = ETree.Element(tags['root'])
    root.append(ETree.Comment('Generated from ' + input_file + ' at ' +
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

    child = None

    for row in reader:
        text = str(row[1]).decode('utf-8')

        # text item
        if row[0] != '':
            child = ETree.SubElement(root, row[0])
            if row[1] != '':
                child.text = text

        # list item
        elif row[0] == '' and row[1] != '':
            li = ETree.SubElement(child, tags['item'])
            li.text = text

        else:
            root.append(ETree.Comment('Empty line'))

    s = prettify_xml(root)

    xml_file = open(output_file, 'w')
    xml_file.write(s)
    xml_file.close()


def to_csv():
    """Convert xml to csv"""

    xml_file = open(input_file, 'r')
    csv_file = open(output_file, 'w')

    tree = ETree.parse(xml_file)
    root = tree.getroot()

    for element in root:
        csv_file.write(unicode(element.tag).encode('utf-8') + ',' + unicode(element.text).encode('utf-8') + '\n')

        for child in element:
            if child.tag == tags['item']:
                csv_file.write(',' + unicode(child.text).encode('utf-8') + '\n')

    csv_file.close()


# check input
if len(sys.argv) <= 1:
    sys.exit("Usage: %s input output[optional]" % sys.argv[0])

input_file = sys.argv[1]
input_type = os.path.splitext(input_file)[1][1:].strip().lower()
output_type = 'csv' if input_type == 'xml' else 'xml' if input_type == 'csv' else ''

# check output
if sys.argv[2:]:
    output_file = sys.argv[2]
else:
    path = os.path.normpath(input_file)
    output_file = os.path.dirname(path) + "/" + os.path.basename(path) + '_' + str(int(time.time())) + '.' + output_type

if input_type != 'csv' and input_type != 'xml':
    sys.exit("Error: unsupported input extension (" + input_type + ")")

print 'convert', input_file + ' to ' + output_type + '...'

if output_type == 'xml':
    to_xml()
elif output_type == 'csv':
    to_csv()

print 'done: ' + output_file
