"""Binary Search pattern: 20 questions (8 Easy, 8 Medium, 4 Hard)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genlib import make_question, write_bank
from bisect import bisect_left, bisect_right

P = "binary-search"
Q = []

def q(**kw):
    Q.append(make_question(pattern=P, **kw))

# ---------------- Easy ----------------

def ref_binsearch(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        m = (l + r) // 2
        if nums[m] == target:
            return m
        if nums[m] < target:
            l = m + 1
        else:
            r = m - 1
    return -1

q(id="binary-search", title="Binary Search", difficulty="Easy",
  description="Given an array of integers nums sorted in ascending order and an integer target, return the index of target if it exists, or -1 if it does not. You must write an algorithm with O(log n) runtime complexity.",
  examples=[("nums = [-1, 0, 3, 5, 9, 12], target = 9", "4", "9 exists at index 4."),
            ("nums = [-1, 0, 3, 5, 9, 12], target = 2", "-1", "2 does not exist.")],
  constraints=["1 <= nums.length <= 10^4", "-10^4 <= nums[i], target <= 10^4", "All integers in nums are unique.", "nums is sorted in ascending order."],
  method_name="search", return_type="int", params=[("nums", "int[]"), ("target", "int")],
  sample_args=[([-1, 0, 3, 5, 9, 12], 9), ([-1, 0, 3, 5, 9, 12], 2)],
  hidden_args=[([5], 5), ([5], 3), ([1, 2, 3, 4, 5], 1), ([1, 2, 3, 4, 5], 5), ([1, 3], 3), ([2, 5], 5)],
  ref=ref_binsearch, tags=["array", "binary-search"],
  time_complexity="O(log n)", space_complexity="O(1)",
  hints=["The array is sorted, so each comparison eliminates half the search space.", "Maintain lo and hi bounds; pick mid = (lo + hi) / 2.", "Move lo or hi past mid based on the comparison; beware integer overflow in other languages."])

def ref_search_insert(nums, target):
    return bisect_left(nums, target)

q(id="search-insert-position", title="Search Insert Position", difficulty="Easy",
  description="Given a sorted array of distinct integers nums and a target value, return the index if the target is found. If not, return the index where it would be inserted in order. You must write an algorithm with O(log n) runtime complexity.",
  examples=[("nums = [1, 3, 5, 6], target = 5", "2", "5 exists at index 2."),
            ("nums = [1, 3, 5, 6], target = 2", "1", "2 would be inserted at index 1."),
            ("nums = [1, 3, 5, 6], target = 7", "4", "7 would be appended at index 4.")],
  constraints=["1 <= nums.length <= 10^4", "-10^4 <= nums[i] <= 10^4", "nums contains distinct values sorted in ascending order.", "-10^4 <= target <= 10^4"],
  method_name="searchInsert", return_type="int", params=[("nums", "int[]"), ("target", "int")],
  sample_args=[([1, 3, 5, 6], 5), ([1, 3, 5, 6], 2)],
  hidden_args=[([1, 3, 5, 6], 7), ([1, 3, 5, 6], 0), ([1], 0), ([1], 2), ([1, 3], 2), ([2, 3, 5, 7], 4)],
  ref=ref_search_insert, tags=["array", "binary-search"],
  time_complexity="O(log n)", space_complexity="O(1)",
  hints=["This is the classic lower-bound problem.", "Binary search for the first index with nums[i] >= target.", "When the loop ends, lo is exactly the insertion position."])

def ref_sqrt(x):
    if x < 2:
        return x
    l, r = 1, x // 2
    while l <= r:
        m = (l + r) // 2
        sq = m * m
        if sq == x:
            return m
        if sq < x:
            l = m + 1
        else:
            r = m - 1
    return r

q(id="sqrtx", title="Sqrt(x)", difficulty="Easy",
  description="Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well. You must not use any built-in exponent function or operator.",
  examples=[("x = 4", "2", "sqrt(4) = 2."),
            ("x = 8", "2", "sqrt(8) = 2.828..., rounded down to 2.")],
  constraints=["0 <= x <= 2^31 - 1"],
  method_name="mySqrt", return_type="int", params=[("x", "int")],
  sample_args=[(4,), (8,)],
  hidden_args=[(0,), (1,), (2,), (3,), (9,), (15,), (16,), (2147395599,)],
  ref=ref_sqrt, tags=["math", "binary-search"],
  time_complexity="O(log n)", space_complexity="O(1)",
  hints=["The answer lies in the range [0, x].", "Binary search that range for the largest m with m * m <= x.", "Compare m with x / m instead of computing m * m to avoid overflow."])

def ref_perfect(num):
    if num < 2:
        return True
    l, r = 2, num // 2
    while l <= r:
        m = (l + r) // 2
        sq = m * m
        if sq == num:
            return True
        if sq < num:
            l = m + 1
        else:
            r = m - 1
    return False

q(id="valid-perfect-square", title="Valid Perfect Square", difficulty="Easy",
  description="Given a positive integer num, return true if num is a perfect square or false otherwise. A perfect square is an integer that is the square of an integer. You must not use any built-in library function, such as sqrt.",
  examples=[("num = 16", "true", "16 = 4 * 4."),
            ("num = 14", "false", "No integer squares to 14.")],
  constraints=["1 <= num <= 2^31 - 1"],
  method_name="isPerfectSquare", return_type="boolean", params=[("num", "int")],
  sample_args=[(16,), (14,)],
  hidden_args=[(1,), (2,), (4,), (9,), (25,), (26,), (2147483647,), (808201,)],
  ref=ref_perfect, tags=["math", "binary-search"],
  time_complexity="O(log n)", space_complexity="O(1)",
  hints=["Binary search the range [1, num] for a value whose square equals num.", "If m * m < num, search higher; if greater, search lower.", "Use long arithmetic (or compare via division) to avoid overflow."])

def ref_coins(n):
    l, r = 0, n
    while l <= r:
        m = (l + r) // 2
        s = m * (m + 1) // 2
        if s == n:
            return m
        if s < n:
            l = m + 1
        else:
            r = m - 1
    return r

q(id="arranging-coins", title="Arranging Coins", difficulty="Easy",
  description="You have n coins and want to build a staircase: the kth row must contain exactly k coins. Given n, return the number of complete rows that can be formed.",
  examples=[("n = 5", "3", "Rows: 1 + 2 coins; the third row needs 3 coins but only 2 remain."),
            ("n = 8", "3", "Rows: 1 + 2 + 3 = 6 coins; 2 remain, insufficient for row 4.")],
  constraints=["1 <= n <= 2^31 - 1"],
  method_name="arrangeCoins", return_type="int", params=[("n", "int")],
  sample_args=[(5,), (8,)],
  hidden_args=[(1,), (2,), (3,), (6,), (10,), (1804289383,)],
  ref=ref_coins, tags=["math", "binary-search"],
  time_complexity="O(log n)", space_complexity="O(1)",
  hints=["k complete rows need k * (k + 1) / 2 coins.", "Binary search the largest k with k * (k + 1) / 2 <= n.", "Use long arithmetic to avoid overflow."])

def ref_letter(letters, target):
    l, r = 0, len(letters) - 1
    while l <= r:
        m = (l + r) // 2
        if letters[m] <= target:
            l = m + 1
        else:
            r = m - 1
    return letters[l % len(letters)]

q(id="find-smallest-letter-greater-than-target", title="Find Smallest Letter Greater Than Target", difficulty="Easy",
  description="You are given an array of characters letters that is sorted in non-decreasing order, and a character target. There are at least two different characters in letters. Return the smallest character in letters that is lexicographically greater than target. If no such character exists, return the first character in letters. (Here letters is passed as a string for simpler I/O.)",
  examples=[('letters = "cfj", target = "a"', '"c"', '"c" is the smallest letter greater than "a".'),
            ('letters = "cfj", target = "c"', '"f"', 'Target itself does not count; need strictly greater.'),
            ('letters = "cfj", target = "d"', '"f"', '"f" is the smallest letter greater than "d".')],
  constraints=["2 <= letters.length <= 10^4", "letters[i] is a lowercase English letter.", "letters is sorted in non-decreasing order.", "target is a lowercase English letter."],
  method_name="nextGreatestLetter", return_type="char", params=[("letters", "String"), ("target", "char")],
  sample_args=[("cfj", "a"), ("cfj", "c")],
  hidden_args=[("cfj", "d"), ("cfj", "j"), ("aaa", "a"), ("abc", "z"), ("xyz", "x"), ("mnop", "m")],
  ref=ref_letter, tags=["array", "binary-search"],
  time_complexity="O(log n)", space_complexity="O(1)",
  hints=["Binary search for the first letter strictly greater than target.", "If every letter is <= target, wrap around to letters[0].", "The answer index is lo % letters.length after the search."])

def ref_peak(arr):
    l, r = 0, len(arr) - 1
    while l < r:
        m = (l + r) // 2
        if arr[m] < arr[m + 1]:
            l = m + 1
        else:
            r = m
    return l

q(id="peak-index-in-a-mountain-array", title="Peak Index in a Mountain Array", difficulty="Easy",
  description="An array arr is a mountain array if: arr.length >= 3; there exists an index i with 0 < i < arr.length - 1 such that arr[0] < arr[1] < ... < arr[i-1] < arr[i] and arr[i] > arr[i+1] > ... > arr[arr.length - 1]. Given such an array, return the index i of the peak. You must write an algorithm with O(log n) runtime complexity.",
  examples=[("arr = [0, 1, 0]", "1", "Peak at index 1."),
            ("arr = [0, 2, 1, 0]", "2", "Peak at index 2."),
            ("arr = [0, 10, 5, 2]", "1", "Peak at index 1.")],
  constraints=["3 <= arr.length <= 10^5", "0 <= arr[i] <= 10^6", "arr is guaranteed to be a mountain array."],
  method_name="peakIndexInMountainArray", return_type="int", params=[("arr", "int[]")],
  sample_args=[([0, 1, 0],), ([0, 2, 1, 0],)],
  hidden_args=[([0, 10, 5, 2],), ([3, 5, 3, 2, 0],), ([1, 2, 3, 4, 5, 4, 3],), ([0, 1, 2, 3, 2],), ([1, 3, 5, 4, 2],), ([24, 69, 100, 99, 79, 78, 67, 36, 26, 19],)],
  ref=ref_peak, tags=["array", "binary-search"],
  time_complexity="O(log n)", space_complexity="O(1)",
  hints=["Compare arr[mid] with arr[mid + 1].", "If arr[mid] < arr[mid + 1], the peak is to the right; otherwise it is at mid or to the left.", "This is binary search on the slope of the mountain."])

def ref_negatives(grid):
    cnt = 0
    for row in grid:
        l, r = 0, len(row) - 1
        first = len(row)
        while l <= r:
            m = (l + r) // 2
            if row[m] < 0:
                first = m
                r = m - 1
            else:
                l = m + 1
        cnt += len(row) - first
    return cnt

q(id="count-negative-numbers-in-a-sorted-matrix", title="Count Negative Numbers in a Sorted Matrix", difficulty="Easy",
  description="Given an m x n matrix grid sorted in non-increasing order both row-wise and column-wise, return the number of negative numbers in grid.",
  examples=[("grid = [[4, 3, 2, -1], [3, 2, 1, -1], [1, 1, -1, -2], [-1, -1, -2, -3]]", "8", "Eight negatives in total."),
            ("grid = [[3, 2], [1, 0]]", "0", "No negatives.")],
  constraints=["1 <= m, n <= 100", "-100 <= grid[i][j] <= 100", "Rows and columns are sorted in non-increasing order."],
  method_name="countNegatives", return_type="int", params=[("grid", "int[][]")],
  sample_args=[([[4, 3, 2, -1], [3, 2, 1, -1], [1, 1, -1, -2], [-1, -1, -2, -3]],), ([[3, 2], [1, 0]],)],
  hidden_args=[([[5, 1, 0], [-5, -5, -5]],), ([[1]],), ([[-1]],), ([[3, 2, 1], [2, 1, 0], [1, 0, -1]],), ([[5, 4, 3], [4, 3, 2], [3, 2, 1]],), ([[-5]],)],
  ref=ref_negatives, tags=["array", "binary-search", "matrix"],
  time_complexity="O(m log n)", space_complexity="O(1)",
  hints=["Each row is sorted, so binary search finds the first negative in O(log n).", "All elements from that index to the row end are negative.", "An O(m + n) staircase walk from the top-right corner also works."])

# ---------------- Medium ----------------

def ref_rotsearch(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        m = (l + r) // 2
        if nums[m] == target:
            return m
        if nums[l] <= nums[m]:
            if nums[l] <= target < nums[m]:
                r = m - 1
            else:
                l = m + 1
        else:
            if nums[m] < target <= nums[r]:
                l = m + 1
            else:
                r = m - 1
    return -1

q(id="search-in-rotated-sorted-array", title="Search in Rotated Sorted Array", difficulty="Medium",
  description="There is an integer array nums sorted in ascending order (with distinct values), rotated at some unknown pivot. Given the rotated array nums and an integer target, return the index of target if it is in nums, or -1 if it is not. You must write an algorithm with O(log n) runtime complexity.",
  examples=[("nums = [4, 5, 6, 7, 0, 1, 2], target = 0", "4", "0 is at index 4."),
            ("nums = [4, 5, 6, 7, 0, 1, 2], target = 3", "-1", "3 is not present."),
            ("nums = [1], target = 0", "-1", "Single element, not present.")],
  constraints=["1 <= nums.length <= 5000", "-10^4 <= nums[i] <= 10^4", "All values of nums are unique.", "nums is a rotated sorted array.", "-10^4 <= target <= 10^4"],
  method_name="search", return_type="int", params=[("nums", "int[]"), ("target", "int")],
  sample_args=[([4, 5, 6, 7, 0, 1, 2], 0), ([4, 5, 6, 7, 0, 1, 2], 3)],
  hidden_args=[([1], 0), ([1], 1), ([3, 1], 1), ([5, 1, 3], 3), ([4, 5, 6, 7, 0, 1, 2], 6), ([2, 3, 4, 5, 1], 1)],
  ref=ref_rotsearch, tags=["array", "binary-search"],
  time_complexity="O(log n)", space_complexity="O(1)",
  hints=["At least one half of the current range is always sorted.", "Check whether the left half [lo, mid] is sorted; if so, decide whether target lies inside it.", "Otherwise the right half is sorted; apply the symmetric check."])

def ref_findmin(nums):
    l, r = 0, len(nums) - 1
    while l < r:
        m = (l + r) // 2
        if nums[m] > nums[r]:
            l = m + 1
        else:
            r = m
    return nums[l]

q(id="find-minimum-in-rotated-sorted-array", title="Find Minimum in Rotated Sorted Array", difficulty="Medium",
  description="Suppose an array of length n sorted in ascending order is rotated between 1 and n times. Given the rotated array nums of unique elements, return its minimum element. You must write an algorithm with O(log n) runtime complexity.",
  examples=[("nums = [3, 4, 5, 1, 2]", "1", "The minimum is 1."),
            ("nums = [4, 5, 6, 7, 0, 1, 2]", "0", "The minimum is 0."),
            ("nums = [11, 13, 15, 17]", "11", "Not rotated; the minimum is the first element.")],
  constraints=["1 <= nums.length <= 5000", "-5000 <= nums[i] <= 5000", "All integers of nums are unique.", "nums is sorted and rotated between 1 and n times."],
  method_name="findMin", return_type="int", params=[("nums", "int[]")],
  sample_args=[([3, 4, 5, 1, 2],), ([4, 5, 6, 7, 0, 1, 2],)],
  hidden_args=[([11, 13, 15, 17],), ([2, 1],), ([1],), ([5, 1, 2, 3, 4],), ([2, 3, 4, 5, 1],), ([7, 0, 1, 2, 4, 5, 6],)],
  ref=ref_findmin, tags=["array", "binary-search"],
  time_complexity="O(log n)", space_complexity="O(1)",
  hints=["Compare nums[mid] with nums[hi].", "If nums[mid] > nums[hi], the minimum is in the right half; otherwise it is at mid or in the left half.", "The loop converges with lo == hi at the minimum."])

def ref_range(nums, target):
    l = bisect_left(nums, target)
    r = bisect_right(nums, target) - 1
    if l <= r:
        return [l, r]
    return [-1, -1]

q(id="find-first-and-last-position-of-element-in-sorted-array", title="Find First and Last Position of Element in Sorted Array", difficulty="Medium",
  description="Given an array of integers nums sorted in non-decreasing order, find the starting and ending position of a given target value. If target is not found, return [-1, -1]. You must write an algorithm with O(log n) runtime complexity.",
  examples=[("nums = [5, 7, 7, 8, 8, 10], target = 8", "[3, 4]", "8 spans indices 3 to 4."),
            ("nums = [5, 7, 7, 8, 8, 10], target = 6", "[-1, -1]", "6 is not present."),
            ("nums = [], target = 0", "[-1, -1]", "Empty array.")],
  constraints=["0 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9", "nums is sorted in non-decreasing order.", "-10^9 <= target <= 10^9"],
  method_name="searchRange", return_type="int[]", params=[("nums", "int[]"), ("target", "int")],
  sample_args=[([5, 7, 7, 8, 8, 10], 8), ([5, 7, 7, 8, 8, 10], 6)],
  hidden_args=[([], 0), ([1], 1), ([2, 2], 2), ([1, 2, 3, 4, 5], 3), ([1, 1, 1, 1], 1), ([0, 0, 1, 1, 1, 2], 1)],
  ref=ref_range, tags=["array", "binary-search"],
  time_complexity="O(log n)", space_complexity="O(1)",
  hints=["Run two binary searches: one for the leftmost target, one for the rightmost.", "The leftmost search finds the first index with nums[i] >= target.", "Verify the found index actually holds target; otherwise return [-1, -1]."])

def ref_search2d(matrix, target):
    if not matrix or not matrix[0]:
        return False
    R, C = len(matrix), len(matrix[0])
    l, r = 0, R * C - 1
    while l <= r:
        m = (l + r) // 2
        v = matrix[m // C][m % C]
        if v == target:
            return True
        if v < target:
            l = m + 1
        else:
            r = m - 1
    return False

q(id="search-a-2d-matrix", title="Search a 2D Matrix", difficulty="Medium",
  description="You are given an m x n integer matrix with: each row sorted in ascending order, and the first integer of each row greater than the last integer of the previous row. Given an integer target, return true if target is in the matrix or false otherwise. You must write a solution in O(log(m * n)) time complexity.",
  examples=[("matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], target = 3", "true", "3 is present."),
            ("matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], target = 13", "false", "13 is not present.")],
  constraints=["1 <= m, n <= 100", "-10^4 <= matrix[i][j], target <= 10^4"],
  method_name="searchMatrix", return_type="boolean", params=[("matrix", "int[][]"), ("target", "int")],
  sample_args=[([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3), ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13)],
  hidden_args=[([[1]], 1), ([[1]], 2), ([[1, 3, 5]], 4), ([[1], [3], [5]], 3), ([[1, 3, 5, 7], [10, 11, 16, 20]], 20), ([[1, 3, 5, 7], [10, 11, 16, 20]], 21)],
  ref=ref_search2d, tags=["array", "binary-search", "matrix"],
  time_complexity="O(log(m * n))", space_complexity="O(1)",
  hints=["The matrix is sorted as if flattened row by row.", "Binary search over the virtual 1D index range [0, m*n).", "Map index i to matrix[i / n][i % n]."])

def ref_koko(piles, h):
    def hours(s):
        return sum((p + s - 1) // s for p in piles)
    l, r = 1, max(piles)
    while l < r:
        m = (l + r) // 2
        if hours(m) <= h:
            r = m
        else:
            l = m + 1
    return l

q(id="koko-eating-bananas", title="Koko Eating Bananas", difficulty="Medium",
  description="Koko loves bananas. There are n piles of bananas where piles[i] is the number of bananas in pile i. Guards return in h hours. Each hour, Koko chooses a pile and eats k bananas from it (k is her speed); if the pile has fewer than k bananas, she eats them all and stops for the hour. Return the minimum integer speed k such that she can eat all bananas within h hours.",
  examples=[("piles = [3, 6, 7, 11], h = 8", "4", "At speed 4: 1 + 2 + 2 + 3 = 8 hours."),
            ("piles = [30, 11, 23, 4, 20], h = 5", "30", "Must finish each pile in one hour."),
            ("piles = [30, 11, 23, 4, 20], h = 6", "23", "Hours: 2 + 1 + 1 + 1 + 1 = 6.")],
  constraints=["1 <= piles.length <= 10^4", "piles.length <= h <= 10^9", "1 <= piles[i] <= 10^9"],
  method_name="minEatingSpeed", return_type="int", params=[("piles", "int[]"), ("h", "int")],
  sample_args=[([3, 6, 7, 11], 8), ([30, 11, 23, 4, 20], 5)],
  hidden_args=[([30, 11, 23, 4, 20], 6), ([100], 1), ([100], 100), ([2, 2], 3), ([312884470], 312884469), ([1, 1, 1, 999999999], 10)],
  ref=ref_koko, tags=["array", "binary-search"],
  time_complexity="O(n log max)", space_complexity="O(1)",
  hints=["This is binary search on the answer: speed ranges from 1 to max(piles).", "The predicate 'can finish within h hours at speed k' is monotonic in k.", "Hours needed at speed k = sum of ceil(pile / k); find the smallest k with hours <= h."])

def ref_ship(weights, days):
    def need(cap):
        d, cur = 1, 0
        for w in weights:
            if cur + w > cap:
                d += 1
                cur = w
            else:
                cur += w
        return d
    l, r = max(weights), sum(weights)
    while l < r:
        m = (l + r) // 2
        if need(m) <= days:
            r = m
        else:
            l = m + 1
    return l

q(id="capacity-to-ship-packages-within-d-days", title="Capacity to Ship Packages Within D Days", difficulty="Medium",
  description="A conveyor belt has packages numbered 1..n with weights[i]. Packages must be shipped in order: each day, load packages in order onto a ship with capacity C, and ship when adding the next package would exceed C. Return the least capacity C such that all packages ship within days days.",
  examples=[("weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], days = 5", "15", "Splits: [1..5], [6,7], [8], [9], [10]."),
            ("weights = [3, 2, 2, 4, 1, 4], days = 3", "6", "Splits: [3,2], [2,4], [1,4]."),
            ("weights = [1, 2, 3, 1, 1], days = 4", "3", "Splits: [1,2], [3], [1], [1].")],
  constraints=["1 <= weights.length <= 5 * 10^4", "1 <= weights[i] <= 500", "1 <= days <= weights.length"],
  method_name="shipWithinDays", return_type="int", params=[("weights", "int[]"), ("days", "int")],
  sample_args=[([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), ([3, 2, 2, 4, 1, 4], 3)],
  hidden_args=[([1, 2, 3, 1, 1], 4), ([10], 1), ([1, 2, 3, 4, 5], 1), ([1, 2, 3, 4, 5], 5), ([7, 2, 5, 10, 8], 2), ([3, 3, 3, 3, 3], 2)],
  ref=ref_ship, tags=["array", "binary-search"],
  time_complexity="O(n log sum)", space_complexity="O(1)",
  hints=["Binary search the answer between max(weights) and sum(weights).", "The predicate 'ships within days at capacity C' is monotonic in C.", "Simulate greedily: count days needed at capacity C and check against days."])

def ref_dupnum(nums):
    l, r = 1, len(nums) - 1
    while l < r:
        m = (l + r) // 2
        cnt = sum(1 for x in nums if x <= m)
        if cnt > m:
            r = m
        else:
            l = m + 1
    return l

q(id="find-the-duplicate-number", title="Find the Duplicate Number", difficulty="Medium",
  description="Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive, there is exactly one repeated number. Return this repeated number. You must solve it without modifying the array and using only constant extra space.",
  examples=[("nums = [1, 3, 4, 2, 2]", "2", "2 is repeated."),
            ("nums = [3, 1, 3, 4, 2]", "3", "3 is repeated.")],
  constraints=["1 <= n <= 10^5", "nums.length == n + 1", "1 <= nums[i] <= n", "Exactly one number is repeated (possibly multiple times)."],
  method_name="findDuplicate", return_type="int", params=[("nums", "int[]")],
  sample_args=[([1, 3, 4, 2, 2],), ([3, 1, 3, 4, 2],)],
  hidden_args=[([1, 1],), ([1, 1, 2],), ([2, 2, 2, 2, 2],), ([1, 4, 4, 2, 4],), ([3, 3, 3, 3, 3],), ([1, 5, 3, 4, 2, 5],)],
  ref=ref_dupnum, tags=["array", "binary-search", "two-pointers", "cycle-detection"],
  time_complexity="O(n log n)", space_complexity="O(1)",
  hints=["Binary search the value range [1, n], not the array indices.", "Count how many numbers are <= mid: if the count exceeds mid, the duplicate is in [1, mid].", "This pigeonhole argument narrows the range without touching the array."])

def ref_single_sorted(nums):
    l, r = 0, len(nums) - 1
    while l < r:
        m = (l + r) // 2
        if m % 2 == 1:
            m -= 1
        if nums[m] == nums[m + 1]:
            l = m + 2
        else:
            r = m
    return nums[l]

q(id="single-element-in-a-sorted-array", title="Single Element in a Sorted Array", difficulty="Medium",
  description="You are given a sorted array consisting of only integers where every element appears exactly twice, except for one element which appears exactly once. Return the single element that appears only once. You must write a solution with O(log n) time complexity and O(1) space complexity.",
  examples=[("nums = [1, 1, 2, 3, 3, 4, 4, 8, 8]", "2", "2 appears once."),
            ("nums = [3, 3, 7, 7, 10, 11, 11]", "10", "10 appears once.")],
  constraints=["1 <= nums.length <= 10^5", "0 <= nums[i] <= 10^5", "nums.length is odd."],
  method_name="singleNonDuplicate", return_type="int", params=[("nums", "int[]")],
  sample_args=[([1, 1, 2, 3, 3, 4, 4, 8, 8],), ([3, 3, 7, 7, 10, 11, 11],)],
  hidden_args=[([1],), ([0, 1, 1],), ([1, 1, 0],), ([1, 1, 2, 2, 3],), ([5, 5, 6, 6, 7, 8, 8],), ([1, 1, 2, 3, 3],)],
  ref=ref_single_sorted, tags=["array", "binary-search"],
  time_complexity="O(log n)", space_complexity="O(1)",
  hints=["Before the single element, pairs start at even indices; after it, they start at odd indices.", "Force mid to be even, then compare nums[mid] with nums[mid + 1].", "If equal, the single element is to the right; otherwise it is at mid or to the left."])

# ---------------- Hard ----------------

def ref_median(a, b):
    merged = sorted(a + b)
    n = len(merged)
    if n % 2 == 1:
        return float(merged[n // 2])
    return (merged[n // 2 - 1] + merged[n // 2]) / 2.0

q(id="median-of-two-sorted-arrays", title="Median of Two Sorted Arrays", difficulty="Hard",
  description="Given two sorted arrays nums1 and nums2, return the median of the two sorted arrays. The overall run time complexity should be O(log (m + n)).",
  examples=[("nums1 = [1, 3], nums2 = [2]", "2.0", "Merged: [1, 2, 3]; median 2."),
            ("nums1 = [1, 2], nums2 = [3, 4]", "2.5", "Merged: [1, 2, 3, 4]; median (2 + 3) / 2.")],
  constraints=["0 <= nums1.length, nums2.length <= 1000", "1 <= nums1.length + nums2.length <= 2000", "-10^6 <= nums[i] <= 10^6"],
  method_name="findMedianSortedArrays", return_type="double", params=[("nums1", "int[]"), ("nums2", "int[]")],
  sample_args=[([1, 3], [2]), ([1, 2], [3, 4])],
  hidden_args=[([0, 0], [0, 0]), ([], [1]), ([2], []), ([1, 3, 5], [2, 4, 6]), ([1, 2, 3, 4, 5, 6, 7, 8], [9, 10]), ([3], [1, 2])],
  ref=ref_median, tags=["array", "binary-search", "divide-and-conquer"],
  time_complexity="O(log(m + n))", space_complexity="O(1)",
  hints=["Binary search the partition point in the smaller array.", "A correct partition has maxLeft1 <= minRight2 and maxLeft2 <= minRight1.", "The median comes from the border elements of the partition."])

def ref_kdist(nums, k):
    a = sorted(nums)
    def count_le(d):
        c = l = 0
        for r in range(len(a)):
            while a[r] - a[l] > d:
                l += 1
            c += r - l
        return c
    lo, hi = 0, a[-1] - a[0]
    while lo < hi:
        m = (lo + hi) // 2
        if count_le(m) >= k:
            hi = m
        else:
            lo = m + 1
    return lo

q(id="find-k-th-smallest-pair-distance", title="Find K-th Smallest Pair Distance", difficulty="Hard",
  description="The distance of a pair of integers a and b is defined as the absolute difference |a - b|. Given an integer array nums and an integer k, return the kth smallest distance among all pairs (i, j) with i < j.",
  examples=[("nums = [1, 3, 1], k = 1", "0", "Distances: 2, 0, 2; smallest is 0."),
            ("nums = [1, 1, 1], k = 2", "0", "All distances are 0."),
            ("nums = [1, 6, 1], k = 3", "5", "Distances: 5, 0, 5; 3rd smallest is 5.")],
  constraints=["2 <= nums.length <= 10^4", "0 <= nums[i] <= 10^6", "1 <= k <= n * (n - 1) / 2"],
  method_name="smallestDistancePair", return_type="int", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([1, 3, 1], 1), ([1, 1, 1], 2)],
  hidden_args=[([1, 6, 1], 3), ([1, 2, 3, 4], 3), ([62, 100, 4], 2), ([9, 10, 7, 10, 6, 1, 5, 4, 2, 3], 4), ([1, 1000000], 1), ([1, 3, 5, 7, 9], 6)],
  ref=ref_kdist, tags=["array", "binary-search", "two-pointers", "sorting"],
  time_complexity="O(n log n + n log W)", space_complexity="O(n)",
  hints=["Binary search the answer d: the distance value range.", "Counting pairs with distance <= d is done with two pointers on the sorted array in O(n).", "Find the smallest d with at least k pairs within distance d."])

def ref_split(nums, k):
    def pieces(mx):
        c, cur = 1, 0
        for x in nums:
            if cur + x > mx:
                c += 1
                cur = x
            else:
                cur += x
        return c
    l, r = max(nums), sum(nums)
    while l < r:
        m = (l + r) // 2
        if pieces(m) <= k:
            r = m
        else:
            l = m + 1
    return l

q(id="split-array-largest-sum", title="Split Array Largest Sum", difficulty="Hard",
  description="Given an integer array nums and an integer k, split nums into k non-empty continuous subarrays. Minimize the largest sum among these k subarrays, and return that minimized largest sum.",
  examples=[("nums = [7, 2, 5, 10, 8], k = 2", "18", "Split [7, 2, 5] and [10, 8]; largest sum 18."),
            ("nums = [1, 2, 3, 4, 5], k = 2", "9", "Split [1, 2, 3] and [4, 5]; largest sum 9."),
            ("nums = [1, 4, 4], k = 3", "4", "Each element alone; largest sum 4.")],
  constraints=["1 <= nums.length <= 1000", "0 <= nums[i] <= 10^6", "1 <= k <= min(50, nums.length)"],
  method_name="splitArray", return_type="int", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([7, 2, 5, 10, 8], 2), ([1, 2, 3, 4, 5], 2)],
  hidden_args=[([1, 4, 4], 3), ([1], 1), ([10, 5, 13, 4, 8, 4, 5, 11, 14, 9, 16, 10, 20, 8], 8), ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), ([2, 3, 1, 2, 4, 3], 5), ([1000000], 1)],
  ref=ref_split, tags=["array", "binary-search", "dynamic-programming", "greedy", "prefix-sum"],
  time_complexity="O(n log sum)", space_complexity="O(1)",
  hints=["Binary search the answer between max(nums) and sum(nums).", "The predicate 'can split into at most k subarrays with each sum <= X' is monotonic.", "Greedily pack subarrays up to X and count how many pieces are needed."])

def ref_kthmult(m, n, k):
    def count_le(x):
        return sum(min(x // i, n) for i in range(1, m + 1))
    l, r = 1, m * n
    while l < r:
        mid = (l + r) // 2
        if count_le(mid) >= k:
            r = mid
        else:
            l = mid + 1
    return l

q(id="kth-smallest-number-in-multiplication-table", title="Kth Smallest Number in Multiplication Table", difficulty="Hard",
  description="The multiplication table of size m x n has cell (i, j) = i * j (1-indexed). Given m, n, and k, return the kth smallest number in the table.",
  examples=[("m = 3, n = 3, k = 5", "3", "Table sorted: [1, 2, 2, 3, 3, 4, 6, 6, 9]; 5th is 3."),
            ("m = 2, n = 3, k = 6", "6", "Table: [1, 2, 3, 2, 4, 6]; 6th is 6.")],
  constraints=["1 <= m, n <= 3 * 10^4", "1 <= k <= m * n"],
  method_name="findKthNumber", return_type="int", params=[("m", "int"), ("n", "int"), ("k", "int")],
  sample_args=[(3, 3, 5), (2, 3, 6)],
  hidden_args=[(1, 1, 1), (3, 3, 9), (2, 2, 3), (1, 10, 5), (5, 5, 12), (42, 34, 401)],
  ref=ref_kthmult, tags=["binary-search", "math"],
  time_complexity="O(m log(m*n))", space_complexity="O(1)",
  hints=["Binary search the value x in [1, m*n].", "Count numbers <= x: row i contributes min(x / i, n).", "Find the smallest x with count >= k."])

write_bank(P, Q)
