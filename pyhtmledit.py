#!/usr/bin/env python

__version__ = 0.44
__releasedate__ = '2009-09-28'
__author__ = 'Ryan McGreal <ryan@quandyfactory.com>'
__homepage__ = 'http://quandyfactory.com/projects/2/pyhtmledit/'
__repository__ = 'http://github.com/quandyfactory/PyHtmlEdit'
__copyright__ = '(C) 2009 by Ryan McGreal. Licenced under GNU GPL 2.0\nhttp://www.gnu.org/licenses/old-licenses/gpl-2.0.html'

import wxversion
wxversion.select('2.8')
import sys
import wx
import re
import os
import pickle

# import html2text
path = os.path.dirname(sys.argv[0])
abspath = os.path.abspath(path)
print abspath
sys.path.extend([abspath, abspath + '/pygithubapi'])

import html2text
h2txt = html2text.html2text

config_filepath = abspath + '/pyhtmledit_config'

#import pygithubapi
try:
    import pygithubapi as github
except:
    github = False

# allow users to convert markdown to HTML if they have markdown or markdown2 installed
# initialize markdown marker
markdown = False 

# try importing markdown
try:
	from markdown import markdown
except:
	markdown = False

# try importing markdown2
if markdown == False:
	try:
		from markdown2 import markdown
	except:
		markdown = False

# the following hash table and kill_gremlins function are courtesy:
# http://effbot.org/zone/unicode-gremlins.htm
cp1252 = {
    # from http://www.microsoft.com/typography/unicode/1252.htm
    u"\x80": u"\u20AC", # EURO SIGN
    u"\x82": u"\u201A", # SINGLE LOW-9 QUOTATION MARK
    u"\x83": u"\u0192", # LATIN SMALL LETTER F WITH HOOK
    u"\x84": u"\u201E", # DOUBLE LOW-9 QUOTATION MARK
    u"\x85": u"\u2026", # HORIZONTAL ELLIPSIS
    u"\x86": u"\u2020", # DAGGER
    u"\x87": u"\u2021", # DOUBLE DAGGER
    u"\x88": u"\u02C6", # MODIFIER LETTER CIRCUMFLEX ACCENT
    u"\x89": u"\u2030", # PER MILLE SIGN
    u"\x8A": u"\u0160", # LATIN CAPITAL LETTER S WITH CARON
    u"\x8B": u"\u2039", # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    u"\x8C": u"\u0152", # LATIN CAPITAL LIGATURE OE
    u"\x8E": u"\u017D", # LATIN CAPITAL LETTER Z WITH CARON
    u"\x91": u"\u2018", # LEFT SINGLE QUOTATION MARK
    u"\x92": u"\u2019", # RIGHT SINGLE QUOTATION MARK
    u"\x93": u"\u201C", # LEFT DOUBLE QUOTATION MARK
    u"\x94": u"\u201D", # RIGHT DOUBLE QUOTATION MARK
    u"\x95": u"\u2022", # BULLET
    u"\x96": u"\u2013", # EN DASH
    u"\x97": u"\u2014", # EM DASH
    u"\x98": u"\u02DC", # SMALL TILDE
    u"\x99": u"\u2122", # TRADE MARK SIGN
    u"\x9A": u"\u0161", # LATIN SMALL LETTER S WITH CARON
    u"\x9B": u"\u203A", # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    u"\x9C": u"\u0153", # LATIN SMALL LIGATURE OE
    u"\x9E": u"\u017E", # LATIN SMALL LETTER Z WITH CARON
    u"\x9F": u"\u0178", # LATIN CAPITAL LETTER Y WITH DIAERESIS
}

# hash of SQL punctuation and matching entity codes
SQLReplace = {
    u"'": u"&#39;",
    u"\"": u"&#34;",
    u"%": u"&#37;",
    u"*": u"&#42;",
    u"[": u"&#91;",
    u"]": u"&#93;",
}

def get_config():
    """
    Gets application config data.
    """
    try:
        # see if there is a config file
        fread = file(config_filepath, 'r')
    except:
        # no config file, so create an empty one
        fwrite = file(config_filepath, 'w')
        config = {}
        pickle.dump(config, fwrite)
        fwrite.close()
        fread = file(config_filepath, 'r')
    # get config hash table
    config = pickle.load(fread)
    return config
    
def set_config(config):
    """
    Saves appplication config data.
    """
    # check if config is a dictionary
    if type(config).__name__ == 'dict':
        fwrite = file(config_filepath, 'w')
        pickle.dump(config, fwrite)
    else:
        raise TypeError, (type(b).__name__, 'Error: config must be a dictionary')
    

def kill_gremlins(text):
    """
    Map cp1252 gremlins to real unicode characters
    """
    if re.search(u"[\x80-\x9f]", text):
        def fixup(m):
            s = m.group(0)
            return cp1252.get(s, s)
        if isinstance(text, type("")):
            # make sure we have a unicode string
            text = unicode(text, "iso-8859-1")
        text = re.sub(u"[\x80-\x9f]", fixup, text)
    return text
    
# catch funky punctuation and replace with ascii
CleanChars = {
    u'\u2026': u'...',# HORIZONTAL ELLIPSIS
    u'\u2018': u'\'', # LEFT SINGLE QUOTATION MARK
    u'\u2019': u'\'', # RIGHT SINGLE QUOTATION MARK
    u'\u201C': u'"',  # LEFT DOUBLE QUOTATION MARK
    u'\u201D': u'"',  # RIGHT DOUBLE QUOTATION MARK
    u'\u2013': u'-',  # EN DASH
    u'\u2014': u'-',  # EM DASH
}

def check_last_update(user='', repo='', proxies = {}):
    """
    Compares the last commit date in the GitHub repository using pygithubapi to __releasedate__.
    """
    try:
        last_update = github.get_last_commit(user=user, repo=repo, proxies=proxies)
    except:
        return 'no connection'
    
    if last_update > __releasedate__:
        return last_update
    else:
        return 'current'

def replace_it(find, replace, selection):
    """
    Takes a selection of text and replaces the value of find with the value of replace.
    """
    return selection.replace(find, replace)

def markdown_it(text):
    """
    Converts markdown syntax to HTML if it's installed
    """
    if markdown != False:
        markeddown = markdown(text)
        markeddown = markeddown.replace('\n</p>', '</p>\n') # fix bug in Windows
        return markeddown
    else:
        return text

def clean_it(text):
    """
    Takes a text string, applies the kill_gremlins function to replace cp1252 characters with Unicode, then runs the cleanchars filter
    """
    text = kill_gremlins(text)
    for k, v in CleanChars.items(): 
        text = text.replace(k, v)
    return text

def safer_sql(text):
    """
    Replaces SQL punctuation with entity codes
    """
    text = clean_it(text)
    for k, v in SQLReplace.items(): 
        text = text.replace(k, v)
    return text

def strip_html(stuff):
    """
    Takes a string with HTML tags and returns the string with the HTML tags removed.
    """
    import re
    return re.sub(r'<[^>]*?>', '', stuff) 

def make_attlist(attributes):
    """
    Takes a diction_ary of HTML attributes and returns a list of attribute names and values to go inside an HTML tag.
    """
    return ' ' + ' '.join(['%s="%s"' % (k, v) for k, v in attributes.items()])

def html2text_it(stuff):
    """
    Uses Aaron Swartz's clever html2text to convert HTML into Markdown-formatted plain text
    """
    return h2txt(stuff)

def tag_it(tag, text, block = False, attributes = {}):
    """
    Takes a selection of text and returns the selection wrapped in HTML tags.
    Also takes an option_al diction_ary of attributes to include in the opening tag.
    """
    atts = ''
    if 'href' in attributes: 
        print 'href starts with ' + attributes['href'][0:4].lower()
        if attributes['href'][0:4].lower() == 'http':
            attributes['target'] = '_blank'
    if attributes != {}: atts = make_attlist(attributes)
    if block == False:
        return '<%s%s>%s</%s>' % (tag, atts, text.rstrip(), tag)
    else:
        return '<%s%s>\n%s\n</%s>\n' % (tag, atts, text.rstrip(), tag)

def list_it(tag, liststring, attributes = {}):
    """
    Takes either "ul" or "ol" and a string with line breaks ('\n') and returns as an HTML list.
    Also takes an option_al diction_ary of attributes to include in the opening tag.
    """
    list = liststring.split('\n')
    atts = ''
    if attributes != {}: atts = make_attlist(attributes)
    output = []
    output.append('<%s%s>' % (tag, atts))
    for item in list:
        output.append('<li>%s</li>' % item)
    output.append('</%s>' % tag)
    return '\n'.join(output)
    
def make_table(caption, rows, cols, attributes = {}):
    """
    Takes a caption string and integer numbers of rows and cols, and returns an empty HTML table.
    Also takes an option_al diction_ary of attributes to include in the opening tag.
    """
    atts = ''
    if attributes != {}: atts = make_attlist(attributes)
    output = []
    output.append('<table%s>' % atts)
    output.append('  <caption>%s</caption>' % caption)
    for row in range(rows):
        tag = 'td'; comment = ''
        if row == 0:
            comment = ' <!-- first row has table headings -->'
            tag = 'th'
        output.append('  <tr>%s' % comment)
        for col in range(cols):
            output.append('    <%s></%s>' % (tag, tag))
        output.append('  </tr>')
    output.append('</table>')
    return '\n'.join(output)

# Set up some button numbers for the menu

ID_ABOUT=101
ID_OPEN=102
ID_SAVE=103
ID_BUTTON1=300
ID_EXIT=200
ID_STRONG = 1
ID_EM = 2
ID_CITE = 3
ID_SUB = 4
ID_SUP = 5
ID_CODE = 6
ID_CUSTOM = 7
ID_P = 8
ID_PPHOTO = 9
ID_BLOCKQUOTE = 10
ID_PRE = 11
ID_H1 = 12
ID_H2 = 13
ID_H3 = 14
ID_H4 = 15
ID_H5 = 16
ID_H6 = 17
ID_A = 18
ID_HREF = 19
ID_UL = 20
ID_OL = 21
ID_TABLENEW = 22
ID_TABLECONVERT = 23
ID_UCASE = 24
ID_LCASE = 25
ID_PCASE = 26
ID_CLEAN = 27
ID_WORDCOUNT = 28
ID_strip_html = 29
ID_MAKEBLOG = 30
ID_DIV = 31
ID_INLINEMENU = 32
ID_BLOCKMENU = 33
ID_LINKMENU = 34
ID_NESTEDMENU = 35
ID_HEADINGMENU = 35
ID_SPAN = 36
ID_ABOUTMENU = 37
ID_TOGGLEWRAP = 38
ID_PINITIAL = 39
ID_SWITCHMODE = 40
ID_HTML2TEXT = 41
ID_MARKDOWN = 42
ID_SQL = 43
ID_REPLACE = 44
ID_UPDATED = 45

# The basic code for this came from a free example I found somewhere online.
# Unfortunately I've forgotten where I got it, so I can't attribute it properly.
# If you recognize where this comes from, please let me know!
class MainWindow(wx.Frame):
    def __init__(self,parent,title):
        # based on a frame, so set up the frame
        wx.Frame.__init__(self,parent,wx.ID_ANY, title, size=(300,300))
        
        self.encoding = 'utf-8'
        # self.encoding = 'iso-8859-1'
        self.wxencoding = wx.FONTENCODING_UTF8
        # self.wxencoding = wx.FONTENCODING_ISO8859_1
        
        #wx.SetDefaultPyEncoding(self.encoding)

        # Add a text editor and a status bar
        # Each of these is within the current instance
        # so that we can refer to them later.
        self.control = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE | wx.TE_AUTO_URL | wx.TE_NOHIDESEL)
        controlfont = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL) #, encoding = self.wxencoding)
        #self.control.SetWindowStyleFlag(wx.TE_NOHIDESEL)
        self.control.SetFont(controlfont)
        #self.control.SetLeftIndent(10)
        #self.control.SetRightIndent(10)
        self.CreateStatusBar() # A Statusbar in the bottom of the window
        
        # Setting up the menu. filemenu is a local variable at this stage.
        filemenu = wx.Menu()
        # use ID_ for future easy reference - much better that "48", "404" etc
        # The & character indicates the short cut key
        filemenu.Append(ID_OPEN, "&Open"," Open a 