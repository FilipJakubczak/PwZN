import re
import argparse
import string
import matplotlib.pyplot as plt
from collections import Counter
from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-n', nargs='?', default=10, help='Number of words to plot (default=10).')
parser.add_argument('-len', nargs='?', default=0, help='Minimum word lenght to plot (default=0).')
parser.add_argument("--ignore", nargs="+", default=[], help='Word list to ignore (default=empty)')
args = parser.parse_args()
with open(args.file, encoding="utf8") as file:
    text = file.read()

words = re.split(r'\W+', text)

table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in words]
wo_numbers = [s.lower() for s in stripped if not re.search(r'\d',s)]

word_counts = Counter(wo_numbers)
list = [(k, v) for k, v in word_counts.items() if len(k) >= int(args.len) and k not in args.ignore]
list = sorted(list, key=lambda tup: tup[1], reverse=True)

list = list[:int(args.n)]
pattern = [Gre, Yel, Red]
data = vcolor(list, pattern)

graph = Pyasciigraph()
for line in graph.graph('Word histogram', data):
    print(line)