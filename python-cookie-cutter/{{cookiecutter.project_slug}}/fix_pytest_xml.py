# Due to https://github.com/gocd/gocd/issues/1132

import os
import sys
import xml.dom.minidom

args = sys.argv[1:]
input_xml_fname = args[0]
output_xml_fname = args[1]

if os.path.isfile(input_xml_fname):
    parsed = xml.dom.minidom.parse(input_xml_fname)
    pretty_xml_as_string = parsed.toprettyxml()
    with open(output_xml_fname, "w") as output_file:
        output_file.write(pretty_xml_as_string)
else:
    print("File do not exists - {0}".format(input_xml_fname))
