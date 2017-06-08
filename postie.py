import sys


class Postie:
    def __init__(self):
        pass

    def run_repl(self):
        """Start the REPL."""
        while True:
            line = input('> ')
            self.__run_line(line)

    def run_file(self, filepath):
        """Run a .postie file."""
        with open(filepath, 'r') as f:
            for line in f:
                self.__run_line(line)

    def __run_line(self, line):
        """Process a line."""
        print(line)


if __name__ == '__main__':
    postie = Postie()

    if len(sys.argv) == 1:
        postie.run_repl()
    elif len(sys.argv) == 2:
        postie.run_file(sys.argv[1])
    else:
        print('Usage: postie [filename]')

