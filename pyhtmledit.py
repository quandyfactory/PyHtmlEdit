#!/usr/bin/env python3

__version__ = 3.00
__releasedate__ = '2020-05-25'
__author__ = 'Ryan McGreal <ryan@quandyfactory.com>'
__homepage__ = 'http://quandyfactory.com/projects/2/pyhtmledit/'
__repository__ = 'http://github.com/quandyfactory/PyHtmlEdit'
__copyright__ = '(C) 2009, 2020 by Ryan McGreal. Licenced under GNU GPL 2.0\nhttp://www.gnu.org/licenses/old-licenses/gpl-2.0.html'

import os
path = os.path.abspath(__file__).replace(os.path.basename(__file__), '')
import sys
icon = r'webtools.gif'
iconpath = r'%s%s' % (path, icon)

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

from markdown2 import markdown
from html2text import html2text
import re

global_values = {
    'find_needle': '',
    'replace_needle': '',
}


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

CleanChars = {
    u'\u2026': u'...',# HORIZONTAL ELLIPSIS
    u'\u2018': u'\'', # LEFT SINGLE QUOTATION MARK
    u'\u2019': u'\'', # RIGHT SINGLE QUOTATION MARK
    u'\u201C': u'"',  # LEFT DOUBLE QUOTATION MARK
    u'\u201D': u'"',  # RIGHT DOUBLE QUOTATION MARK
    u'\u2013': u'-',  # EN DASH
    u'\u2014': u'-',  # EM DASH
}


def remove_whitespace(text):
    """
    Remove all white space characters from a string
    """
    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', text)


def remove_multiple_spaces(text):
    """
    Replaces multiple   spaces (like the spaces between "multiple" and "spaces") with one space.
    """
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text


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


def make_attlist(attributes):
    """
    Takes a diction_ary of HTML attributes and returns a list of attribute names and values to go inside an HTML tag.
    """
    return ' ' + ' '.join(['%s="%s"' % (k, v) for k, v in attributes.items()])


def tag_it(tag, text, block=False, attributes={}):
    """
    Takes a selection of text and returns the selection wrapped in HTML tags.
    Also takes an option_al diction_ary of attributes to include in the opening tag.
    """
    atts = ''
    if 'href' in attributes:
        #if attributes['href'][0:4].lower() == 'http':
        #    attributes['target'] = '_blank'
        pass # don't give it a target="_blank" attribute
    if attributes != {}: atts = make_attlist(attributes)
    if block == False:
        return '<%s%s>%s</%s>' % (tag, atts, text.rstrip(), tag)
    else:
        return '<%s%s>\n%s\n</%s>\n' % (tag, atts, text.rstrip(), tag)


def list_it(tag, liststring, attributes={}):
    """
    Takes either "ul" or "ol" and a string with line breaks ('\n') and returns as an HTML list.
    Also takes an option_al diction_ary of attributes to include in the opening tag.
    """
    item_list = [item for item in liststring.split('\n') if item.strip() != '']
    atts = ''
    if attributes != {}: atts = make_attlist(attributes)
    output = []
    output.append('<%s%s>' % (tag, atts))
    for item in item_list:
        output.append('<li>%s</li>' % item)
    output.append('</%s>' % tag)
    return '\n'.join(output)


def clean_it(text):
    """
    Takes a text string, applies the kill_gremlins function to replace cp1252 characters with Unicode, then runs the cleanchars filter
    """
    text = kill_gremlins(text)
    text = remove_multiple_spaces(text)
    for k, v in CleanChars.items():
        text = text.replace(k, v)
    return text


def get_selection():
    try:
        return content.get('sel.first', 'sel.last')
    except:
        return ''


def replace_selection(newtext):
    try:
        start = content.index('sel.first')
        end = content.index('sel.last')
        selected = content.get('sel.first', 'sel.last')
        content.delete('sel.first', 'sel.last')
        content.insert(start, newtext)
    except:
        content.insert(tk.INSERT, '\n\n%s' % (newtext))    


def tag_selection(tag, block=False, attributes={}):
    selected = get_selection()
    newtext = tag_it(tag, selected, block, attributes)
    replace_selection(newtext)


def list_selection(tag, attributes={}):
    selected = get_selection()
    newtext = list_it(tag, selected, attributes)
    replace_selection(newtext)


def p_photo_it():
    selected = get_selection()
    twolines = selected.split('\n')
    src = twolines[0]
    try: alt = twolines[1].strip()
    except: alt = ''
    newtext = '<p class="photo">\n<img src="%s" alt="%s" title="%s"><br>\n%s</p>' % (
        src, alt, alt, alt
    )
    replace_selection(newtext)


def table_it(caption='Table Caption', rows=4, cols=4, attributes={}):
    """
    Takes a caption string and integer numbers of rows and cols, and returns an empty HTML table.
    Also takes an option_al diction_ary of attributes to include in the opening tag.
    """
    atts = ''
    if attributes != {}: atts = make_attlist(attributes)
    output = []
    addline = output.append
    addline('<table%s>' % atts)
    addline('  <caption>%s</caption>' % caption)
    for row in range(rows+1):
        tag = 'td'; comment = ''
        if row == 0:
            comment = ' <!-- initial row has table headings -->'
            tag = 'th'
            addline('  <thead>')
        else:
            comment = '<!-- row %s -->' % (row)
        output.append('    <tr>%s' % comment)
        for col in range(cols):
            addline('      <%s></%s>' % (tag, tag))

        if row == 0:
            addline('    </tr>')
            addline('  </head>')
            addline('  <tbody>')
        else:
            addline('    </tr>')
    addline('  </tbody>')
    addline('</table>')
    return '\n'.join(output)


def table_convert_it(blob, caption=''):
    tdata = blob.split('\n')
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
                addline('    </tr>')
                addline('  </thead>')
                addline('  <tbody>')
            else:
                addline('    </tr>')
    addline('  </tbody>')
    addline('</table>')
    return '\n'.join(output)


def markdown_it(text):
    """
    Converts markdown syntax to HTML if it's installed
    """
    markeddown = markdown(text)
    markeddown = markeddown.replace('\n</p>', '</p>\n') # fix bug in Windows
    block_tags = '</p> </ul> </ol> </blockquote> </h1> </h2> </h3> </h4> </h5> </h6> </div>'.split(' ')
    for tag in block_tags:
        # put block tags on new lines
        markeddown = markeddown.replace(tag, '%s\n' % (tag))
        # get rid of blank line above closing tag
        markeddown = markeddown.replace('\n\n%s' % (tag), '\n%s' % (tag))

    # get rid of triple spaces between paragraphs on Windows
    while '\n\n\n' in markeddown:
        markeddown = markeddown.replace('\n\n\n', '\n\n') 
    
    # fix stupid extra space thing inside block quotes
    markeddown = markeddown.replace('\n\n  \n  ', '\n\n  ')

    # finally, add the "initial" class to the first paragraph after an h3
    markeddown = markeddown.replace('</h3>\n\n<p>', '</h3>\n\n<p class="initial">')

    return markeddown


def html2text_it(text):
    """Converts HTML to plain text (essentially markdown format)"""
    return html2text(text)


def strip_html_it(stuff):
    """
    Takes a string with HTML tags and returns the string with the HTML tags removed.
    """
    return re.sub(r'<[^>]*?>', '', stuff)
    

def file_open():
    filename = filedialog.askopenfilename()
    with open(filename, 'r') as myfile:
        file_contents = myfile.read()
        content.delete("1.0", tk.END)
        content.insert("1.0", file_contents)


def file_open_insert():
    filename = filedialog.askopenfilename()
    with open(filename, 'r') as myfile:
        file_contents = '%s\n\n' % (myfile.read())
        content.insert("1.0", file_contents)

def file_open_append():
    filename = filedialog.askopenfilename()
    with open(filename, 'r') as myfile:
        file_contents = '\n\n%s' % (myfile.read())
        content.insert(tk.END, file_contents)


def file_save(event=None):
    file_name = filedialog.asksaveasfile(mode='w', defaultextension='.html')
    if file_name is None:
        return
    
    file_contents = content.get('1.0', tk.END)
    file_contents = file_contents.encode('utf8')
    
    print(file_name)
    
    with open(file_name.name, 'wb') as myfile:
        myfile.write(file_contents)
    
    messagebox.showinfo('File Saved', 'The file has been saved.')


def file_quit(event=None):
    confirm_quit = messagebox.askquestion('Quit PyHtmlEdit', 'Are you sure you want to quit?', icon='warning')
    if confirm_quit == 'yes':
        exit()

    return True
    
    messagebox.showinfo('Return', 'Yay! You chose not to quit.')


def edit_select_all(event=None):
    content.tag_add("sel","1.0","end")


def edit_copy():
    pass


def edit_cut():
    pass


def edit_paste():
    pass


def edit_find(event=None):
    
    print('')
    print('inside edit_find')
    
    try:
        highlighted_end = content.index('sel.last')
    except:
        highlighted_end = ''
    print('highlighted_end = %s' % (highlighted_end))

    find_needle = global_values['find_needle']
    
    find_needle = simpledialog.askstring('Find', 'Text to find: ', initialvalue=find_needle)
    if find_needle == '':
        return

    print('find_needle = %s' % (find_needle))

    if highlighted_end == '':
        current_position = content.index(tk.INSERT)
    else:
        current_position = highlighted_end

    print('current_position = %s' % (current_position))

    end_position = content.index("end-1c")
    print('end_position = %s' % (end_position))
    
    if current_position == end_position:
        current_position = "1.0"
    
    print('current_position = %s' % (current_position))
    pos = content.search(find_needle, current_position, stopindex=tk.END)
    print('pos = %s' % (pos))
    
    if pos == '':
        messagebox.showinfo('Not Found', 'The search term was not found.')
        return True
    
    poslist = pos.split('.')
    row = poslist[0]
    col = int(poslist[1])
    newcol = col + len(find_needle)
    
    pos_end = '%s.%s' % (row, newcol)
    
    print('pos_end = %s' % (pos_end))
    content.tag_add("sel", pos, pos_end)
    content.see(pos)
    
    global_values['find_needle'] = find_needle



def edit_replace_all(event=None):
    print('')
    print('inside edit_replace_all')
    
    try:
        highlighted_end = content.index('sel.last')
    except:
        highlighted_end = ''
    print('highlighted_end = %s' % (highlighted_end))

    find_needle = global_values['find_needle']
    
    find_needle = simpledialog.askstring('Replace All', 'Text to find: ', initialvalue=find_needle)
    if find_needle == '':
        return
    
    replace_needle = global_values['replace_needle']
    
    replace_needle = simpledialog.askstring('Replace All', 'Replace with: ', initialvalue=replace_needle)

    all_content = content.get("1.0", tk.END)
    
    occurrences = all_content.count(find_needle)
    
    all_content = all_content.replace(find_needle, replace_needle)
    
    edit_select_all()
    
    replace_selection(all_content)
    
    messagebox.showinfo('Replace All', 'The search term "%s" was replaced with "%s" %s time%s.' % (find_needle, replace_needle, occurrences, 's' if occurrences > 1 else ''))



def edit_replace_next(event=None):
    print('')
    print('inside edit_replace_next')
    
    try:
        highlighted_end = content.index('sel.last')
    except:
        highlighted_end = ''
    print('highlighted_end = %s' % (highlighted_end))

    find_needle = global_values['find_needle']
    
    find_needle = simpledialog.askstring('Replace Next', 'Text to find: ', initialvalue=find_needle)
    if find_needle == '':
        return
    
    replace_needle = global_values['replace_needle']
    
    replace_needle = simpledialog.askstring('Replace Next', 'Replace with: ', initialvalue=replace_needle)

    if highlighted_end == '':
        current_position = content.index(tk.INSERT)
    else:
        current_position = highlighted_end

    print('current_position = %s' % (current_position))

    end_position = content.index("end-1c")
    print('end_position = %s' % (end_position))
    
    if current_position == end_position:
        current_position = "1.0"
    
    print('current_position = %s' % (current_position))
    pos = content.search(find_needle, current_position, stopindex=tk.END)
    print('pos = %s' % (pos))
    
    poslist = pos.split('.')
    row = poslist[0]
    col = int(poslist[1])
    newcol = col + len(find_needle)
    
    pos_end = '%s.%s' % (row, newcol)
    print('pos_end = %s' % (pos_end))

    content.tag_add("sel", pos, pos_end)
    
    replace_selection(replace_needle)
    
    replaced_newcol = col + len(replace_needle)
    replace_pos_end = '%s.%s' % (row, replaced_newcol)
    content.tag_add("sel", pos, replace_pos_end)
    content.see(pos)
    
    global_values['find_needle'] = find_needle
    global_values['replace_needle'] = replace_needle



def html_inline_cite():
    tag_selection('cite')   


def html_inline_emphasis():
    tag_selection('em')


def html_inline_code():
    tag_selection('code')


def html_inline_span():
    tag_selection('span')


def html_inline_strong():
    tag_selection('strong')


def html_inline_subscript():
    tag_selection('sub')


def html_inline_superscript():
    tag_selection('sup')


def html_block_blockquote():
    tag_selection('blockquote', block=True)


def html_block_div():
    tag_selection('div', block=True)


def html_block_div_centered():
    tag_selection('div', block=True, attributes={ 'class': 'centered' })


def html_block_paragraph():
    tag_selection('p')


def html_block_paragraph_photo():
    p_photo_it()


def html_block_paragraph_initial():
    tag_selection('p', attributes = { 'class': 'initial' })


def html_heading_h1():
    tag_selection('h1')


def html_heading_h2():
    tag_selection('h2')


def html_heading_h3():
    tag_selection('h3')


def html_heading_h4():
    tag_selection('h4')


def html_heading_h5():
    tag_selection('h5')


def html_heading_h6():
    tag_selection('h6')


def html_nested_ul():
    list_selection('ul', {})


def html_nested_ol():
    list_selection('ol', {'type': '1' })


def html_nested_table_convert():
    selected = get_selection()
    caption = simpledialog.askstring('Caption', 'Enter the Table Caption: ')
    newtext = table_convert_it(selected, caption)
    replace_selection(newtext)


def html_nested_table_new():

    caption = simpledialog.askstring('Caption', 'Enter the Table Caption: ')
    rows = simpledialog.askstring('Rows', 'Enter the number of rows: ')
    cols = simpledialog.askstring('Columns', 'Enter the number of columns: ')

    try:
        rows = int(rows)
    except:
        messagebox.showinfo('Rows', 'Number of rows needs to be a number. Defaulting to 4.')
        rows = 4
    
    try:
        cols = int(cols)
    except:
        cols = messagebox.showinfo('Columns', 'Number of columns needs to be a number. Defaulting to 4.')

    selected = get_selection()
    newtext = table_it(caption, rows, cols)
    replace_selection(newtext)


def format_lowercase():
    selected = get_selection()
    newtext = selected.lower()
    replace_selection(newtext)


def format_uppercase():
    selected = get_selection()
    newtext = selected.upper()
    replace_selection(newtext)


def format_capitalize():
    selected = get_selection()
    newtext = selected.title()
    replace_selection(newtext)


def format_clean():
    selected = get_selection()
    newtext = clean_it(selected)
    replace_selection(newtext)


def tools_strip_html():
    selected = get_selection()
    newtext = strip_html_it(selected)
    replace_selection(newtext)


def tools_html_to_text():
    selected = get_selection()
    newtext = html2text_it(selected)
    replace_selection(newtext)


def tools_markdown():
    selected = get_selection()
    newtext = markdown_it(selected)
    replace_selection(newtext)


def about_about():
    info = messagebox.showinfo('About PyHtmlEdit', 'PyHtmlEdit is a simple HTML editor written in Python3 using the tkinter GUI library.\n\nCreated by %s\n\nVersion: %s, released on %s\n\nCopyright: %s\n\nHomepage: %s' % (__author__, __version__, __releasedate__, __copyright__, __homepage__))


window = tk.Tk()
window.minsize(800,600)
window.title('PyHTMLEdit')

window_icon = tk.PhotoImage(file=iconpath)
window.tk.call('wm', 'iconphoto', window._w, window_icon)

menubar = tk.Menu(window)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label='Open File', command=file_open, underline=0)
file_menu.add_command(label='Open (Insert)', command=file_open_insert, underline=6)
file_menu.add_command(label='Open (Append)', command=file_open_append, underline=6)
file_menu.add_command(label='Save', command=file_save, underline=0, accelerator='Ctrl+s')
file_menu.add_command(label='Quit', command=file_quit, underline=0, accelerator='Ctrl+q')

menubar.add_cascade(label='File', menu=file_menu, underline=0)

edit_menu = tk.Menu(window, tearoff=0)
edit_menu.add_command(label='Select All', command=edit_select_all, underline=0, accelerator='Ctrl+a')
edit_menu.add_command(label='Copy', command=edit_copy, underline=0, accelerator='Ctrl+c')
edit_menu.add_command(label='Cut', command=edit_cut, underline=1, accelerator='Ctrl+x')
edit_menu.add_command(label='Paste', command=edit_paste, underline=0, accelerator='Ctrl+v')
edit_menu.add_command(label='Find Next', command=edit_find, underline=0, accelerator='Ctrl+f')
edit_menu.add_command(label='Replace All', command=edit_replace_all, underline=0, accelerator='Ctrl+r')
edit_menu.add_command(label='Replace Next', command=edit_replace_next, underline=8, accelerator='Ctrl+n')

menubar.add_cascade(label='Edit', menu=edit_menu, underline=0)

html_menu = tk.Menu(menubar, tearoff=0)
html_inline_menu = tk.Menu(html_menu, tearoff=0)
html_block_menu = tk.Menu(html_menu, tearoff=0)
html_heading_menu = tk.Menu(html_menu, tearoff=0)
html_link_menu = tk.Menu(html_menu, tearoff=0)
html_nested_menu = tk.Menu(html_menu, tearoff=0)

html_inline_menu.add_command(label='Cite', command=html_inline_cite, underline=0)
html_inline_menu.add_command(label='Emphasis', command=html_inline_emphasis, underline=0)
html_inline_menu.add_command(label='Code', command=html_inline_code, underline=1)
html_inline_menu.add_command(label='Span', command=html_inline_span, underline=0)
html_inline_menu.add_command(label='Strong', command=html_inline_strong, underline=1)
html_inline_menu.add_command(label='Subscript', command=html_inline_subscript, underline=1)
html_inline_menu.add_command(label='Superscript', command=html_inline_superscript, underline=2)

html_block_menu.add_command(label='Blockquote', command=html_block_blockquote, underline=0)
html_block_menu.add_command(label='Div', command=html_block_div, underline=0)
html_block_menu.add_command(label='Centered', command=html_block_div_centered, underline=0)
html_block_menu.add_command(label='Paragraph', command=html_block_paragraph, underline=0)
html_block_menu.add_command(label='P.photo', command=html_block_paragraph_photo, underline=4)
html_block_menu.add_command(label='P.initial', command=html_block_paragraph_initial, underline=2)

html_heading_menu.add_command(label='H1', command=html_heading_h1, underline=1)
html_heading_menu.add_command(label='H2', command=html_heading_h2, underline=1)
html_heading_menu.add_command(label='H3', command=html_heading_h3, underline=1)
html_heading_menu.add_command(label='H4', command=html_heading_h4, underline=1)
html_heading_menu.add_command(label='H5', command=html_heading_h5, underline=1)
html_heading_menu.add_command(label='H6', command=html_heading_h6, underline=1)

html_nested_menu.add_command(label='UL', command=html_nested_ul, underline=0)
html_nested_menu.add_command(label='OL', command=html_nested_ol, underline=0)
html_nested_menu.add_command(label='Table (Convert)', command=html_nested_table_convert, underline=7)
html_nested_menu.add_command(label='Table (New)', command=html_nested_table_new, underline=7)

html_menu.add_cascade(label='Inline', menu=html_inline_menu, underline=0)
html_menu.add_cascade(label='Block', menu=html_block_menu, underline=0)
html_menu.add_cascade(label='Heading', menu=html_heading_menu, underline=0)
html_menu.add_cascade(label='Nested', menu=html_nested_menu, underline=0)

menubar.add_cascade(label='HTML', menu=html_menu, underline=0)

format_menu = tk.Menu(menubar, tearoff=0)
format_menu.add_command(label='Clean', command=format_clean, underline=0)
format_menu.add_command(label='Lowercase', command=format_lowercase, underline=0)
format_menu.add_command(label='Uppercase', command=format_uppercase, underline=0)
format_menu.add_command(label='Capitalize', command=format_capitalize, underline=1)

menubar.add_cascade(label='Format', menu=format_menu, underline=1)

tools_menu = tk.Menu(menubar, tearoff=0)

tools_menu.add_command(label='Strip HTML', command=tools_strip_html, underline=0)
tools_menu.add_command(label='HTML to Text', command=tools_html_to_text, underline=0)
tools_menu.add_command(label='Markdown', command=tools_markdown, underline=0)

menubar.add_cascade(label='Tools', menu=tools_menu, underline=0)

about_menu = tk.Menu(menubar, tearoff=0)

about_menu.add_command(label='About', command=about_about, underline=0)

menubar.add_cascade(label='About', menu=about_menu, underline=0)


scroll = tk.Scrollbar(window)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

content = tk.Text(window, wrap=tk.WORD, yscrollcommand=scroll.set)
content.pack(fill="both", expand=True)
content.focus()



window.config(menu=menubar)

# attach keyboard shortcut to event handlers
window.bind_all('<Control-a>', edit_select_all)
window.bind_all('<Control-q>', file_quit)
window.bind_all('<Control-s>', file_save)
window.bind_all('<Control-f>', edit_find)
window.bind_all('<Control-r>', edit_replace_all)
window.bind_all('<Control-n>', edit_replace_next)

args = sys.argv
if len(args) > 1:
    import requests
    r = requests.get('https://baconipsum.com/api/?type=meat-and-filler&paras=10&format=text')
    content.insert(tk.END, r.text)



window.mainloop()
