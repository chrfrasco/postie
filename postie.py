from collections import deque, namedtuple
import math
import sys

from utils.symbol_type import *

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
        token_stack = deque()
        char_queue = deque(line)

        while char_queue:
            next_char = char_queue.popleft()

            if next_char in WHITESPACE:
                continue

            elif next_char == '=':
                if len(token_stack) < 2:
                    raise ValueError(f'Not enough arguments for "{next_char}"')
                if len(token_stack) > 2:
                    raise ValueError(f'Assigment must be the last operation')

                first = token_stack.pop()
                second = token_stack.pop()

                if is_identifier(second):
                    self.__identifiers[second] = first
                    return f'{second} = {first}'
                else:
                    raise ValueError(f'Cannot assign {second} to {first}')

            elif next_char in OPERATORS:
                if len(token_stack) < 2:
                    raise ValueError(f'Not enough arguments for "{next_char}"')

                first = self.__get_value(token_stack.pop())
                second = self.__get_value(token_stack.pop())
                value = self.__apply(first, second, next_char)

                token_stack.append(value)

            elif is_numeral(next_char):
                number_literal = next_char

                while char_queue and char_queue[0] not in WHITESPACE:
                    next_char = char_queue.popleft()
                    if is_numeral(next_char) or next_char == '.':
                        number_literal += next_char
                    elif is_alpha(next_char):
                        raise ValueError('Identifiers must not begin with numbers')
                    else:
                        raise ValueError(f'Bad symbol "{next_char}" in numeric literal')

                token_stack.append(number_literal)

            elif is_alpha(next_char):
                identifier = next_char

                while char_queue and char_queue[0] not in WHITESPACE:
                    next_char = char_queue.popleft()
                    if is_alphanumeric(next_char):
                        identifier += next_char
                    else:
                        raise ValueError(f'Bad symbol "{next_char}" in identifier')

                token_stack.append(identifier)

        if len(token_stack) == 1:
            return self.__get_value(token_stack.pop())
        else:
            print(token_stack)
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
            if is_identifier(symbol):
                if symbol in self.__identifiers:
                    return self.__get_value(self.__identifiers[symbol])
                else:
                    raise ValueError(f'Unknown identifier "{symbol}"')

            if is_number(symbol):
                if is_int(symbol):
                    return int(symbol)
                else:
                    return float(symbol)

        return symbol


if __name__ == '__main__':
    postie = Postie()

    if len(sys.argv) == 1:
        postie.run_repl()
    elif len(sys.argv) == 2:
        postie.run_file(sys.argv[1])
    else:
        print('Usage: postie [filename]')
