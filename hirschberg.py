import argparse

# Handle arguments
my_parser = argparse.ArgumentParser()
my_parser.add_argument('-t', action='store_const', const=True, help="Print (i,j)")
my_parser.add_argument('-f', action='store_const', const=True, help="Read txt")
my_parser.add_argument('g')
my_parser.add_argument('m')
my_parser.add_argument('d')
my_parser.add_argument('a')
my_parser.add_argument('b')
args = my_parser.parse_args()

g = int(args.g)
m = int(args.m)
d = int(args.d)
if args.f:
    with open(args.a, 'r') as f:
        a = f.read()
    with open(args.b, 'r') as f:
        b = f.read()
else:
    a = args.a
    b = args.b


def needleman_wunsch(A, B):
    F = [[0 for _ in range(len(B) + 1)] for _ in range(len(A) + 1)]
    for i in range(len(F)):
        for j in range(len(F[i])):
            if i == j == 0:
                F[i][j] = 0
            elif j == 0:
                F[i][0] = g * i
            elif i == 0:
                F[0][j] = g * j
            else:
                x1 = F[i - 1][j] + g
                x2 = F[i][j - 1] + g
                x3 = F[i - 1][j - 1] + m if A[i - 1] == B[j - 1] else F[i - 1][j - 1] + d
                F[i][j] = max(x1, x2, x3)
    return enumerate_alignments(A, B, F, "", "", [], [])


def Compare(A, B):
    if A == B:
        return m
    else:
        return d


def enumerate_alignments(A, B, F, W, Z, WW, ZZ):
    i = len(A)
    j = len(B)
    if i == 0 and j == 0:
        WW.append(W)
        ZZ.append(Z)
        return WW, ZZ
    if i > 0 and j > 0:
        x = Compare(A[i - 1], B[j - 1])
        if F[i][j] == F[i - 1][j - 1] + x:
            enumerate_alignments(A[0:i - 1], B[0:j - 1], F, A[i - 1] + W, B[j - 1] + Z, WW, ZZ)
    if i > 0 and F[i][j] == F[i - 1][j] + g:
        enumerate_alignments(A[0:i - 1], B, F, A[i - 1] + W, "-" + Z, WW, ZZ)
    if j > 0 and F[i][j] == F[i][j - 1] + g:
        enumerate_alignments(A, B[0:j - 1], F, "-" + W, B[j - 1] + Z, WW, ZZ)
    return WW, ZZ


def compute_alignment_score(A, B):
    L = [0 for _ in range(len(B) + 1)]
    for j in range(len(L)):
        L[j] = g * j
    K = [0 for _ in range(len(B) + 1)]
    for i in range(1, len(A) + 1):
        L, K = K, L
        L[0] = g * i
        for j in range(1, len(B) + 1):
            x1 = L[j - 1] + g
            x2 = K[j] + g
            x3 = K[j - 1] + Compare(A[i - 1], B[j - 1])
            L[j] = max(x1, x2, x3)
    return L


def update_alignments(WW, ZZ, WW_l, WW_r, ZZ_l, ZZ_r):
    for i in range(len(WW_l)):
        for j in range(len(WW_r)):
            temp = WW_l[i] + WW_r[j]
            temp = "".join(temp)
            WW.append(temp)
    for i in range(len(ZZ_l)):
        for j in range(len(ZZ_r)):
            temp = ZZ_l[i] + ZZ_r[j]
            temp = "".join(temp)
            ZZ.append(temp)
    duplicate = []
    for i in range(len(WW) - 1):
        for j in range(i + 1, len(WW)):
            if WW[i] == WW[j] and ZZ[i] == ZZ[j]:
                duplicate += [(i, j)]
    if duplicate:
        for dup in duplicate:
            WW.pop(dup[1])
            ZZ.pop(dup[1])
            duplicate.pop(0)
    return WW, ZZ


def hirschberg(A, B):
    if len(A) == 0:
        WW = ["-" * len(B)]
        ZZ = [B]
    elif len(B) == 0:
        WW = [A]
        ZZ = ["-" * len(A)]
    elif len(A) == 1 or len(B) == 1:
        WW, ZZ = needleman_wunsch(A, B)
    else:
        i = len(A) // 2
        S_l = compute_alignment_score(A[0:i], B)
        S_r = compute_alignment_score(A[i:][::-1], B[::-1])
        S = [S_l[x] + S_r[len(S_r) - 1 - x] for x in range(len(S_l))]
        J = [index for index, element in enumerate(S) if element == max(S)]
        WW = []
        ZZ = []
        for j in J:
            if args.t:
                print(str(i) + ", " + str(j))
            WW_l, ZZ_l = hirschberg(A[0:i], B[0:j])
            WW_r, ZZ_r = hirschberg(A[i:len(A)], B[j:len(B)])
            WW, ZZ = update_alignments(WW, ZZ, WW_l, WW_r, ZZ_l, ZZ_r)
    return WW, ZZ


first, second = hirschberg(a, b)

for z in range(len(first)):
    print(first[z])
    print(second[z])
    if z != len(first) - 1:
        print()
