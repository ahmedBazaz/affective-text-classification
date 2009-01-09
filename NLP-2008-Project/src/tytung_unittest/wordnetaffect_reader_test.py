#
# NLP 2008 Project
# Copyright (C) 2008-2009
# Author: Tsai-Yeh Tung <tytung@iis.sinica.edu.tw, d96028@csie.ntu.edu.tw>, 
#         Institute of Information Science, Academia Sinica, Taiwan.
#
"""
UnitTest for the NLP 2008 Project.
"""

__version__ = "0.1"
__author__ = "Tsai-Yeh Tung"
__author_email__ = "tytung@iis.sinica.edu.tw"

import unittest
from tytung import config
from tytung import wordnetaffect_reader as r

class EmotionWordTokenizerTestCase(unittest.TestCase):
    def setUp(self):
        self.tokenizer = r.EmotionWordTokenizer()
    
    def test_tokenize(self):
        list = ["n#05588822 umbrage offense"]
        list += ["n#05589637 pique temper irritation"]
        list += ["n#05588413 fury rage madness"]
        answers = []
        for line in list:
            answer = []
            for w in line.split()[1:]:
                answer += [w]
            answers += [answer]
        # answers = [['umbrage', 'offense'], ['pique', 'temper', 'irritation'], ['fury', 'rage', 'madness']]
        for i in range(0, len(list)):
            self.assertEqual(answers[i], self.tokenizer.tokenize(list[i]))

class WordNetAffectEmotionListsReaderTestCase(unittest.TestCase):
    def setUp(self):
        root_WordNetAffect = config.default_WordNetAffect
        self.reader = r.WordNetAffectEmotionListsReader(root_WordNetAffect)
    
    def test_read_distinct(self):
        emotionTerms = self.reader.read_distinct("anger.txt")
        self.assertEqual("wrath", emotionTerms[0])
        self.assertEqual("umbrage", emotionTerms[1])
        self.assertEqual("offense", emotionTerms[2])
        self.assertEqual("pique", emotionTerms[3])
        self.assertEqual("temper", emotionTerms[4])
        self.assertEqual("irritation", emotionTerms[5])
    
    def test_loadWordNetAffect(self):
        dictWordNetAffect = self.reader.loadWordNetAffect()
        keys = dictWordNetAffect.keys()
        keys.sort()
        self.assertEqual(['anger','disgust','fear','joy','sadness','surprise'], keys)
    