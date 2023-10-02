from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles.named_colors import NAMED_COLORS
from prompt_toolkit.completion import NestedCompleter


class RainbowLexer(Lexer):
    def lex_document(self, document):
        colors = list(sorted({"Teal": "#008080"}, key=NAMED_COLORS.get))

        def get_line(lineno):
            return [
                (colors[i % len(colors)], c)
                for i, c in enumerate(document.lines[lineno])
            ]

        return get_line


Completer = NestedCompleter.from_nested_dict({'Add a Note'   : None, 'Edit a Note'      : None, 'Delete a Note': None,
                                            'Search by Tag'  : None, 'Search by Content': None, 'Display Notes': None,
                                            'Edit a Note'    : None, 'Exit'             : None, 'Sort'         : None})

Sort_Completer = NestedCompleter.from_nested_dict({'Sort by tags' : None, 'Sort by name'  : None, 'Sort by date' : None})


     