#!/usr/bin/env python

__version__ = 0.3
__author__ = "Ryan McGreal ryan@quandyfactory.com"
__homepage__ = "http://quandyfactory.com/projects/pyhtmledit/"
__copyright__ = "(C) 2009 Ryan McGreal. GNU GPL 2."

import sys

# old kludge to get the python interpreter to use wx2.8 instead of wx2.6
#try:
#    sys.path.remove('/usr/lib/python2.6/dist-packages/wx-2.6-gtk2-unicode')
#except:
#    pass

import wxversion
wxversion.select('2.8')

import wx
import re
import os

# import html2text
path = os.path.dirname(sys.argv[0])
abspath = os.path.abspath(path)
sys.path.append(abspath)
import html2text
h2txt = html2text.html2text


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


# the following hash table and KillGremlins function are courtesy:
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

def KillGremlins(text):
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

def MarkdownIt(text):
    """
    Converts markdown syntax to HTML if it's installed
    """
    if markdown != False:
        return markdown(text)
    else:
        return text

def CleanIt(text):
    """
    Takes a text string, applies the KillGremlins function to replace cp1252 characters with Unicode, then runs the cleanchars filter
    """
    text = KillGremlins(text)
    for k, v in CleanChars.items(): text = text.replace(k, v)
    return text


def StripHtml(stuff):
    """
    Takes a string with HTML tags and returns the string with the HTML tags removed.
    """
    import re
    return re.sub(r'<[^>]*?>', '', stuff) 

def AttList(attributes):
    """
    Takes a dictionary of HTML attributes and returns a list of attribute names and values to go inside an HTML tag.
    """
    return ' ' + ' '.join(['%s="%s"' % (k, v) for k, v in attributes.items()])

def Html2TextIt(stuff):
    """
    Uses Aaron Swartz's clever html2text to convert HTML into Markdown-formatted plain text
    """
    return h2txt(stuff)

def TagIt(tag, text, block = False, attributes = {}):
    """
    Takes a selection of text and returns the selection wrapped in HTML tags.
    Also takes an optional dictionary of attributes to include in the opening tag.
    """
    atts = ''
    if 'href' in attributes: 
        print 'href starts with ' + attributes['href'][0:4].lower()
        if attributes['href'][0:4].lower() == 'http':
            attributes['target'] = '_blank'
    if attributes != {}: atts = AttList(attributes)
    if block == False:
        return '<%s%s>%s</%s>' % (tag, atts, text.rstrip(), tag)
    else:
        return '<%s%s>\n%s\n</%s>\n' % (tag, atts, text.rstrip(), tag)

def ListIt(tag, liststring, attributes = {}):
    """
    Takes either "ul" or "ol" and a string with line breaks ('\n') and returns as an HTML list.
    Also takes an optional dictionary of attributes to include in the opening tag.
    """
    list = liststring.split('\n')
    atts = ''
    if attributes != {}: atts = AttList(attributes)
    output = []
    output.append('<%s%s>' % (tag, atts))
    for item in list:
        output.append('<li>%s</li>' % item)
    output.append('</%s>' % tag)
    return '\n'.join(output)
    
def MakeTable(caption, rows, cols, attributes = {}):
    """
    Takes a caption string and integer numbers of rows and cols, and returns an empty HTML table.
    Also takes an optional dictionary of attributes to include in the opening tag.
    """
    atts = ''
    if attributes != {}: atts = AttList(attributes)
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
ID_STRIPHTML = 29
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
        filemenu.Append(ID_OPEN, "&Open"," Open a file to edit")
        filemenu.AppendSeparator()
        filemenu.Append(ID_SAVE, "&Save"," Save file")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")
        
        inline_menu = wx.Menu()
        inline_menu.Append(ID_CITE, "&cite", "Citation")
        inline_menu.Append(ID_EM, "&em", "Emphasis")
        inline_menu.Append(ID_CODE, "c&ode","Programming code")
        inline_menu.Append(ID_SPAN, "spa&n","generic inline element")
        inline_menu.Append(ID_STRONG, "&strong", "Strong emphasis")
        inline_menu.Append(ID_SUB, "su&b","Subscript")
        inline_menu.Append(ID_SUP, "su&p","Superscript")
        
        block_menu = wx.Menu()
        block_menu.Append(ID_BLOCKQUOTE, "&blockquote", "Block quotation")
        block_menu.Append(ID_DIV, "&div", "Generic block element")
        block_menu.Append(ID_P, "&p", "Paragraph")
        block_menu.Append(ID_PINITIAL, "p.&initial", "First paragraph in an article or section")
        block_menu.Append(ID_PPHOTO, "p.ph&oto", "Paragraph with photo")
        block_menu.Append(ID_PRE, "pr&e", "Preformatted block text")
        
        heading_menu = wx.Menu()
        heading_menu.Append(ID_H1, "h&1", "Heading 1")
        heading_menu.Append(ID_H2, "h&2", "Heading 2")
        heading_menu.Append(ID_H3, "h&3", "Heading 3")
        heading_menu.Append(ID_H4, "h&4", "Heading 4")
        heading_menu.Append(ID_H5, "h&5", "Heading 5")
        heading_menu.Append(ID_H6, "h&6", "Heading 6")

        link_menu = wx.Menu()
        link_menu.Append(ID_A, "&a", "Anchor")
        link_menu.Append(ID_HREF, "a &href", "Hyperlink")
        
        nested_menu = wx.Menu()
        nested_menu.Append(ID_OL, "&ol", "Ordered list")
        nested_menu.Append(ID_UL, "&ul", "Unordered List")
        nested_menu.Append(ID_TABLECONVERT, "table (&convert)", "Convert existing tab data to a table")
        nested_menu.Append(ID_TABLENEW, "table (&new)", "Create new empty table with 4 rows and 4 columns")
        
        htmlmenu = wx.Menu()
        htmlmenu.AppendMenu(ID_INLINEMENU, "&Inline", inline_menu)
        htmlmenu.AppendSeparator()
        htmlmenu.AppendMenu(ID_BLOCKMENU, "&Block", block_menu)
        htmlmenu.AppendSeparator()
        htmlmenu.AppendMenu(ID_HEADINGMENU, "&Heading", heading_menu)
        htmlmenu.AppendSeparator()
        htmlmenu.AppendMenu(ID_LINKMENU, "&Link", link_menu)
        htmlmenu.AppendSeparator()
        htmlmenu.AppendMenu(ID_NESTEDMENU, "&Nested", nested_menu)
        
        format_menu = wx.Menu()
        format_menu.Append(ID_SWITCHMODE, "Switch &Mode", "Alternate between Edit Mode and Preview Mode")
        format_menu.AppendSeparator()
        format_menu.Append(ID_LCASE, "&lcase", "Convert text to lowercase")
        format_menu.Append(ID_UCASE, "&UCASE", "Convert text to uppercase")
        format_menu.Append(ID_PCASE, "&Pcase", "Convert text to proper case (capitalized)")
        format_menu.AppendSeparator()
        format_menu.Append(ID_CLEAN, "&Clean", "Clean up MS Word characters")

        tools_menu = wx.Menu()
        tools_menu.Append(ID_WORDCOUNT, "&Word Count", "Return a count of words")
        tools_menu.Append(ID_STRIPHTML, "&Strip HTML", "Remove all HTML elements and leave the text")
        tools_menu.Append(ID_HTML2TEXT, "&Html2Text", "Convert HTML into Markdown-formatted plain text")
        if markdown != False:
            tools_menu.Append(ID_MARKDOWN, "&Markdown", "Convert Markdown-formatted plain text into HTML")
        
        about_menu = wx.Menu()
        about_menu.Append(ID_ABOUT, "&About PyHtmlEdit"," Information about this program")
        
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File") 
        menuBar.Append(htmlmenu, "&HTML")
        menuBar.Append(format_menu, "F&ormat")
        menuBar.Append(tools_menu, "&Tools")
        menuBar.Append(about_menu, "&About")
        
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Define the code to be run when a menu option is selected
        wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, ID_OPEN, self.OnOpen)
        wx.EVT_MENU(self, ID_SAVE, self.OnSave)
        wx.EVT_MENU(self, ID_STRONG, self.OnStrong)
        wx.EVT_MENU(self, ID_EM, self.OnEm)
        wx.EVT_MENU(self, ID_SPAN, self.OnSpan)
        wx.EVT_MENU(self, ID_CITE, self.OnCite)
        wx.EVT_MENU(self, ID_SUB, self.OnSub)
        wx.EVT_MENU(self, ID_SUP, self.OnSup)
        wx.EVT_MENU(self, ID_CODE, self.OnCode)
        wx.EVT_MENU(self, ID_DIV, self.OnDiv)
        wx.EVT_MENU(self, ID_P, self.OnP)
        wx.EVT_MENU(self, ID_PPHOTO, self.OnPPhoto)
        wx.EVT_MENU(self, ID_PINITIAL, self.OnPInitial)
        wx.EVT_MENU(self, ID_BLOCKQUOTE, self.OnBlockquote)
        wx.EVT_MENU(self, ID_PRE, self.OnPre)
        wx.EVT_MENU(self, ID_H1, self.OnH1)
        wx.EVT_MENU(self, ID_H2, self.OnH2)
        wx.EVT_MENU(self, ID_H3, self.OnH3)
        wx.EVT_MENU(self, ID_H4, self.OnH4)
        wx.EVT_MENU(self, ID_H5, self.OnH5)
        wx.EVT_MENU(self, ID_H6, self.OnH6)
        wx.EVT_MENU(self, ID_A, self.OnA)
        wx.EVT_MENU(self, ID_HREF, self.OnHref)
        wx.EVT_MENU(self, ID_UL, self.OnUl)
        wx.EVT_MENU(self, ID_OL, self.OnOl)
        wx.EVT_MENU(self, ID_TABLENEW, self.OnTableNew)
        wx.EVT_MENU(self, ID_TABLECONVERT, self.OnTableConvert)
        wx.EVT_MENU(self, ID_UCASE, self.OnUcase)
        wx.EVT_MENU(self, ID_LCASE, self.OnLcase)
        wx.EVT_MENU(self, ID_PCASE, self.OnPcase)
        wx.EVT_MENU(self, ID_CLEAN, self.OnClean)
        wx.EVT_MENU(self, ID_WORDCOUNT, self.OnWordCount)
        wx.EVT_MENU(self, ID_STRIPHTML, self.OnStripHtml)
        wx.EVT_MENU(self, ID_TOGGLEWRAP, self.OnToggleWrap)
        wx.EVT_MENU(self, ID_SWITCHMODE, self.OnSwitchMode)
        wx.EVT_MENU(self, ID_HTML2TEXT, self.OnHtml2Text)
        wx.EVT_MENU(self, ID_MARKDOWN, self.OnMarkdown)

        self.Show(1)

        self.aboutme = wx.MessageDialog( self, "PyHtmlEdit is a simple HTML editor written in Python using the wxPython GUI library (v2.8).\n\nAssembled by Ryan McGreal.\n\nhttp://quandyfactory.com/projects/pyhtmledit","About PyHtmlEdit", wx.OK)
        self.doiexit = wx.MessageDialog( self, "Are you sure you want to exit? \n", "Confirm Exit", wx.YES_NO)

        self.dirname = ''

    def OnAbout(self,e):
        self.aboutme.ShowModal()

    def OnExit(self,e):
        igot = self.doiexit.ShowModal()
        if igot == wx.ID_YES:
            self.Close(True)

    def OnOpen(self,e):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            filehandle=open(os.path.join(self.dirname, self.filename),'r')
            self.control.SetValue(filehandle.read())
            filehandle.close()
            self.SetTitle('PyHtmlEdit: Editing "%s"' % self.filename)
        dlg.Destroy()

    def OnSave(self,e):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", \
                wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            itcontains = self.control.GetValue()
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            filehandle=open(os.path.join(self.dirname, self.filename),'w')
            filehandle.write(itcontains)
            filehandle.close()
        dlg.Destroy()
        
    def OnStrong(self,e):
        self.control.WriteText(TagIt('strong', self.control.StringSelection))
    def OnEm(self,e):
        self.control.WriteText(TagIt('em', self.control.StringSelection))
    def OnCite(self,e):
        self.control.WriteText(TagIt('cite', self.control.StringSelection))
    def OnSpan(self,e):
        self.control.WriteText(TagIt('span', self.control.StringSelection))
    def OnSub(self,e):
        self.control.WriteText(TagIt('sub', self.control.StringSelection))
    def OnSup(self,e):
        self.control.WriteText(TagIt('sup', self.control.StringSelection))
    def OnCode(self,e):
        self.control.WriteText(TagIt('code', self.control.StringSelection))
    def OnP(self,e):
        self.control.WriteText(TagIt('p', self.control.StringSelection))
    def OnPPhoto(self,e):
        self.control.WriteText('<p class="photo">\n<img src="%s" alt="" title=""><br>\n\n</p>\n' % self.control.StringSelection)
    def OnPInitial(self,e):
        self.control.WriteText(TagIt('p', self.control.StringSelection, attributes = {'class':'initial'}))
    def OnBlockquote(self,e):
        self.control.WriteText(TagIt('blockquote', self.control.StringSelection, block = True))
    def OnDiv(self,e):
        self.control.WriteText(TagIt('div', self.control.StringSelection, block = True))
    def OnPre(self,e):
        self.control.WriteText(TagIt('pre', self.control.StringSelection, block = True))
    def OnH1(self,e):
        self.control.WriteText(TagIt('h1', self.control.StringSelection))
    def OnH2(self,e):
        self.control.WriteText(TagIt('h2', self.control.StringSelection))
    def OnH3(self,e):
        self.control.WriteText(TagIt('h3', self.control.StringSelection))
    def OnH4(self,e):
        self.control.WriteText(TagIt('h4', self.control.StringSelection))
    def OnH5(self,e):
        self.control.WriteText(TagIt('h5', self.control.StringSelection))
    def OnH6(self,e):
        self.control.WriteText(TagIt('h6', self.control.StringSelection))
    def OnA(self,e):
        dialog = wx.TextEntryDialog(self, 'Enter anchor name: ', 'Anchor Name', '')
        dialog.ShowModal()
        named = dialog.GetValue()
        self.control.WriteText(TagIt('a', self.control.StringSelection, attributes = {'name': named, }))
    def OnHref(self,e):
        dialog = wx.TextEntryDialog(self, 'Enter the HREF:', 'Hyper-Reference', '')
        dialog.ShowModal()
        href = dialog.GetValue()
        self.control.WriteText(TagIt('a', self.control.StringSelection, attributes = {'href': href, }))
    def OnUl(self,e):
        self.control.WriteText(ListIt('ul', self.control.StringSelection))
    def OnOl(self,e):
        self.control.WriteText(ListIt('ol', self.control.StringSelection, attributes = {'type':'1',}))
    def OnTableNew(self,e):
        self.control.WriteText(MakeTable('Table Caption', 4, 4))
    def OnTableConvert(self,e):
        dialog = wx.TextEntryDialog(self, 'Enter a Table Caption:', 'Table Caption', '')
        dialog.ShowModal()
        caption = dialog.GetValue()
        tdata = self.control.StringSelection.split('\n')
        output = []
        addline = output.append
        addline('<table>')
        addline('<caption>%s</caption>' % caption)
        for row in tdata:
            addline('<tr>')
            cells = row.split('\t')
            tag = 'td'; comment = ''
            if tdata.index(row) == 0: 
                tag = 'th'; comment = '<!-- first row has table headings -->'
            for cell in cells:
                addline('<%s>%s</%s>' % (tag, cell, tag))
            addline('</tr>')
        addline('</tble>')
        self.control.WriteText('\n'.join(output))
        
    def OnUcase(self,e):
        self.control.WriteText(self.control.StringSelection.upper())
    def OnLcase(self,e):
        self.control.WriteText(self.control.StringSelection.lower())
    def OnPcase(self,e):
        self.control.WriteText(' '.join([w.capitalize() for w in self.control.StringSelection.split(' ')]))
    def OnHtml2Text(self,e):
        self.control.WriteText(Html2TextIt(self.control.StringSelection))
    def OnMarkdown(self,e):
        self.control.WriteText(MarkdownIt(self.control.StringSelection))
    def OnClean(self,e):
        dirtytext = self.control.StringSelection
        dirtytext = CleanIt(dirtytext)
        self.control.WriteText(dirtytext)

    def OnWordCount(self,e):
        # first, try to get the selected text
        selection = self.control.StringSelection
        # if no selected text, use entire document
        if len(selection) == 0: selection = self.control.Value
        # get count of lines
        linelist = selection.split('\n')
        lines = len(linelist)
        # get count of characters
        chars = len(selection)
        # remove HTML tags
        selection = StripHtml(selection)
        # convert tabs and line breaks to spaces
        selection = selection.replace('\n', ' ')
        selection = selection.replace('\t', ' ')
        #eliminates multiple spaces between words
        while '  ' in selection:
            selection = selection.replace('  ', ' ')
        # split selection into a list of words
        wordlist = selection.split(' ')
        # get count of words
        words = len(wordlist)
        msg = wx.MessageBox('Chars: %s\nWords: %s\nLines: %s' % (chars, words, lines), 'Word Count')
    def OnStripHtml(self,e):
        self.control.WriteText(StripHtml(self.control.StringSelection))
    def OnToggleWrap(self,e):
        msg = wx.MessageBox('Line Wrap toggle not implemented yet', 'Line Wrap')
    def OnSwitchMode(self,e):
        pass

# Set up a window based app, and create a main window in it
app = wx.PySimpleApp()
view = MainWindow(None, "PyHtmlEdit")
# Enter event loop
app.MainLoop()
