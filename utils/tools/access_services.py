import random
import string
import strgen


def password_generate(length=8):
    """
    Generate random password with minimum 2 digits, 2 uppercase and 2 lowercase chars
    Exclude symbols: I,l,1,O,0
    """
    if length < 6:
        length = 6

    accepted_symbols_lower = 'abcdefghijkmnopqrstuvwxyz'
    accepted_symbols_upper = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    accepted_digits = '23456789'
    accepted_chars = accepted_symbols_upper + accepted_symbols_lower + accepted_digits

    password_mask = '[{chars}]{{{length}}}&[{digits}]{{2}}&[{upper}]{{2}}&[{lower}]{{2}}'.format(
        length=length - 6,
        lower=accepted_symbols_lower,
        upper=accepted_symbols_upper,
        digits=accepted_digits,
        chars=accepted_chars
    )
    return strgen.StringGenerator(password_mask).render()


def carddav_pin_generate():
    """
    Generate random CardDav PIN (6 digits)
    """
    return ''.join(random.choice(string.digits) for x in range(0, 6))
