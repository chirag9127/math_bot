def correct(original, output):
    newString = []
    index = 0
    while index < len(original):
        if output and len(output) > 0 and index == output[0][0]:
            newString.append(output[0][1])
            if output and len(output) > 0:
                output.pop(0)
            index += get_len_diff(original, index)
        else:
            newString.append(original[index])
            index += 1
    return ''.join(newString)


def get_len_diff(original, start):
    beg = start
    while (start < len(original) and original[start] != ' '):
        start += 1
    return start-beg


if __name__ == "__main__":
    correct('i wnt ot lern algebra', [(2, 'want'), (6, 'to'), (9, 'learn')])
