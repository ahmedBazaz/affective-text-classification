
def affectivetextReader(xmlfilename):
    from nltk.corpus.util import LazyCorpusLoader
    from nltk.corpus.reader import XMLCorpusReader
    affectivetext = LazyCorpusLoader('affectivetext', XMLCorpusReader, r'(?!\.).*\.xml')
    return [(node.get('id'), node.text.strip()) for node in affectivetext.xml(xmlfilename)]

def demo_affectivetextReader(xmlfilename):
    list = affectivetextReader(xmlfilename)
    print "*"*40 + "len('" + xmlfilename + "')=" + str(len(list)) + "*"*40
    for item in list:
        print "%s\t%s" % (item[0], item[1]) #id {TAB} news_headline

def registerEnvironmentVariable(regtype, method, env_var_name, env_var_value=""):
    """ 
    add the environment variable "NLTK_DATA"  
    into "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    or "HKEY_CURRENT_USER\Environment"
    """
    if env_var_name <> "NLTK_DATA":
        print "Dangerous! '%s' is not a legal environment variable" % env_var_name
    else:
        import os, _winreg
        # user or global
        if regtype == "global":
            HKEY = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
            keypath = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        else: # user
            HKEY = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
            keypath = r"Environment"
        key = _winreg.OpenKey(HKEY, keypath, 0, _winreg.KEY_ALL_ACCESS)
        # add or delete
        if method == "add":
            _winreg.SetValueEx(key, env_var_name, 0, _winreg.REG_EXPAND_SZ, env_var_value)
            new_value = _winreg.QueryValueEx(key, env_var_name)[0]
            print "Environment variable: '%s = %s' has been added" % (env_var_name, new_value)
        else: # delete
            try:
                _winreg.DeleteValue(key, env_var_name)
                print "Environment variable: '%s' has been deleted" % (env_var_name)
            except:
                print "Environment variable: '%s' doesn't exist" % (env_var_name)
        _winreg.CloseKey(key)
        _winreg.CloseKey(HKEY)
        print os.environ.get('NLTK_DATA') #It seems to need to reboot for seeing this value
        print os.getenv("NLTK_DATA")      #It seems to need to reboot for seeing this value

def demo():
    # Corpora location
    import nltk
    #nltk_data = r"C:\eclipseJEE\eclipse_workspace_PyDev\nltk-0.9.7.win32\nltk_data"
    nltk_data = config.nltk_data
    #nltk.data.path += [nltk_data] #equals nltk.data.path.append(nltk_data)
    nltk.data.path.insert(0, nltk_data)
    # tokenize
    '''from nltk.tokenize import *
    tokenizer = WordPunctTokenizer()
    print tokenizer.tokenize("She said 'hello'.")'''
#    # stemming
#    from nltk.stem.porter import PorterStemmer
#    print PorterStemmer().stem('tokenization') #token
#    print PorterStemmer().stem('stemming') #stem
#    print PorterStemmer().stem('sadness') #sad
#    print PorterStemmer().stem('happy') #happi
#    print PorterStemmer().stem('unhappy') #unhappi
    # Demo
    #import nltk
    #nltk.stem.porter.demo()
    #nltk.stem.lancaster.demo()
    #nltk.probability.demo()
    #nltk.chunk.regexp.demo()
    #nltk.parse.chart.demo()
    #nltk.sem.evaluate.demo()
    #nltk.sem.logic.demo()
    #help(nltk)
    '''
    affectivetext_test.xml :
    <instance id="666">Beckham & Posh and more athlete-celebrity couples</instance>
    <instance id="1233">'Cagney & Lacey' finally coming to DVD</instance>
    The '&' token must be replaced with '&amp;' in order to conform to valid XML format.
    '''
    #demo_affectivetextReader('affectivetext_trial.xml')
    #demo_affectivetextReader('affectivetext_test.xml')
    #registerEnvironmentVariable("user", "add", "NLTK_DATA", "C:\\nltk_data")
    #registerEnvironmentVariable("user", "delete", "NLTK_DATA")
    
    # Corpus test
    #nltk.download() # GUI corpus downloader
#    import sys
#    from nltk.corpus import reuters
#    [sys.stdout.write(" ".join(sent)) for sent in reuters.sents()[:2]]
    
#    from nltk import stem
#    wnl = stem.WordNetLemmatizer()
#    #{ Part-of-speech constants
#    #ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
#    #}
#    print wnl.lemmatize('tokenization', 'n') #tokenization
#    print wnl.lemmatize('stemming', 'v') #v:stem, n,a:stemming
#    print wnl.lemmatize('sadness') #sadness
#    print wnl.lemmatize('happy') #happy
#    print wnl.lemmatize('unhappy') #unhappy
    
    # WordNet Corpus
    from nltk.corpus.reader import wordnet
    #print wordnet.demo()
    wn = wordnet.WordNetCorpusReader(nltk.data.find('corpora/wordnet'))
#    print wn.morphy('tokenization') #None
#    print wn.morphy('stemming') #stem
#    print wn.morphy('sadness') #sadness
#    print wn.morphy('happy') #happy
#    print wn.morphy('unhappy') #unhappy
    listSynset = wn.synsets('sadness')
    print listSynset
    for synset in listSynset:
        print synset.lemma_names
    #[Synset('sadness.n.01'), Synset('sadness.n.02'), Synset('gloominess.n.03')]
    #['sadness', 'unhappiness']
    #['sadness', 'sorrow', 'sorrowfulness']
    #['gloominess', 'lugubriousness', 'sadness']
    
    from nltk.corpus.reader import PlaintextCorpusReader
    #root = r"C:\eclipseJEE\eclipse_workspace_PyDev\NLP-2008-Project\nlp2008project\WordNetAffectEmotionLists"
    root = config.default_WordNetAffect
    reader = PlaintextCorpusReader(root, '.*\.txt')
    print reader.files()

    # affectivetext_classifier
    from tytung import affectivetext_classifier
    affectivetext_classifier.demo()
    
#    # RegexpTokenizer
#    from nltk.tokenize import RegexpTokenizer
#    pattern = r'[^# ][a-zA-Z_\-]+'
#    list = ["n#05588822 umbrage offense"]
#    list += ["n#05589637 pique temper irritation"]
#    list += ["n#05588413 fury rage madness"]
#    for i in range(0, len(list)):
#        print RegexpTokenizer(pattern).tokenize(list[i])
    
if __name__ == '__main__':
    import sys
    from tytung import config
    print sys.executable or sys.platform, sys.version
    demo()
