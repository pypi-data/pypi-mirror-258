class HTMLTagBase(object):
    element_name = ""  # element name
    have_value = False
    have_size = False
    have_close = True  # have close
    self_close = False  # close immediately

    _starting = "<"
    _ending = ">"
    _end = "/"

    def __init__(self, value="", size=1, end=""):
        if self.have_size:
            self.size = size
        if self.have_value:
            self.value = value
        self.html_tag = self.ret_tag()

    def _auto_complete(self, word, end=""):
        return self._starting + end + word + self._ending

    def have_close_tag(self):
        return self.have_close

    def close_tag(self):
        if self.have_close:
            return self._auto_complete(word=self.element_name, end=self._end)
        return ""

    def is_self_close(self):
        return self.self_close

    def ret_tag(self):
        word = self._auto_complete(word=self.element_name)
        if self.have_value:
            word += self.value
        if self.self_close:
            word += self._auto_complete(word=self.element_name, end=self._end)
        return word


class DOCTYPE(HTMLTagBase):
    element_name = "!--DOCTYPE--"
    have_close = False


class HTML(HTMLTagBase):
    element_name = "html"


class Head(HTMLTagBase):
    element_name = "head"


class Title(HTMLTagBase):
    element_name = "title"
    have_value = True
    self_close = True


class Body(HTMLTagBase):
    element_name = "body"


class Heading(HTMLTagBase):
    element_name = "head"
    have_size = True


class Paragraph(HTMLTagBase):
    element_name = "p"


class Br(HTMLTagBase):
    element_name = "br"
    have_close = False


class Hr(HTMLTagBase):
    element_name = "br"
    have_close = False


class Comment(HTMLTagBase):
    element_name = "comment"
    have_close = False


