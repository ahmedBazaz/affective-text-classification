import os, sys, time
from tytung import affectivetext_classifier
from tytung import config

def run():
    """
    classify and output
    """
    # trial.xml = 250 news headlines
    # test.xml = 1000 news headlines
    classifier = affectivetext_classifier.AffectiveTextClassifier()
    # WordNetAffect for trial.F=0.0984, test.F=0.0947
    #classifier.classifyAndOutput("WordNetAffect", argv[1], argv[2])
    # MutualInformation spends about 9.8 hours for trial.F=0
    #classifier.classifyAndOutput("MutualInformation", argv[1], argv[2])
    # WordNetAffect for trial.F=0.2858, test.F=0.1868
    classifier.classifyAndOutput("WordNetAffectExtendByWordNetSynset", argv[1], argv[2])
    print "\nTotal time is %f s" % time.clock()

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 3:
        pyfile = argv[0].split(os.path.sep)[-1]
        print '\nUsage: python %s <input> <output>\n' % pyfile
        print 'input : affectivetext_trial.xml'
        print 'output: systemoutput'
    else:
        if argv[1].startswith('"') or argv[1].startswith("'"):
            argv[1] = argv[1][1:-1]
        if argv[2].startswith('"') or argv[2].startswith("'"):
            argv[2] = argv[2][1:-1]
        print sys.executable or sys.platform, sys.version
        run()
