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

  * Version: 0.51

  * Release Date: 2009-11-25

## Revision History

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

## Requirements

  * Python 2.5 or newer (not Python 3) [http://www.python.org/](http://www.python.org/)
  * wxPython 2.8 [http://www.wxpython.org/](http://www.wxpython.org/)
  * python-markdown [http://www.freewisdom.org/projects/python-markdown/](http://www.freewisdom.org/projects/python-markdown/) or python-markdown2 [http://code.google.com/p/python-markdown2/](http://code.google.com/p/python-markdown2/)
  * pyyaml [http://pyyaml.org/](http://pyyaml.org/)

## Notes

### wxPython version

This program requires wxPython 2.8, and specifically makes use of the TextCtrl StringSelection property, which doesn't exist in wxPython 2.6.

My home system (Ubuntu 9.04 Jaunty) comes with wxPython 2.6 pre-installed, and apparently some basic system code depends on this older version, so I had to install 2.8 separately:

[http://wiki.wxpython.org/InstallingOnUbuntuOrDebian][8]

Unfortunately, when importing wx, Python grabs the older version by default, not the newer one. The solution is to import wxversion first, and select version 2.8, as per this example:

[http://www.wxpython.org/docs/api/wxversion-module.html][9]

Fixed from version 0.1.

### Markdown

This software does not come bundled with a markdown parser. It checks your system to see if you already have python-markdown installed.

[http://www.freewisdom.org/projects/python-markdown/][6]

If not, it checks to see if you have python-markdown2 installed.

[http://code.google.com/p/python-markdown2/][7]

Note: both modules are available through easy_install.

If you have one of these modules installed, it provides the ability to convert markdown syntax to HTML in the Tools menu. If you don't have either module installed, it simply doesn't offer that function.

Added in version 0.3.

Some time in the future, I might add support for PottyMouth as well.

### Missing Functionality

#### HTML Preview

A handy feature would be an HTML Preview so you can see what your code will look like.

#### Toggle Line Wrap

I'd like to be able to toggle between line wrapping and horizontal scrolling, but apparently you can't change the style wx.TE_MULTILINE on a TextCtrl after creating it. Instead, you would have to subclass the control and flip between two controls, one of which is set to wrap and the other set to scroll.

[http://aspn.activestate.com/ASPN/Mail/Message/wxpython-users/3698130][10]

So this is also on my list of things to do.

#### Add Words to spelling_dict {}

Right now, the spelling_dict is hard-coded, which means I need a version update just to add words and limits the ability of users to add their own words.

It would be better to check if the user has a spelling_dict file, load it if available, or else load the default spelling_dict if not available.


   [1]: mailto:ryan@quandyfactory.com

   [2]: http://quandyfactory.com/projects/2/pyhtmledit

   [3]: http://github.com/quandyfactory/PyHtmlEdit

   [4]: http://www.gnu.org/licenses/old-licenses/gpl-2.0.html

   [5]: http://www.aaronsw.com/2002/html2text/

   [6]: http://www.freewisdom.org/projects/python-markdown/'

   [7]: http://code.google.com/p/python-markdown2/

   [8]: http://wiki.wxpython.org/InstallingOnUbuntuOrDebian

   [9]: http://www.wxpython.org/docs/api/wxversion-module.html

   [10]: http://aspn.activestate.com/ASPN/Mail/Message/wxpython-users/3698130

