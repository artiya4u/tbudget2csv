specials = ['ุ', 'ู', 'ึ', 'ำ', 'ั', 'ี', '้', '็', '่', '๋']


def fix_align(txt):
    input_txt = list(txt)
    result = list('')
    skip_next = False
    for idx, val in enumerate(input_txt):
        if val in specials and idx > 1 and idx + 1 < len(input_txt) and input_txt[idx + 1] == ' ':
            temp = result.pop()
            result.append(val)
            result.append(temp)
            skip_next = True
        else:
            if not skip_next:
                result.append(val)
            skip_next = False

    return ''.join(result)
