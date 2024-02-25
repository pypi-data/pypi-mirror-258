from .tag import tag

global_html_element = [
    "accesskey",  # Specifies a shortcut key to activate/focus an element
    "class",  # Specifies one or more classnames for an element (refers to a class in a style sheet)
    "contenteditable",  # Specifies whether the content of an element is editable or not
    "data-*",  # Used to store custom data private to the page or application
    "dir",  # Specifies the text direction for the content in an element
    "draggable",  # Specifies whether an element is draggable or not
    "hidden",  # Specifies that an element is not yet, or is no longer, relevant
    "id",  # Specifies a unique id for an element
    "lang",  # Specifies the language of the element's content
    "spellcheck",  # Specifies whether the element is to have its spelling and grammar checked or not
    "style",  # Specifies an inline CSS style for an element
    "tabindex",  # Specifies the tabbing order of an element
    "title",  # Specifies extra information about an element
    "translate",  # Specifies whether the content of an element should be translated or not
]


class HTML(object):
    record_tag = []

    # basic start

    def doctype(self):
        return tag.DOCTYPE().html_tag

    def html(self):
        return tag.HTML().html_tag

    def head(self):
        return tag.Head().html_tag

    def title(self, title):
        return tag.Title(value=title).html_tag

    def body(self):
        word = "body"
        return tag.Body().html_tag

    def heading(self, size=1):
        if size < 1:
            size = 1
        elif size > 6:
            size = 6

        return tag.Title(size=size).html_tag

    def paragraph(self):
        return tag.Paragraph().html_tag

    def break_line(self):
        return tag.Br().html_tag

    def thematic_break(self):
        return tag.Hr().html_tag

    def comment(self):
        return tag.Comment().html_tag

    def _check(self, word):
        return word

    def create_html(self):
        word = ""
        word += self.doctype()
        word += self.html()
        word += self.head()
        word += self.title(title="Test")
        word += self.body()
        # word = self._check(word=word)
        return word
