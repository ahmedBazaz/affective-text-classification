#
# NLP 2008 Project
# Copyright (C) 2008-2009
# Author: Tsai-Yeh Tung <tytung@iis.sinica.edu.tw, d96028@csie.ntu.edu.tw>, 
#         Institute of Information Science, Academia Sinica, Taiwan.
#
"""
AffectiveTextClassifier for the NLP 2008 Project.
"""

__version__ = "0.1"
__author__ = "Tsai-Yeh Tung"
__author_email__ = "tytung@iis.sinica.edu.tw"

from nltk import stem
from nltk.tokenize import WordTokenizer
from wordnetaffect_reader import WordNetAffectEmotionListsReader

import os, sys, time
import nltk
import config

# Corpora location
# nltk.data.path = ['C:\\eclipseJEE\\eclipse_workspace_PyDev\\nltk-0.9.7.win32\\nltk_data', 
#                   'C:\\Documents and Settings\\Tsaiyeh/nltk_data', 
#                   'C:\\nltk_data', 'D:\\nltk_data', 'E:\\nltk_data', 
#                   'C:\\Python25\\nltk_data', 
#                   'C:\\Python25\\lib\\nltk_data']
nltk.data.path.insert(0, config.nltk_data)

# WordNetAffectEmotionLists location
default_WordNetAffect = config.default_WordNetAffect

class AffectiveTextClassifier():
    """
    Classifier for the NLP 2008 Project.
    """
    def __init__(self):
        self.dictWordNetAffect = {}
        # load stopwords
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.wnl = stem.WordNetLemmatizer()
        
    def classifyByWordNetAffect(self, headline, dictWordNetAffect):
        """
        @param headline: a news headline
        @param dictWordNetAffect: a dictionary of WordNetAffect
        @return: emotions separated by whitespace
        """
        emotionsList = []
        emotions = ""
        for affectType, listAffectTerm in dictWordNetAffect.items():
            for affectTerm in listAffectTerm:
                # check
                if headline.lower().find(affectTerm) > -1:
                    if affectType not in emotionsList:
                        emotionsList += [affectType]
        emotionsList.sort()
        for s in emotionsList:
            emotions += " " + s
        return emotions

    def classifyByWordNetAffectExtendByWordNetSynset(self, headline, dictWordNetAffect):
        """
        @param headline: a news headline
        @param dictWordNetAffect: a dictionary of WordNetAffect
        @return: emotions separated by whitespace
        """
        # remove the stopwords
        nonStopwordsHeadline = []
        for token in WordTokenizer().tokenize(headline.lower()):
            meet_stopwords = False
            for w in self.stopwords:
                if token == w:
                    meet_stopwords = True
                    break
            if token.isdigit():
                meet_stopwords = True
            if not meet_stopwords:
                nonStopwordsHeadline.append(token)
                # WordNet stemming
                # ADJ, ADV, NOUN, VERB = 'a', 'r', 'n', 'v'
                for pos in ('a', 'r', 'n', 'v'):
                    stemmedToken = self.wnl.lemmatize(token, pos)
                    if stemmedToken not in nonStopwordsHeadline:
                        nonStopwordsHeadline.append(stemmedToken)
        # classify
        dictAffect = {'anger':0, 'disgust':0, 'fear':0, 'joy':0, 'sadness':0,'surprise':0}
        emotionsList = []
        emotions = ""
        for affectType, listAffectTerm in dictWordNetAffect.items():
            for word in nonStopwordsHeadline:
                for affectTerm in listAffectTerm:
                    # check
                    if affectTerm == word:
                        dictAffect[affectType] += 1
        for affectType, count in dictAffect.items():
            if count > 0:
                emotionsList += [affectType]
#        if dictAffect['joy'] > 0: # low F score
#            for w in (('anger'), ('fear')):
#                if w in emotionsList:
#                    emotionsList.remove(w)
        #print dictAffect.values()
        emotionsList.sort()
        for s in emotionsList:
            emotions += " " + s
        return emotions

    def classifyByMutualInformation(self, headline, listReutersArticles, dictWordNetAffect):
        """
        It spends a lot of time (9 hours or more for trial data: 250 news) 
        calculating the Pointwise Mutual Information value.
        
        @param headline: a news headline
        @return: emotions separated by whitespace
        """
        # remove the stopwords
        nonStopwordsHeadline = []
        for token in WordTokenizer().tokenize(headline.lower()):
            meet_stopwords = False
            for w in self.stopwords:
                if token == w:
                    meet_stopwords = True
                    break
            if token.isdigit():
                meet_stopwords = True
            if not meet_stopwords:
                nonStopwordsHeadline.append(token)
        # calculate MI
        emotionsList = []
        emotions = ""
        articleCount = len(listReutersArticles)
        self.id += 1
        # wrap line per headline
        print "#%s" % self.id
        for affectType, listAffectTerm in dictWordNetAffect.items():
        #for listAffectTerm in (['anger'],['disgust'],['fear'],['joy'],['sadness'],['surprise']):
            #affectType = listAffectTerm[0]
            totalMI = 0
            # word should be extended
            for word in nonStopwordsHeadline:
                # the number of the articles occur w1 and w2 together, w1 only, and w2 only
                # counter = [c(w1,w2), c(w1), c(w2)] 
                counter = [0.0, 0.0, 0.0]
                for listWordsOfArticle in listReutersArticles:
                    occurrences = self.occur(listWordsOfArticle, listAffectTerm, [word])
                    for i in range(0, len(counter)):
                        if occurrences[i]:
                            counter[i] += 1
                # the probability of P(w1,w2), P(w1), P(w2)
                prob = [counter[0]/articleCount, counter[1]/articleCount, counter[2]/articleCount]
                print affectType, word, counter, prob,
                import math
                try:
                    MI = math.log(prob[0]/prob[1]*prob[2], 2)
                except:
                    MI = 0
                totalMI += MI
                print "MI=%s" % MI
                if MI > 0:
                    print "###MI=%s" % MI
            averageMI = totalMI / len(nonStopwordsHeadline)
            if averageMI > 0:
                print "###averageMI=%s" % averageMI
                emotionsList += [affectType]
        for s in emotionsList:
            emotions += " " + s
        return emotions
    
    def occur(self, listWordsOfArticle, listAffectTerm, listHeadlineWord):
        """
        find out if the words appear in the article
        @return: [has(w1,w2), has(w1), has(w2)] where has() is True or False, and
                    w1=listAffectTerm, w2=listHeadlineWord
        """
        occurrences = [False, False, False]
        for articleWord in listWordsOfArticle:
            if articleWord > 2:
                # check w1
                for affectTerm in listAffectTerm:
                    if affectTerm == articleWord:
                        occurrences[1] = True
                        break
                # check w2
                for headlineWord in listHeadlineWord:
                    if headlineWord == articleWord:
                        occurrences[2] = True
                        break
                # check (w1,w2)
                if occurrences[1] and occurrences[2]:
                    occurrences[0] = True
                    break
        return occurrences

    def classifyAndOutput(self, classifiedMethod, xmlFilePath, outputFilePath, 
                          start=None, end=None):
        """
        @param classifiedMethod:
                            MutualInformation
                            WordNetAffect
                            WordNetAffectExtendByWordNetSynset
        @param xmlFilePath: the input file path of the XML news
        @param outputFilePath: the output file path
        @param start: the starting index of the XML news instances, start from 0
        @param end: the ending index of the XML news instances
        @return: the final output file path
        """
        # read the XML content
        news_list = self.loadXMLInput(xmlFilePath, start, end)
        # filename suffix
        filename_suffix = time.strftime('_%Y-%m-%d') #_%H-%M-%S
        # modify the output file path
        filepath = outputFilePath + filename_suffix + "_" + classifiedMethod
        # console hint
        sys.stdout.write("\nPlease wait ...") # means no wrap line, or uses { print "Please wait ", }
        # time counter
        clock = initialClock = time.clock()
        # load ReutersCorpus
        if classifiedMethod == "MutualInformation":
            self.id = 0
            listReutersArticles = self.loadReutersCorpus()
            reader = WordNetAffectEmotionListsReader(default_WordNetAffect)
            dictWordNetAffect = reader.loadWordNetAffect()
        # loadWordNetAffect()
        elif classifiedMethod == "WordNetAffect":
            reader = WordNetAffectEmotionListsReader(default_WordNetAffect)
            dictWordNetAffect = reader.loadWordNetAffect()
        # loadWordNetAffect(extendByWordNet=True)
        elif classifiedMethod == "WordNetAffectExtendByWordNetSynset":
            reader = WordNetAffectEmotionListsReader(default_WordNetAffect)
            dictWordNetAffect = reader.loadWordNetAffect(extendByWordNetSynset=True)
        # output classification result
        f = open(filepath, 'w') # write
        for news in news_list:
            emotions = ""
            # classify
            if classifiedMethod == "MutualInformation":
                print "=" * 90
                print "affect_word, news_word, Count[c(aw,nw),c(aw),c(nw)], Prob[P(aw,nw),P(aw),P(nw)] MI=?"
                print "=" * 90
                emotions = self.classifyByMutualInformation(news[1], listReutersArticles, dictWordNetAffect)
            elif classifiedMethod == "WordNetAffect":
                emotions = self.classifyByWordNetAffect(news[1], dictWordNetAffect)
            elif classifiedMethod == "WordNetAffectExtendByWordNetSynset":
                emotions = self.classifyByWordNetAffectExtendByWordNetSynset(news[1], dictWordNetAffect)
            else:
                f.close()
                os.remove(filepath)
                raise Exception("No such classification method: %s" % classifiedMethod)
            # time counter and console hint
            if time.clock() - clock > 1:
                clock = time.clock()
                sys.stdout.write(".") # means no wrap line, or uses { print ".", }
            f.write("%s%s\n" % (news[0], emotions))
        f.close()
        print "\nTime spent on '%s' classification is %f s" % (classifiedMethod, clock-initialClock)
        print "Result can be seen in '%s'" % filepath
        return filepath

    def loadXMLInput(self, xmlFilePath, start=None, end=None):
        """
        affectivetext_trial.xml or affectivetext_test.xml
        
        @param xmlFilePath: the input file path of the XML news
        @param start: the starting index of the XML news instances, start from 0
        @param end: the ending index of the XML news instances
        @return: a list of tuple of news id and headline [(id, headline), ...]
        """
        import xml.etree.ElementTree as ET #python 2.5
        #print 'Reading %s\n' % xmlFilePath
        if os.path.exists(xmlFilePath):
            try:
                # parse XML to DOM tree
                doc = ET.parse(xmlFilePath)
                # process XML: (/corpus/instance) to news_list=[(id, headline), ...]
                news_list = [(node.get('id'), node.text.strip()) 
                             for node in doc.findall("./instance")][start:end]
                return news_list
            except:
                raise Exception("Not a valid XML file: %r" % xmlFilePath)
        else:
            raise IOError("No such file: %r" % xmlFilePath)

    def loadReutersCorpus(self, start=None, end=None):
        """
        The Reuters-21578 benchmark corpus, ApteMod version
        
        @param start: the starting index of the Reuters articles, start from 0
        @param end: the ending index of the Reuters articles
        @return: a list of the Reuters articles [['w1','w2',...], ['w3','w4',...], ...]
        """
        startClock = time.clock()
        print "\nLoading Reuters Corpus ..."
        from nltk.corpus import reuters
        reutersFiles = reuters.files()[start:end]
        listReutersArticles = []
        for file in reutersFiles:
            list = reuters.words(file)
            list = [w.lower() for w in list]
            listReutersArticles += [list]
        periodClock = time.clock() - startClock
        print "Reuters Corpus has been loaded in %f s" % periodClock
        return listReutersArticles

def demo():
    """
    demo for AffectiveTextClassifier
    """
    # testing AffectiveTextClassifier()
    classifier = AffectiveTextClassifier()
    print "\n" + "*"*20 + " testing AffectiveTextClassifier() " + "*"*20
    print "classifier = AffectiveTextClassifier()"
    # testing loadXMLInput()
    print "## testing loadXMLInput()"
    xmlFilePath = config.trial_xml
    print "xmlFilePath = " + xmlFilePath
    newsList = classifier.loadXMLInput(xmlFilePath, 8, 10)
    print "classifier.loadXMLInput(xmlFilePath, 8, 10) = %s" % newsList
    # testing classifyByWordNetAffect()
    print "\n## testing classifyByWordNetAffect()"
    reader = WordNetAffectEmotionListsReader(default_WordNetAffect)
    news = newsList[0]
    print "default_WordNetAffect = " + default_WordNetAffect
    print "reader = WordNetAffectEmotionListsReader(default_WordNetAffect)"
    dictWordNetAffect = reader.loadWordNetAffect()
    emotions = classifier.classifyByWordNetAffect(news[1], dictWordNetAffect)
    print "\ndictWordNetAffect = reader.loadWordNetAffect()"
    print "classifier.classifyByWordNetAffect('%s', dictWordNetAffect)" % news[1]
    print "Classify for news id %s: ['%s']" % (news[0], emotions.strip())
    dictWordNetAffect = reader.loadWordNetAffect(extendByWordNetSynset=True)
    emotions = classifier.classifyByWordNetAffectExtendByWordNetSynset(news[1], dictWordNetAffect)
    print "\ndictWordNetAffect = reader.loadWordNetAffect(extendByWordNetSynset=True)"
    print "classifier.classifyByWordNetAffectExtendByWordNetSynset('%s', dictWordNetAffect)" % news[1]
    print "Classify for news id %s: ['%s']" % (news[0], emotions.strip())
    print "*"*40 + " end " + "*"*40 + "\n"

if __name__ == '__main__':
    demo()    
