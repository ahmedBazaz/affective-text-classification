import os, sys

semEvalPath = r"C:\eclipseJEE\eclipse_workspace_PyDev\NLP-2008-Project\ref_SemEval2007"
emotions = ('anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise')
files = []
for var in ('trial', 'test'):
    files += [semEvalPath + r"\AffectiveText.%s\affectivetext_%s.emotions.gold" % (var, var)]

for xml in files:
    """ uncomment [Ctrl+/] the following lines to output *.gold.key files """
#    f = open(xml+".key", 'w')
#    for line in open(xml, 'r').readlines():
#        f.write(line.split()[0])
#        list = line.split()
#        #print list
#        for i in range(0, len(emotions)): 
#            if int(list[i+1]) > 49:
#                #print int(list[i+1]), emotions[i]
#                f.write(" %s" % emotions[i])
#        f.write("\n")
#    f.close()
    [sys.stdout.write(line) for line in open(xml+".key", 'r').readlines()]
