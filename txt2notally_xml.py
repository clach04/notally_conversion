#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import glob
import os
import sys

try:
    # Python 3.8 and later
    # py3
    from html import escape as escape
except ImportError:
    # py2
    from cgi import escape as escape


is_win = sys.platform.startswith('win')
extensions_to_check = ['.md', '.txt']


template_string = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<exported-notes>
  <notes>
    <note>
      <color>DEFAULT</color>
      <date-created>0</date-created>
      <pinned>false</pinned>
      <title>Pinned note title</title>
      <body>Pinned content</body>
    </note>
  </notes>
</exported-notes>
"""

template_string_bare_minimum = u"""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<exported-notes>
  <notes>
    <note>
      <title>%s</title>
      <body>%s</body>
    </note>
  </notes>
</exported-notes>
"""

template_string_bare_minimum_head = u"""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<exported-notes>
  <notes>
"""
template_string_bare_minimum_tail = u"""  </notes>
</exported-notes>
"""

template_string_bare_minimum_single_note = u"""    <note>
      <title>%s</title>
      <body>%s</body>
    </note>
"""

def gen_xml_single_note(note_title, note_body):
    """Manually construct XML for one note, for better or worse; does NOT use any XML libs
    NOTE assumes note_title is a filename (with extension)
    """
    note_title = note_title.strip()
    note_title = os.path.splitext(os.path.basename(note_title))[0]  # filename without file extension

    note_title = escape(note_title)
    note_body = escape(note_body)  # FIXME/TODO expected Windows newlines CR+LF - ensure this is present

    xml_content = template_string_bare_minimum_single_note % (note_title, note_body)
    return xml_content

def process_file(filename):
    note_f = open(filename, 'rb')
    file_string_contents = note_f.read().decode('utf-8')  # no error checking :-) If we fail, we fail loudly
    note_f.close()
    xml_content_single_note = gen_xml_single_note(filename, file_string_contents)
    return xml_content_single_note



def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Python %s on %s' % (sys.version.replace('\n', ' '), sys.platform.replace('\n', ' ')))

    xml_filename = 'NotallyBackup_test.xml'  # FIXME param, envvar

    if is_win:
        filenames = []
        for filename_pattern in argv[1:]:
            filenames += glob.glob(filename_pattern)
    else:
        filenames = argv[1:]

    if len(filenames) < 1:
        for filename_pattern in extensions_to_check:
            filenames += glob.glob('*' + filename_pattern)

    xml_content_all_notes = []
    #for filename_counter, filename in enumerate(filenames):
    filename_counter = 0
    for filename in filenames:
        # TODO progress logging, filename_counter of len(filenames)
        filename_counter += 1
        xml_content_single_note = process_file(filename)
        xml_content_all_notes.append(xml_content_single_note)
    print('processed %d files' % filename_counter)

    print('writting to %s files' % xml_filename)
    f = open(xml_filename, 'wb')
    # lets rely on buffering to keep performance at reasonable level...
    f.write(template_string_bare_minimum_head.encode('utf-8'))
    f.write(''.join(xml_content_all_notes).encode('utf-8'))
    f.write(template_string_bare_minimum_tail.encode('utf-8'))
    f.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
