__author__ = 'petlja'

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from ..python_kernel import setup_py_kernel
import html



def setup(app):
    setup_py_kernel(app)
    app.add_css_file('py-code.css')
    app.add_js_file('py-code.js')
    app.add_directive('py-code', PyCodeDirective)
    app.add_node(PyCodeNode, html=(visit_pycode_node, depart_pycode_node))


TEMPLATE_START = '''
  <py-code id="%(divid)s" %(ai)s>
    %(py_packages)s
    <textarea>
%(code)s
      </textarea>
    '''


TEMPLATE_END = '''
    </py-code>
    '''


class PyCodeNode(nodes.General, nodes.Element):
    def __init__(self, content):
        super(PyCodeNode, self).__init__()
        self.note = content


def visit_pycode_node(self, node):
    node.delimiter = "_start__{}_".format("info")
    self.body.append(node.delimiter)
    res = TEMPLATE_START % node.note
    self.body.append(res)


def depart_pycode_node(self, node):
    res = TEMPLATE_END
    self.body.append(res)
    self.body.remove(node.delimiter)


class PyCodeDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    has_content = True
    option_spec = {}
    option_spec.update({
        'packages': directives.unchanged,
        'opt-in-ai': directives.unchanged,
    })


    def run(self):
        """
        generate html to include note box.
        :param self:
        :return:
        """
        self.options['divid'] = self.arguments[0]
        self.options['code'] = encode("\n".join(self.content))
        self.options['py_packages'] = ""

        if 'packages' in self.options:
            for package in self.options['packages'].split(','):
                self.options['py_packages'] += "<python-package>" + package + "</python-package>" + "\n"

        if 'opt-in-ai' in self.options:
            self.options['ai'] = 'opt-in-ai'
        else:
            self.options['ai'] = ''

        innode = PyCodeNode(self.options)

        return [innode]
    

def encode(html_code):
    return html.escape(html_code)