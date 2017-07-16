import re

def unfold(s):
    return re.sub(r'[ \t]*[\r\n][ \t\r\n]*', ' ', s).strip(' ')

def ascii_splitlines(s):
    lines = []
    lastend = 0
    for m in re.finditer(r'\r\n?|\n', s):
        lines.append(s[lastend:m.end()])
        lastend = m.end()
    if lastend < len(s):
        lines.append(s[lastend:])
    return lines
