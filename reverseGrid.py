from __future__ import print_function
"""
Read an rF2 result file (XML) and create a server batch file
to start the next race in reverse order of finishers.
"""
import xml.etree.ElementTree as ET
import os
import sys

batchfile = 'rgrid'

if len(sys.argv)>1: # XML file in command line
  result_file = sys.argv[1]
  try:
    tree = ET.parse(result_file)
    root = tree.getroot()

    finish = []
    for child in root.iter('Driver'):
        finish.append((child.find('Name').text, child.find('Position').text))

    sorted_by_second = sorted(finish,
                             key=lambda tup: int(tup[1]),
                             reverse=True)

    try:
      print('Reversed grid order from finish of %s:\n' % os.path.basename(result_file))
      with open(batchfile, 'w') as fp:
        fp.write('// Server or administrator can run batch files by chatting "/batch %s"\n' % batchfile)
        for i, driver in enumerate(sorted_by_second):
          fp.write('/editgrid %d %s\n' % (i+1, driver[0]))
          print('%d: %s' % (i+1, driver[0]))
      print('\nServer or administrator can run the batch file\nthat sets that order by chatting "/batch %s"' % batchfile)
    except:
      print('ERROR writing batch file "%s"\n\n' % batchfile)
  except:
    print('ERROR reading XML file "%s"\n\n' % result_file)
else:
  _this = os.path.basename(sys.argv[0])
  print('Usage: %s <XML file of previous race>\ne.g. %s 2019_04_26_22_20_24-15R1.xml' % (_this, _this))
print('\nPress Enter to continue')
input()

