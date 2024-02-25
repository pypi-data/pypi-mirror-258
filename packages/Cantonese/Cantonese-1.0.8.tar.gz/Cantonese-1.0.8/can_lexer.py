import re
import zlib
from can_keywords import *
from util.infoprinter import ErrorPrinter
from collections import namedtuple
import zhconv

Pos = namedtuple('Pos', ['line', 'offset'])
MMap = []

def remove_comment(code: str) -> str:
    match_search = re.search(re.compile(r'/\*.*?\*/', re.S), code)
    while match_search:
        comment = match_search.group()
        code = code.replace(match_search.group(), '  ' + "\n" * (comment.count("\n")) + '  ', 1)
        match_search = re.search(re.compile(r'/\*.*?\*/', re.S), code)
    return code

def getCtxByLine(line: int) -> str:
    return zlib.decompress(MMap[line]).decode('utf-8')

class can_token:
    def __init__(self, pos: Pos, typ: TokenType, value: str):
        self.pos = pos
        self.typ = typ
        self.value = value

    @property
    def lineno(self):
        return self.pos.line

    @property
    def offset(self):
        return self.pos.offset

    def __repr__(self) -> str:
        return f"{self.value} ({self.typ.name})"

"""
    Get the Cantonese Token List
"""
class lexer:
    def __init__(self, file: str, code: str, keywords: tuple):
        self.file = file
        self.code = code
        self.keywords = keywords
        self.line = 1
        self.offset = 0
        self.buffer = ""

        self.re_number = r"^0[xX][0-9a-fA-F]*(\.[0-9a-fA-F]*)?([pP][+\-]?[0-9]+)?|^[0-9]*(\.[0-9]*)?([eE][+\-]?[0-9]+)?"
        self.re_id = r"^[_\d\w]+|^[\u4e00-\u9fa5]+"
        self.re_str = r"(?s)(^'(\\\\|\\'|\\\n|\\z\s*|[^'\n])*')|(^\"(\\\\|\\\"|\\\n|\\z\s*|[^\"\n])*\")"
        self.re_expr = r"[|][\S\s]*?[|]"
        self.re_python_expr = r"#XD[\S\s]*?二五仔係我"
        self.re_callfunc = r"[&](.*?)[)]"

    def getCurPos(self):
        return Pos(line=self.line, offset=self.offset)

    def next(self, n: int):
        self.offset += n
        self.code = self.code[n:]

    def check(self, s: str):
        return self.code.startswith(s)

    @staticmethod
    def is_white_space(c: str):
        return c in ('\t', '\n', '\v', '\f', '\r', ' ')

    @staticmethod
    def is_new_line(c: str):
        return c in ('\r', '\n')

    @staticmethod
    def isChinese(word: str):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False

    def skip_space(self):
        while len(self.code) > 0:
            if self.check('\r\n') or self.check('\n\r'):
                self.next(2)
                self.line += 1
                self.offset = 0
            elif lexer.is_new_line(self.code[0]):
                self.next(1)
                self.line += 1
                self.offset = 0
            elif self.check('?') or self.check(':') or self.check('：') or self.check('？'):
                self.next(1)
            elif self.check('「') or self.check('」'):
                self.next(1)
            elif lexer.is_white_space(self.code[0]):
                self.next(1)
            else:
                break

    def scan(self, pattern: str):
        m = re.match(pattern, self.code)
        if m:
            token = m.group()
            cnt_newline = token.count('\n')
            if cnt_newline:
                self.line += cnt_newline
            self.next(len(token))
            return token
    
    def scan_identifier(self):
        return self.scan(self.re_id)

    def scan_expr(self):
        return self.scan(self.re_expr)

    def scan_python_expr(self):
        return self.scan(self.re_python_expr)

    def scan_number(self):
        return self.scan(self.re_number)

    def scan_callfunc(self):
        return self.scan(self.re_callfunc)

    def scan_short_string(self):
        m = re.match(self.re_str, self.code)
        if m:
            s = m.group()
            self.next(len(s))
            return s
        self.error('unfinished string')

    def error(self, args: str):
        from difflib import get_close_matches
        
        ctx = getCtxByLine(self.getCurPos().line)
        get_tips = lambda s: ','.join(get_close_matches(s, syms))
        p = ErrorPrinter(
                info=f"{args}\n 喺 lexer 中察覺到有D痴线", pos=self.getCurPos(), ctx=ctx,
                tips=f" 係咪`\033[5;33m{get_tips(ctx[self.getCurPos().offset])}\033[0m` ??", _file=self.file)
        p.show()
        exit()

    def get_token(self) -> can_token:
        self.skip_space()
        if len(self.code) == 0:
            return can_token(self.getCurPos(), TokenType.EOF, 'EOF')

        c = self.code[0]
        
        if c == '&':
            start_pos = self.getCurPos()
            if self.check('&&'):
                self.next(2)
                return can_token(start_pos, TokenType.KEYWORD, '&&')
            else:
                self.next(1)
                return can_token(start_pos, TokenType.OP_BAND, '&')

        if c == '|':
            start_pos = self.getCurPos()
            if self.check('|>'):
                self.next(2)
                return can_token(start_pos, TokenType.SEPICFIC_ID_END, '|>')
            else:
                self.next(1)
                return can_token(start_pos, TokenType.KEYWORD, '|')

        if c == '%':
            start_pos = self.getCurPos()
            if self.check('%%'):
                self.next(2)
                return can_token(start_pos, TokenType.KEYWORD, kw_func_end)
            else:
                self.next(1)
                return can_token(start_pos, TokenType.OP_MOD, '%')

        if c == '~':
            start_pos = self.getCurPos()
            token = self.scan_python_expr()
            return can_token(start_pos, TokenType.CALL_NATIVE_EXPR, token)

        if c == '-':
            start_pos = self.getCurPos()
            if self.check('->'):
                self.next(2)
                return can_token(start_pos, TokenType.KEYWORD, kw_do)
            else:
                self.next(1)
                return can_token(start_pos, TokenType.OP_MINUS, '-')

        if c == '=':
            start_pos = self.getCurPos()
            if self.check('=>'):
                self.next(2)
                return can_token(start_pos, TokenType.KEYWORD, kw_do)
            elif self.check('==>'):
                self.next(3)
                return can_token(start_pos, TokenType.KEYWORD, '==>')
            elif self.check('=='):
                self.next(2)
                return can_token(start_pos, TokenType.OP_EQ, '==')
            else:
                self.next(1)
                return can_token(start_pos, TokenType.OP_ASSIGN, '=')
            
        if c == '$':
            start_pos = self.getCurPos()
            if self.check('$$'):
                self.next(2)
                return can_token(start_pos, TokenType.KEYWORD, '$$')
            self.next(1)
            return can_token(start_pos, TokenType.KEYWORD, '$')

        if c == '<':
            start_pos = self.getCurPos()
            if self.check('<*>'):
                self.next(3)
                return can_token(start_pos, TokenType.KEYWORD, '<*>')

            elif self.check('<|>'):
                self.next(3)
                return can_token(start_pos, TokenType.OP_BOR, '<|>')

            elif self.check('<->'):
                self.next(3)
                return can_token(start_pos, TokenType.OP_CONCAT, '<->')

            elif self.check('<$>'):
                self.next(3)
                return can_token(start_pos, TokenType.KEYWORD, '<$>')

            elif self.check('<='):
                self.next(2)
                return can_token(start_pos, TokenType.OP_LE, '<=')
            
            elif self.check('<<'):
                self.next(2)
                return can_token(start_pos, TokenType.OP_SHL, '<<')

            elif self.check('<|'):
                self.next(2)
                return can_token(start_pos, TokenType.SEPCIFIC_ID_BEG, '<|')

            else:
                self.next(1)
                return can_token(start_pos, TokenType.OP_LT, '<')
        
        if c == '>':
            start_pos = self.getCurPos()
            if self.check('>='):
                self.next(2)
                return can_token(start_pos, TokenType.OP_GE, '>=')
            elif self.check('>>'):
                self.next(2)
                return can_token(start_pos, TokenType.OP_SHR, '>>')
            else:
                self.next(1)
                return can_token(start_pos, TokenType.OP_GT, '>')

        if c == '!':
            start_pos = self.getCurPos()
            if self.check('!='):
                self.next(2)
                return can_token(start_pos, TokenType.OP_NE, '!=')
            else:
                self.next(1)
                return can_token(start_pos, TokenType.OP_NOT, '!')

        if c == '@':
            start_pos = self.getCurPos()
            if self.check('@@@'):
                self.next(3)
                return can_token(start_pos, TokenType.KEYWORD, '@@@')
            elif self.check('@@'):
                self.next(2)
                return can_token(start_pos, TokenType.KEYWORD, '@@')
            else:
                self.next(1)
                return can_token(start_pos, TokenType.KEYWORD, '@')
        
        if c == '{':
            start_pos = self.getCurPos()
            self.next(1)
            return can_token(start_pos, TokenType.SEP_LCURLY, '{')
        
        if c == '}':
            start_pos = self.getCurPos()
            self.next(1)
            return can_token(start_pos, TokenType.SEP_RCURLY, '}')

        if c == '(':
            start_pos = self.getCurPos()
            self.next(1)
            return can_token(start_pos, TokenType.SEP_LPAREN, '(')

        if c == ')':
            start_pos = self.getCurPos()
            self.next(1)
            return can_token(start_pos, TokenType.SEP_RPAREN, ')')

        if c == '[':
            start_pos = self.getCurPos()
            self.next(1)
            return can_token(start_pos, TokenType.SEP_LBRACK, '[')

        if c == ']':
            start_pos = self.getCurPos()
            self.next(1)
            return can_token(start_pos, TokenType.SEP_RBRACK, ']')

        if c == '.':
            start_pos = self.getCurPos()
            self.next(1)
            return can_token(start_pos, TokenType.SEP_DOT, c)

        if lexer.isChinese(c) or c == '_' or c.isalpha():
            start_pos = self.getCurPos()
            token = self.scan_identifier()
            token = zhconv.convert(token, 'zh-hk').replace("僕", "仆") 
            if token in self.keywords:
                return can_token(start_pos, TokenType.KEYWORD, token)
            return can_token(start_pos, TokenType.IDENTIFIER, token)
        
        if c in ('\'', '"'):
            start_pos = self.getCurPos()
            return can_token(start_pos, TokenType.STRING, self.scan_short_string())
        
        if c.isdigit():
            start_pos = self.getCurPos()
            token = self.scan_number()
            return can_token(start_pos, TokenType.NUM, token)

        if c == '+':
            start_pos = self.getCurPos()
            self.next(1)
            return can_token(start_pos, TokenType.OP_ADD, c)

        if c == '-':
            start_pos = self.getCurPos()
            self.next(1)
            return can_token(start_pos, TokenType.OP_MINUS, c)

        if c == '*':
            start_pos = self.getCurPos()
            if self.check('**'):
                self.next(2)
                return can_token(start_pos, TokenType.OP_POW, c)
            else:
                self.next(1)
                return can_token(start_pos, TokenType.OP_MUL, c)

        if c == '/':
            start_pos = self.getCurPos()
            if self.check('//'):
                self.next(2)
                return can_token(start_pos, TokenType.OP_IDIV, '//')
            else:
                self.next(1)
                return can_token(start_pos, TokenType.OP_DIV, c)

        if c == '&':
            start_pos = self.getCurPos()
            self.next(1)
            return can_token(start_pos, TokenType.OP_BAND, c)

        if c == '^':
            start_pos = self.getCurPos()
            self.next(1)
            return can_token(start_pos, TokenType.OP_WAVE, c)

        if c == ',':
            start_pos = self.getCurPos()
            self.next(1)
            return can_token(start_pos, TokenType.SEP_COMMA, ',')

        if c == '#':
            start_pos = self.getCurPos()
            if self.check('##'):
                self.next(2)
                return can_token(start_pos, TokenType.KEYWORD, '##')

            if self.check('#XD'):
                token = self.scan_python_expr()
                return can_token(start_pos, TokenType.CALL_NATIVE_EXPR, token)

        self.error(f"\033[0;31m濑嘢!!!\033[0m:睇唔明嘅Token: `{c}`")

def cantonese_token(file: str, code: str) -> list:
    
    global MMap, file_name
    MMap = list(map(lambda _ : zlib.compress(bytes(_, 'utf-8')), code.split('\n')))
    MMap.insert(0, "")

    code = remove_comment(code)
    lex: lexer = lexer(file, code, keywords)
    tokens: list = []

    while True:
        token = lex.get_token()
        tokens.append(token)
        if token.typ == TokenType.EOF:
            break
    return tokens