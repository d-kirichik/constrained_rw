import numpy as np
import math
import pandas as pd
import sys

def get_split_index(A):
    i = len(A) - 1
    while i > 0:
        if A[i] < A[i - 1]:
            i -= 1
        else:
            break
    return i - 1


def get_change_index(A, i):
    j = len(A) - 1
    while j >= i:
        if A[j] > A[i]:
            break
        else:
            j -= 1
    return j


def swap(A, i, j):
    A[i], A[j] = (A[j], A[i])


def reverse(A, start):
    left = start
    right = len(A) - 1
    while left < right:
        swap(A, left, right)
        left += 1
        right -= 1


def next_permutation(A):
    split_index = get_split_index(A)
    # the Array is sorted in descreased order
    if split_index == -1:
        reverse(A, 0)
    else:
        change_index = get_change_index(A, split_index)
        swap(A, split_index, change_index)
        reverse(A, split_index + 1)


def factorial(n):
    ans = 1
    for i in range(2, n + 1):
        ans *= i
    return ans


def permutations(d):
    a = []
    for j in range(d):
        a.append(j + 1)
    perm = dict()
    perm[str(a)] = 0
    for j in range(factorial(d) - 1):
        next_permutation(a)
        perm[str(a)] = j + 1
    return perm


def s_max(d):
    return math.log(factorial(d))


def s_max_list(d):
    return [1 / factorial(d)] * factorial(d)


def pi(arr, d):
    pr = [0] * factorial(d)
    permutation_dict = permutations(d)
    for i in range(d - 1, len(arr)):
        curr = []
        curr_perm = []
        for j in range(i - d + 1, i + 1):
            curr.append([arr[j], len(curr) + 1])
        curr.sort()
        for k in curr:
            curr_perm.append(k[1])
        pr[permutation_dict[str(curr_perm)]] += 1
    for i in range(len(pr)):
        pr[i] /= len(arr) - d + 1
    return pr


def si(pr):
    entropy = 0
    for i in range(len(pr)):
        if pr[i] != 0:
            entropy -= pr[i] * math.log(pr[i])
    return entropy

def q_0_calculation(d):
    pr = [0] * factorial(d)
    pr[0] = 1
    b = s_max_list(d)
    b = [pr + b for pr, b in zip(pr, b)]
    b = [i * 0.5 for i in b]
    return 1 / (si(b) - si(pr) / 2 - s_max(d) / 2)

def q_j(arr, d):
    pr = pi(arr, d)
    b = s_max_list(d)
    b = [pr + b for pr, b in zip(pr, b)]
    b = [i * 0.5 for i in b]
    return q_0_calculation(d) * (si(b) - si(pr) / 2 - s_max(d) / 2)

def entropy_measure(arr, d):
    return si(pi(arr, d))/s_max(d)

def mpr_complexity(arr, entropy_measure, d):
    return q_j(arr, d) * entropy_measure

filename = sys.argv[1]
xs = np.loadtxt(filename)
entropy_measure = entropy_measure(xs, 4)

print("Entropy = ", entropy_measure)
print("Compleixty = ", mpr_complexity(xs, entropy_measure, 4))


