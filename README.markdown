# PyHtmlEdit README

PyHtmlEdit is a simple Python text editor optimized for the kinds of HTML formatting that I commonly do.

## Author

  * Author: Ryan McGreal
  * Email: [ryan@quandyfactory.com][1]
  * Homepage: [http://quandyfactory.com/projects/2/pyhtmledit][2]
  * Repository: [http://github.com/quandyfactory/PyHtmlEdit][3]

PyHtmlEdit was assembled from stuff I found online and some functions I've written.

## Licence

Released under the GNU General Public Licence, Version 2: [http://www.gnu.org/licenses/old-licenses/gpl-2.0.html][4]

## This Version

  * Version: 3.0

  * Release Date: 2020-05-25

## Requirements

  * Python 3
  * python-markdown2 [https://pypi.org/project/markdown2/](http://code.google.com/p/python-markdown2/)
  * HTML2text [https://pypi.org/project/html2text/][5]
  
## Notes

### Python 3

The biggest change is that previous versions of this program used Python 2.x, which is now obsolete and has met its end-of-life. The current version uses Python3.

### Tkinter

Previous versions of this program used wxPython as the GUI library, which turned out to be quite a hassle. Now it uses Tkinter, which ships with Python by default and should be available to all users.

### Markdown2

This software does not come bundled with a markdown parser. It assumes you have python-markdown2 installed.

[https://pypi.org/project/markdown2/][6]

So you should install it.

## Revision History

### Version 3.0

* Release Date: 2020-05-25

* Changes:

    * Switched from Python 2.x to Python 3.x.
    * Swapped the GUI library from wxPython to Tkinter.
    * Added File -> Open-Insert, which opens a new file and adds it to the current document at the top.
    * Added File -> Open-Append, which opens a new file and adds it to the current document at the bottom.
    * Added Edit -> Find, which finds and highlights the next occurrence of the search term.
    * Added Edit -> Replace Next, which finds and replaces the next occurrence of the search term.
    * Added Edit -> Replace All, which finds and replaces every occurrence of the search term.
    * Fixed a long-standing bug in the table creation function, which misplaced the </tr> tag before the </thead> tag.
    * Added ability to specify caption, number of rows and number of columns for a new table.
    * Removed some Format menu options that I literally never use.
    * Dropped support for python-markdown, which is not as good as python-markdown2.
    * Added Ctrl keyboard shortcuts for some common actions (e.g. Ctrl-r for replace all). (Alt keyboard shortcuts still work.)

### Version 0.63

* Release Date: 2013-01-16
 
* Changes:

    * Added div.centered to HTML > Block menu

### Version 0.62

* Release Date: 2012-06-08
 
* Changes:

    * Fixed the extra spaces inside `blockquote` elements on `markdown_it()`
    * Added `class="initial"` to the first `<p>` after an `</h3>`

### Version 0.61

* Release Date: 2011-08-16
 
* Changes:

    * Change hyperlink function so it does not add a target="_blank".

### Version 0.60

* Release Date: 2011-08-15

* Changes:

    * Moved document statistics from menu item into status bar, updated constantly
    * Minor bug fix in function calculating word count when there are no words in document

### Version 0.58

* Release Date: 2011-03-11

* Changes:

    * Added `try ... except ImportError` around `import wxversion` to catch people who don't have wx installed.

### Version: 0.57

  * Release Date: 2011-02-10

  * Changes:

    * Add blank line between block elements in Tools -> Markdown.

### Version: 0.56

  * Release Date: 2010-06-22

  * Changes:

    * Fixed small bug in Excel-to-table converter to trim extraneous white space from data rows.

### Version: 0.55

  * Release Date: 2010-06-07

  * Changes:

    * Changed alt-h-b-o (convert block to image) so that if you highlight an image source on one line with the title on the next line, the function formats both.


### Version: 0.54

  * Release Date: 2010-01-07

  * Changes:

    * Finally added icon
    * Removed extranous print statements from code

### Version: 0.53

  * Release Date: 2009-12-02

  * Changes:

    * Clean function now replaces multiple spaces with a single space

### Version: 0.52

  * Release Date: 2009-12-01

  * Changes:

    * Word Count now includes a separate count of non-blank lines

### Version: 0.51

  * Release Date: 2009-11-25

  * Changes:

    * Generated tables (new and convert) now include `thead` and `tbody` elements.

### Version: 0.5

  * Release Date: 2009-09-29

  * Changes:

    * Added fix_common_misspellings(), which automatically replaces commonly misspelled words with their correct spellings. Case sensitive.

### Version: 0.44

  * Release Date: 2009-09-28

  * Changes:

    * Updated check_last_update() to reflect change in pygithubapi (send over user, repo instead of URL).

### Version: 0.43

  * Release Date: 2009-09-25

  * Changes:

    * Added proxy support for `check_last_update()`.
    * PyGithubApi.py must be at least version 0.11 to work with this version of PyHtmlEdit.
    * Added `set_config(config)` to save configuration values in a pickled dictionary. Saves in a file called `pyhtmledit_config` in the same folder as `pyhtmledit.py`.
    * Added `get_config()` to get configuration values from a pickled dictionary

### Version: 0.42

  * Release Date: 2009-09-24

  * Changes:

    * added check_last_update() function, which uses [pygithubapi](http://quandyfactory.com/projects/25/pygithubapi) and is available as "Check Version" from About menu. It compares __version__ with the latest commit date in the GitHub API for the PyHtmlEdit repository.
    * Added __repository__ variable to top to link to public repository

### Version: 0.41

  * Release Date: 2009-09-22

  * Changes:

    * Modified Replace function to replace over entire document if no selection
    * Added release date to About page.

### Version: 0.4

  * Release Date: 2009-09-22

  * Changes:

    * Fixed bug in table creation code that was adding </tble> as closing tag.
    * Added a Replace function that takes a selection of text and replaces the value of `find` with the value of `replace`.
    * Added an SQL function that converts special SQL punctuation to entity codes.
    * Replaced CamelCase on function and method names to lowercase_with_underscores.
    * Changed Markdown function to stop closing </p> tag from going to a new line on Windows, and also adding a blank line after each paragraph.

### Version: 0.3

  * Release Date: 2009-08-07

  * Changes:

    * Added Tools function to convert markdown syntax into HTML. See note, below, for details.

### Version: 0.2

  * Release Date: 2009-08-06

  * Changes:

    * Replaced wx version kludge with wxversion.select()
    * Added html2text function from: [http://www.aaronsw.com/2002/html2text/][5]
    * Added an icon (webtools.ico)
    * Added a note in README to add a tutorial in the future
    * Included both a README.html and a README.txt

### Version: 0.1

  * Release Date: 2009-08-06

   [1]: mailto:ryan@quandyfactory.com

   [2]: http://quandyfactory.com/projects/2/pyhtmledit

   [3]: http://github.com/quandyfactory/PyHtmlEdit

   [4]: http://www.gnu.org/licenses/old-licenses/gpl-2.0.html

   [5]: https://pypi.org/project/html2text/

   [6]: https://pypi.org/project/markdown2/

   [7]: https://pypi.org/project/markdown2/

   [8]: http://wiki.wxpython.org/InstallingOnUbuntuOrDebian

   [9]: http://www.wxpython.org/docs/api/wxversion-module.html

   [10]: http://aspn.activestate.com/ASPN/Mail/Message/wxpython-users/3698130
