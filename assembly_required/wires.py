import sys

FILENAME = sys.argv[1]
TARGET = sys.argv[2]

OPERATIONS = {}  # In the form of {'letter': [var1, operator, var2]} where [] can vary
RESULTS = {}  # In the form of {'letter': 'result'}


def find(target):
    if target.isdigit():  # Covers the case the target comes from an operation but it is an integer
        return int(target)

    if target in RESULTS:  # Speeds up and avoids a potential circular recursion call
        return RESULTS[target]

    try:
        operation = OPERATIONS[target]
    except KeyError:
        print(f'Something is wrong with the input. {target} does not exist')
        sys.exit(0)

    if len(operation) == 1:
        try:
            RESULTS[target] = int(operation[0])  # We got to an end with an integer...
        except ValueError:
            return find(operation[0])  # ...or we found another non-numerical element

    elif len(operation) == 2:
        # Python's NOT bitwise operator is two's complement which means it's gonna
        # return -n - 1, or a signed integer (~4 will be -5, so a 4 bit representation
        # or 2^4, allows us to write 16 ints from -8 to 7).
        # What we want to achieve is the unsigned int, which goes from
        # 0 to 15 so we need to mask it with 0xFFFF (4 bits for each hexa, so 16 in total
        # or 2^16 which is 65535). We are doing the negation of N, or 65535 - N. So NOT 1 = 65534, NOT 2 = 65533...
        RESULTS[target] = ~find(operation[1]) & 0xFFFF
    else:
        operator = operation[1]

        if operator == 'AND':
            res = find(operation[0]) & find(operation[2])
        elif operator == 'OR':
            res = find(operation[0]) | find(operation[2])
        elif operator == 'RSHIFT':
            res = find(operation[0]) >> int(operation[2])
        elif operator == 'LSHIFT':
            res = find(operation[0]) << int(operation[2])

        RESULTS[target] = res

    OPERATIONS.pop(target)

    return RESULTS[target]


if __name__ == '__main__':

    with open(FILENAME, 'r') as infile:
        for line in infile.read().splitlines():
            op, letter = line.split(' -> ')
            OPERATIONS[letter] = op.split(' ')

    print(find(TARGET))
