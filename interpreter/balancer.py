stack = []

tks = '()<[]>[<[()]>]'

matches = {
    '(': ')',
    '[': ']',
    '<': '>',
}

for k in list(matches.keys()):
    v = matches[k]
    matches[v]= k

def is_opening(tk):
    return tk in ['(', '[', '<']

def is_closing(tk):
    return tk in [']', ')', '>']



for tk in tks:
    if is_opening(tk):
        stack.append(tk)
    elif is_closing(tk) and stack[-1] == matches[tk]:
        stack.pop()
    else:
        raise RuntimeError()

if len(stack) != 0:
    raise RuntimeError()
print('balanced')


