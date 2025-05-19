import sys

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
            print('Usage: COEFFS <coeffs_number')
            sys.exit(1)
        coeffsCount = int(potential_digit, 10)
        currLine += 1
        for i in range(coeffsCount):
            line = lines[currLine]
            s = line.split(' ')
            if len(s) != 2:
                print(f'In COEFFS section the coeff-value pairs must be presented; got: {s}')
                sys.exit(1)
            k = s[1][:-1]
            if not k.isdigit():
                print(f'In COEFFS section the coeff-value pairs must be presented; got: {s}')
                sys.exit(1)
            ks.append(int(k, 10))
            currLine += 1

        if len(lines[currLine][:-1]) != 0:
            print('After each section there must be an empty line')
            sys.exit(1)

        currLine += 1
        line = lines[currLine][:-1]
        if 'CS' not in line:
            print("CS section is expected")
            sys.exit(1)
        potential_digit = line.split(' ')
        if len(potential_digit) != 2:
            print('CS section must contain the number of variables')
            sys.exit(1)
        potential_digit = potential_digit[1]
        if not potential_digit.isdigit():
            print('CS must contain the number of variables')
            sys.exit(1)

        c_count = int(potential_digit, 10)

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
        return ks, c_count, equations
"""
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: diff_equ.py <input_file_name>")
        sys.exit(1)
        
    filename = sys.argv[1]
    ks, c_count, equations_str = read_file(filename)
"""

class CParser:
    def __init__(self, program):
        self.program = program
        self.curr_char = 0

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

    def s(self):
        self.expr()

    def expr(self):
        self.num()
        while True:
            op = self.get_next_char()
            if op == '+':
                self.move_next()
                self.num()
                print('+ ')
            elif op == '':
                break
            else:
                self.move_next()
                continue

    def num(self):
        token = self.get_next_token()
        if len(token) == 0:
            return
        print(token + ' ')
        
parser = CParser(input())
parser.s()