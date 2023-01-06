def anonymize_name(name, anonymize=True, num_chars_beginning=1, num_chars_end=1, hidden_char='*'):
    if not anonymize:
        return name
    chars = []
    if num_chars_beginning + num_chars_end >= len(name):
        return name
    for i in range (0, num_chars_beginning, 1):
        chars.append(name[i])
    for i in range(num_chars_beginning, len(name) - num_chars_end, 1):
        chars.append(hidden_char)
    for i in range(len(name) - num_chars_end, len(name), 1):
        chars.append(name[i])

    return "".join(chars)
