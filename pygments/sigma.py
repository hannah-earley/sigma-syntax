"""
to install:
    - symlink to /usr/local/lib/python3.6/site-packages/pygments/lexers
    - cd to /usr/local/lib/python3.6/site-packages/pygments/lexers
    - run python3 _mapping.py
"""


from pygments.lexer import RegexLexer, include, bygroups, using, \
                           this, inherit, default, words
from pygments.token import *

__all__ = ['SigmaLexer', 'SigmaREPLLexer']

class SigmaLexer(RegexLexer):
    name = 'Sigma'
    aliases = ['sigma', 'sig']
    filenames = ['*.sig']

    tokens = {
        'reserved': [(r'\b(inh|beq|grp|def|perm)\b', Generic.Error)],
        'reserved#': [(r'\b(inh|beq|grp|def|perm)\b', Generic.Error, '#pop')],
        'reserved)': [(r'\b(inh|beq|grp|def|perm)\b', Generic.Error, ')')],
        'ml-comment': [
            (r'[^*()]+', Comment.Multiline),
            (r'\(\*', Comment.Multiline, '#push'),
            (r'\*\)', Comment.Multiline, '#pop'),
            (r'[*()]', Comment.Multiline),
        ],
        'whitespace': [
            (r'^#!.*?$', Comment.Hashbang),
            (r'\(\*', Comment.Multiline, 'ml-comment'),
            (r';.*?$', Comment.Single),
            (r'\n', Text),
            (r'\s+', Text),
        ],
        'string': [
            (r'"', String, '#pop'),
            (r'\\([\\abfnrtv"\']|x[a-fA-F0-9]{2,4}|'
             r'u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|[0-7]{1,3})', String.Escape),
            (r'[^\\"\n]+', String),  # all other characters
            (r'\\\n', String),  # line continuation
            (r'\\', String),  # stray backslash
        ],
        'number#': [
            (r'0[xX][0-9a-fA-F]+', Number.Hex, '#pop'),
            (r'0[xX][0-7]+', Number.Oct, '#pop'),
            (r'[0-9]+', Number, '#pop')
        ],

        'tl-term': [
            include('whitespace'),
            (r'perm\*?', Keyword.Declaration, (')', 'term-permr(', 'term-perml')),
            (r'def\*?', Keyword.Declaration, (')', 'sigma1', 'defid1')),
            (r'inh\*?', Keyword.Namespace, 'term-inh'),
            (r'beq\*?', Keyword.Namespace, 'term-beq'),
            (r'grp', Keyword.Namespace, 'term-grp'),
            (r'\)', Punctuation, '#pop'),
            (r'[^\s)]+', Generic.Error, ')')
        ],
        'term-perml': [
            include('whitespace'),
            (r'\(', Punctuation, (')', 'psigmas', 'defid1'))
        ],
        'term-permr(': [
            include('whitespace'),
            (r'\(', Punctuation, ('#pop', 'term-permr'))
        ],
        'term-permr': [
            include('whitespace'),
            (r'\)', Punctuation, '#pop'),
            (r'([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(@)(\s*)([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(\))',
                bygroups(Name.Function, Text, Operator, Text,
                         Name.Namespace, Text, Punctuation), '#pop'),
            (r'([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(\))',
                bygroups(Name.Namespace, Text, Punctuation), '#pop'),
            (r'(?=[^:.@>)\]}])', Punctuation, 'psigma1'),
        ],
        'term-inh': [
            include('whitespace'),
            (r'"', String, ('defid-list)', 'string'))
        ],
        'term-beq': [
            include('whitespace'),
            (r'\)', Punctuation, '#pop:2'),
            include('defid')
        ],
        'term-grp': [
            include('root'),
            (r'\)', Punctuation, '#pop:2')
        ],
        'id': [
            include('whitespace'),
            include('reserved'),
            (r'[^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*', Name.Function)
        ],
        'id)': [
            include('whitespace'),
            include('reserved)'),
            (r'[^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*', Name.Function, ')')
        ],
        ')': [
            include('whitespace'),
            (r'\)', Punctuation, '#pop:2')
        ],
        ']': [
            include('whitespace'),
            (r'\]', Punctuation, '#pop:2')
        ],
        ']3': [
            include('whitespace'),
            (r'\]', Punctuation, '#pop:3')
        ],
        '}': [
            include('whitespace'),
            (r'\}', Punctuation, '#pop:2')
        ],
        'defid': [
            include('whitespace'),
            include('reserved'),
            (r'([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(@)(\s*)([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)', bygroups(Name.Function, Text, Operator, Text, Name.Namespace)),
            (r'[^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*', Name.Namespace),
        ],
        'defid1': [
            include('whitespace'),
            include('reserved#'),
            (r'([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(@)(\s*)([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)', bygroups(Name.Function, Text, Operator, Text, Name.Namespace), '#pop'),
            (r'[^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*', Name.Namespace, '#pop'),
        ],
        'defid-list)': [
            include('whitespace'),
            (r'\)', Punctuation, '#pop:3'),
            include('defid')
        ],
        'root': [
            include('whitespace'),
            (r'\(', Punctuation, 'tl-term'),
        ],


        'psigmas': [
            include('whitespace'),
            (r'(?=[^:.@>)\]}])', Punctuation, 'psigma1'),
            (r'', Text, '#pop')
        ],
        'psigma1': [
            include('whitespace'),
            include('reserved#'),
            (r'\#', Name.Constant, '#pop'),
            (r'\(', Punctuation, (')', 'psigmas')),
            include('number#'),
            (r'`[^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*', Name.Function, '#pop'),
            (r'[^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*', Name.Label, '#pop'),
            (r'\[', Punctuation, ('psigma]', 'psigmas')),
            (r'\{', Punctuation, ('}', 'psigmas')),
            (r'(?=<)', Punctuation, ('#pop', 'ppermr:', 'pperml'))
        ],
        'psigma]': [
            include('whitespace'),
            include(']'),
            (r'\.', Literal, (']3', 'psigma1'))
        ],

        'pperml': [
            include('whitespace'),
            (r'<', Punctuation, ('#pop', 'psigmas', 'defid1'))
        ],
        'ppermr:': [
            include('whitespace'),
            (r':', Generic.Error, ('#pop', 'ppermr'))
        ],
        'ppermr': [
            include('whitespace'),
            (r'>', Punctuation, '#pop'),
            (r'([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(@)(\s*)([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(>)',
                bygroups(Name.Function, Text, Operator, Text,
                         Name.Namespace, Text, Punctuation), '#pop'),
            (r'([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(>)',
                bygroups(Name.Namespace, Text, Punctuation), '#pop'),
            (r'(?=[^:.@>)\]}])', Punctuation, 'psigma1'),
        ],


        'sigmas': [
            include('whitespace'),
            (r'(?=[^:.@>)\]}])', Punctuation, 'sigma1'),
            (r'', Text, '#pop')
        ],
        'sigma1': [
            include('whitespace'),
            include('reserved'),
            (r'\#', Name.Constant, '#pop'),
            (r'\(', Punctuation, (')', 'sigmas')),
            include('number#'),
            (r'[^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*', Name.Function, '#pop'),
            (r'\[', Punctuation, ('sigma]', 'sigmas')),
            (r'\{', Punctuation, ('}', 'sigmas')),
            (r'(?=<)', Punctuation, ('#pop', 'ppermr:', 'pperml'))
        ],
        'sigma]': [
            include('whitespace'),
            include(']'),
            (r'\.', Literal, (']3', 'sigma1'))
        ],
    }

class SigmaREPLLexer(RegexLexer):
    name = 'SigmaREPL'
    aliases = ['sigma-repl']
    filenames = []

    tokens = {
        'reserved': [(r'\b(inh|beq|grp|def|perm)\b', Generic.Error)],
        'reserved#': [(r'\b(inh|beq|grp|def|perm)\b', Generic.Error, '#pop')],
        'reserved)': [(r'\b(inh|beq|grp|def|perm)\b', Generic.Error, ')')],
        'ml-comment': [
            (r'[^*()]+', Comment.Multiline),
            (r'\(\*', Comment.Multiline, '#push'),
            (r'\*\)', Comment.Multiline, '#pop'),
            (r'[*()]', Comment.Multiline),
        ],
        'whitespace': [
            (r'^#!.*?$', Comment.Hashbang),
            (r'\(\*', Comment.Multiline, 'ml-comment'),
            (r';.*?$', Comment.Single),
            (r'\n', Text),
            (r'\s+', Text),
        ],
        'string': [
            (r'"', String, '#pop'),
            (r'\\([\\abfnrtv"\']|x[a-fA-F0-9]{2,4}|'
             r'u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|[0-7]{1,3})', String.Escape),
            (r'[^\\"\n]+', String),  # all other characters
            (r'\\\n', String),  # line continuation
            (r'\\', String),  # stray backslash
        ],
        'number#': [
            (r'0[xX][0-9a-fA-F]+', Number.Hex, '#pop'),
            (r'0[xX][0-7]+', Number.Oct, '#pop'),
            (r'[0-9]+', Number, '#pop')
        ],

        'tl-term': [
            include('whitespace'),
            (r'perm\*?', Keyword.Declaration, (')', 'term-permr(', 'term-perml')),
            (r'def\*?', Keyword.Declaration, (')', 'sigma1', 'defid1')),
            (r'inh\*?', Keyword.Namespace, 'term-inh'),
            (r'beq\*?', Keyword.Namespace, 'term-beq'),
            (r'grp', Keyword.Namespace, 'term-grp'),
            (r'\)', Punctuation, '#pop'),
            (r'(?=[^:.@>)\]}])', Punctuation, (')', 'sigmas')),
            (r'[^\s)]+', Generic.Error, ')')
        ],
        'term-perml': [
            include('whitespace'),
            (r'\(', Punctuation, (')', 'psigmas', 'defid1'))
        ],
        'term-permr(': [
            include('whitespace'),
            (r'\(', Punctuation, ('#pop', 'term-permr'))
        ],
        'term-permr': [
            include('whitespace'),
            (r'\)', Punctuation, '#pop'),
            (r'([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(@)(\s*)([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(\))',
                bygroups(Name.Function, Text, Operator, Text,
                         Name.Namespace, Text, Punctuation), '#pop'),
            (r'([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(\))',
                bygroups(Name.Namespace, Text, Punctuation), '#pop'),
            (r'(?=[^:.@>)\]}])', Punctuation, 'psigma1'),
        ],
        'term-inh': [
            include('whitespace'),
            (r'"', String, ('defid-list)', 'string'))
        ],
        'term-beq': [
            include('whitespace'),
            (r'\)', Punctuation, '#pop:2'),
            include('defid')
        ],
        'term-grp': [
            include('root'),
            (r'\)', Punctuation, '#pop:2')
        ],
        'id': [
            include('whitespace'),
            include('reserved'),
            (r'[^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*', Name.Function)
        ],
        'id)': [
            include('whitespace'),
            include('reserved)'),
            (r'[^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*', Name.Function, ')')
        ],
        ')': [
            include('whitespace'),
            (r'\)', Punctuation, '#pop:2')
        ],
        ']': [
            include('whitespace'),
            (r'\]', Punctuation, '#pop:2')
        ],
        ']3': [
            include('whitespace'),
            (r'\]', Punctuation, '#pop:3')
        ],
        '}': [
            include('whitespace'),
            (r'\}', Punctuation, '#pop:2')
        ],
        'defid': [
            include('whitespace'),
            include('reserved'),
            (r'([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(@)(\s*)([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)', bygroups(Name.Function, Text, Operator, Text, Name.Namespace)),
            (r'[^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*', Name.Namespace),
        ],
        'defid1': [
            include('whitespace'),
            include('reserved#'),
            (r'([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(@)(\s*)([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)', bygroups(Name.Function, Text, Operator, Text, Name.Namespace), '#pop'),
            (r'[^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*', Name.Namespace, '#pop'),
        ],
        'defid-list)': [
            include('whitespace'),
            (r'\)', Punctuation, '#pop:3'),
            include('defid')
        ],
        'root': [
            include('whitespace'),
            (r'(sigma>|^Loaded:[^\n]*$)', Generic.Prompt),
            (r'%[^\n]*$', Generic.Prompt),
            (r'[σ>]+', Generic.Prompt),
            (r'(:\{|\}|:e)', Generic.Prompt),
            (r':[^\n]*$', Generic.Prompt),
            (r'\(', Punctuation, 'tl-term'),
            (r'(?=[^:.@>)\]}])', Punctuation, 'sigma1'),
            (r'[^\n]+$', Generic.Prompt)
        ],


        'psigmas': [
            include('whitespace'),
            (r'(?=[^:.@>)\]}])', Punctuation, 'psigma1'),
            (r'', Text, '#pop')
        ],
        'psigma1': [
            include('whitespace'),
            include('reserved#'),
            (r'\#', Name.Constant, '#pop'),
            (r'\(', Punctuation, (')', 'psigmas')),
            include('number#'),
            (r'`[^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*', Name.Function, '#pop'),
            (r'[^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*', Name.Label, '#pop'),
            (r'\[', Punctuation, ('psigma]', 'psigmas')),
            (r'\{', Punctuation, ('}', 'psigmas')),
            (r'(?=<)', Punctuation, ('#pop', 'ppermr:', 'pperml'))
        ],
        'psigma]': [
            include('whitespace'),
            include(']'),
            (r'\.', Literal, (']3', 'psigma1'))
        ],

        'pperml': [
            include('whitespace'),
            (r'<', Punctuation, ('#pop', 'psigmas', 'defid1'))
        ],
        'ppermr:': [
            include('whitespace'),
            (r':', Generic.Error, ('#pop', 'ppermr'))
        ],
        'ppermr': [
            include('whitespace'),
            (r'>', Punctuation, '#pop'),
            (r'([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(@)(\s*)([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(>)',
                bygroups(Name.Function, Text, Operator, Text,
                         Name.Namespace, Text, Punctuation), '#pop'),
            (r'([^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*)(\s*)(>)',
                bygroups(Name.Namespace, Text, Punctuation), '#pop'),
            (r'(?=[^:.@>)\]}])', Punctuation, 'psigma1'),
        ],


        'sigmas': [
            include('whitespace'),
            (r'(?=[^:.@>)\]}])', Punctuation, 'sigma1'),
            (r'', Text, '#pop')
        ],
        'sigma1': [
            include('whitespace'),
            include('reserved'),
            (r'\#', Name.Constant, '#pop'),
            (r'\(', Punctuation, (')', 'sigmas')),
            include('number#'),
            (r'[^\s.#@<>()\[\]{}`:"0-9][^\s.#@<>()\[\]{}`:"]*', Name.Function, '#pop'),
            (r'\[', Punctuation, ('sigma]', 'sigmas')),
            (r'\{', Punctuation, ('}', 'sigmas')),
            (r'(?=<)', Punctuation, ('#pop', 'ppermr:', 'pperml'))
        ],
        'sigma]': [
            include('whitespace'),
            include(']'),
            (r'\.', Literal, (']3', 'sigma1'))
        ],
    }
