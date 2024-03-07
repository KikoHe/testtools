from random import randint
def shuffle(lst, i):
    N = randint(i+1, len(lst)-1)
    return lst[i:N] + lst[:i] + lst[N:]


def cleaner(lst):
    if len(lst) == 1:
        return lst[0]
    lst = lst[1:]+lst[:1]
    del lst[0]
    return cleaner(lst)

def LQ(lst, isMale, fromN=1):
    lst = lst + lst
    lst = shuffle(lst,3)
    ass = lst[0]
    lst = lst[1:]
    lst = shuffle(lst, fromN)
    if isMale:
        del lst[0]
    else:
        del lst[:2]
    for i in range(7):
        lst = lst[1:] + lst[:1]
    hand = cleaner(lst)
    print(ass, hand)

LQ(["3", "6", "10", "J"], 1, 3)  # A A
# LQ(["J", "Q", "K", "A"], 0, 2)  # A A
# LQ(["J", "Q", "K", "A"], 1, 1)  # A A
