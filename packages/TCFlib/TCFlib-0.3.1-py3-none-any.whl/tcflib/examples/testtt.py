import sys

from tcflib.service import Read, Write
from tcflib.tcf import TextCorpus

from tcflib.examples.treetagger import TreeTagger, Model

class MyTreeTagger(TreeTagger):
    executable = '/home/frederik/Apps/TreeTagger/bin/tree-tagger'
    models = {'de': Model('stts', '/home/frederik/Apps/TreeTagger/lib/german-utf8.par')}

Read('karin.xml') | MyTreeTagger() | Write(sys.stdout.buffer)