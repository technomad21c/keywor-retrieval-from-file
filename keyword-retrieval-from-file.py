#!/usr/bin/python

import sys, getopt
import re

class KeywordRetrieval:
  titles = []
  results = []
  output = False

  def __init__(self, argv):
    try:
      opts, args = getopt.getopt(argv, "hi:k:o:", ["ifile=", "keywords", "ofile="])
    except getopt.GetoptError as err:
      print(err)
      sys.exit(2)

    for opt, arg in opts:
      if opt == '-h':
        print('keyword-retrieval-from-file.py -i filename -k keyword1,keyword2 -o result.txt')
        sys.exit()
      elif opt in ('-i', '--ifile'):
        self.inputfile = arg
      elif opt in ('-k', '--keywords'):
        self.keywords = arg.split(',')
      elif opt in ('-o', '--ofile'):
        self.output = arg

  def get_title(self, row):
    _titles = row.split()
    for k in _titles:
      self.titles.append(k.strip())

  def get_field(self, row):
    _fields = row.split('\t')
    fields = []
    for f in _fields:
      fields.append(f.strip())

    self.results.append(fields)

  def search(self):
    if '.txt' not in self.inputfile:
      filename = self.inputfile + 'data.txt'
    else:
      filename = self.inputfile
    with open(filename, 'r') as f:
      self.filename = f.readline()  # First line : file name
      titles_row = f.readline()     # Second line: tab-separated field headers,
      self.get_title(titles_row)

      for element in f:
        if all(x.lower() in element.lower() for x in self.keywords):  # if the line contains all keywords
          self.get_field(element)   # From third line to end of file: tab-separated field values

  def get_result(self):
    self.search()

    if self.output:
      filename = self.output.split('/')[-1]
      f = open(filename, 'w')

    for res in self.results:
      print('***************************************')
      if self.output:
        f.write('***************************************\n')
      for i in range(len(res)):
        print(self.titles[i] + ': ' + res[i])
        if self.output:
          f.write(self.titles[i] + ': ' + res[i] + '\n')

      print('***************************************')
      if self.output:
        f.write('***************************************\n')
        f.write('\n')
    print('filename:', self.filename)
    print('total size:', len(self.results))
    if self.output:
      f.write('filename:' + self.filename + '\n')
      f.write('total size:' + str(len(self.results)) + '\n')

if __name__ == '__main__':
  data_loader = KeywordRetrieval(sys.argv[1:])
  data_loader.get_result()
