
key_map={
    "1": [""],
    "2": ["a","b","c"],
    "3": ["d","e","f"],
    "4": ["g","h","i"],
    "5": ["j","k","l"],
    "6": ["m","n","o"],
    "7": ["p","q","r","s"],
    "8": ["t","u","v"],
    "9": ["w","x","y","z"],
    "0": [""]
}


def doit(input):
    open_set = []
    closed_set = [""]
    for i in range(len(input)):
        number = input[i]
        chars = key_map[str(number)]
        for c in chars:
            for string in closed_set:
                open_set.append("%s%s" % (string, c))
        closed_set = open_set
        open_set = []
    return closed_set

for lajos in doit("8711111110000000847"):
    print lajos
