# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

import subprocess
from collections import defaultdict
from functools import partial

from docutils import nodes
from docutils.parsers.rst.roles import set_classes


def create_shortcut_defs():
    defns = defaultdict(list)

    for line in open('../kitty/kitty.conf'):
        if line.startswith('map '):
            _, sc, name = line.split(maxsplit=2)
            sc = sc.replace('kitty_mod', 'ctrl+shift')
            name = name.rstrip().replace(' ', '_').replace('-', '_').replace('+', 'plus').replace('.', '_').replace('___', '_').replace('__', '_').strip('_')
            defns[name].append(':kbd:`' + sc.replace('>', ' → ') + '`')

    defns = [
        '.. |sc_{}| replace:: {}'.format(name, ' or '.join(defns[name]))
        for name in sorted(defns)
    ]
    return '\n'.join(defns)


# -- Project information -----------------------------------------------------

project = 'kitty'
copyright = '2018, Kovid Goyal'
author = 'Kovid Goyal'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
needs_sphinx = '1.7'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'generated/cli-*']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

rst_prolog = '''
.. |kitty.conf| replace:: :doc:`kitty.conf </conf>`
.. |kitty| replace:: *kitty*
.. role:: green
.. role:: italic
.. role:: bold
.. role:: cyan
.. role:: title
.. role:: env

''' + create_shortcut_defs()


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'logo': 'kitty.png',
    'show_powered_by': False,
    'fixed_sidebar': True,
    'sidebar_collapse': True,
    'github_button': False,
    'github_banner': True,
    'github_user': 'kovidgoyal',
    'github_repo': 'kitty',
}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static', '../logo/kitty.png']
html_context = {
    'css_files': ['_static/custom.css']
}
html_favicon = '../logo/kitty.png'

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
html_sidebars = {
    '**': [
        'about.html',
        'support.html',
        'searchbox.html',
        'localtoc.html',
        'relations.html',
    ]
}
html_show_sourcelink = False


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'kittydoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'kitty.tex', 'kitty Documentation',
     'Kovid Goyal', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'kitty', 'kitty Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'kitty', 'kitty Documentation',
     author, 'kitty', 'One line description of project.',
     'Miscellaneous'),
]


# GitHub linking inlne roles {{{

def issue_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    ' Link to a github issue '
    try:
        issue_num = int(text)
        if issue_num <= 0:
            raise ValueError
    except ValueError:
        msg = inliner.reporter.error(
            'GitHub issue number must be a number greater than or equal to 1; '
            '"%s" is invalid.' % text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    url = f'https://github.com/kovidgoyal/kitty/issues/{issue_num}'
    set_classes(options)
    node = nodes.reference(rawtext, f'#{issue_num}', refuri=url, **options)
    return [node], []


def commit_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    ' Link to a github commit '
    try:
        commit_id = subprocess.check_output(f'git rev-list --max-count=1 --skip=# {text}'.split()).decode('utf-8').strip()
    except Exception:
        msg = inliner.reporter.error(
            f'GitHub commit id "{text}" not recognized.', line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    url = f'https://github.com/kovidgoyal/kitty/commit/{commit_id}'
    set_classes(options)
    short_id = subprocess.check_output(f'git rev-list --max-count=1 --abbrev-commit --skip=# {commit_id}'.split()).decode('utf-8').strip()
    node = nodes.reference(rawtext, f'(commit:{short_id})', refuri=url, **options)
    return [node], []
# }}}


# Sidebar ToC {{{
def create_toc(app, pagename):
    toctree = app.env.get_toc_for(pagename, app.builder)
    if toctree is not None:
        subtree = toctree[toctree.first_child_matching_class(nodes.list_item)]
        bl = subtree.first_child_matching_class(nodes.bullet_list)
        if bl is None:
            return  # Empty ToC
        subtree = subtree[bl]
        # for li in subtree.traverse(nodes.list_item):
        #     modify_li(li)
        # subtree['ids'] = [ID]
        return app.builder.render_partial(subtree)['fragment']


def add_html_context(app, pagename, templatename, context, *args):
    if 'toc' in context:
        context['toc'] = create_toc(app, pagename) or context['toc']
# }}}


# CLI docs {{{
def write_cli_docs():
    from kitty.cli import option_spec_as_rst
    with open('generated/cli-kitty.rst', 'w') as f:
        f.write(option_spec_as_rst(appname='kitty').replace('kitty --to', 'kitty @ --to'))
    as_rst = partial(option_spec_as_rst, heading_char='_')
    from kitty.remote_control import global_options_spec, cli_msg, cmap, all_commands
    with open('generated/cli-kitty-at.rst', 'w') as f:
        p = partial(print, file=f)
        p('kitty @\n' + '-' * 80)
        p('.. program::', 'kitty @')
        p('\n\n' + as_rst(
            global_options_spec, message=cli_msg, usage='command ...', appname='kitty @'))
        from kitty.cmds import cli_params_for
        for cmd_name in all_commands:
            func = cmap[cmd_name]
            p('kitty @', func.name + '\n' + '-' * 120)
            p('.. program::', 'kitty @', func.name)
            p('\n\n' + as_rst(*cli_params_for(func)))
    from kittens.runner import all_kitten_names, get_kitten_cli_docs
    for kitten in all_kitten_names():
        data = get_kitten_cli_docs(kitten)
        if data:
            with open(f'generated/cli-kitten-{kitten}.rst', 'w') as f:
                p = partial(print, file=f)
                p('.. program::', f'kitty +kitten {kitten}')
                p('\n\n' + option_spec_as_rst(
                    data['options'], message=data['help_text'], usage=data['usage'], appname=f'kitty +kitten {kitten}',
                    heading_char='^'))

# }}}


def setup(app):
    write_cli_docs()
    app.add_role('iss', issue_role)
    app.add_role('commit', commit_role)
    app.connect('html-page-context', add_html_context)
