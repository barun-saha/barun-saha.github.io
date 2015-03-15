#!/usr/bin/python
#
# Convert Jinja templates into HTML files. Currently, only inheritance is used
# in the templates.
#
# Source: http://pbpython.com/pdf-reports.html
#
# Barun Saha
# 15 March 2015

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./templates'))

# List of files to be rendered
file_list = ['contact', 'index', 'misc', 'projects', 'research',]

# Title of individual pages
titles = {
    'contact': 'Barun Saha | Contact',
    'index': 'Barun Saha',
    'misc': 'Barun Saha | Miscellaneous',
    'projects': 'Barun Saha | Projects',
    'research': 'Barun Saha | Research',
}

for item in file_list:
    file_name = item + '.html'
    template = env.get_template(file_name)
    html = template.render(title=titles[item])

    #print html
    # Write output in the corresponding HTML file
    print 'Writing', file_name
    with open(file_name, 'w') as out_file:
        out_file.write(html)