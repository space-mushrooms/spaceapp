
def change_keyboard_layout(string, src='en', dst='ru'):
    """
    Change string letters to another keyboard layout
    """
    layout = {
        'en': 'qwertyuiop[]asdfghjkl;\'\zxcvbnm,./',
        'ru': 'йцукенгшщзхъфывапролджэ\\ячсмитьбю.',
    }
    mapping = {}

    for i, x in enumerate(list(layout[src])):
        mapping[x] = layout[dst][i]

    result = [mapping.get(x) if mapping.get(x) else x for x in list(string)]

    return ''.join(result)
