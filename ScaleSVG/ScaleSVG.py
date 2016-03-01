#!/usr/bin/env python
import sys


class Parser():

  def __init__(self):
    pass

  def process(self, tokens, splitter, depth):
    if not isinstance(tokens, list):
      tokens = [tokens]

    chs = ' :\",;'
    l = len(tokens)
    idx = 0

    for token in tokens:
      # hack
      if token == 'version="1.1"':
        self.fout.write(token + ' ')
        continue
      processed = False
      for ch in chs:
        if processed:
          continue
        if ch in token:
          self.process(token.split(ch), ch, depth + 1)
          processed = True

      idx += 1
      if not processed:

        try:
          val = float(token)
          self.fout.write(str(val * self.scale))
        except ValueError:
          self.fout.write(token)

      if idx < l:
        self.fout.write(splitter)

  def resize(self, scale, src, dest):
    self.src = src
    self.dest = dest
    self.scale = scale

    print 'resizing from', src, 'to', dest, 'scale =', scale
    fin = open(src, 'r')
    fout = open(dest, 'w')

    self.fin = fin
    self.fout = fout

    header = True
    for l in fin:
      if header:
        # skip one line header
        fout.write(l)
        header = False
      else:
        self.process(l, '', 0)

    fin.close()
    fout.close()

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print 'Scale svg'
    print 'Usage:', sys.argv[0], 'scale src_filename dest_filename'
  else:
    Parser().resize(float(sys.argv[1]), sys.argv[2], sys.argv[3])
