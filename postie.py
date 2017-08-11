from collections import deque
import math
import sys

WHITESPACE = (' ', '\n')
OPERATORS = ('+', '-', '*', '/')
GLOBALS = dict()


class Postie:
    def __init__(self, out=print, err=print):
        self.__identifiers = GLOBALS
        self.__print = out
        self.__err = err

    def run_repl(self):
        """Start the REPL."""
        while True:
            line = input('> ').strip()
            try:
                res = self.run_line(line)
                self.__print(res)
            except ValueError as e:
                self.__err(f'Error: {e}')

    def run_file(self, filepath):
        """Run a .postie file."""
        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f):
                try:
                    self.run_line(line)
                except ValueError as e:
                    self.__err(f'Error on line {line_num}: {e}')

    def run_line(self, line):
        """Process a line."""
        calc_stack = deque()
        token_queue = deque(line)

        while token_queue:
            token = token_queue.popleft()

            if token in WHITESPACE:
                continue

            elif token == '=':
                if len(calc_stack) < 2:
                    raise ValueError(f'Not enough arguments for "{token}"')
                if len(calc_stack) > 2:
                    raise ValueError(f'Assigment must be the last operation')

                first = calc_stack.pop()
                second = calc_stack.pop()

                if self.__is_identifier(second):
                    self.__identifiers[second] = first
                    return f'{second} = {first}'
                else:
                    raise ValueError(f'Cannot assign {second} to {first}')

            elif token in OPERATORS:
                if len(calc_stack) < 2:
                    raise ValueError(f'Not enough arguments for "{token}"')

                first = self.__get_value(calc_stack.pop())
                second = self.__get_value(calc_stack.pop())
                value = self.__apply(first, second, token)

                calc_stack.append(value)

            elif self.__is_numeral(token):
                number_literal = token

                while token_queue and token_queue[0] not in WHITESPACE:
                    token = token_queue.popleft()
                    if self.__is_numeral(token) or token == '.':
                        number_literal += token
                    elif self.__is_alpha(token):
                        raise ValueError('Identifiers must not begin with numbers')
                    else:
                        raise ValueError(f'Bad symbol "{token}" in numeric literal')

                calc_stack.append(number_literal)

            elif self.__is_alpha(token):
                identifier = token

                while token_queue and token_queue[0] not in WHITESPACE:
                    token = token_queue.popleft()
                    if self.__is_alphanumeric(token):
                        identifier += token
                    else:
                        raise ValueError(f'Bad symbol "{token}" in identifier')

                calc_stack.append(identifier)

        if len(calc_stack) == 1:
            return self.__get_value(calc_stack.pop())
        else:
            print(calc_stack)
            raise ValueError(f'Too many arguments')

    def __apply(self, first, second, operator):
        if operator == '+':
            return second + first
        elif operator == '-':
            return second - first
        elif operator == '*':
            return second * first
        elif operator == '/':
            return second / first
        else:
            raise ValueError(f'Unknown operator "{operator}"')

    def __get_value(self, symbol):
        if type(symbol) == str:
            if self.__is_identifier(symbol):
                if symbol in self.__identifiers:
                    return self.__get_value(self.__identifiers[symbol])
                else:
                    raise ValueError(f'Unknown identifier "{symbol}"')

            if self.__is_number(symbol):
                if self.__is_int(symbol):
                    return int(symbol)
                else:
                    return float(symbol)

        return symbol

    def __is_alpha(self, token):
        return token in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __is_numeral(self, token):
        return token in '1234567890'

    def __is_alphanumeric(self, token):
        return self.__is_numeral(token) or self.__is_alpha(token)

    def __is_identifier(self, symbol):
        return (
            type(symbol) == str and
            self.__is_alpha(symbol[0]) and
            all(self.__is_alphanumeric(token) for token in symbol)
        )

    def __is_number(self, symbol):
        return all(
            self.__is_numeral(token) or token == '.'
            for token in symbol
        )

    def __is_int(self, symbol):
        return all(self.__is_numeral(token) for token in symbol)


if __name__ == '__main__':
    postie = Postie()

    if len(sys.argv) == 1:
        postie.run_repl()
    elif len(sys.argv) == 2:
        postie.run_file(sys.argv[1])
    else:
        print('Usage: postie [filename]')
