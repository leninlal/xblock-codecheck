import pkg_resources
from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Field
from xblock.fragment import Fragment
import requests
from bs4 import BeautifulSoup


class CodecheckXBlock(XBlock):n url
    href = String(display_name="href",
                  default="http://codecheck.it/codecheck/files?repo=bj4cc&problem=ch02/c02_exp_2_102",
                  scope=Scope.settings,
                  help="codecheck url")

    form = """
          <form action="/codecheck/check" method="post"><p>Complete the following file:</p><p>AverageTester.java</p><textarea cols="66" name="AverageTester.java" rows="22">public class AverageTester
                        {
           public static void main(String[] args)
           {
              String word1 = "Mary";
              String word2 = "had";
              String word3 = "a";
              String word4 = "little";
              String word5 = "lamb";

              // your work here

              int length1 = . . .;
              int length2 = . . .;
              . . .
              . . .
              . . .
              . . .
              System.out.println(average);
              System.out.println("Expected: 3.6");
           }
        }
        </textarea><p><input type="submit"/><input name="repo" type="hidden" value="bj4cc"><input name="problem" type="hidden" value="ch02/c02_exp_2_102"><input name="level" type="hidden" value="check"/></input></input></p></form>

                   """
    form = form.replace('/codecheck/check','http://codecheck.it/codecheck/check')
    con = String(display_name="content",
                          default=form,
                          scope=Scope.settings,
                          help="content")
 

    display_name = String(display_name="Display Name",
                          default="Display name",
                          scope=Scope.settings,
                          help="Name of the component in the edxplatform")

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")


    def student_view(self, context=None):
        """
        The primary view of the codecheckXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/code.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/code.css"))
        return frag


    def studio_view(self, context=None):
        """
        The primary view of the paellaXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/code_edit.html")
        frag = Fragment(html.format(self=self))
        frag.add_javascript(self.resource_string("static/js/src/code_edit.js"))
        frag.initialize_js('CodecheckXBlock')
        return frag

    @XBlock.json_handler
    def save_code(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        self.href = data['href']
        content = requests.get(self.href).content
        b = BeautifulSoup(content, "html.parser")
        self.con = str(b.find_all('form')[0]).replace('/codecheck/check','http://codecheck.it/codecheck/check')
        self.display_name = data['display_name']

        return {
            'result': 'success',
        }

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("CodecheckXBlock",
             """<vertical_demo>
                <pdf/>
                </vertical_demo>
             """),
        ]
