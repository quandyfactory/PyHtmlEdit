#!/usr/bin/env python

__version__ = 0.60
__releasedate__ = '2011-08-15'
__author__ = 'Ryan McGreal <ryan@quandyfactory.com>'
__homepage__ = 'http://quandyfactory.com/projects/2/pyhtmledit/'
__repository__ = 'http://github.com/quandyfactory/PyHtmlEdit'
__copyright__ = '(C) 2009 by Ryan McGreal. Licenced under GNU GPL 2.0\nhttp://www.gnu.org/licenses/old-licenses/gpl-2.0.html'

import sys

try:
    import wxversion
except ImportError:
    print "You must have the wxPython GUI library installed to use this application."
    sys.exit()
    
wxversion.select('2.8')
from wx import *

import re
import os
import pickle

# import html2text
path = os.path.dirname(sys.argv[0])
filepath = globals()['__file__']
abspath = os.path.abspath(path)
filename = filepath.replace(abspath, '').replace('\\', '').replace('/', '')

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

spelling_dict = {
    '50\'s': '\'50s',
    '60\'s': '\'60s',
    '70\'s': '\'70s',
    '80\'s': '\'80s',
    '90\'s': '\'90s',
    '??': '?',
    '  ': ' ',
    'acceptible': 'acceptable',
    'Acceptible': 'Acceptable',
    'accidently': 'accidentally',
    'Accidently': 'Accidentally',
    'agression': 'aggression',
    'Agression': 'Aggression',
    'arguement': 'argument',
    'Arguement': 'Argument',
    'balence': 'balance',
    'Balence': 'Balance',
    'baloon': 'balloon',
    'Baloon': 'Balloon',
    'buisness': 'business',
    'Buisness': 'Business',
    'bycicle': 'bicycle',
    'Bycicle': 'Bicycle',
    'cemetary': 'cemetery',
    'Cemetary': 'Cemetery',
    'cieling': 'ceiling',
    'Cieling': 'Ceiling',
    'conceed': 'concede',
    'Conceed': 'Concede',
    'concensus': 'consensus',
    'Concensus': 'Consensus',
    'Councilor': 'Councillor',
    'councilor': 'Councillor',
    'councillor': 'Councillor',
    'definate': 'definite',
    'Definate': 'Definite',
    'embarass': 'embarrass',
    'Embarass': 'Embarrass',
    'harrass': 'harass',
    'Harrass': 'Harass',
    'In order to': 'To',
    'in order to': 'to',
    'independant': 'independent',
    'Independant': 'Independent',
    'neighborhood': 'neighbourhood',
    'Neighborhood': 'Neighbourhood',
    'reccomend': 'recommend',
    'Reccomend': 'Recommend',
    'reccommend': 'recomment',
    'Reccomment': 'Recomment',
    'seperate': 'separate',
    'Seperate': 'Separate',
    'skillful': 'skilful',
    'Skillful': 'Skilful',
    'truely': 'truly',
    'Truely': 'Truly',
    'wierd': 'weird',
    'Wierd': 'Weird',
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

def remove_whitespace(text):
    """
    Remove all white space characters from a string
    """
    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', text)

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

def fix_common_misspellings(text):
    """
    Automatically replaces commonly misspelled words with their correct spellings. Case sensitive.
    """
    for k, v in spelling_dict.items():
        text = text.replace(k, v)
    return text


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

def remove_multiple_spaces(text):
    """
    Replaces multiple   spaces (like the spaces between "multiple" and "spaces") with one space.
    """
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text

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
        block_tags = '</p> </ul> </ol> </blockquote> </h1> </h2> </h3> </h4> </h5> </h6> </div>'.split(' ')
        for tag in block_tags:
            markeddown = markeddown.replace(tag, '%s%s' % (tag, '\n'))

        markeddown = markeddown.replace('\n\n\n', '\n\n') # get rid of triple spaces between paragraphs on Windows
        return markeddown
    else:
        return text

def clean_it(text):
    """
    Takes a text string, applies the kill_gremlins function to replace cp1252 characters with Unicode, then runs the cleanchars filter
    """
    text = kill_gremlins(text)
    text = remove_multiple_spaces(text)
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
        #print 'href starts with ' + attributes['href'][0:4].lower()
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
            output.append('  <thead>')
        output.append('    <tr>%s' % comment)
        for col in range(cols):
            output.append('      <%s></%s>' % (tag, tag))

        if row == 0:
            output.append('  </head>')
            output.append('  <tbody>')
        output.append('    </tr>')
    output.append('  </tbody>')
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
ID_MISSPELLINGS = 46
#ID_STATUSBAR = 47

# The basic code for this came from a free example I found somewhere online.
# Unfortunately I've forgotten where I got it, so I can't attribute it properly.
# If you recognize where this comes from, please let me know!
class MainWindow(Frame):
    def __init__(self,parent,title):
        # based on a frame, so set up the frame
        Frame.__init__(self, parent, ID_ANY, title, size=(600,400))

        self.encoding = 'utf-8'
        self.wxencoding = FONTENCODING_UTF8

        # set icon

        #print filename
        #print abspath

        iconfile = 'webtools.ico'
        filepath = os.path.abspath(__file__).replace(filename, '')
        iconpath = '%s%s' % (filepath, iconfile)
        icon = Icon(iconpath, BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Add a text editor and a status bar
        # Each of these is within the current instance
        # so that we can refer to them later.
        self.control = TextCtrl(self, 1, style=TE_MULTILINE | TE_AUTO_URL | TE_NOHIDESEL)
        controlfont = Font(10, FONTFAMILY_TELETYPE, NORMAL, NORMAL) #, encoding = self.wxencoding)
        #self.control.SetWindowStyleFlag(TE_NOHIDESEL)
        self.control.SetFont(controlfont)
        #self.control.SetLeftIndent(10)
        #self.control.SetRightIndent(10)

        # status bar
        self.CreateStatusBar() # A Statusbar in the bottom of the window
        self.SetStatusText('Chars: 0 | Words: 0 | Lines: 1 | Non-Blank Lines: 0')

        # Setting up the menu. filemenu is a local variable at this stage.
        filemenu = Menu()
        # use ID_ for future easy reference - much better that "48", "404" etc
        # The & character indicates the short cut key
        filemenu.Append(ID_OPEN, "&Open"," Open a file to edit")
        filemenu.AppendSeparator()
        filemenu.Append(ID_SAVE, "&Save"," Save file")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")

        inline_menu = Menu()
        inline_menu.Append(ID_CITE, "&cite", "Citation")
        inline_menu.Append(ID_EM, "&em", "Emphasis")
        inline_menu.Append(ID_CODE, "c&ode","Programming code")
        inline_menu.Append(ID_SPAN, "spa&n","generic inline element")
        inline_menu.Append(ID_STRONG, "&strong", "Strong emphasis")
        inline_menu.Append(ID_SUB, "su&b","Subscript")
        inline_menu.Append(ID_SUP, "su&p","Superscript")

        block_menu = Menu()
        block_menu.Append(ID_BLOCKQUOTE, "&blockquote", "Block quotation")
        block_menu.Append(ID_DIV, "&div", "Generic block element")
        block_menu.Append(ID_P, "&p", "Paragraph")
        block_menu.Append(ID_PINITIAL, "p.&initial", "First paragraph in an article or section")
        block_menu.Append(ID_PPHOTO, "p.ph&oto", "Paragraph with photo")
        block_menu.Append(ID_PRE, "pr&e", "Preformatted block text")

        heading_menu = Menu()
        heading_menu.Append(ID_H1, "h&1", "Heading 1")
        heading_menu.Append(ID_H2, "h&2", "Heading 2")
        heading_menu.Append(ID_H3, "h&3", "Heading 3")
        heading_menu.Append(ID_H4, "h&4", "Heading 4")
        heading_menu.Append(ID_H5, "h&5", "Heading 5")
        heading_menu.Append(ID_H6, "h&6", "Heading 6")

        link_menu = Menu()
        link_menu.Append(ID_A, "&a", "Anchor")
        link_menu.Append(ID_HREF, "a &href", "Hyperlink")

        nested_menu = Menu()
        nested_menu.Append(ID_OL, "&ol", "Ordered list")
        nested_menu.Append(ID_UL, "&ul", "Unordered List")
        nested_menu.Append(ID_TABLECONVERT, "table (&convert)", "Convert existing tab data to a table")
        nested_menu.Append(ID_TABLENEW, "table (&new)", "Create new empty table with 4 rows and 4 columns")

        htmlmenu = Menu()
        htmlmenu.AppendMenu(ID_INLINEMENU, "&Inline", inline_menu)
        htmlmenu.AppendSeparator()
        htmlmenu.AppendMenu(ID_BLOCKMENU, "&Block", block_menu)
        htmlmenu.AppendSeparator()
        htmlmenu.AppendMenu(ID_HEADINGMENU, "&Heading", heading_menu)
        htmlmenu.AppendSeparator()
        htmlmenu.AppendMenu(ID_LINKMENU, "&Link", link_menu)
        htmlmenu.AppendSeparator()
        htmlmenu.AppendMenu(ID_NESTEDMENU, "&Nested", nested_menu)

        format_menu = Menu()
        #format_menu.Append(ID_SWITCHMODE, "Switch &Mode", "Alternate between Edit Mode and Preview Mode")
        #format_menu.AppendSeparator()
        format_menu.Append(ID_REPLACE, '&Replace', 'Find and Replace a search string')
        format_menu.AppendSeparator()
        format_menu.Append(ID_LCASE, "&lcase", "Convert text to lowercase")
        format_menu.Append(ID_UCASE, "&UCASE", "Convert text to uppercase")
        format_menu.Append(ID_PCASE, "&Pcase", "Convert text to proper case (capitalized)")
        format_menu.AppendSeparator()
        format_menu.Append(ID_CLEAN, "&Clean", "Clean up MS Word characters and multiple spaces")
        format_menu.Append(ID_SQL, "&SaferSQL", "Replace SQL punctuation with entity codes")
        format_menu.Append(ID_MISSPELLINGS, 'Common &Misspellings', 'Replace commonly misspelled words with the correct spelling')

        tools_menu = Menu()
        #tools_menu.Append(ID_WORDCOUNT, "&Word Count", "Word count, line count, etc.")
        tools_menu.Append(ID_strip_html, "&Strip HTML", "Remove all HTML elements and leave the text")
        tools_menu.Append(ID_HTML2TEXT, "&Html2Text", "Convert HTML into Markdown-formatted plain text")
        if markdown != False:
            tools_menu.Append(ID_MARKDOWN, "&Markdown", "Convert Markdown-formatted plain text into HTML")

        about_menu = Menu()
        about_menu.Append(ID_ABOUT, "&About PyHtmlEdit","Information about this program")
        if github is not False:
            about_menu.Append(ID_UPDATED, "&Check Version","Checks this program's GitHub repository to see if there is a newer version.")

        # Creating the menubar.
        menuBar = MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(htmlmenu, "&HTML")
        menuBar.Append(format_menu, "F&ormat")
        menuBar.Append(tools_menu, "&Tools")
        menuBar.Append(about_menu, "&About")

        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Define the code to be run when a menu option is selected
        EVT_MENU(self, ID_ABOUT, self.on_about)
        EVT_MENU(self, ID_EXIT, self.on_exit)
        EVT_MENU(self, ID_OPEN, self.on_open)
        EVT_MENU(self, ID_SAVE, self.on_save)
        EVT_MENU(self, ID_STRONG, self.on_strong)
        EVT_MENU(self, ID_EM, self.on_em)
        EVT_MENU(self, ID_SPAN, self.on_span)
        EVT_MENU(self, ID_CITE, self.on_cite)
        EVT_MENU(self, ID_SUB, self.on_sub)
        EVT_MENU(self, ID_SUP, self.on_sup)
        EVT_MENU(self, ID_CODE, self.on_code)
        EVT_MENU(self, ID_DIV, self.on_div)
        EVT_MENU(self, ID_P, self.on_p)
        EVT_MENU(self, ID_PPHOTO, self.on_photo)
        EVT_MENU(self, ID_PINITIAL, self.on_p_initial)
        EVT_MENU(self, ID_BLOCKQUOTE, self.on_blockquote)
        EVT_MENU(self, ID_PRE, self.on_pre)
        EVT_MENU(self, ID_H1, self.on_h1)
        EVT_MENU(self, ID_H2, self.on_h2)
        EVT_MENU(self, ID_H3, self.on_h3)
        EVT_MENU(self, ID_H4, self.on_h4)
        EVT_MENU(self, ID_H5, self.on_h5)
        EVT_MENU(self, ID_H6, self.on_h6)
        EVT_MENU(self, ID_A, self.on_a)
        EVT_MENU(self, ID_HREF, self.on_href)
        EVT_MENU(self, ID_UL, self.on_ul)
        EVT_MENU(self, ID_OL, self.on_ol)
        EVT_MENU(self, ID_TABLENEW, self.on_table_new)
        EVT_MENU(self, ID_TABLECONVERT, self.on_table_convert)
        EVT_MENU(self, ID_UCASE, self.on_ucase)
        EVT_MENU(self, ID_LCASE, self.on_lcase)
        EVT_MENU(self, ID_PCASE, self.on_pcase)
        EVT_MENU(self, ID_CLEAN, self.on_clean)
        EVT_MENU(self, ID_WORDCOUNT, self.on_word_count)
        EVT_MENU(self, ID_strip_html, self.on_strip_html)
        EVT_MENU(self, ID_TOGGLEWRAP, self.on_toggle_wrap)
        EVT_MENU(self, ID_SWITCHMODE, self.on_switch_mode)
        EVT_MENU(self, ID_HTML2TEXT, self.on_html2text)
        EVT_MENU(self, ID_MARKDOWN, self.on_markdown)
        EVT_MENU(self, ID_SQL, self.on_sql)
        EVT_MENU(self, ID_REPLACE, self.on_replace)
        EVT_MENU(self, ID_UPDATED, self.on_updated)
        EVT_MENU(self, ID_MISSPELLINGS, self.on_misspelling)

        # catch key up events to update statusbar
        self.control.Bind(EVT_KEY_UP, self.update_statusbar) 

        self.Show(1)

        self.aboutme = MessageDialog(self, "PyHtmlEdit is a simple HTML editor written in Python using the wxPython GUI library (v2.8).\n\nCreated by %s\n\nVersion %s, Released on %s\n\n%s\n\nHomepage: %s" % (__author__, __version__, __releasedate__, __copyright__, __homepage__), "About PyHtmlEdit", OK)
        self.doiexit = MessageDialog(self, "Are you sure you want to exit? \n", "Confirm Exit", YES_NO)

        self.dirname = ''

    def on_updated(self,e):
        """
        Checks the github repository to see if a newer version is available.
        """
        github_user = 'quandyfactory'
        github_repo = 'PyHtmlEdit'
        config = get_config()

        try:
            proxy = config['proxy']
        except:
            proxy = ''

        if proxy != '':
            proxies = {'http': proxy }
            last_updated = check_last_update(user=github_user, repo=github_repo, proxies=proxies)
        else:
            last_updated = check_last_update(user=github_user, repo=github_repo)

        if last_updated == 'no connection':
            dlg_proxy = TextEntryDialog(self,
                'This program cannot connect to the internet.\n\n' +
                'If you know the http proxy server and port, you can enter it here to see if that works.',
                'No Connection to Internet',
                defaultValue=proxy
                )

            dlg_proxy.SetValue("")

            if dlg_proxy.ShowModal() == ID_OK:
                proxy = dlg_proxy.GetValue()
                if proxy[:7] != 'http://':
                    proxy = 'http://' + proxy
                proxies = { 'http': proxy }
                last_updated = check_last_update(user=github_user, repo=github_repo, proxies=proxies)
                config['proxy'] = proxy
                set_config(config)

        if last_updated == 'no connection':
            self.uptodate = MessageDialog(self, "Sorry, but the proxy connection did not work.\n\nHey, it was worth a try.", "No Connection to Internet", OK)
            self.uptodate.ShowModal()
        elif last_updated == 'current':
            self.uptodate = MessageDialog(self, "Your version of PyHtmlEdit is up to date.\n", "Version is Current", OK)
            self.uptodate.ShowModal()
        else:
            self.uptodate = MessageDialog(self, "A newer version of PyHtmlEdit was published on %s.\n\nYou can download it from here:\n\n%s" % (last_updated, __repository__), "Newer Version Available", OK)
            self.uptodate.ShowModal()



    def on_about(self,e):
        """
        Show About page as a dialog.
        """
        self.aboutme.ShowModal()

    def on_exit(self,e):
        """
        Exit the program
        """
        igot = self.doiexit.ShowModal()
        if igot == ID_YES:
            self.Close(True)

    def on_open(self,e):
        """
        Open a file.
        """
        dlg = FileDialog(self, "Choose a file", self.dirname, "", "*.*", OPEN)
        if dlg.ShowModal() == ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            filehandle=open(os.path.join(self.dirname, self.filename),'r')
            self.control.SetValue(filehandle.read())
            filehandle.close()
            self.SetTitle('PyHtmlEdit: Editing "%s"' % self.filename)
        dlg.Destroy()

    def on_save(self,e):
        """
        Save the file.
        """
        dlg = FileDialog(self, "Choose a file", self.dirname, "", "*.*", \
                SAVE | OVERWRITE_PROMPT)
        if dlg.ShowModal() == ID_OK:
            itcontains = self.control.GetValue()
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            filehandle=open(os.path.join(self.dirname, self.filename),'w')
            filehandle.write(itcontains)
            filehandle.close()
        dlg.Destroy()

    def on_misspelling(self,e):
        """
        Replace common misspellings with correct spelling.
        """
        self.control.WriteText(fix_common_misspellings(self.control.StringSelection))


    def on_strong(self,e):
        """
        Wrap <strong> element around selection
        """
        self.control.WriteText(tag_it('strong', self.control.StringSelection))

    def on_em(self,e):
        self.control.WriteText(tag_it('em', self.control.StringSelection))

    def on_cite(self,e):
        self.control.WriteText(tag_it('cite', self.control.StringSelection))

    def on_span(self,e):
        self.control.WriteText(tag_it('span', self.control.StringSelection))

    def on_sub(self,e):
        self.control.WriteText(tag_it('sub', self.control.StringSelection))

    def on_sup(self,e):
        self.control.WriteText(tag_it('sup', self.control.StringSelection))

    def on_code(self,e):
        self.control.WriteText(tag_it('code', self.control.StringSelection))

    def on_p(self,e):
        self.control.WriteText(tag_it('p', self.control.StringSelection))

    def on_photo(self,e):
        twolines = self.control.StringSelection.split('\n')
        src = twolines[0].strip()
        try: alt = twolines[1].strip()
        except: alt = ''
        self.control.WriteText('<p class="photo">\n<img src="%s" alt="%s" title="%s"><br>\n%s</p>\n' % (src, alt, alt, alt))

    def on_p_initial(self,e):
        self.control.WriteText(tag_it('p', self.control.StringSelection, attributes = {'class':'initial'}))

    def on_blockquote(self,e):
        self.control.WriteText(tag_it('blockquote', self.control.StringSelection, block = True))

    def on_div(self,e):
        self.control.WriteText(tag_it('div', self.control.StringSelection, block = True))

    def on_pre(self,e):
        self.control.WriteText(tag_it('pre', self.control.StringSelection, block = True))

    def on_h1(self,e):
        self.control.WriteText(tag_it('h1', self.control.StringSelection))

    def on_h2(self,e):
        self.control.WriteText(tag_it('h2', self.control.StringSelection))

    def on_h3(self,e):
        self.control.WriteText(tag_it('h3', self.control.StringSelection))

    def on_h4(self,e):
        self.control.WriteText(tag_it('h4', self.control.StringSelection))

    def on_h5(self,e):
        self.control.WriteText(tag_it('h5', self.control.StringSelection))

    def on_h6(self,e):
        self.control.WriteText(tag_it('h6', self.control.StringSelection))

    def on_a(self,e):
        dialog = TextEntryDialog(self, 'Enter anchor name: ', 'Anchor Name', '')
        dialog.ShowModal()
        named = dialog.GetValue()
        self.control.WriteText(tag_it('a', self.control.StringSelection, attributes = {'name': named, }))

    def on_href(self,e):
        dialog = TextEntryDialog(self, 'Enter the HREF:', 'Hyper-Reference', '')
        dialog.ShowModal()
        href = dialog.GetValue()
        self.control.WriteText(tag_it('a', self.control.StringSelection, attributes = {'href': href, }))

    def on_ul(self,e):
        self.control.WriteText(list_it('ul', self.control.StringSelection))

    def on_ol(self,e):
        self.control.WriteText(list_it('ol', self.control.StringSelection, attributes = {'type':'1',}))

    def on_table_new(self,e):
        self.control.WriteText(make_table('Table Caption', 4, 4))

    def on_table_convert(self,e):
        dialog = TextEntryDialog(self, 'Enter a Table Caption:', 'Table Caption', '')
        dialog.ShowModal()
        caption = dialog.GetValue()
        tdata = self.control.StringSelection.split('\n')
        output = []
        addline = output.append
        addline('<table>')
        addline('<caption>%s</caption>' % caption)
        for row in tdata:
            if row.strip() != '':
                cells = row.strip().split('\t')
                tag = 'td'; comment = ''
                if tdata.index(row) == 0:
                    tag = 'th'; comment = '<!-- first row has table headings -->'
                    addline('  <thead>')
                addline('    <tr>')
                for cell in cells:
                    addline('      <%s>%s</%s>' % (tag, cell, tag))
                if tdata.index(row) == 0:
                    addline('  </thead>')
                    addline('  <tbody>')
                addline('    </tr>')
        addline('  </tbody>')
        addline('</table>')
        self.control.WriteText('\n'.join(output))

    def on_ucase(self,e):
        self.control.WriteText(self.control.StringSelection.upper())

    def on_lcase(self,e):
        self.control.WriteText(self.control.StringSelection.lower())

    def on_pcase(self,e):
        self.control.WriteText(' '.join([w.capitalize() for w in self.control.StringSelection.split(' ')]))

    def on_html2text(self,e):
        self.control.WriteText(html2text_it(self.control.StringSelection))

    def on_markdown(self,e):
        self.control.WriteText(markdown_it(self.control.StringSelection))

    def on_sql(self,e):
        self.control.WriteText(safer_sql(self.control.StringSelection))

    def on_clean(self,e):
        dirtytext = self.control.StringSelection
        cleantext = clean_it(dirtytext)
        self.control.WriteText(cleantext)

    def on_word_count(self, e, status=False):
        # first, try to get the selected text
        selection = self.control.StringSelection
        # if no selected text, use entire document
        if len(selection) == 0:
            selection = self.control.Value
        # get count of lines
        linelist = selection.split('\n')
        lines = len(linelist)
        # get count of active lines
        activelines = 0
        for line in linelist:
            if line != '': activelines += 1
        # get count of characters
        chars = len(selection)
        # remove HTML tags
        selection = strip_html(selection)
        # convert tabs and line breaks to spaces
        selection = selection.replace('\n', ' ')
        selection = selection.replace('\t', ' ')
        #eliminates multiple spaces between words
        while '  ' in selection:
            selection = selection.replace('  ', ' ')
        # split selection into a list of words
        wordlist = selection.split(' ')
        # get count of words
        nonblanks = remove_whitespace(selection)
        if len(nonblanks) == 0:
            words = 0
        else:
            words = len(wordlist)
        if status == False:
            msg = MessageBox('Chars: %s\nWords: %s\nLines: %s\nNon-Blank Lines: %s' % (chars, words, lines, activelines), 'Word Count')
        else:
            return 'Chars: %s | Words: %s | Lines: %s | Non-Blank Lines: %s' % (chars, words, lines, activelines)

    def update_statusbar(self, e):
        text = self.on_word_count(e, status=True)
        self.SetStatusText(text)

    def on_strip_html(self,e):
        self.control.WriteText(strip_html(self.control.StringSelection))

    def on_toggle_wrap(self,e):
        msg = MessageBox('Line Wrap toggle not implemented yet', 'Line Wrap')

    def on_switch_mode(self,e):
        pass

    def on_replace(self,e):
        """
        Asks for a find string and a replace string, and replaces the former with the latter
        """
        dlg_find = TextEntryDialog(self, 'Text to find', 'Find')
        dlg_find.SetValue("")
        if dlg_find.ShowModal() == ID_OK:
            find = dlg_find.GetValue()
            dlg_find.Destroy()
            dlg_replace = TextEntryDialog(self, 'Text to replace', 'Replace')
            dlg_replace.SetValue("")
            if dlg_replace.ShowModal() == ID_OK:
                replace = dlg_replace.GetValue()
                dlg_replace.Destroy()
        if find != '':
            self.control.WriteText(replace_it(find, replace, self.control.StringSelection))


# Set up a window based app, and create a main window in it
app = PySimpleApp()
view = MainWindow(None, "PyHtmlEdit")
# Enter event loop
app.MainLoop()