import sys
import matplotlib.pyplot as plt
import json
import argparse

MEMORY = {
    'k': {

    },
    'c': {

    },
    'equations': []
}

class Token:
    def value(self):
        #assert False, "You must override this method"
        return None

    def __str__(self) -> str:
        return "Token"

class Literal(Token):
    def __init__(self, value: int):
        self.__value: int = value

    def __str__(self) -> str:
        return f"Literal({self.__value})"

    def value(self):
        return self.__value

class Neg:
    def __init__(self, token: Token):
        self.token = token

    def __str__(self) -> str:
        return f'-{self.token.__str__()}'

    def value(self):
        return self.token.value() * -1

class Var:
    def __init__(self, label):
        self.label = label

    def __str__(self) -> str:
        return self.label

    def value(self):
        return None

class KVar(Var):
    def __init__(self, label):
        super().__init__(label)

    def value(self):
        return MEMORY['k'][self.label]

class CVar(Var):
    def __init__(self, label):
        super().__init__(label)

    def value(self):
        return MEMORY['c'][self.label]

class Op(Token):
    def __init__(self, operand1: Token, operand2: Token):
        self.operand1: Token = operand1
        self.operand2: Token = operand2
    
    def value(self):
        return None

class Add(Op):
    def __init__(self, operand1, operand2):
        super().__init__(operand1, operand2)

    def __str__(self) -> str:
        return f"Add({self.operand1.__str__(), self.operand2.__str__()})"
        
    def value(self):
        return self.operand1.value() + self.operand2.value()

class Sub(Op):
    def __init__(self, operand1, operand2):
        super().__init__(operand1, operand2)

    def __str__(self) -> str:
        return f"Sub({self.operand1.__str__(), self.operand2.__str__()})"

    def value(self):
        return self.operand1.value() - self.operand2.value()

class Mul(Op):
    def __init__(self, operand1, operand2):
        super().__init__(operand1, operand2)

    def __str__(self) -> str:
        return f"Mul({self.operand1.__str__(), self.operand2.__str__()})"

    def value(self):
        return self.operand1.value() * self.operand2.value()

class CParser:
    def __init__(self, program):
        self.program: str = program
        self.curr_char = 0
        self.stack = list()

    def get_next_char(self):
        if self.curr_char == len(self.program):
            return ""
        next_char = self.program[self.curr_char]
        return next_char

    def move_next(self):
        self.curr_char += 1

    def get_next_token(self):
        token = ""
        while True:
            char = self.get_next_char()
            if char == ' ':
                if len(token) == 0:
                    self.move_next()
                    continue
                else:
                    return token
            if char == '':
                return token
            if char.isdigit() or char.isalpha() or (char == '-' and len(token) == 0):
                token += char
                self.move_next()
                continue
            return token    

    def parse(self):
        self.expr()

    def expr(self):
        self.num()
        while True:
            op = self.get_next_char()
            if op == '+':
                self.move_next()
                self.factor()
                operand2 = self.stack[-1]
                self.stack.pop()
                operand1 = self.stack[-1]
                self.stack.pop()
                self.stack.append(Add(operand1, operand2))
            elif op == '-':
                self.move_next()
                self.factor()
                operand2 = self.stack[-1]
                self.stack.pop()
                operand1 = self.stack[-1]
                self.stack.pop()
                self.stack.append(Sub(operand1, operand2))
            elif op == '' or op in ')':
                break
            else:
                self.factor()

    def factor(self):
        self.num()
        while True:
            op = self.get_next_char()
            if op == '*':
                self.move_next()
                self.num()
                operand2 = self.stack[-1]
                self.stack.pop()
                operand1 = self.stack[-1]
                self.stack.pop()
                self.stack.append(Mul(operand1, operand2))
            elif op == '(':
                self.move_next()
                self.expr()
                if self.get_next_char() != ')':
                    print(f"'(' is not closed. Please check again: {self.program}")
                self.move_next()
            else:
                return

    def num(self):
        token = self.get_next_token()
        if len(token) == 0:
            return
        is_signed = token[0] == '-'
        token_str = token if not is_signed else token[1:]
        if token_str.isdigit():
            result = Literal(int(token_str, 10))
        elif token_str[0] == "k":
            result = KVar(token_str)
        elif token_str[0] == "c":
            result = CVar(token_str)
        else:
            assert False, f"The way of treating the token '{token}' is unspecified"
        
        self.stack.append(Neg(result) if is_signed else result)


def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        currLine = 0
        if "COEFFS" not in lines[currLine]:
            print('COEFFS section must be in the beginning')
            sys.exit(1)

        ks = list()
        coeffsCount = lines[currLine].split(' ')
        potential_digit = coeffsCount[1][:-1]
        if len(coeffsCount) != 2 or not potential_digit.isdigit():
            print('Usage: COEFFS coeffs_number')
            sys.exit(1)
        coeffsCount = int(potential_digit, 10)
        currLine += 1
        for i in range(coeffsCount):
            line = lines[currLine]
            s = line.split(' ')
            if len(s) != 2:
                print(f'In COEFFS section the coeff-value pairs must be presented; got: {s}')
                sys.exit(1)
            k_name = s[0]
            k_value = s[1][:-1]
            if not k_value.isdigit():
                print(f'In COEFFS section the coeff-value pairs must be presented; got: {s}')
                sys.exit(1)
            ks.append((k_name, float(k_value)))
            currLine += 1

        if len(lines[currLine][:-1]) != 0:
            print('After each section there must be an empty line')
            sys.exit(1)

        currLine +=1 
        line = lines[currLine][:-1]
        if 'EQUATIONS' not in line:
            print('EQUATIONS is expected')
            sys.exit(1)
        
        potential_digit = line.split(' ')
        if len(potential_digit) != 2:
            print('You must specify the number of equations in EQUATIONS section')
            sys.exit(1)

        potential_digit = potential_digit[1]
        if not potential_digit.isdigit():
            print('EQUATIONS must contain the number of equations')
            sys.exit(1)
        potential_digit = int(potential_digit, 10)
        currLine += 1
        equations = list()
        for i in range(potential_digit):
            line = lines[currLine][:-1]
            equations.append(line)
            currLine += 1
        
        currLine += 1
        line = lines[currLine][:-1]
        if 'STEPS' not in line:
            print('STEPS is expected')
            sys.exit(1)
        steps = line.split(' ')
        if len(steps) != 2:
            print('You must specify the number of steps in STEPS section')
            sys.exit(1)
        steps = int(steps[1], 10)
        
        currLine += 2
        line = lines[currLine]
        if 'H' not in line:
            print('H is expected')
            sys.exit(1)
        h = line.split(' ')
        if len(h) != 2:
            print('You must specify the step size in H section')
            sys.exit(1)
        h = float(h[1])
        
        currLine += 2
        line = lines[currLine]
        if 'X0' not in line:
            print('X0 is expected')
            sys.exit(1)
        x0 = line.split(' ')
        if len(x0) != 2:
            print('You must specify the step size in X0 section')
            sys.exit(1)
        x0 = float(x0[1])
        return ks, len(equations), equations, steps, h, x0

def eiler(x0, count, h, c_count):
    c: list[list] = list([[value for _, value in MEMORY['c'].items()]]) #создание массива y с начальными условиями
    x = x0
    for i in range (1, count):
        right_parts = list([equation.value() for equation in MEMORY['equations']])
        c.append ([]) #добавление пустой строки
        for j in range (c_count):
            c[i].append(c[i-1][j] + h * right_parts[j])
            MEMORY['c'][f'c{j}'] = c[i][j]
        x += h
    return c

if __name__ == "__main__":
    cmd_parser = argparse.ArgumentParser()
    cmd_parser.add_argument('filename', help='Specify the file where the input data is stored')
    cmd_parser.add_argument('-o', '--output', default=None, nargs=1, help='Specify the json file name where the results must be stored. Note: the name must be without an extension')
    cmd_parser.add_argument('--image_show', const=True, nargs='?', help="Show the graphics of the process")
    cmd_parser.add_argument('--image_save', nargs=1, help="Save the graphics of the process into a file. Note: the file extention must be the part of the file name")

    args = cmd_parser.parse_args()
    print(args)
    
    if args.filename is None:
        cmd_parser.print_help()
        sys.exit(1)
        
    print('[INFO] Reading the file')
    ks, c_count, equations_str, steps, h, x0 = read_file(args.filename)

    print('[INFO] Setting up k coefficients')
    for k in ks:
        MEMORY['k'][k[0]] = k[1]
    print('[INFO] Done setting up k coefficients')
    
    print('[INFO] Setting up c equations')
    for i in range(c_count):
        MEMORY['c'][f'c{i}'] = 0
    MEMORY['c']['c0'] = 1
    print('[INFO] Done setting up c equations')

    print('[INFO] Start parsing the equations')
    for equation in equations_str:
        print(f"[INFO] Parse the equation '{equation}'")
        parser = CParser(equation)
        parser.parse()
        MEMORY['equations'].append(*parser.stack)
    print('[INFO] Start parsing the equations')
    
    print('[INFO] Start doing calculations')
    result = eiler(x0, steps, h, c_count)
    print('[INFO] Done doing calculations')

    c_results = list([[c[i] for c in result] for i in range(c_count)])

    if args.output is not None:
        print(f'[INFO] Saving the results into the file {args.output[0]}')
        result_json = json.dumps({f'c{i}': c_results[i] for i in range(len(c_results))})
        with open(f'{args.output[0]}.json', 'w') as output_file:
            output_file.write(result_json)
        print(f'[INFO] Successfully saved into the file {args.output[0]}')

    if args.image_show is not None or args.image_save is not None:
        X = list([x0 + i * h for i in range(steps)])
        for c in c_results:
            plt.plot(X, c)
        
        plt.legend([f'c{i}' for i in range(c_count)])
        
        if args.image_save is not None:
            print(f'[INFO] Saving the graphics into the file {args.image_save[0]}')
            plt.savefig(args.image_save[0])
            print(f'[INFO] Successfully saved the graphics into the file {args.image_save[0]}')

        if args.image_show is not None:
            plt.show()
