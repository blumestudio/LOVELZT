from pygments import highlight
from pygments.lexers import get_lexer_by_name, ClassNotFound
from pygments.formatters import TerminalFormatter

class SyntaxHighlighter:
    def __init__(self, language='python'):
        self.set_language(language)

    def set_language(self, language):
        try:
            self.lexer = get_lexer_by_name(language)
        except ClassNotFound:
            print(f"Lexer for language '{language}' not found. Defaulting to Python.")
            self.lexer = get_lexer_by_name('python')

    def highlight(self, text):
        return highlight(text, self.lexer, TerminalFormatter())
