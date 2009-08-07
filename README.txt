# PyHtmlEdit README

PyHtmlEdit is a simple Python text editor optimized for the kinds of HTML
formatting that I commonly do.

## Author

  * Author: Ryan McGreal

  * Email: [ryan@quandyfactory.com][1]

  * Homepage: [http://quandyfactory.com/projects/pyhtmledit][2]

  * Repository: [http://github.com/quandyfactory/PyHtmlEdit][3]

PyHtmlEdit was assembled from stuff I found online and some functions I've
written.

## Licence

Released under the GNU General Public Licence, Version 2:

[http://www.gnu.org/licenses/old-licenses/gpl-2.0.html][4]

## This Version

  * Version: 0.2

  * Release Date: 2009-08-06

## Revision History

  * Version: 0.2

  * Release Date: 2009-08-06

  * Changes:

    * Replaced wx version kludge with wxversion.select()

    * Added html2text function from: [http://www.aaronsw.com/2002/html2text/][5]

    * Added an icon (webtools.ico)

    * Added a note in README to add a tutorial in the future

    * Included both a README.html and a README.txt

  * Version: 0.1

  * Release Date: 2009-08-06

## Requirements

  * Python 2.5 or newer

  * wxPython 2.8

## Notes

### wxPython version

This program requires wxPython 2.8, and specifically makes use of the TextCtrl
StringSelection property, which doesn't exist in wxPython 2.6.

My home system (Ubuntu 9.04 Jaunty) comes with wxPython 2.6 pre-installed, and
apparently some basic system code depends on this older version, so I had to
install 2.8 separately:

[http://wiki.wxpython.org/InstallingOnUbuntuOrDebian][6]

Unfortunately, when importing wx, Python grabs the older version by default,
not the newer one. The solution is to import wxversion first, and select
version 2.8, as per this example:

[http://www.wxpython.org/docs/api/wxversion-module.html][7]

Fixed from version 0.1.

### 2. Missing Functionality

#### Search/Replace

The most obvious missing function is any kind of search and search/replace.
That's one of the first things I'd like to add.

#### HTML Preview

Another handy feature would be an HTML Preview so you can see what your code
will look like.

#### Toggle Line Wrap

I'd like to be able to toggle between line wrapping and horizontal scrolling,
but apparently you can't change the style wx.TE_MULTILINE on a TextCtrl after
creating it. Instead, you would have to subclass the control and flip between
two controls, one of which is set to wrap and the other set to scroll.

[http://aspn.activestate.com/ASPN/Mail/Message/wxpython-users/3698130][8]

So this is also on my list of things to do.

#### Add a Tutorial

The tool is not complicated to use, and all the functionality is in the menus
across the stop. Still, it may be valuable to add a tutorial for new users who
are not used to it already.

   [1]: mailto:ryan@quandyfactory.com

   [2]: http://quandyfactory.com/projects/pyhtmledit

   [3]: http://github.com/quandyfactory/PyHtmlEdit

   [4]: http://www.gnu.org/licenses/old-licenses/gpl-2.0.html

   [5]: http://www.aaronsw.com/2002/html2text/

   [6]: http://wiki.wxpython.org/InstallingOnUbuntuOrDebian

   [7]: http://www.wxpython.org/docs/api/wxversion-module.html

   [8]: http://aspn.activestate.com/ASPN/Mail/Message/wxpython-users/3698130

