__author__ = 'petlja'

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from ..python_kernel import setup_py_kernel
import html



def setup(app):
    setup_py_kernel(app)
    app.add_css_file('database-queries.css')
    app.add_js_file('database-queries.js')
    app.add_directive('db-query', DBComponentDirective)
    app.add_node(DBComponentNode, html=(visit_DBComponent_node, depart_DBComponent_node))

TEMPLATE_START = '''
  <db-query id="%(divid)s" %(check_colum_name)s %(show_expected_result)s>
    <file>%(db_path)s</file>
    <name>%(db_name)s</name>
    %(solution_query)s
    %(check_query)s
    %(hint)s
    <textarea>
    %(query)s
    </textarea>
    '''


TEMPLATE_END = '''
  </db-query>
    '''


class DBComponentNode(nodes.General, nodes.Element):
    def __init__(self, content):
        super(DBComponentNode, self).__init__()
        self.note = content


def visit_DBComponent_node(self, node):
    node.delimiter = "_start__{}_".format("info")
    self.body.append(node.delimiter)
    res = TEMPLATE_START % node.note
    self.body.append(res)


def depart_DBComponent_node(self, node):
    res = TEMPLATE_END
    self.body.append(res)
    self.body.remove(node.delimiter)


class DBComponentDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    has_content = True
    option_spec = {}
    option_spec.update({
        'db-path': directives.unchanged,
        'solution-query': directives.unchanged,
        'name': directives.unchanged,
        'check-query': directives.unchanged,
        'hint': directives.unchanged,
        'check-colum-name': directives.unchanged,
        'show-expected-result': directives.unchanged,
    })


    def run(self):
        """
        generate html to include note box.
        :param self:
        :return:
        """
        self.options['divid'] = self.arguments[0]

        if 'db-path' not in self.options:
            raise ValueError("db-path is required")
        if 'name' not in self.options:
            raise ValueError("name is required")
        
        self.options['db_path'] = self.options['db-path']
        self.options['db_name'] = self.options['name']

        if 'solution-query' in self.options:
            self.options['solution_query'] = "<solution-query>" + self.options['solution-query'] + "</solution-query>" + "\n"
        else:
            self.options['solution_query'] = ""
        
        if 'check-query' in self.options:
            self.options['check_query'] = "<check-query>" + self.options['check-query'] + "</check-query>" + "\n"
        else:
            self.options['check_query'] = ""

        if 'hint' in self.options:
            self.options['hint'] = "<hint>" + self.options['hint'] + "</hint>" + "\n"
        else:
            self.options['hint'] = ""
        
        if 'check-colum-name' in self.options:
            self.options['check_colum_name'] = "check-colum-name"
        else:
            self.options['check_colum_name'] = ""

        if 'show-expected-result' in self.options:
            self.options['show_expected_result'] = "show-expected-result"
        else:
            self.options['show_expected_result'] = ""

        self.options['query'] = encode("\n".join(self.content))
        
        innode = DBComponentNode(self.options)

        return [innode]
    

def encode(html_code):
    return html.escape(html_code)