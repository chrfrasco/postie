from postie import Postie

def main():
    postie = Postie()

    # Basic addition
    assert postie.run_line('1 1 +') == 2

    # More complicated expressions
    assert postie.run_line('5 1 2 + 4 * + 3 -') == 14

    # Variable assignment
    postie.run_line('a 3 =')
    postie.run_line('b 4 =')
    assert postie.run_line('a b *') == 11

    print('All tests passed!')

if __name__ == '__main__':
    main()
