# coding:utf:8
import random
# En iyi varyasyonu seç
def select_best_mutaion(s, distmat):
    s_res = [slide_mutation(s[:]), inversion_mutation(s[:]), irgibnnm_mutation(s[:], distmat)]
    res = [get_distance(s_res[0], distmat), get_distance(s_res[1], distmat), get_distance(s_res[2], distmat)]
    min_index = res.index(min(res))
    return s_res[min_index]
# Varyasyon değişimi
def slide_mutation(s):
    a, b = get_two_randint(len(s))
    t = s[a]
    for i in range(a + 1, b + 1):
        s[i - 1] = s[i]
    s[b] = t
    return s
# Mesafe hesapla
def get_distance(sequence, distmat):
    cost = 0
    for i in range(len(sequence)):
        cost += distmat[sequence[i - 1]][sequence[i]]
    return cost
# Ters mutasyon
def inversion_mutation(s):
    a, b = get_two_randint(len(s))
    for i in range(a, (a + b) // 2 + 1):
        s[i], s[b + a - i] = s[b + a - i], s[i]
    return s
def get_two_randint(size):
    b = a = random.randint(0, size - 1)
    while a == b:
        b = random.randint(0, size - 1)
    if a > b:
        return b, a
    return a, b
def irgibnnm_mutation(s, distmat):
    a, b = get_two_randint(len(s))
    # İlk ters çevirme
    for i in range(a, (a + b) // 2 + 1):
        s[i], s[b + a - i] = s[b + a - i], s[i]
    b = (b + 1) % len(s)
    min = b - 1
    for i in range(len(s)):
        if i == b:
            continue
        if distmat[b][min] > distmat[b][i]:
            min = i
    s[b], s[min - 4] = s[min - 4], s[b]
    return s

