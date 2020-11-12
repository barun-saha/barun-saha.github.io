#!/usr/bin/python
#
# Convert Jinja templates into HTML files. Currently, only inheritance
# is used in the templates.
#
# Source: http://pbpython.com/pdf-reports.html
#
# Barun Saha
# 15 March 2015
#
# This script is released under a GNU GPL v3 license. You are free to
# use this script as per the license terms. No warranties provided.
#

from jinja2 import Environment, FileSystemLoader


def rotate_array(active):
    '''Rotate the entries of an array by a single position to the right'''
    # Remove the last element from the array
    element = active.pop()
    # Insert it as the first element of the array
    active.insert(0, element)


ENV = Environment(loader=FileSystemLoader('./templates'))

# List of pages to be rendered -- MUST be listed according to their order
# in the navigation bar
PAGE_LIST = ['index', 'research', 'the_omn_book', 'poetry', 'software', 'misc',]

# Title of individual pages
TITLES = {
    'index': 'Barun Saha',
    'misc': 'Barun Saha | Miscellaneous',
    'software': 'Barun Saha | Software',
    'research': 'Barun Saha | Research',
    'the_omn_book': 'Barun Saha | Opportunistic Mobile Networks',
    'poetry': 'Barun Saha | Poetry',
}

# CSS active class for the navigation bar list items
state = ['active', '', '', '', '', '',]

for item in PAGE_LIST:
    file_name = item + '.html'
    template = ENV.get_template(file_name)
    #print state
    html = template.render(title=TITLES[item], active_state=state)

    #print html
    # Write output in the corresponding HTML file
    print('Writing', file_name)
    with open(file_name, 'w') as out_file:
        out_file.write(html)

    # Rotate active states for the next page
    rotate_array(state)
