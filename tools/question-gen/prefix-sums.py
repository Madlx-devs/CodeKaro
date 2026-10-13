"""Prefix Sums pattern: 20 questions (8 Easy, 8 Medium, 4 Hard)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genlib import make_question, write_bank
from collections import Counter, defaultdict

P = "prefix-sums"
Q = []

def q(**kw):
    Q.append(make_question(pattern=P, **kw))

# ---------------- Easy ----------------

def ref_runningsum(nums):
    out, s = [], 0
    for x in nums:
        s += x
        out.append(s)
    return out

q(id="running-sum-of-1d-array", title="Running Sum of 1d Array", difficulty="Easy",
  description="Given an array nums, return the running sum: runningSum[i] = sum(nums[0] ... nums[i]).",
  examples=[("nums = [1, 2, 3, 4]", "[1, 3, 6, 10]", "Cumulative sums."),
            ("nums = [1, 1, 1, 1, 1]", "[1, 2, 3, 4, 5]", "Cumulative sums."),
            ("nums = [3, 1, 2, 10, 1]", "[3, 4, 6, 16, 17]", "Cumulative sums.")],
  constraints=["1 <= nums.length <= 1000", "-10^6 <= nums[i] <= 10^6"],
  method_name="runningSum", return_type="int[]", params=[("nums", "int[]")],
  sample_args=[([1, 2, 3, 4],), ([1, 1, 1, 1, 1],)],
  hidden_args=[([3, 1, 2, 10, 1],), ([5],), ([-1, 2, -3, 4],), ([0, 0, 0],), ([10, -10, 10],), ([2, 4, 6, 8],)],
  ref=ref_runningsum, tags=["array", "prefix-sum"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["The running sum at i is the previous running sum plus nums[i].", "A single left-to-right pass maintains the cumulative total.", "You can even write the result back into the input array for O(1) extra space."])

def ref_pivot(nums):
    total = sum(nums)
    left = 0
    for i, x in enumerate(nums):
        if left == total - left - x:
            return i
        left += x
    return -1

q(id="find-pivot-index", title="Find Pivot Index", difficulty="Easy",
  description="Given an array of integers nums, calculate the pivot index of this array. The pivot index is the index where the sum of all the numbers strictly to the left of the index equals the sum of all the numbers strictly to the right. Return the leftmost pivot index, or -1 if none exists.",
  examples=[("nums = [1, 7, 3, 6, 5, 6]", "3", "Left sum = 1 + 7 + 3 = 11; right sum = 5 + 6 = 11."),
            ("nums = [1, 2, 3]", "-1", "No index balances."),
            ("nums = [2, 1, -1]", "0", "Left sum = 0; right sum = 1 + (-1) = 0.")],
  constraints=["1 <= nums.length <= 10^4", "-1000 <= nums[i] <= 1000"],
  method_name="pivotIndex", return_type="int", params=[("nums", "int[]")],
  sample_args=[([1, 7, 3, 6, 5, 6],), ([1, 2, 3],)],
  hidden_args=[([2, 1, -1],), ([-1, -1, 0, 1, 1, 0],), ([1],), ([1, 1],), ([0, 0, 0],), ([-1, -1, -1, -1, -1, 0],)],
  ref=ref_pivot, tags=["array", "prefix-sum"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Compute the total sum once up front.", "Walk left to right maintaining the left sum.", "At index i, the right sum is total - left - nums[i]; return the first i where they match."])

def ref_altitude(gain):
    h = best = 0
    for g in gain:
        h += g
        best = max(best, h)
    return best

q(id="find-the-highest-altitude", title="Find the Highest Altitude", difficulty="Easy",
  description="A biker starts at altitude 0 and follows a road trip where gain[i] is the net altitude gain between points i and i + 1. Return the highest altitude reached during the trip.",
  examples=[("gain = [-5, 1, 5, 0, -7]", "1", "Altitudes: 0, -5, -4, 1, 1, -6; highest is 1."),
            ("gain = [-4, -3, -2, -1, 4, 3, 2]", "0", "Altitudes never exceed the starting 0.")],
  constraints=["1 <= gain.length <= 100", "-100 <= gain[i] <= 100"],
  method_name="largestAltitude", return_type="int", params=[("gain", "int[]")],
  sample_args=[([-5, 1, 5, 0, -7],), ([-4, -3, -2, -1, 4, 3, 2],)],
  hidden_args=[([1],), ([-1],), ([0, 0, 0],), ([5, -3, 2],), ([-2, 3, -1, 4],), ([1, 2, 3, -10, 5],)],
  ref=ref_altitude, tags=["array", "prefix-sum"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["The altitude after step i is the prefix sum of gain[0..i].", "Track the running altitude and the maximum seen.", "Start the maximum at 0 since the trip begins at altitude 0."])

def ref_lrdiff(nums):
    total = sum(nums)
    left = 0
    out = []
    for x in nums:
        right = total - left - x
        out.append(abs(left - right))
        left += x
    return out

q(id="left-and-right-sum-differences", title="Left and Right Sum Differences", difficulty="Easy",
  description="Given an integer array nums, return an array answer where answer[i] = |leftSum[i] - rightSum[i]|. leftSum[i] is the sum of elements to the left of index i, and rightSum[i] is the sum of elements to the right of index i.",
  examples=[("nums = [10, 4, 8, 3]", "[15, 1, 11, 22]", "|0-15|=15, |10-11|=1, |14-3|=11, |22-0|=22."),
            ("nums = [1]", "[0]", "Both sums are 0.")],
  constraints=["1 <= nums.length <= 1000", "1 <= nums[i] <= 10^5"],
  method_name="leftRightDifference", return_type="int[]", params=[("nums", "int[]")],
  sample_args=[([10, 4, 8, 3],), ([1],)],
  hidden_args=[([1, 2, 3],), ([5, 5, 5, 5],), ([0, 0],), ([7, 3],), ([1, 2, 3, 4, 5],), ([9],)],
  ref=ref_lrdiff, tags=["array", "prefix-sum"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Compute the total sum once.", "Maintain the left sum as you scan; right sum = total - left - nums[i].", "Take the absolute difference at each index."])

def ref_minstart(nums):
    s = mn = 0
    for x in nums:
        s += x
        mn = min(mn, s)
    return 1 - mn

q(id="minimum-value-to-get-positive-step-by-step-sum", title="Minimum Value to Get Positive Step by Step Sum", difficulty="Easy",
  description="Given an array of integers nums, pick a positive startValue such that the step-by-step sum startValue + nums[0] + ... + nums[i] is greater than 0 for every i. Return the minimum such positive startValue.",
  examples=[("nums = [-3, 2, -3, 4, 2]", "5", "With start 5, running sums are 2, 4, 1, 5, 7: all positive."),
            ("nums = [1, 2]", "1", "With start 1, running sums are 2, 4."),
            ("nums = [1, -2, -3]", "5", "With start 5, running sums are 6, 4, 1.")],
  constraints=["1 <= nums.length <= 100", "-100 <= nums[i] <= 100"],
  method_name="minStartValue", return_type="int", params=[("nums", "int[]")],
  sample_args=[([-3, 2, -3, 4, 2],), ([1, 2],)],
  hidden_args=[([1, -2, -3],), ([2, 3, 5, -5, -1],), ([-1, -2, -3],), ([1, 2, 3],), ([0, 0, 0],), ([-5, 4],)],
  ref=ref_minstart, tags=["array", "prefix-sum"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Track the prefix sums of nums (starting from 0).", "The worst dip determines the answer: you must offset the minimum prefix.", "Answer = 1 - minPrefix, where minPrefix is the smallest prefix sum (or 0 if none negative)."])

def ref_oddsum(arr):
    n = len(arr)
    total = 0
    for i, x in enumerate(arr):
        left_choices = i + 1
        right_choices = n - i
        total_odd = (left_choices * right_choices + 1) // 2
        total += x * total_odd
    return total

q(id="sum-of-all-odd-length-subarrays", title="Sum of All Odd Length Subarrays", difficulty="Easy",
  description="Given an array arr of positive integers, consider all possible odd-length subarrays. Return the sum of all their sums. A subarray is a contiguous subsequence of the array.",
  examples=[("arr = [1, 4, 2, 5, 3]", "58", "Odd-length subarrays: length 1 sum 15, length 3 sum 31, length 5 sum 12; total 58."),
            ("arr = [1, 2]", "3", "Only [1] and [2]: total 3."),
            ("arr = [10, 11, 12]", "66", "Length 1: 33; length 3: 33; total 66.")],
  constraints=["1 <= arr.length <= 100", "1 <= arr[i] <= 1000"],
  method_name="sumOddLengthSubarrays", return_type="int", params=[("arr", "int[]")],
  sample_args=[([1, 4, 2, 5, 3],), ([1, 2],)],
  hidden_args=[([10, 11, 12],), ([1],), ([7, 7, 7],), ([1, 2, 3, 4],), ([5, 4],), ([-1, -2],)],
  ref=ref_oddsum, tags=["array", "prefix-sum", "math"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Brute force enumerates O(n^2) subarrays; a smarter count is O(n).", "Element arr[i] appears in (i+1) * (n-i) subarrays; half of those (rounded up) have odd length.", "Contribution of arr[i] = arr[i] * ceil((i+1)*(n-i) / 2)."])

def ref_maxpop(logs):
    diff = [0] * 102
    for b, d in logs:
        diff[b - 1950] += 1
        diff[d - 1950] -= 1
    best = cur = 0
    year = 1950
    for i, v in enumerate(diff):
        cur += v
        if cur > best:
            best, year = cur, 1950 + i
    return year

q(id="maximum-population-year", title="Maximum Population Year", difficulty="Easy",
  description="You are given a 2D integer array logs where logs[i] = [birthi, deathi] indicates the ith person was alive during years [birthi, deathi): born in birthi (inclusive) and died in deathi (exclusive). All years satisfy 1950 <= birthi < deathi <= 2050. Return the earliest year with the maximum population.",
  examples=[("logs = [[1993, 1999], [2000, 2010]]", "1993", "Both years have population 1; earliest is 1993."),
            ("logs = [[1950, 1961], [1960, 1971], [1970, 1981]]", "1960", "Population peaks at 2 during 1960-1961.")],
  constraints=["1 <= logs.length <= 100", "1950 <= birthi < deathi <= 2050"],
  method_name="maximumPopulation", return_type="int", params=[("logs", "int[][]")],
  sample_args=[([[1993, 1999], [2000, 2010]],), ([[1950, 1961], [1960, 1971], [1970, 1981]],)],
  hidden_args=[([[2000, 2001]],), ([[1990, 1995], [1995, 2000]],), ([[1980, 1990], [1980, 1990], [1980, 1990]],), ([[2000, 2010], [2005, 2015], [2010, 2020]],), ([[1993, 1999], [1993, 1999]],), ([[1950, 1951], [1950, 1952]],)],
  ref=ref_maxpop, tags=["array", "prefix-sum", "difference-array", "counting"],
  time_complexity="O(n + Y)", space_complexity="O(Y)",
  hints=["Model each life as +1 at birth year and -1 at death year (death is exclusive).", "A difference array over the years 1950..2050 accumulates the population.", "Scan the years in order, tracking the running population and the earliest year achieving the max."])

def ref_splitways(nums):
    total = sum(nums)
    left = 0
    ways = 0
    for i in range(len(nums) - 1):
        left += nums[i]
        if left >= total - left:
            ways += 1
    return ways

q(id="number-of-ways-to-split-array", title="Number of Ways to Split Array", difficulty="Easy",
  description="You are given an integer array nums. A split divides the array at some index i (0 <= i < n - 1) into a left part nums[0..i] and a right part nums[i+1..n-1]. A split is valid if the left sum is greater than or equal to the right sum. Return the number of valid splits.",
  examples=[("nums = [10, 4, -8, 7]", "2", "Splits after index 0 (10 >= -3? 10 >= -3 yes) and after index 1 (14 >= -1 yes)."),
            ("nums = [2, 3, 1, 0]", "2", "Splits after index 1 (5 >= 1) and after index 2 (6 >= 0).")],
  constraints=["2 <= nums.length <= 10^5", "-10^5 <= nums[i] <= 10^5"],
  method_name="waysToSplitArray", return_type="int", params=[("nums", "int[]")],
  sample_args=[([10, 4, -8, 7],), ([2, 3, 1, 0],)],
  hidden_args=[([1, 1],), ([1, 2],), ([0, 0, 0],), ([-1, 2, -3, 4],), ([5, -5, 5, -5],), ([100000, -100000],)],
  ref=ref_splitways, tags=["array", "prefix-sum"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Compute the total sum once.", "Scan split points left to right, maintaining the left sum.", "Right sum = total - left; count splits where left >= right."])

# ---------------- Medium ----------------

def ref_product(nums):
    n = len(nums)
    out = [1] * n
    for i in range(1, n):
        out[i] = out[i - 1] * nums[i - 1]
    suf = 1
    for i in range(n - 1, -1, -1):
        out[i] *= suf
        suf *= nums[i]
    return out

q(id="product-of-array-except-self", title="Product of Array Except Self", difficulty="Medium",
  description="Given an integer array nums, return an array answer such that answer[i] is the product of all elements of nums except nums[i]. Solve it in O(n) time without using the division operator, and with O(1) extra space (the output array does not count).",
  examples=[("nums = [1, 2, 3, 4]", "[24, 12, 8, 6]", "Products excluding each index."),
            ("nums = [-1, 1, 0, -3, 3]", "[0, 0, 9, 0, 0]", "The zero forces most products to 0.")],
  constraints=["2 <= nums.length <= 10^5", "-30 <= nums[i] <= 30", "The product of any prefix or suffix fits in a 32-bit integer."],
  method_name="productExceptSelf", return_type="int[]", params=[("nums", "int[]")],
  sample_args=[([1, 2, 3, 4],), ([-1, 1, 0, -3, 3],)],
  hidden_args=[([2, 3],), ([0, 0],), ([5],), ([-2, -3],), ([1, 2, 3, 4, 5],), ([0, 1, 2, 3],)],
  ref=ref_product, tags=["array", "prefix-sum"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["answer[i] = (product left of i) * (product right of i).", "One left-to-right pass fills prefix products into the output array.", "A second right-to-left pass multiplies in the suffix products using a running variable."])

def ref_contig(nums):
    first = {0: -1}
    pref = best = 0
    for i, x in enumerate(nums):
        pref += 1 if x == 1 else -1
        if pref in first:
            best = max(best, i - first[pref])
        else:
            first[pref] = i
    return best

q(id="contiguous-array", title="Contiguous Array", difficulty="Medium",
  description="Given a binary array nums, return the maximum length of a contiguous subarray with an equal number of 0 and 1.",
  examples=[("nums = [0, 1]", "2", "The whole array is balanced."),
            ("nums = [0, 1, 0]", "2", "Subarrays [0, 1] or [1, 0].")],
  constraints=["1 <= nums.length <= 10^5", "nums[i] is 0 or 1."],
  method_name="findMaxLength", return_type="int", params=[("nums", "int[]")],
  sample_args=[([0, 1],), ([0, 1, 0],)],
  hidden_args=[([0, 0, 1, 0, 0, 0, 1, 1],), ([0, 0, 0, 1, 1, 1],), ([1, 1, 1],), ([0],), ([0, 1, 1, 0, 1, 1, 1, 0],), ([1, 0, 1, 0, 1],)],
  ref=ref_contig, tags=["array", "hash-table", "prefix-sum"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Treat 0 as -1; then you need the longest subarray summing to 0.", "Equal prefix sums at indices i and j mean subarray (i, j] sums to 0.", "Store the first index where each prefix sum occurs in a hash map."])

def ref_divk(nums, k):
    freq = {0: 1}
    pref = ans = 0
    for x in nums:
        pref = (pref + x) % k
        ans += freq.get(pref, 0)
        freq[pref] = freq.get(pref, 0) + 1
    return ans

q(id="subarray-sums-divisible-by-k", title="Subarray Sums Divisible by K", difficulty="Medium",
  description="Given an integer array nums and an integer k, return the number of non-empty subarrays whose sum is divisible by k.",
  examples=[("nums = [4, 5, 0, -2, -3, 1], k = 5", "7", "Seven subarrays have sums divisible by 5."),
            ("nums = [5], k = 9", "0", "The only subarray [5] is not divisible by 9.")],
  constraints=["1 <= nums.length <= 3 * 10^4", "-10^4 <= nums[i] <= 10^4", "2 <= k <= 10^4"],
  method_name="subarraysDivByK", return_type="int", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([4, 5, 0, -2, -3, 1], 5), ([5], 9)],
  hidden_args=[([0, 0], 2), ([1, 2, 3], 3), ([-1, 2, 9], 2), ([7, 4, -10], 7), ([2, -2, 2, -2], 2), ([1, 2, 3, 4], 5)],
  ref=ref_divk, tags=["array", "hash-table", "prefix-sum"],
  time_complexity="O(n)", space_complexity="O(k)",
  hints=["A subarray sum is divisible by k iff its two bounding prefix sums are congruent mod k.", "Track prefix sums modulo k in a frequency map.", "In Java, normalize negative remainders with ((x % k) + k) % k."])

def ref_binsum(nums, goal):
    freq = {0: 1}
    pref = ans = 0
    for x in nums:
        pref += x
        ans += freq.get(pref - goal, 0)
        freq[pref] = freq.get(pref, 0) + 1
    return ans

q(id="binary-subarrays-with-sum", title="Binary Subarrays With Sum", difficulty="Medium",
  description="Given a binary array nums and an integer goal, return the number of non-empty subarrays with sum equal to goal.",
  examples=[("nums = [1, 0, 1, 0, 1], goal = 2", "4", "Four subarrays sum to 2."),
            ("nums = [0, 0, 0, 0, 0], goal = 0", "15", "Every subarray sums to 0: 5*6/2 = 15.")],
  constraints=["1 <= nums.length <= 3 * 10^4", "nums[i] is 0 or 1.", "0 <= goal <= nums.length"],
  method_name="numSubarraysWithSum", return_type="int", params=[("nums", "int[]"), ("goal", "int")],
  sample_args=[([1, 0, 1, 0, 1], 2), ([0, 0, 0, 0, 0], 0)],
  hidden_args=[([1, 1, 1], 3), ([0, 1], 1), ([1, 0, 0], 0), ([1, 0, 1], 1), ([0, 0, 1, 1, 0], 2), ([1, 0, 0, 1], 1)],
  ref=ref_binsum, tags=["array", "hash-table", "prefix-sum", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["This is the prefix-sum counting pattern: subarray (i, j] sums to goal iff pref[j] - pref[i] = goal.", "Keep frequencies of prefix sums seen so far in a hash map.", "For each new prefix P, add freq[P - goal] to the answer."])

def ref_nice(nums, k):
    def at_most(K):
        if K < 0:
            return 0
        l = odd = ans = 0
        for r, x in enumerate(nums):
            odd += x & 1
            while odd > K:
                odd -= nums[l] & 1
                l += 1
            ans += r - l + 1
        return ans
    return at_most(k) - at_most(k - 1)

q(id="count-number-of-nice-subarrays", title="Count Number of Nice Subarrays", difficulty="Medium",
  description="Given an array of integers nums and an integer k, a subarray is nice if it contains exactly k odd numbers. Return the number of nice non-empty subarrays.",
  examples=[("nums = [1, 1, 2, 1, 1], k = 3", "2", "Subarrays [1,1,2,1] and [1,2,1,1]."),
            ("nums = [2, 4, 6], k = 1", "0", "No odd numbers at all."),
            ("nums = [2, 2, 2, 1, 2, 2, 1, 2, 2, 2], k = 2", "16", "Sixteen subarrays contain exactly 2 odds.")],
  constraints=["1 <= nums.length <= 50000", "1 <= nums[i] <= 10^5", "1 <= k <= nums.length"],
  method_name="numberOfSubarrays", return_type="int", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([1, 1, 2, 1, 1], 3), ([2, 4, 6], 1)],
  hidden_args=[([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2), ([1, 1, 1], 1), ([1, 1, 1], 2), ([2, 2, 2], 1), ([1, 3, 5], 3), ([1, 2, 1, 2, 1], 2)],
  ref=ref_nice, tags=["array", "hash-table", "prefix-sum", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Map each number to 1 if odd, 0 if even; then count subarrays summing to k.", "The prefix-sum + hash map approach works directly.", "Alternatively: exactly-k = atMost(k) - atMost(k-1) with a sliding window."])

def ref_maxlen_k(nums, k):
    first = {0: -1}
    pref = best = 0
    for i, x in enumerate(nums):
        pref += x
        if pref - k in first:
            best = max(best, i - first[pref - k])
        if pref not in first:
            first[pref] = i
    return best

q(id="maximum-size-subarray-sum-equals-k", title="Maximum Size Subarray Sum Equals K", difficulty="Medium",
  description="Given an integer array nums and an integer k, return the maximum length of a subarray that sums to k. If no such subarray exists, return 0.",
  examples=[("nums = [1, -1, 5, -2, 3], k = 3", "4", "Subarray [1, -1, 5, -2] sums to 3."),
            ("nums = [-2, -1, 2, 1], k = 1", "2", "Subarray [-1, 2] sums to 1.")],
  constraints=["1 <= nums.length <= 2 * 10^5", "-10^4 <= nums[i] <= 10^4", "-10^5 <= k <= 10^5"],
  method_name="maxSubArrayLen", return_type="int", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([1, -1, 5, -2, 3], 3), ([-2, -1, 2, 1], 1)],
  hidden_args=[([1, 2, 3], 3), ([1, 2, 3], 7), ([1, -1, 1, -1], 0), ([5], 5), ([-1, 1, -1, 1, -1], 0), ([3, 1, 2], 3)],
  ref=ref_maxlen_k, tags=["array", "hash-table", "prefix-sum"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["For the longest subarray, you want the earliest occurrence of each prefix sum.", "Subarray (i, j] sums to k iff pref[j] - pref[i] = k.", "Store only the first index of each prefix sum in the hash map."])

def ref_checksub(nums, k):
    seen = {0: -1}
    pref = 0
    for i, x in enumerate(nums):
        pref += x
        r = pref % k
        if r in seen:
            if i - seen[r] >= 2:
                return True
        else:
            seen[r] = i
    return False

q(id="continuous-subarray-sum", title="Continuous Subarray Sum", difficulty="Medium",
  description="Given an integer array nums and an integer k, return true if nums has a continuous subarray of size at least 2 whose elements sum to a multiple of k (i.e., sum % k == 0), or false otherwise.",
  examples=[("nums = [23, 2, 4, 6, 7], k = 6", "true", "Subarray [2, 4] sums to 6."),
            ("nums = [23, 2, 6, 4, 7], k = 6", "true", "The whole array sums to 48, a multiple of 6."),
            ("nums = [23, 2, 6, 4, 7], k = 13", "false", "No qualifying subarray.")],
  constraints=["1 <= nums.length <= 10^5", "0 <= nums[i] <= 10^9", "0 <= sum(nums[i]) <= 2^31 - 1", "1 <= k <= 2^31 - 1"],
  method_name="checkSubarraySum", return_type="boolean", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([23, 2, 4, 6, 7], 6), ([23, 2, 6, 4, 7], 6)],
  hidden_args=[([23, 2, 6, 4, 7], 13), ([0, 0], 1), ([1, 0], 2), ([5, 0, 0], 5), ([1, 2, 3], 5), ([0], 1)],
  ref=ref_checksub, tags=["array", "hash-table", "prefix-sum", "math"],
  time_complexity="O(n)", space_complexity="O(k)",
  hints=["A subarray sum is a multiple of k iff its bounding prefix sums are congruent mod k.", "Store the first index of each prefix-mod value.", "When a mod repeats at index i with first occurrence j, check i - j >= 2."])

def ref_shift(s, shifts):
    n = len(s)
    suf = 0
    out = [""] * n
    for i in range(n - 1, -1, -1):
        suf = (suf + shifts[i]) % 26
        out[i] = chr((ord(s[i]) - 97 + suf) % 26 + 97)
    return "".join(out)

q(id="shifting-letters", title="Shifting Letters", difficulty="Medium",
  description="You are given a string s of lowercase English letters and an integer array shifts of the same length. For each i, shift s[i] forward by shifts[i] positions in the alphabet (wrapping z to a), and also apply all shifts[j] for j > i to s[i]. Equivalently, s[i] is shifted by the suffix sum shifts[i] + shifts[i+1] + ... . Return the final string.",
  examples=[('s = "abc", shifts = [3, 5, 9]', '"rpl"', 'Suffix shifts: 17, 14, 9 -> "rpl".'),
            ('s = "a", shifts = [1]', '"b"', "A single shift of 1.")],
  constraints=["1 <= s.length <= 10^5", "s consists of lowercase English letters.", "0 <= shifts[i] <= 10^9"],
  method_name="shiftingLetters", return_type="String", params=[("s", "String"), ("shifts", "int[]")],
  sample_args=[("abc", [3, 5, 9]), ("a", [1])],
  hidden_args=[("z", [1]), ("abc", [0, 0, 0]), ("xyz", [27, 27, 27]), ("aaa", [1, 2, 3]), ("bad", [10, 20, 30]), ("ruu", [26, 9, 17])],
  ref=ref_shift, tags=["string", "prefix-sum"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Naively applying every shift to every later character is O(n^2).", "Process from right to left, maintaining the running suffix sum modulo 26.", "Each character shifts by the accumulated suffix total; use long arithmetic to avoid overflow."])

# ---------------- Hard ----------------

def ref_countrange(nums, lower, upper):
    pref = [0]
    for x in nums:
        pref.append(pref[-1] + x)
    ans = 0
    n = len(pref)
    for i in range(n):
        for j in range(i + 1, n):
            if lower <= pref[j] - pref[i] <= upper:
                ans += 1
    return ans

q(id="count-of-range-sum", title="Count of Range Sum", difficulty="Hard",
  description="Given an integer array nums and two integers lower and upper, return the number of range sums: pairs (i, j) with 0 <= i <= j < nums.length such that lower <= sum(nums[i..j]) <= upper.",
  examples=[("nums = [-2, 5, -1], lower = -2, upper = 2", "3", "Range sums: [-2], [5, -1], [-1] fall in [-2, 2]."),
            ("nums = [0], lower = 0, upper = 0", "1", "The single range sum 0 is in range.")],
  constraints=["1 <= nums.length <= 10^5", "-2^31 <= nums[i] <= 2^31 - 1", "-10^5 <= lower <= upper <= 10^5"],
  method_name="countRangeSum", return_type="int", params=[("nums", "int[]"), ("lower", "int"), ("upper", "int")],
  sample_args=[([-2, 5, -1], -2, 2), ([0], 0, 0)],
  hidden_args=[([1, 2, 3], 3, 6), ([-1, -2, -3], -6, -1), ([1, 1, 1], 2, 2), ([5, -3, 2], -1, 4), ([0, 0, 0], 0, 0), ([2, 1, -1], 0, 2)],
  ref=ref_countrange, tags=["array", "prefix-sum", "divide-and-conquer", "merge-sort", "binary-search"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Range sum (i, j] equals pref[j] - pref[i]; the problem becomes counting valid prefix pairs.", "Brute force over prefix pairs is O(n^2).", "Merge sort on prefix sums counts, for each left-half prefix, how many right-half prefixes fall in [pref + lower, pref + upper] using two pointers or binary search."])

def ref_shortest(nums, k):
    from collections import deque as dq
    n = len(nums)
    pref = [0] * (n + 1)
    for i, x in enumerate(nums):
        pref[i + 1] = pref[i] + x
    de = dq()
    best = float("inf")
    for i, p in enumerate(pref):
        while de and p - pref[de[0]] >= k:
            best = min(best, i - de.popleft())
        while de and pref[de[-1]] >= p:
            de.pop()
        de.append(i)
    return -1 if best == float("inf") else best

q(id="shortest-subarray-with-sum-at-least-k", title="Shortest Subarray with Sum at Least K", difficulty="Hard",
  description="Given an integer array nums and an integer k, return the length of the shortest non-empty subarray of nums with sum at least k. If there is no such subarray, return -1. Note nums may contain negative numbers, so the sliding-window two-pointer technique does not apply.",
  examples=[("nums = [1], k = 1", "1", "[1] sums to 1."),
            ("nums = [1, 2], k = 4", "-1", "No subarray reaches 4."),
            ("nums = [2, -1, 2], k = 3", "3", "The whole array sums to 3.")],
  constraints=["1 <= nums.length <= 10^5", "-10^5 <= nums[i] <= 10^5", "1 <= k <= 10^9"],
  method_name="shortestSubarray", return_type="int", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([1], 1), ([1, 2], 4)],
  hidden_args=[([2, -1, 2], 3), ([84, -37, 32, 40, 95], 167), ([1, 2, 3, 4], 10), ([5, -2, 5], 7), ([-1, -2, -3], 1), ([2, 7, 3, -8, 4, 2, 8, 1, 9], 15)],
  ref=ref_shortest, tags=["array", "prefix-sum", "deque", "monotonic-queue"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Negatives break the sliding window; use prefix sums with a monotonic deque of candidate start indices.", "Keep deque indices in increasing prefix-sum order.", "For each end i, pop from the front while pref[i] - pref[front] >= k (record the length), then pop from the back while pref[back] >= pref[i]."])

def ref_submatrix(matrix, target):
    R, C = len(matrix), len(matrix[0])
    ans = 0
    for top in range(R):
        colsum = [0] * C
        for bot in range(top, R):
            for c in range(C):
                colsum[c] += matrix[bot][c]
            freq = {0: 1}
            pref = 0
            for v in colsum:
                pref += v
                ans += freq.get(pref - target, 0)
                freq[pref] = freq.get(pref, 0) + 1
    return ans

q(id="number-of-submatrices-that-sum-to-target", title="Number of Submatrices That Sum to Target", difficulty="Hard",
  description="Given a matrix of integers and an integer target, return the number of non-empty submatrices that sum to target. A submatrix is a contiguous rectangular region of the matrix.",
  examples=[("matrix = [[0, 1, 0], [1, 1, 1], [0, 1, 0]], target = 0", "4", "Four single cells contain 0."),
            ("matrix = [[1, -1], [-1, 1]], target = 0", "5", "Four single cells? No: the 1s and -1s; the five are: the whole matrix, the two rows, and the two columns.")],
  constraints=["1 <= matrix.length, matrix[0].length <= 100", "-1000 <= matrix[i][j] <= 1000", "-10^8 <= target <= 10^8"],
  method_name="numSubmatrixSumTarget", return_type="int", params=[("matrix", "int[][]"), ("target", "int")],
  sample_args=[([[0, 1, 0], [1, 1, 1], [0, 1, 0]], 0), ([[1, -1], [-1, 1]], 0)],
  hidden_args=[([[1]], 1), ([[0, 0], [0, 0]], 0), ([[1, 2], [3, 4]], 10), ([[1, -1], [-1, 1]], 1), ([[2, 2], [2, 2]], 4), ([[1, 2, 3]], 3)],
  ref=ref_submatrix, tags=["array", "matrix", "hash-table", "prefix-sum"],
  time_complexity="O(R^2 * C)", space_complexity="O(C)",
  hints=["Fix the top and bottom rows; column sums between them reduce the problem to 1D.", "For each row pair, count subarrays of the column-sum array equal to target with the prefix-sum hash map.", "Iterate over the smaller dimension for the outer pair loop."])

def ref_3sub(nums, k):
    n = len(nums)
    wsum = [0] * (n - k + 1)
    s = sum(nums[:k])
    wsum[0] = s
    for i in range(1, n - k + 1):
        s += nums[i + k - 1] - nums[i - 1]
        wsum[i] = s
    m = len(wsum)
    left = [0] * m
    best = 0
    for i in range(m):
        if wsum[i] > wsum[best]:
            best = i
        left[i] = best
    right = [0] * m
    best = m - 1
    for i in range(m - 1, -1, -1):
        if wsum[i] >= wsum[best]:
            best = i
        right[i] = best
    ans = None
    best_sum = -1
    for j in range(k, m - k):
        i, l = left[j - k], right[j + k]
        tot = wsum[i] + wsum[j] + wsum[l]
        if tot > best_sum:
            best_sum = tot
            ans = [i, j, l]
    return ans

q(id="maximum-sum-of-3-non-overlapping-subarrays", title="Maximum Sum of 3 Non-Overlapping Subarrays", difficulty="Hard",
  description="Given an integer array nums and an integer k, find three non-overlapping subarrays of length k with maximum sum. Return the starting indices [i, j, k] of the three subarrays. If there are multiple answers, return the lexicographically smallest one. It is guaranteed that 3 * k <= nums.length.",
  examples=[("nums = [1, 2, 1, 2, 6, 7, 5, 1], k = 2", "[0, 3, 5]", "Subarrays [1,2], [2,6], [7,5] sum to 3 + 8 + 12 = 23."),
            ("nums = [1, 2, 1, 2, 1, 2, 1, 2, 1], k = 2", "[0, 2, 4]", "Every window sums to 3; the lexicographically smallest triple wins.")],
  constraints=["1 <= nums.length <= 2 * 10^4", "1 <= nums[i] <= 2^16", "1 <= k <= floor(nums.length / 3)", "3 * k <= nums.length"],
  method_name="maxSumOfThreeSubarrays", return_type="int[]", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([1, 2, 1, 2, 6, 7, 5, 1], 2), ([1, 2, 1, 2, 1, 2, 1, 2, 1], 2)],
  hidden_args=[([1, 2, 3, 4, 5, 6, 7, 8, 9], 3), ([4, 5, 10, 6, 11, 17, 4, 11, 1, 3], 1), ([1, 2, 3, 4, 5, 6], 2), ([1, 1, 1, 1, 1, 1], 2), ([10, 1, 1, 10, 1, 1, 10], 1), ([5, 4, 3, 2, 1, 6, 7, 8, 9], 3)],
  ref=ref_3sub, tags=["array", "prefix-sum", "sliding-window", "dynamic-programming"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Precompute every length-k window sum with a sliding window.", "For each middle window j, the best left window lies in [0, j-k] and the best right window in [j+k, end].", "Precompute best-left and best-right index arrays; use strict > on the left and >= on the right to get the lexicographically smallest answer."])

write_bank(P, Q)
