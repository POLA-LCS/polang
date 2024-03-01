from lexer import *

NONE_VAR = 'Literal'

class Var:
    def __init__(self, name: str, value: Optional[float | str] = None):
        self.name = name
        self.value = value
        if not value:
            self.type = None
        elif isinstance(value, str):
            self.type = 'string'
        elif isinstance(value, float | int):
            self.type = 'number'
            self.value = float(value)
    def __repr__(self) -> str:
        return f'({self.name}: {self.type} = {self.value})'
        
class Ram:
    def __init__(self):
        self.vars: list[Var] = []
    
    def get_var(self, name: str):
        for var in self.vars:
            if var.name == name:
                return var
            
    def del_var(self, name: str):
        for var in self.vars:
            if var.name == name:
                self.vars.remove(var)
                break
            
    def set_var(self, name: str, value: str | float):
        self.del_var(name)
        self.vars.append(Var(name, value))
        
    def __repr__(self) -> str:
        return f'{self.vars}'

class Op(Enum):
    set = auto()
    out = auto()

class Operation:
    def __init__(self, type: Op, args: Optional[tuple] = (None, None)):
        self.type = type
        self.args = args
        
    def __repr__(self) -> str:
        return '{' + f'{self.type}' + f': {self.args}' + '}'
        
Program = list[Operation]

def set_var(name: str, value: str | float | Var):
    value = float(value) if isinstance(value, int) else value
    return Operation(Op.set, (name, value))

def main():
    program: Program = [
        set_var('a', 1),
        set_var('b', 2),
        set_var('tmp', Var('a')),
        set_var('a', Var('b')),
        set_var('b', Var('tmp'))
    ]

    ram = Ram()
    for i, op in enumerate(program):
        name, value = op.args
        if op.type == Op.set: # SET A VARIABLE IN THE RAM
            var = ram.get_var(name)
            
            if var:
                foo = ram.get_var(value.name) if isinstance(value, Var) else Var(NONE_VAR, value)
                if not foo:
                    ERROR(f"variable doesn't exist: {value}")
                if var.type != foo.type:
                    ERROR(f"types don't match: {var} <- {foo}")
                var.value = foo.value
            else:
                foo = ram.get_var(value.name) if isinstance(value, Var) else Var(NONE_VAR, value)
                if not foo:
                    ERROR(f"variable doesn't exist: {value}")
                ram.set_var(name, foo.value)

            
    print(ram)

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        DEV(err)