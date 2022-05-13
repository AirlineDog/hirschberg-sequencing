import argparse

# Handle arguments
my_parser = argparse.ArgumentParser()
my_parser.add_argument('-t', action='store_const', const=True, help="Print (i,j)")
my_parser.add_argument('-f', action='store_const', const=True, help="Read txt")
my_parser.add_argument('-l', action='store_const', const=True, help="lines")
my_parser.add_argument('g')
my_parser.add_argument('m')
my_parser.add_argument('d')
my_parser.add_argument('a')
my_parser.add_argument('b')
args = my_parser.parse_args()

g = int(args.g)
m = int(args.m)
d = int(args.d)
a = args.a
b = args.b

matrix = [[0 for x in range(len(b) + 1)] for y in range(len(a) + 1)]

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if i == j == 0:
            matrix[i][j] = 0
        elif j == 0:
            matrix[i][0] = g * i
        elif i == 0:
            matrix[0][j] = g * j
        else:
            x1 = matrix[i - 1][j] + g
            x2 = matrix[i][j - 1] + g
            x3 = matrix[i - 1][j - 1] + m if a[i - 1] == b[j - 1] else matrix[i - 1][j - 1] + d
            matrix[i][j] = max(x1, x2, x3)


def Compare(a, b):
    if a == b:
        return m
    else:
        return d


def enumerate_alignments(A, B, F, W, Z):
    WW = []
    ZZ = []
    i = len(A)
    j = len(B)
    if i == 0 and j == 0:
        WW.append(W)
        ZZ.append(Z)
        return WW, ZZ
    if i > 0 and j > 0:
        x = Compare(A[i - 1], B[j - 1])
        if F[i][j] == F[i - 1][j - 1] + x:
            r = enumerate_alignments(A[0:i - 1], B[0:j - 1], F, A[i - 1] + W, B[j - 1] + Z)
            if r:
                WW.extend(r[0])
                ZZ.extend(r[1])
    if i > 0 and F[i][j] == F[i - 1][j] + g:
        r = enumerate_alignments(A[0:i - 1], B, F, A[i - 1] + W, "-" + Z)
        if r:
            WW.extend(r[0])
            ZZ.extend(r[1])
    if j > 0 and F[i][j] == F[i][j - 1] + g:
        r = enumerate_alignments(A, B[0:j - 1], F, "-" + W, B[j - 1] + Z)
        if r:
            WW.extend(r[0])
            ZZ.extend(r[1])
    return WW, ZZ


WW, ZZ = enumerate_alignments(a, b, matrix, "", "")

for i in range(len(WW)):
    print(WW[i])
    print(ZZ[i])
    print()
