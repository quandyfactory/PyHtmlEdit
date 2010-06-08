#PyHtmlEdit Documentation

##Summary

PyHtmlEdit is a simple Python text editor optimized for the kinds of HTML formatting that I commonly do.

##About this Document

* Author: Ryan McGreal
* Email: ryan@quandyfactory.com
* Homepage: http://quandyfactory.com/projects/2/pyhtmledit
* Repository: http://github.com/quandyfactory/PyHtmlEdit

##Licence

This document is licenced under the GNU Free Documentation Licence, v. 1.3 http://www.gnu.org/copyleft/fdl.html

##This Version

* Version 0.5
* Release Date: 2009-10-07

##Functions

###<u>F</u>ile Menu

####<u>O</u>pen

Open launches a file selection dialog so you can open a file.

####<u>S</u>ave

Save launches a file selection dialog so you can save a file.

####<u>E</u>xit

Exit closes PyHtmlEdit.

###<u>H</u>TML

Highlight some text (optionally) and select an HTML element to apply to the selected material.

####<u>I</u>nline

Inserts the following inline HTML elements:

* cite
* em
* code
* span
* strong
* sub
* sup

####<u>Block

Inserts the following block HTML elements:

* <u>b</u>lockquote
* <u>d</u>iv
* <u>p</u>
* p.<u>i</u>nitial - inserts a paragraph with class "initial"
* p.ph<u>o</u>to - inserts a paragraph with class "photo" and an interior img (image source is highlighted text; if a second line of text is also highlighted, that serves as the image title)
* pr<u>e</u>

####<u>H</u>eading

* h<u>1</u>
* h<u>2</u>
* h<u>3</u>
* h<u>4</u>
* h<u>5</u>
* h<u>6</u>

####<u>L</u>ink

* <u>a</u> (named anchor)
* a <u>h</u>ref (hyperlink - prompt to enter href)

####<u>N</u>ested

* <u>u</u>l - highlight a linebreak-separated list of items
* <u>o</u>l - highlight a linebreak-separated list of items
* table (<u>c</u>onvert) - sets rows based on linebreaks, cols based on tabs
* table (<u>n</u>ew) - generates a simple 4x4 table with a caption

### F<u>o</u>rmat

####<u>R</u>eplace

Prompts for a string to search for and a string to replace with, and then runs the replace on selected text.

####<u>l</u>case

Converts selected text to lowercase.

####<u>U</u>CASE

Converts selected text to UPPERCASE.

####<u>P</u>case

Converts selected text to Proper Case (first word capitalized).

####<u>C</u>lean

Cleans up MS Office special characters.

####<u>S</u>afer SQL

Converts SQL punctuation to entity codes. **Warning:** not a replacement for parameterized queries!

####Common <u>M</u>isspellings

Replaces commonly misspelled words with their proper spelling.

###Tools

####<u>W</u>ord Count

Provides a summary of characters, words, and lines for selected text, or, if no text is selected, the entire document.

####<u>S</u>trip HTML

Removes all HTML from the text. Deprecated in favour of Html2Text, which is reversible.

####<u>H</u>tml2Text

Converts HTML to Markdown.

####<u>M</u>arkdown

Converts Markdown to HTML. Note: either [python-markdown](http://www.freewisdom.org/projects/python-markdown/) or [python-markdown2](http://code.google.com/p/python-markdown2/) must be installed.

###<u>A</u>bout

####<u>A</u>bout PyHTmlEdit

Pops up a dialog with a summary of PyHtmlEdit, version and release date, author name and email, web address, and licence.

####<u>C</u>heck Version

Uses PyGithubApi to check the version release date against the newest version release date on GitHub.

