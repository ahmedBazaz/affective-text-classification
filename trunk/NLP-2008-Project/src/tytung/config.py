import sys

# change this if necessary
if sys.platform == "win32":
    workspace = r"C:\eclipseJEE\eclipse_workspace_PyDev" # for windows
else:
    workspace = r"/nfs/p2/96/d96028/nlp2008/eclipse_workspace_PyDev" # for linux

nltk_data = workspace + r"/nltk-0.9.7/nltk_data"
default_WordNetAffect = workspace + r"/NLP-2008-Project/nlp2008project/WordNetAffectEmotionLists"
trial_xml = workspace + r"/NLP-2008-Project/nlp2008project/trial/affectivetext_trial.xml"

# change this if necessary
sys.path.append(workspace + r"/NLP-2008-Project/src")
sys.path.append(workspace + r"/nltk-0.9.7/src")
