from postie import Postie

def main():
    postie = Postie()
    run = postie.run_line

    # Basic addition
    assert run('1 1 +') == 2

    # More complicated expressions
    assert run('5 1 2 + 4 * + 3 -') == 14

    # Variable assignment
    run('a 3 =')
    run('b 4 =')
    assert run('a b *') == 12

    # Floating point numbers
    run('a 9.2 =')
    run('b 2.3 =')
    assert run('a b /') == 4

    print('All tests passed!')

if __name__ == '__main__':
    main()
