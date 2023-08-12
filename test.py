_matritsa = [
    [1, 2, 3, 4],
    [6, 2, 0, 3]
]

_min = _matritsa[0][0]

for _list in _matritsa:
    for i in _list:
        if _min>i:
            _min = i

print(_min)
