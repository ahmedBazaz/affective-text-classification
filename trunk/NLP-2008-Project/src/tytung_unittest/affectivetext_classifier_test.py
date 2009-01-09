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
from tytung import affectivetext_classifier as c
from tytung import wordnetaffect_reader as r

class AffectiveTextClassifierTestCase(unittest.TestCase):
    def setUp(self):
        root_WordNetAffect = config.default_WordNetAffect
        self.reader = r.WordNetAffectEmotionListsReader(root_WordNetAffect)
        self.classifier = c.AffectiveTextClassifier()
        #trial_xml = r"C:\eclipseJEE\eclipse_workspace_PyDev\NLP-2008-Project\nlp2008project\trial\affectivetext_trial.xml"
        self.xmlFilePath = config.trial_xml
        self.news = ("9", "Happy birthday, iPod")
    
    def test_classifyByWordNetAffect(self):
        dictWordNetAffect = self.reader.loadWordNetAffect()
        emotions = self.classifier.classifyByWordNetAffect(self.news[1], dictWordNetAffect)
        self.assertEqual("joy", emotions.strip())
    
    def test_classifyByWordNetAffectExtendByWordNetSynset(self):
        dictWordNetAffect = self.reader.loadWordNetAffect(extendByWordNetSynset=True)
        emotions = self.classifier.classifyByWordNetAffectExtendByWordNetSynset(self.news[1], dictWordNetAffect)
        self.assertEqual("joy", emotions.strip())
    
    def test_classifyByMutualInformation(self):
        #listReutersArticles = self.classifier.loadReutersCorpus()
        #dictWordNetAffect = self.reader.loadWordNetAffect()
        # spend 326 s (5.4 minutes)
        #emotions = self.classifier.classifyByMutualInformation(self.news[1], listReutersArticles, dictWordNetAffect)
        #self.assertEqual("", emotions)
        pass
    
    def test_classifyAndOutput(self):
        import os, tempfile, shutil
        try:
            # create temp folder
            tempDirPath = tempfile.mkdtemp()
            outputFilePath = tempDirPath + os.path.sep + "tempOutputFile"
            filepath = self.classifier.classifyAndOutput("WordNetAffect", self.xmlFilePath, outputFilePath, 0, 1)
            self.assertEqual("1", open(filepath, 'r').readlines()[0][0])
        finally:
            # cleanup temp folder
            if os.path.exists(tempDirPath):
                shutil.rmtree(tempDirPath)
                print "File has been deleted : %s" % filepath
    
    def test_loadXMLInput(self):
        news_list = self.classifier.loadXMLInput(self.xmlFilePath, 8, 9)
        self.assertEqual([self.news], news_list)
    
    def test_loadReutersCorpus(self):
        listReutersArticles = self.classifier.loadReutersCorpus(0, 1)
        self.assertEqual(['asian', 'exporters', 'fear', 'damage'], listReutersArticles[0][0:4])
    