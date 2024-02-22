# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.insert(0, os.path.abspath('../../'))

from unittest.mock import Mock  # noqa: F401, E402

# from sphinx.ext.autodoc.importer import _MockObject as Mock
Mock.Module = object
sys.modules['torch'] = Mock()
sys.modules['numpy'] = Mock()
sys.modules['numpy.linalg'] = Mock()
sys.modules['scipy'] = Mock()
sys.modules['scipy.optimize'] = Mock()
sys.modules['scipy.interpolate'] = Mock()
sys.modules['scipy.ndimage'] = Mock()
sys.modules['scipy.ndimage.filters'] = Mock()
sys.modules['tensorflow'] = Mock()
sys.modules['theano'] = Mock()
sys.modules['theano.tensor'] = Mock()
sys.modules['torch'] = Mock()
sys.modules['torch.autograd'] = Mock()
sys.modules['torch.autograd.gradcheck'] = Mock()
sys.modules['torch.distributions'] = Mock()
sys.modules['torch.nn'] = Mock()
sys.modules['torch.nn.functional'] = Mock()
sys.modules['torch.optim'] = Mock()
sys.modules['torch.nn.modules'] = Mock()
sys.modules['torch.nn.modules.utils'] = Mock()
sys.modules['torch.nn.modules.loss'] = Mock()
sys.modules['torch.utils'] = Mock()
sys.modules['torch.utils.model_zoo'] = Mock()
sys.modules['torch.nn.init'] = Mock()
sys.modules['torch.utils.data'] = Mock()
sys.modules['torchvision'] = Mock()
sys.modules['randomstate'] = Mock()
sys.modules['scipy._lib'] = Mock()
sys.modules['sklearn.cluster'] = Mock()
import torchcp

project = 'TorchCP'
copyright = '2023, ml-stat-Sustech'
author = 'ml-stat-Sustech'
with open(os.path.join(os.path.abspath('../../'), 'torchcp/VERSION')) as f:
    version = f.read().strip()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.autosummary',
    # 'sphinx.ext.linkcode',
    'nbsphinx',
    'numpydoc',

]

templates_path = ['_templates']
numpydoc_show_class_members = False
exclude_patterns = []

source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

todo_include_todos = False

# Resolve function for the linkcode extension.
def linkcode_resolve(domain, info):
    def find_source():
        # try to find the file and line number, based on code from numpy:
        # https://github.com/numpy/numpy/blob/master/doc/source/conf.py#L286
        obj = sys.modules[info['module']]
        for part in info['fullname'].split('.'):
            obj = getattr(obj, part)
        import inspect
        import os
        fn = inspect.getsourcefile(obj)
        fn = os.path.relpath(fn, start=os.path.dirname(torchcp.__file__))
        source, lineno = inspect.getsourcelines(obj)
        return fn, lineno, lineno + len(source) - 1

    if domain != 'py' or not info['module']:
        return None
    try:
        filename = 'torchcp/%s#L%d-L%d' % find_source()
    except Exception:
        filename = info['module'].replace('.', '/') + '.py'
    tag = 'master'
    url = "https://github.com/ml-stat-Sustech/TorchCP/blob/%s/%s"
    return url % (tag, filename)

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


import sphinx_rtd_theme

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


