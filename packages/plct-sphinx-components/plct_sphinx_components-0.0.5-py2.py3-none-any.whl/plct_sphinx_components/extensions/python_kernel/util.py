from sphinx.util.fileutil import copy_asset
from pkg_resources import resource_filename

def setup_py_kernel(app):
    # Check if the global variable 'files_added' exists
    if not hasattr(app, 'files_added'):
        app.add_js_file('translation.js')
        app.add_js_file('editor.js')
        # If it doesn't exist, add the files and set the variable to True
        app.add_js_file('https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js')
        app.add_js_file('python-kernel.js')
        app.connect('env-updated', copy_workers)
        app.files_added = True

def copy_workers(app, _):
    static_files = resource_filename('plct_sphinx_components', 'extensions/python_kernel/workers')
    if app.builder.name == 'plct_builder':
        copy_asset(static_files, app.builder.rootdir)
    else:
        copy_asset(static_files, app.builder.outdir)