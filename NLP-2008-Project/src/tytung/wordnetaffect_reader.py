#
# NLP 2008 Project
# Copyright (C) 2008-2009
# Author: Tsai-Yeh Tung <tytung@iis.sinica.edu.tw, d96028@csie.ntu.edu.tw>, 
#         Institute of Information Science, Academia Sinica, Taiwan.
#
"""
WordNetAffectEmotionLists Reader for the NLP 2008 Project.
"""

__version__ = "0.1"
__author__ = "Tsai-Yeh Tung"
__author_email__ = "tytung@iis.sinica.edu.tw"

from nltk.corpus import stopwords
from nltk.corpus.reader import PlaintextCorpusReader
from nltk.corpus.reader import read_line_block
from nltk.corpus.reader import wordnet
from nltk.tokenize import RegexpTokenizer

import os, sys, time
import nltk
import config

# WordNetAffectEmotionLists location
default_WordNetAffect = config.default_WordNetAffect

class EmotionWordTokenizer(RegexpTokenizer):
    """
    A tokenizer that divides a text into sequences of alphabetic
    characters.  Any non-alphabetic characters are discarded.  E.g.:

        >>> EmotionWordTokenizer().tokenize("n#05588822 umbrage offense")
        ['umbrage', 'offense']
        >>> EmotionWordTokenizer().tokenize("n#05589637 pique temper irritation")
        ['pique', 'temper', 'irritation']
    """
    def __init__(self):
        # regular expressions '[^# ]' filter 'n#05588822' away
        # regular expressions '[a-zA-Z_\-]+' match the desired words
        RegexpTokenizer.__init__(self, r'[^# ][a-zA-Z_\-]+')

class WordNetAffectEmotionListsReader(PlaintextCorpusReader):
    """
    Reader for WordNetAffectEmotionLists *.txt documents.
    """
    
    # wordnet.WordNetCorpusReader(nltk.data.find('corpora/wordnet'))
    wnReader = None
    
    def __init__(self, root_WordNetAffect):
        """
        @param root_WordNetAffect: the path of the WordNetAffectEmotionLists folder
        """
        PlaintextCorpusReader.__init__(self, root_WordNetAffect, '.*\.txt',
                                       word_tokenizer=EmotionWordTokenizer(),
                                       para_block_reader=read_line_block)
    
    def read_distinct(self, txtName):
        """
        @param txtName: the txt filename
        @return: a list of distinct emotional terms from WordNetAffectEmotionLists
        """
        # self.root: The directory where this corpus is stored.
        txtFolderPath = self.root
        txtPath = txtFolderPath + os.path.sep + txtName
        if os.path.exists(txtPath):
            try:
                originalList = []
                for line in open(txtPath).readlines():
                    for term in line.split()[1:]:
                        originalList += [term]
                # filter the duplicated words
                distinctList = []
                for term in originalList:
                    # replace the "-" and "_" in phrase
                    if term.find("-") > -1:
                        term = term.replace("-", " ")
                    if term.find("_") > -1:
                        term = term.replace("_", " ")
                    if term not in distinctList:
                        distinctList += [term]
                return distinctList
            except:
                raise Exception("Error while reading this file: %r" % txtPath)
        else:
            raise IOError("No such file: %r" % txtPath)
    
    def loadWordNetAffect(self, extendByWordNetSynset="False"):
        """
        load WordNetAffect into a dictionary data structure
        
        @param extendByWordNetSynset: indicate if extend WordNetAffect by WordNet Synset
        @return: a dictionary of WordNetAffect
            dictWordNetAffect = {'anger':['wrath','umbrage'], 'disgust':['repugnance','repulsion'], ...}
        """
        dictWordNetAffect = {}
        for txtName in self.files():
            # txtName = 'anger.txt' and so on ...
            distinctList = self.read_distinct(txtName)
            if extendByWordNetSynset == True:
                wnReader = self._getWordNetCorpusReader()
                distinctList = self._extendByWordNetSynset(distinctList, wnReader)
            # dictWordNetAffect[key] = value
            dictWordNetAffect[txtName.split(".")[0]] = distinctList
        return dictWordNetAffect
    
    def _getWordNetCorpusReader(self):
        """
        @return: a WordNetCorpusReader
        """
        if self.wnReader == None:
            startClock = time.clock()
            print "\nLoading WordNet Corpus ..."
            self.wnReader = wordnet.WordNetCorpusReader(nltk.data.find('corpora/wordnet'))
            periodClock = time.clock() - startClock
            print "WordNet Corpus has been loaded in %f s" % periodClock
        return self.wnReader
    
    def _extendByWordNetSynset(self, listWords, wnReader):
        """
        @param listWords: the words whose will be extended by WordNet Synset
        @param wnReader: a WordNetCorpusReader
        @return: a list of words extended by WordNet Synset
        """
        listWordsWithSynset = listWords
        # extended by WordNet stemming (morphy)
        # ADJ, ADV, NOUN, VERB = 'a', 'r', 'n', 'v'
        for word in listWordsWithSynset:
            for pos in ('a', 'r', 'n', 'v'):
                lemma = wnReader.morphy(word, pos)
                if lemma is not None and lemma not in listWordsWithSynset:
                    listWordsWithSynset += [lemma]
        # extended by WordNet Synset
        for i in range(0, len(listWords)):
            #print i, listWords[i]
            # e.g.: word = "sadness"
            listSynset = wnReader.synsets(listWords[i])
            # listSynset = [Synset('sadness.n.01'), Synset('sadness.n.02'), Synset('gloominess.n.03')]
            for synset in listSynset:
                # synset.lemma_names[0] = ['sadness', 'unhappiness']
                # synset.lemma_names[1] = ['sadness', 'sorrow', 'sorrowfulness']
                # synset.lemma_names[2] = ['gloominess', 'lugubriousness', 'sadness']
                for term in synset.lemma_names:
                    # replace the "-" and "_" in phrase
                    if term.find("-") > -1:
                        term = term.replace("-", " ")
                    if term.find("_") > -1:
                        term = term.replace("_", " ")
                    if term not in listWordsWithSynset:
                        listWordsWithSynset.append(term)
        # WordNet stemming (morphy)
        # ADJ, ADV, NOUN, VERB = 'a', 'r', 'n', 'v'
        for word in listWordsWithSynset:
            for pos in ('a', 'r', 'n', 'v'):
                lemma = wnReader.morphy(word, pos)
                if lemma is not None and lemma not in listWordsWithSynset:
                    listWordsWithSynset += [lemma]
        return listWordsWithSynset

def demo():
    """
    demo for WordNetAffectEmotionListsReader
    """
    # testing WordNetAffectEmotionListsReader()
    reader = WordNetAffectEmotionListsReader(default_WordNetAffect)
    wnReader = reader._getWordNetCorpusReader()
    print "\n" + "*"*20 + " testing WordNetAffectEmotionListsReader() " + "*"*20
    print "default_WordNetAffect = " + default_WordNetAffect
    print "reader = WordNetAffectEmotionListsReader(default_WordNetAffect)"
    print "wnReader = reader._getWordNetCorpusReader()"
    print "reader.files() = %s\n" % repr(reader.files())
    for txtName in reader.files():
        # original words (have duplicated words)
        originalList = [w for w in reader.words(txtName)]
        print "%s (original %s tokens) %s" % (txtName, len(reader.words(txtName)), originalList)
        # distinct words (filter duplicated words)
        distinctList = reader.read_distinct(txtName)
        print "%s (distinct %s tokens) %s" % (txtName, len(distinctList), distinctList)
        # extended words (extend by WordNet Synset words)
        extendedList = reader._extendByWordNetSynset(distinctList, wnReader)
        print "%s (extended %s tokens) %s" % (txtName, len(extendedList), extendedList)
        # raw data
        #print "%s (raw %s chars) \n%s" % (txtName, len(reader.raw(txtName)), reader.raw(txtName))
    # testing loadWordNetAffect()
    print "\n## testing loadWordNetAffect()"
    dictWordNetAffect = reader.loadWordNetAffect()
    print "dictWordNetAffect = reader.loadWordNetAffect()"
    print "dictWordNetAffect = %s" % dictWordNetAffect
    # testing loadWordNetAffect()
    print "\n## testing loadWordNetAffect(extendByWordNetSynset=True)"
    dictWordNetAffect = reader.loadWordNetAffect(extendByWordNetSynset=True)
    print "dictWordNetAffect = reader.loadWordNetAffect(extendByWordNetSynset=True)"
    print "dictWordNetAffect = %s" % dictWordNetAffect
    print "*"*40 + " end " + "*"*40 + "\n"

if __name__ == '__main__':
    demo()
