import regex


def count_graphemes(text):

    if not text:
        return 0
    return len(regex.findall(r"\X", text))
