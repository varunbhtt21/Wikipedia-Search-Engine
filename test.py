


set_list = [set([1, 2, 3]), set([5, 9, 3]), set([17, 3, 14])]
print(reduce(lambda s1, s2: s1 & s2, set_list))