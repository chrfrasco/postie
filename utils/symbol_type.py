"""
Functions for detecting the type of value represented by the supplied string
"""

def is_alpha(token):
    return token in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def is_numeral(token):
    return token in '1234567890'


def is_alphanumeric(token):
    return is_numeral(token) or is_alpha(token)


def is_identifier(symbol):
    """Identifiers may contain alphabet characters (upper/lower) and numerals,
    as long as the identifier begins with an alphabet character."""
    return (
        type(symbol) == str and
        is_alpha(symbol[0]) and
        all(is_alphanumeric(token) for token in symbol)
    )


def is_number(symbol):
    """Numbers may contain numerals or decimal points."""
    return all(
        is_numeral(token) or token == '.'
        for token in symbol
    )


def is_int(symbol):
    """Integers may only contain numerals."""
    return all(is_numeral(token) for token in symbol)
