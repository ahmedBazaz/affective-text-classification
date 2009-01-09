#
# NLP 2008 Project
# Copyright (C) 2008-2009
# Author: Tsai-Yeh Tung <tytung@iis.sinica.edu.tw, d96028@csie.ntu.edu.tw>, 
#         Institute of Information Science, Academia Sinica, Taiwan.
#

Win32 Development Tools:

JDK 1.5.0_17 (or JDK 1.6.0_11)
Python 2.5.4 (or Python 2.6.1)
Python "Natural Language Toolkit 0.9.7" (can use the below NLTK project instead of an installation)

eclipseJEE 3.4.1 (eclipse-jee-ganymede-SR1-win32.zip or eclipse-java-ganymede-SR1-win32.zip)
PyDev 1.4.0 (a plugin that enables users to use Eclipse for Python development)

Two projects are located on
C:\eclipseJEE\eclipse_workspace_PyDev\NLP-2008-Project (this project)
C:\eclipseJEE\eclipse_workspace_PyDev\nltk-0.9.7 (related project: NLTK library and corpus)
# You need to change the path "C:\eclipseJEE\eclipse_workspace_PyDev" in "src/tytung/config.py"

========================================================================

eclipse_launch	: eclipse launch files
nlp2008project	: the term project provided by TA
ref_SemEval2007	: the term project's related data (correct answers) found by me
src				: python code
output			: python output for the term project

========================================================================

affectivetext_test.xml :
<instance id="666">Beckham & Posh and more athlete-celebrity couples</instance>
<instance id="1233">'Cagney & Lacey' finally coming to DVD</instance>
The '&' token must be replaced with '&amp;' in order to conform to valid XML format.
