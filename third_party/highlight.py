def highlight(string):
    attr = []
    if "-" in string:
        # red
        attr.append('31')
    else:
        # green
        attr.append('32')

    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)