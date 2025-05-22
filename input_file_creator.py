print("Hello! Welcome to the Input File Creator! The process is done step-by-step. Please be careful when typing the info")
content = ""
coeffs_count = 0
while coeffs_count <= 0:
    coeffs_count = int(input("Input the number of coefficients (k-labeled). The number must be positive: "))
content += f"COEFFS {coeffs_count}\n"

print('Now you are supposed to specify the k coeffs and their values. Each k is typed in a new line')
for i in range(coeffs_count):
    label, value = input("Input the name of k and its value (space between is required): ").split()
    content += f'{label} {value}\n'

content += '\n'
    
c_count = 0
while c_count <= 0:
    c_count = int(input('Input the number of equations: '))
content += f"EQUATIONS {c_count}\n"

print('Now you are supposed to type the equations themselves line-by-line')
for i in range(c_count):
    equation = input(">> ")
    content += equation + "\n"

content += '\n'

steps = 0
while steps <= 0:
    steps = int(input('Input the number of steps: '))
content += f"STEPS {steps}\n"

content += '\n'

h = 0.0
while h <= 0.0:
    h = float(input('Input the step size (e.g. 0.1): '))
content += f"H {h}\n"

content += '\n'

x0 = 0.0
while x0 < 0.0:
    x0 = float(input('Input X0: '))
content += f"X0 {x0}"

print()
print('The result is:')
print('=' * 20)
print(content)
print('=' * 20)
print()

output_file_name = input('Please type the file name (with extension) where to store the data: ')
with open(output_file_name, 'w') as f:
    f.write(content)