#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Frederik Elwert <frederik.elwert@web.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
A service that converts TCF to the Mallet input format.

"""

from collections import Counter
import re

from lxml import etree
from tcflib import tcf
from tcflib.tagsets import TagSet
from tcflib.service import ExportingWorker, run_as_cli


class LemmalistGenerator(ExportingWorker):

    layers = ['tokens', 'lemmas']

    def export(self):
        # ExportingWorker just has to override `export()` to return the target
        # Format as bytes. It can access `self.corpus` like an `AddingWorker`.
        lemmalist = {}
        for token in self.corpus.tokens:
            lemmatokens = lemmalist.setdefault(token.lemma, set())
            lemmatokens.add(token.text)
            # Deal with TreeTagger’s `<unknown>` pseudo-lemma
            if '<unknown>' in lemmalist:
                del lemmalist['<unknown>']
        # ExportingWorker returns output as bytes.
        output = ['{lemma}->{tokens}'.format(lemma=lemma,
                                             tokens=','.join(tokens))
                  for lemma, tokens in lemmalist.items()]
        return '\n'.join(output).encode('utf8')


if __name__ == '__main__':
    run_as_cli(LemmalistGenerator)
