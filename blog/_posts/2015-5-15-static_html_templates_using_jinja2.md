---
layout: post
title: Static HTML Templates using Jinja2
category:
tagline:
tags: html, static, template, jinja2, python
description: An article on the use of templates with static HTML pages and rendering them using Jinja2. In particular, setting the active CSS class for navigation menu items is discussed here.
---

### Introduction

HTML templates are to web development as superclass is to object oriented programming. HTML templates help in reusing the commonly used design elements (for example, headers, footers and navigation bars) across different pages. Thus, if the copyright notice has to be updated or a new item has to be added to the navigation bar, just edit the template and the changes would reflect in all the pages. Server side languages and frameworks (such as, [Django][django]) have typically supported the use of templates. However, it is possible to leverage the potential of templates even when you have a static website.

[Jinja2][jinja2] is a powerful templating engine for Python. Jinja2 templates can be specified entirely as a string ([an example][jinja2_example]) or can be loaded from a file. Moreover, it supports template inheritance. Thus, with a little effort we have, HTML templates + some Python code = final HTML pages! With static websites becoming popular, this is particularly useful.



### Objectives

Here, we would discuss how Jinja2 was used to create the static pages of this [website][my_website]. This, however, is not a tutorial on Jinja2 or web development. This article has two-fold objectives.

1. Discuss how Jinja2 can be used to set the active menu item in the navigation bar for different pages. As the title of the article suggests, we are not seeking for a dynamic approach at run time.
2. Describe how titles of different pages can be automatically set. Although this is a rather simple example, but hopefully it would demonstrate the power of templates and Jinja2.


**Quick tip**: If you want to highlight the currently active menu item in the navigation bar, you may have a look at the [Jinja tips and tricks][jinja_tricks]. In the following, we would look at an alternative approach to do the same. Moreover, greater control over the templates could possibly be achieved using the following approach.



### The Base Template

Before proceeding further, let us summarize the general steps while working with templates.

1. Create a base HTML template containing the common design elements.
2. Insert block template tags into the template for placing content.
3. Create templates for other pages with actual content by extending the base template.
4. Generate final HTML pages from the templates using Jinja2.

Let us begin with the (partial) content of the file `base.html`, which is the base template page. All other templates extend this page.

{% highlight html %}

<nav class="navbar navbar-default" role="navigation">
	<div class="container">
		<div class="navbar-header">
			<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar-collapse-1">
			<span class="sr-only">Toggle navigation</span>
			<span class="icon-bar"></span>
			<span class="icon-bar"></span>
			<span class="icon-bar"></span>
			</button>
		</div>

	<div class="navbar-center nav">
	  <a href="/">
		<img src="images/self/pentacle_transparent_bg2_20.png" alt="Logo" class="logo">
	  </a>
	</div>

	<div class="collapse navbar-collapse" id="navbar-collapse-1">
	  <ul class="nav navbar-nav">
		<li class="{{ "{{ active_state[0]" }} }}"><a href="/"><span class="glyphicon glyphicon-home"></span> Home</a></li>
		<li class="{{ "{{ active_state[1]" }} }}"><a href="research.html"><span class="glyphicon glyphicon-dashboard"></span> Research</a></li>
		<li class="dropdown {{ "{{ active_state[2]" }} }}">
		  <a href="projects.html" class="dropdown-toggle" data-toggle="dropdown"
			 role="button" aria-expanded="false"><span class="glyphicon glyphicon-cog"></span>
			Projects <span class="caret"></span></a>
		  <ul class="dropdown-menu" role="menu">
			<li><a href="projects.html">View all</a></li>
			<li><a href="projects.html#virtual_labs">Virtual Labs</a></li>
			<li><a href="projects.html#the_one_kb">The ONE Knowledge Base</a></li>
			<li><a href="projects.html#se_lite">Software Engineering Lite</a></li>
		  </ul>
		</li>
	  </ul>

	  <ul class="nav navbar-nav navbar-right">
		<li><a href="/blog/"><span class="glyphicon glyphicon-list"></span> Blog</a></li>
		<li class="{{ "{{ active_state[3]" }} }}"><a href="misc.html"><span class="glyphicon glyphicon-list-alt"></span> Miscellaneous<span class="sr-only">(current)</span></a></li>
		<li class="{{ "{{ active_state[4]" }} }}"><a href="contact.html"><span class="glyphicon glyphicon-envelope"></span> Contact</a></li>
	  </ul>
	</div><!-- /.navbar-collapse -->
	</div>
</nav>

{{ "{% block content " }}%}{{ "{% endblock "}}%}

{% endhighlight %}

The code of the navigation bar shown above is based on Twitter's [Bootstrap][bootstrap]. A few points may be noted here.

- Every list item `li` has a class property. These classes are assigned template variables.
- The variable `active_state` is an array, and different entries of the array are assigned to different list items. As we shall see later on, the sequence of index used here is important.
- The actual array would be provided by Jinja2 when we render the templates.
- At the end of the above code there is a {{ " `{% block  "}} %}` template tag to be used by the child templates.



### Other Templates

Contents of other pages would go inside the above declared template block. For example, the `contact.html` page looks like the following.

{% highlight html %}

{{ "{% extends 'base.html' "}}%}

{{ "{% block content " }}%}
	<div class="container">
	  <p>
		Glad to know that you wish to get in touch!
	  </p>

	  <p>
		Join me in <a href="http://in.linkedin.com/in/barunsaha">LinkedIn</a>
		or send me an email to <img src="images/self/email.jpg">. I am also
		available in <a href="https://github.com/barun-saha">GitHub</a> and
		<a href="https://www.researchgate.net/profile/Barun_Saha">ResearchGate</a>.
	  </p>
	</div>
{{ "{% endblock " }}%}

{% endhighlight %}



### Rendering the Templates

Finally, the `jinja_render.py` script would render the templates. By rendering we mean that all the template variables, expressions, and blocks would be replaced with actual content. The content of the script is given below.

Here, let us recall our objective once again. We want to set the CSS active class *only* for the list item in the navigation bar corresponding to the currently active page. The list named `state` (line # 42) in the following code helps us to achieve that. Note that one of the entries of this list is `'active'`, the name of the CSS class to highlight the active menu, while the remaining are empty strings. Moreover, the number of entries in this list is exactly same as the number of pages pointed to in the navigation bar.

The `PAGE_LIST` list (line # 30) stores the names of the individual HTML pages pointed by the navigation bar. Note that in this website we do not have nested pages (although there is a single menu with sub-menus). The order of this names correspond to the sequence of menu items in the navigation bar.

The logic to set the CSS class for the active menu item for each page is simple &mdash; for the `i`<sup>th</sup> page in `PAGE_LIST`, the corresponding CSS class is `state[i]`. However, after one such assignment has been done, the items of the list `state` should be moved a position to the right side so that the CSS class for the active menu (the `'active'` entry in the list `state`) of the next HTML page is obtained. The `rotate_array` method (line # 18) is used to rotate the elements of a list by one position to the right side.

{% highlight python linenos %}
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

# List of pages to be rendered -- MUST be listed according to their
# order in the navigation bar
PAGE_LIST = ['index', 'research', 'projects', 'misc', 'contact',]

# Title of individual pages
TITLES = {
    'contact': 'Barun Saha | Contact',
    'index': 'Barun Saha',
    'misc': 'Barun Saha | Miscellaneous',
    'projects': 'Barun Saha | Projects',
    'research': 'Barun Saha | Research',
}

# CSS active class for the navigation bar list items
state = ['active', '', '', '', '', '',]

for item in PAGE_LIST:
    file_name = item + '.html'
    template = ENV.get_template(file_name)
    html = template.render(title=TITLES[item], active_state=state)

    # Write output in the corresponding HTML file
    print 'Writing', file_name
    with open(file_name, 'w') as out_file:
        out_file.write(html)

    # Rotate active states for the next page
    rotate_array(state)

{% endhighlight %}

Finally, in line #s 44 through 55, we render each template by passing on the active CSS class and page title (the `TITLES` dictionary in line # 33), and write the rendered output to the corresponding HTML file (line # 52).

Thus, next time there is a need to alter the design of the pages, we just need to change the `base.html` file and execute the above script once again. However, if it is required to change the content of one or more pages, we need to makes the changes in the corresponding template(s), and also need to execute the `jinja_render.py` script.



### Conclusion

HTML templates are a great way to increase reusability and productivity. Jinja2, a templating engine for Python, is useful in this regard. Of course, one can use various static website generator engines available today. However, the flexibility of Jinja2 (or any other similar templates) not only help in creating static HTML pages, but they can be later [converted to other formats][pdf_report] as well. A next possible step would be to use [Jinja2 together with YAML][yaml_jinja].



[django]: https://www.djangoproject.com/
[jinja2]: http://jinja.pocoo.org/
[jinja2_example]: http://jinja.pocoo.org/docs/dev/intro/#basic-api-usage
[my_website]: http://barunsaha.me/
[jinja_tricks]: http://jinja.pocoo.org/docs/dev/tricks/
[bootstrap]: http://getbootstrap.com/
[pdf_report]: http://pbpython.com/pdf-reports.html
[yaml_jinja]: http://www.bernhardwenzel.com/blog/2013/07/01/jinja-with-yaml
