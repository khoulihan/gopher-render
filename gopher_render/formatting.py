import textwrap

# TODO: Add additional formatting helper functions
# TODO: Add the formatting classes/functions here

def full_justify(text, width, **kwargs):
    lines = textwrap.wrap(text, width, **kwargs)
    out_lines = []
    for line in lines[:-1]:
        orig_len = len(line)
        ls = line.lstrip()
        indent = ' ' * (orig_len - len(ls))
        padding_spaces = width - orig_len
        rs = ls.rstrip()
        #padding_spaces = len(ls) - len(rs)
        if padding_spaces == 0:
            out_lines.append(line)
            continue
        words = rs.split(' ')
        gaps = (len(words) - 1)
        if gaps == 0:
            out_lines.append(line)
            continue
        n, r = divmod(padding_spaces, gaps)
        narrow = ' ' * (n + 1)
        if r == 0:
            # No remainder
            out_lines.append(indent + narrow.join(words))
        else:
            wide = ' ' * (n + 2)
            out_lines.append(indent + wide.join(words[:r]) + wide + narrow.join(words[r:]))
    out_lines.append(lines[-1])
    for l in out_lines:
        print(len(l))
    return '\n'.join(out_lines)
