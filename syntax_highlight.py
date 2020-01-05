from common_tasks import CommonTask
from pygments import lex
from pygments.lexers.python import Python3Lexer

class Highlighting(CommonTask):
    """Highlight the text according language specific.
    Currently support only for Python"""
    def tag_conf(self):
        # self.previousContent = text.get("1.0", 'end')
        text = self.get_current()
        text.tag_configure("Token.Keyword", foreground="orange")
        # text.tag_configure("Token.Name", foreground="red")
        text.tag_configure("Token.Keyword.Constant", foreground="#CC7A00")
        text.tag_configure("Token.Keyword.Declaration", foreground="#CC7A00")
        text.tag_configure("Token.Keyword.Namespace", foreground="orange")
        text.tag_configure("Token.Keyword.Pseudo", foreground="#CC7A00")
        text.tag_configure("Token.Keyword.Reserved", foreground="blue")
        text.tag_configure("Token.Keyword.Type", foreground="#CC7A00")
        text.tag_configure("Token.Name.Class", foreground="blue")
        text.tag_configure("Token.Name.Exception", foreground="#003D99")
        text.tag_configure("Token.Operator.Word", foreground="#CC7A00")
        text.tag_configure("Token.Comment", foreground="gray")
        text.tag_configure("Token.Name.Function", foreground="purple")
        text.tag_configure("Token.Name.Builtin", foreground="purple")
        text.tag_configure("Token.Literal.String.Single", foreground="green")
        text.tag_configure("Token.Literal.String.Double", foreground="green")
        text.tag_configure("Token.Punctuation", foreground="blue")
        text.tag_configure("Token.Literal.String.Doc", foreground="gray")

    def remove_tags(self, row):
        text = self.get_current()
        text.tag_remove("Token.Keyword", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Keyword.Constant", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Keyword.Declaration", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Keyword.Namespace", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Keyword.Pseudo", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Keyword.Reserved", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Keyword.Type", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Name.Class", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Name.Exception", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Name.Function", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Operator.Word", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Comment", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Literal.String.Single", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Literal.String.Double", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Name.Builtin", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Name.Function", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Punctuation", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Name", f"{row}.0", f"{row}.end")
        text.tag_remove("Token.Literal.String.Doc", f"{row}.0", f"{row}.end")


    def highlight(self, event=None):
        """Highlight the syntax of the current line"""
        # current = self.file_list[self.nb.index('current')]
        # if current is not None and current.endswith('.py'):
        text_widget = self.get_current()
        row = text_widget.index('insert').split('.')[0]
        self.remove_tags(row)
        content = text_widget.get("1.0", 'end')
        lines = content.split("\n")
        text_widget.mark_set("range_start", row + ".0")
        data = text_widget.get(row + ".0", row + "." + str(len(lines[int(row) - 1])))
        for token, content in lex(data, Python3Lexer()):
            text_widget.mark_set("range_end", "range_start + %dc" % len(content))
            text_widget.tag_add(str(token), "range_start", "range_end")
            text_widget.mark_set("range_start", "range_end")
        self.tag_conf()
        
    
    def remove_tags2(self, row):
        text = self.get_current()
        text.tag_remove("Token.Keyword", f"{row}.0", "end")
        text.tag_remove("Token.Keyword.Constant", f"{row}.0", "end")
        text.tag_remove("Token.Keyword.Declaration", f"{row}.0", "end")
        text.tag_remove("Token.Keyword.Namespace", f"{row}.0", "end")
        text.tag_remove("Token.Keyword.Pseudo", f"{row}.0", "end")
        text.tag_remove("Token.Keyword.Reserved", f"{row}.0", "end")
        text.tag_remove("Token.Keyword.Type", f"{row}.0", "end")
        text.tag_remove("Token.Name.Class", f"{row}.0", "end")
        text.tag_remove("Token.Name.Exception", f"{row}.0", "end")
        text.tag_remove("Token.Name.Function", f"{row}.0", "end")
        text.tag_remove("Token.Operator.Word", f"{row}.0", "end")
        text.tag_remove("Token.Comment", f"{row}.0", "end")
        text.tag_remove("Token.Literal.String.Single", f"{row}.0", "end")
        text.tag_remove("Token.Literal.String.Double", f"{row}.0", "end")
        text.tag_remove("Token.Name.Builtin", f"{row}.0", "end")
        text.tag_remove("Token.Name.Function", f"{row}.0", "end")
        text.tag_remove("Token.Punctuation", f"{row}.0", "end")
        text.tag_remove("Token.Name", f"{row}.0", "end")
        text.tag_remove("Token.Literal.String.Doc", f"{row}.0", "end")
        
    
    def highlight2(self, event=None):
        """Highlight the syntax of the current line"""
        # current = self.file_list[self.nb.index('current')]
        # if current is not None and current.endswith('.py'):
        text_widget = self.get_current()
        # row = text_widget.index('insert').split('.')[0]
        self.remove_tags2(1)
        # content = text_widget.get("1.0", 'end')
        # lines = content.split("\n")
        text_widget.mark_set("range_start", "1" + ".0")
        data = text_widget.get("1.0", "end")
        for token, content in lex(data, Python3Lexer()):
            text_widget.mark_set("range_end", "range_start + %dc" % len(content))
            text_widget.tag_add(str(token), "range_start", "range_end")
            text_widget.mark_set("range_start", "range_end")
        self.tag_conf()