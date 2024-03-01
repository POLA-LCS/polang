from typing import Optional
from enum import Enum, auto
from icecream import ic as DEV

def ERROR(message: str):
    assert False, message

class TType(Enum):
    none = auto()
    
    unknown = auto()
    
    string = auto() # ''
    number = auto() # 0123456789.
    operation = auto() # + - < > is not

    colon = auto() # :
    set_can = auto() # unknown:

    lbrace = auto()
    rbrace = auto()
    dot = auto()
    
    comment = auto()
class Token:
    def __init__(self, type: TType, value: Optional[tuple]):
        self.type = type
        self.value = value
        
    def __repr__(self) -> str:
        if self.value:
            return f'[{self.type}: {self.value}]'
        return f'[{self.type}]'

OPERANDS = ['+', '-', '*', '/', '<', '>', 'is', 'not']


def lex(string: str) -> list[Token]:
    tokens: list[Token] = []
    
    def app(kind: TType, value: Optional[tuple]):
        tokens.append(Token(kind, value))
        
    string = string.split(' ')
    
    record = ''
    scope = None
    expect = None
    for i, part in enumerate(string):
        if not scope:
            record += part
            if record.startswith("\'"): # FOUND A STRING
                if record.endswith("\'"): # SINGLE STEP STRING
                    app(TType.string, (record[1:-1],))
                    scope = None
                    record = ''
                else:
                    scope = 'string'
                    record += ' '
            elif record.startswith('_'):
                if record.endswith('_'): # SINGLE STEP COMMENTS
                    app(TType.comment, (record[1:-1],))
                    scope = None
                    record = ''
                else:
                    scope = 'comment'
                    record += ' '
            elif record == '[':
                app(TType.lbrace)
                record = ''
            elif record == ']':
                app(TType.rbrace)
                record = ''
            elif record == '.':
                app(TType.dot)
                record = ''
            elif record.isdigit():
                app(TType.number, (record,))
                record = ''
            elif record in OPERANDS: # OPERANDS
                app(TType.operation, (record,))
                record = ''
            elif record == ':':
                app(TType.colon, None)
                record = ''
            elif record.endswith(':'): # SET CANDIDATE
                app(TType.set_can, (record[:-1],))
                record = ''
            elif record == 'out':
                app(TType.out)
                record = ''
            else:
                app(TType.unknown, (record,))
                record = ''
        elif scope == 'string':
            record += part + ' '
            if record.endswith("\' "): # FOUND END OF THE STRING
                app(TType.string, (record[1:-2],))
                scope = None
                record = ''
        elif scope == 'comment':
            record += part + ' '
            if record.endswith('_ '):
                app(TType.comment, (record[1:-2],))
                scope = None
                record = ''
            
    return tokens