# PyHtmlEdit Documentation

## Summary

PyHtmlEdit is a simple Python text editor optimized for the kinds of HTML formatting that I commonly do.

## About this Document

* Author: Ryan McGreal
* Email: ryan@quandyfactory.com
* Homepage: http://quandyfactory.com/projects/2/pyhtmledit
* Repository: http://github.com/quandyfactory/PyHtmlEdit

## Licence

This document is licenced under the GNU Free Documentation Licence, v. 1.3 http://www.gnu.org/copyleft/fdl.html

## This Version

* Version 3.0
* Release Date: 2020-05-25

## Menu Functions

### File Menu

#### Open

Open launches a file selection dialog so you can open a file.

#### Open-Insert

Launches a file selection dialog to open a file and insert it at the beginning of the current file.

#### Open-Append

Launches a file selection dialog to open a file and insert it at the end of the current file.

#### Save

Save launches a file selection dialog so you can save a file.

#### Quit (Ctrl-q)

Quit closes PyHtmlEdit.

### Edit Menu

#### Select All (Ctrl-a)

Selects all the text in the open document.

#### Copy (Ctrl-c)

Copies highlighted text.

#### Cut (Ctrl-x)

Cuts highlighted text.

#### Paste (Ctrl-v)

Pastes text from the clipboard at the cursor position.

#### Find Next (Ctrl-f)

Launches a dialog to enter search text and then highlights the next instance of that text (if it exists) past the cursor position. At the end of the document, it continues to search from the beginning.

#### Replace All (Ctrl-r)

Launches a dialog to enter search text and a dialog to enter replacement text, and then replaces all occurrences of the former with the latter.

#### Replace Next (Ctrl-n)

Launches a dialog to enter search text and a dialog to enter replacement text, and then replaces the next occurrence of the former after the cursor position with the latter. At the end of the document, it continues to search and replace from the beginning.


### HTML Menu

Highlight some text (optionally) and select an HTML element to apply to the selected material.

#### Inline

Inserts the following inline HTML elements:

* cite
* em
* code
* span
* strong
* sub
* sup

#### Block

Inserts the following block HTML elements:

* blockquote
* div
* p
* p.initial - inserts a paragraph with class "initial"
* p.photo - inserts a paragraph with class "photo" and an interior img (image source is highlighted text; if a second line of text is also highlighted, that serves as the image title)
* pre

#### Heading

* h1
* h2
* h3
* h4
* h5
* h6

#### Nested

* ul - highlight a linebreak-separated list of items
* ol - highlight a linebreak-separated list of items
* table (convert) - sets rows based on line breaks, cols based on tabs
* table (new) - prompts for caption, # of rows and # of columns and generates empty HTML for the table.

###  Format Menu

#### Clean

Cleans up MS Office special characters and removes double spaces.

#### Lowercase

Converts selected text to lowercase.

#### Uppercase

Converts selected text to UPPERCASE.

#### Capitalize

Converts selected text to Proper Case (first word capitalized).

### Tools Menu

#### Strip HTML

Removes all HTML from the text.

#### Html to Text

Converts HTML to Markdown.

#### Markdown

Converts Markdown to HTML. Note: [python-markdown2](https://pypi.org/project/markdown2/) must be installed.

### About

#### About PyHTmlEdit

Pops up a dialog with a summary of PyHtmlEdit, version and release date, author name and email, web address, and licence.

