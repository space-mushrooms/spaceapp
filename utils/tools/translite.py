translit_mapping = (
    ('Щ', 'Sch'), ('Щ', 'SCH'), ('Ё', 'Yo'), ('Ё', 'YO'), ('Ж', 'Zh'), ('Ж', 'ZH'), ('Ц', 'Ts'), ('Ц', 'TS'),
    ('Ч', 'Ch'), ('Ч', 'CH'), ('Ш', 'Sh'), ('Ш', 'SH'), ('Ы', 'Yi'), ('Ы', 'YI'), ('Ю', 'Y'), ('Ю', 'Y'),
    ('Я', 'Ya'), ('Я', 'YA'),

    ('А', 'A'), ('Б', 'B'), ('В', 'V'), ('Г', 'G'), ('Д', 'D'), ('Е', 'E'), ('З', 'Z'), ('И', 'I'), ('Й', 'Y'),
    ('К', 'K'), ('Л', 'L'), ('М', 'M'), ('Н', 'N'), ('О', 'O'), ('П', 'P'), ('Р', 'R'), ('С', 'S'), ('Т', 'T'),
    ('У', 'U'), ('Ф', 'F'), ('Х', 'H'), ('Э', 'E'), ('Ъ', '`'), ('Ь', ''),

    ('щ', 'sch'), ('ё', 'yo'), ('ж', 'zh'), ('ц', 'ts'), ('ч', 'ch'), ('ш', 'sh'), ('ы', 'y'), ('ю', 'y'),
    ('я', 'ya'),

    ('а', 'a'), ('б', 'b'), ('в', 'v'), ('г', 'g'), ('д', 'd'), ('е', 'e'), ('з', 'z'), ('и', 'i'), ('й', 'y'),
    ('к', 'k'), ('л', 'l'), ('м', 'm'), ('н', 'n'), ('о', 'o'), ('п', 'p'), ('р', 'r'), ('с', 's'), ('т', 't'),
    ('у', 'u'), ('ф', 'f'), ('х', 'h'), ('э', 'e'), ('ь', '')
)


def translitirate_to_latin(string):
    if not string:
        return ''

    for symb_in, symb_out in translit_mapping:
        string = string.replace(symb_in, symb_out)

    return string
