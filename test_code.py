from numpy import zeros, sum, arange, average, ceil

matrix = zeros([4, 5])
matrix[-1][-1] = 1.
matrix[-1][1] = 1
matrix[-1][0] = 1.
matrix[-1][-2] = 1.
matrix[-1][-2] = 1.

print(matrix)


def get_mid(mat):
    columns = sum(mat, axis=0)
    print(columns)
    center_of_mass = average(arange(len(columns)), weights=columns)
    return int((columns.size - 1) - int(ceil(center_of_mass)))
    # print(columns)
    # l, r = 0, columns.size - 1
    # ls = rs = 0
    #
    # while l < r:
    #     if ls == rs:
    #         ls += columns[l]
    #         rs += columns[r]
    #         l += 1
    #         r -= 1
    #     elif ls < rs:
    #         ls += columns[l]
    #         l += 1
    #     else:
    #         rs += columns[r]
    #         r -= 1
    #     return l, r


print(get_mid(matrix))
