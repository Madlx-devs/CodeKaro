"""Sliding Window pattern: 20 questions (8 Easy, 8 Medium, 4 Hard)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genlib import make_question, write_bank
from collections import Counter, deque, defaultdict

P = "sliding-window"
Q = []

def q(**kw):
    Q.append(make_question(pattern=P, **kw))

# ---------------- Easy ----------------

def ref_maxavg(nums, k):
    s = sum(nums[:k])
    best = s
    for i in range(k, len(nums)):
        s += nums[i] - nums[i - k]
        best = max(best, s)
    return best / k

q(id="maximum-average-subarray-i", title="Maximum Average Subarray I", difficulty="Easy",
  description="You are given an integer array nums consisting of n elements, and an integer k. Find a contiguous subarray whose length is exactly k that has the maximum average value, and return this value.",
  examples=[("nums = [1, 12, -5, -6, 50, 3], k = 4", "12.75", "Subarray [12, -5, -6, 50] averages 12.75."),
            ("nums = [5], k = 1", "5.0", "Only one subarray.")],
  constraints=["1 <= k <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
  method_name="findMaxAverage", return_type="double", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([1, 12, -5, -6, 50, 3], 4), ([5], 1)],
  hidden_args=[([0, 1, 1, 3, 3], 4), ([-1], 1), ([4, 2, 1, 3, 3], 2), ([1, 2, 3, 4, 5], 5), ([-3, -2, -1], 2), ([8, 0], 2)],
  ref=ref_maxavg, tags=["array", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["The average is maximized exactly when the window sum is maximized.", "Slide a fixed-size window of length k across the array.", "Update the sum in O(1) by adding the new element and subtracting the one that leaves."])

def ref_decrypt(code, k):
    n = len(code)
    if k == 0:
        return [0] * n
    out = []
    for i in range(n):
        if k > 0:
            out.append(sum(code[(i + j) % n] for j in range(1, k + 1)))
        else:
            out.append(sum(code[(i - j) % n] for j in range(1, -k + 1)))
    return out

q(id="defuse-the-bomb", title="Defuse the Bomb", difficulty="Easy",
  description="You have a circular array code of n integers. To defuse the bomb, replace every number with the sum of the next k numbers if k is positive, the sum of the previous k numbers if k is negative, or 0 if k is zero. The array is circular, so indices wrap around. Return the resulting array.",
  examples=[("code = [5, 7, 1, 4], k = 3", "[12, 10, 16, 13]", "Each element becomes the sum of the next 3 (wrapping around)."),
            ("code = [1, 2, 3, 4], k = 0", "[0, 0, 0, 0]", "k = 0 replaces everything with 0."),
            ("code = [2, 4, 9, 3], k = -2", "[12, 5, 6, 13]", "Each element becomes the sum of the previous 2 (wrapping around).")],
  constraints=["1 <= code.length <= 100", "1 <= code[i] <= 100", "-100 <= k <= 100"],
  method_name="decrypt", return_type="int[]", params=[("code", "int[]"), ("k", "int")],
  sample_args=[([5, 7, 1, 4], 3), ([1, 2, 3, 4], 0)],
  hidden_args=[([2, 4, 9, 3], -2), ([10, 20, 30], 1), ([10, 20, 30], -1), ([1, 2, 3, 4, 5], 2), ([3, 1, 2], -3), ([7, 7, 7], 2)],
  ref=ref_decrypt, tags=["array", "sliding-window"],
  time_complexity="O(n * |k|)", space_complexity="O(n)",
  hints=["Handle k = 0 as a special case returning all zeros.", "For k > 0, index (i + j) % n wraps around the circular array.", "A sliding window can compute all sums in O(n), but the direct O(n*|k|) simulation is fine for n <= 100."])

def ref_recolors(blocks, k):
    w = sum(1 for c in blocks[:k] if c == "W")
    best = w
    for i in range(k, len(blocks)):
        if blocks[i] == "W":
            w += 1
        if blocks[i - k] == "W":
            w -= 1
        best = min(best, w)
    return best

q(id="minimum-recolors-to-get-k-consecutive-black-blocks", title="Minimum Recolors to Get K Consecutive Black Blocks", difficulty="Easy",
  description='You are given a string blocks of length n, where blocks[i] is either "W" (white) or "B" (black), and an integer k. In one operation you can recolor a white block black. Return the minimum number of operations needed so that there are at least k consecutive black blocks.',
  examples=[('blocks = "WBBWWBBWBW", k = 7', "3", "Recolor 3 whites inside the best window of 7."),
            ('blocks = "WBWBBBW", k = 2', "0", '"BB" already exists at indices 3-4.')],
  constraints=["1 <= blocks.length <= 100", 'blocks[i] is "W" or "B".', "1 <= k <= blocks.length"],
  method_name="minimumRecolors", return_type="int", params=[("blocks", "String"), ("k", "int")],
  sample_args=[("WBBWWBBWBW", 7), ("WBWBBBW", 2)],
  hidden_args=[("B", 1), ("W", 1), ("WWWW", 2), ("BBBB", 3), ("WBWBWB", 4), ("BWWB", 2)],
  ref=ref_recolors, tags=["string", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Any valid answer corresponds to some window of k consecutive positions.", "The cost of a window equals its number of white blocks.", "Slide the window and track the minimum white count."])

def ref_dup2(nums, k):
    win = set()
    for i, x in enumerate(nums):
        if x in win:
            return True
        win.add(x)
        if len(win) > k:
            win.discard(nums[i - k])
    return False

q(id="contains-duplicate-ii", title="Contains Duplicate II", difficulty="Easy",
  description="Given an integer array nums and an integer k, return true if there are two distinct indices i and j in the array such that nums[i] == nums[j] and abs(i - j) <= k.",
  examples=[("nums = [1, 2, 3, 1], k = 3", "true", "Indices 0 and 3: same value, distance 3."),
            ("nums = [1, 0, 1, 1], k = 1", "true", "Indices 2 and 3: same value, distance 1."),
            ("nums = [1, 2, 3, 1, 2, 3], k = 2", "false", "No equal values within distance 2.")],
  constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9", "0 <= k <= 10^5"],
  method_name="containsNearbyDuplicate", return_type="boolean", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([1, 2, 3, 1], 3), ([1, 0, 1, 1], 1)],
  hidden_args=[([1, 2, 3, 1, 2, 3], 2), ([1, 2, 3, 4], 3), ([1, 1], 0), ([5, 5, 5], 2), ([99, 99], 2), ([1, 2, 3, 1], 2)],
  ref=ref_dup2, tags=["array", "hash-table", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(k)",
  hints=["Only the last k elements can pair with the current one.", "Maintain a sliding window of at most k recent values in a hash set.", "If the current value is already in the set, return true; otherwise add it and evict the element falling out of the window."])

def ref_diet(calories, k, lower, upper):
    s = sum(calories[:k])
    pts = (1 if s > upper else -1 if s < lower else 0)
    for i in range(k, len(calories)):
        s += calories[i] - calories[i - k]
        pts += 1 if s > upper else -1 if s < lower else 0
    return pts

q(id="diet-plan-performance", title="Diet Plan Performance", difficulty="Easy",
  description="A dieter consumes calories[i] calories on day i. For every consecutive sequence of k days, they gain 1 point if the total exceeds upper, lose 1 point if the total is below lower, and gain/lose nothing otherwise. Return the total points after evaluating every k-day window.",
  examples=[("calories = [1, 2, 3, 4, 5], k = 1, lower = 3, upper = 3", "0", "Windows: 1<3 (-1), 2<3 (-1), 3 (=0), 4>3 (+1), 5>3 (+1): total 0."),
            ("calories = [3, 2], k = 2, lower = 0, upper = 1", "1", "Total 5 > 1: +1 point."),
            ("calories = [6, 5, 0, 0], k = 2, lower = 1, upper = 5", "0", "Windows 11 (>5: +1) and 0 (<1: -1): total 0.")],
  constraints=["1 <= k <= calories.length <= 10^5", "0 <= calories[i] <= 30000", "0 <= lower <= upper"],
  method_name="dietPlanPerformance", return_type="int", params=[("calories", "int[]"), ("k", "int"), ("lower", "int"), ("upper", "int")],
  sample_args=[([1, 2, 3, 4, 5], 1, 3, 3), ([3, 2], 2, 0, 1)],
  hidden_args=[([6, 5, 0, 0], 2, 1, 5), ([6, 13, 8, 7, 10, 1, 12, 11], 6, 5, 37), ([1, 1, 1, 1], 4, 4, 4), ([1, 100, 1, 100], 2, 50, 150), ([100, 200, 300], 1, 50, 150), ([20, 20, 20], 2, 30, 50)],
  ref=ref_diet, tags=["array", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Each k-day window contributes -1, 0, or +1 based on its sum.", "A fixed-size sliding window maintains each window sum in O(1).", "Add the new day's calories and subtract the day leaving the window."])

def ref_kbeauty(num, k):
    s = str(num)
    cnt = 0
    for i in range(len(s) - k + 1):
        v = int(s[i:i + k])
        if v != 0 and num % v == 0:
            cnt += 1
    return cnt

q(id="find-the-k-beauty-of-a-number", title="Find the K-Beauty of a Number", difficulty="Easy",
  description="The k-beauty of an integer num is the number of substrings of its decimal representation, of length k, that are divisors of num (substrings equal to 0 are not divisors). Return the k-beauty of num.",
  examples=[("num = 240, k = 2", "2", 'Substrings "24" and "40": 240 % 24 = 0 and 240 % 40 = 0.'),
            ("num = 430043, k = 2", "2", 'Substrings: "43","30","00","04","43": divisors of 430043 are the two "43"s.')],
  constraints=["1 <= num <= 10^9", "1 <= k <= number of digits of num"],
  method_name="divisorSubstrings", return_type="int", params=[("num", "int"), ("k", "int")],
  sample_args=[(240, 2), (430043, 2)],
  hidden_args=[(30003, 3), (1, 1), (10, 1), (101, 2), (1000, 2), (999, 1)],
  ref=ref_kbeauty, tags=["string", "sliding-window", "math"],
  time_complexity="O(d)", space_complexity="O(d)",
  hints=["Convert num to a string and slide a window of length k over its digits.", "Parse each window as an integer; skip zeros.", "Count the windows whose value divides num evenly."])

def ref_good3(s):
    cnt = 0
    for i in range(len(s) - 2):
        if len(set(s[i:i + 3])) == 3:
            cnt += 1
    return cnt

q(id="substrings-of-size-three-with-distinct-characters", title="Substrings of Size Three with Distinct Characters", difficulty="Easy",
  description='A string is good if there are no repeated characters. Given a string s, return the number of good substrings of length three in s. Note that if there are multiple occurrences of the same substring, every occurrence counts.',
  examples=[('s = "xyzzaz"', "1", 'Only "xyz"? No: substrings are "xyz","yzz","zza","zaz": only "xyz" has all distinct characters.'),
            ('s = "aababcabc"', "4", 'Good length-3 windows: "abc" (index 3), "bca" (4), "cab" (5), "abc" (6).')],
  constraints=["1 <= s.length <= 100", "s consists of lowercase English letters."],
  method_name="countGoodSubstrings", return_type="int", params=[("s", "String")],
  sample_args=[("xyzzaz",), ("aababcabc",)],
  hidden_args=[("abc",), ("aaa",), ("ab",), ("abcd",), ("xyxyxy",), ("abcabc",)],
  ref=ref_good3, tags=["string", "sliding-window", "hash-table"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["The window size is fixed at 3.", "Slide it across the string one step at a time.", "A window is good when its 3 characters are all different; a small set or frequency check decides that."])

def ref_mindiff(nums, k):
    a = sorted(nums)
    return min(a[i + k - 1] - a[i] for i in range(len(a) - k + 1))

q(id="minimum-difference-between-highest-and-lowest-of-k-scores", title="Minimum Difference Between Highest and Lowest of K Scores", difficulty="Easy",
  description="You are given a 0-indexed integer array nums, where nums[i] represents the score of the ith student. Pick k students and return the minimum possible difference between the highest and lowest of their scores.",
  examples=[("nums = [90], k = 1", "0", "One student: difference 0."),
            ("nums = [9, 4, 1, 7], k = 2", "2", "Pick 7 and 9: difference 2.")],
  constraints=["1 <= k <= nums.length <= 1000", "0 <= nums[i] <= 10^5"],
  method_name="minimumDifference", return_type="int", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([90], 1), ([9, 4, 1, 7], 2)],
  hidden_args=[([1, 2, 3, 4, 5], 3), ([5, 5, 5, 5], 2), ([10, 100, 300, 200, 1000, 20, 30], 3), ([1, 1000000], 1), ([4, 9, 3, 7, 1], 4), ([8, 8, 8, 8, 8], 5)],
  ref=ref_mindiff, tags=["array", "sorting", "sliding-window"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Sort the scores first; the optimal k students will be consecutive in sorted order.", "Then the problem is a fixed-size sliding window.", "The answer is the minimum of a[i + k - 1] - a[i] over all windows."])

# ---------------- Medium ----------------

def ref_longest_norep(s):
    last = {}
    l = best = 0
    for r, c in enumerate(s):
        if c in last and last[c] >= l:
            l = last[c] + 1
        last[c] = r
        best = max(best, r - l + 1)
    return best

q(id="longest-substring-without-repeating-characters", title="Longest Substring Without Repeating Characters", difficulty="Medium",
  description="Given a string s, find the length of the longest substring without repeating characters.",
  examples=[('s = "abcabcbb"', "3", '"abc" is the longest; "bca" also qualifies.'),
            ('s = "bbbbb"', "1", '"b" is the longest.'),
            ('s = "pwwkew"', "3", '"wke" is the longest.')],
  constraints=["0 <= s.length <= 5 * 10^4", "s consists of English letters, digits, symbols and spaces."],
  method_name="lengthOfLongestSubstring", return_type="int", params=[("s", "String")],
  sample_args=[("abcabcbb",), ("bbbbb",)],
  hidden_args=[("pwwkew",), ("a",), ("abcdef",), ("abba",), ("tmmzuxt",), ("dvdf",)],
  ref=ref_longest_norep, tags=["string", "hash-table", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(min(n, alphabet))",
  hints=["Expand the right end of the window one character at a time.", "Keep the last index of each character in a hash map.", "When a repeat appears inside the window, jump the left edge past the previous occurrence."])

def ref_minsub(target, nums):
    l = s = 0
    best = float("inf")
    for r, x in enumerate(nums):
        s += x
        while s >= target:
            best = min(best, r - l + 1)
            s -= nums[l]
            l += 1
    return 0 if best == float("inf") else best

q(id="minimum-size-subarray-sum", title="Minimum Size Subarray Sum", difficulty="Medium",
  description="Given an array of positive integers nums and a positive integer target, return the minimal length of a contiguous subarray whose sum is greater than or equal to target. If there is no such subarray, return 0.",
  examples=[("target = 7, nums = [2, 3, 1, 2, 4, 3]", "2", "Subarray [4, 3] sums to 7."),
            ("target = 4, nums = [1, 4, 4]", "1", "Subarray [4] sums to 4."),
            ("target = 11, nums = [1, 1, 1, 1, 1, 1, 1, 1]", "0", "Total sum is only 8.")],
  constraints=["1 <= target <= 10^9", "1 <= nums.length <= 10^5", "1 <= nums[i] <= 10^5"],
  method_name="minSubArrayLen", return_type="int", params=[("target", "int"), ("nums", "int[]")],
  sample_args=[(7, [2, 3, 1, 2, 4, 3]), (4, [1, 4, 4])],
  hidden_args=[(11, [1, 1, 1, 1, 1, 1, 1, 1]), (15, [1, 2, 3, 4, 5]), (100, [1, 2, 3]), (3, [1, 1, 1]), (6, [10, 2, 3]), (5, [2, 3, 1, 2, 4, 3])],
  ref=ref_minsub, tags=["array", "sliding-window", "binary-search", "prefix-sum"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Because all numbers are positive, the window sum grows monotonically as the window expands.", "Expand the right edge; while the sum reaches target, record the length and shrink from the left.", "Each element enters and leaves the window once: O(n)."])

def ref_charrepl(s, k):
    freq = Counter()
    l = best = 0
    for r, c in enumerate(s):
        freq[c] += 1
        while (r - l + 1) - max(freq.values()) > k:
            freq[s[l]] -= 1
            l += 1
        best = max(best, r - l + 1)
    return best

q(id="longest-repeating-character-replacement", title="Longest Repeating Character Replacement", difficulty="Medium",
  description="You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times. Return the length of the longest substring containing the same letter you can get after performing the operations.",
  examples=[('s = "ABAB", k = 2', "4", 'Replace the two "B"s with "A"s to get "AAAA".'),
            ('s = "AABABBA", k = 1', "4", 'Replace one "A" with "B" to get "BBBB" inside "ABBA"? The best window "AABA" -> "AAAA" has length 4.')],
  constraints=["1 <= s.length <= 10^5", "s consists of only uppercase English letters.", "0 <= k <= s.length"],
  method_name="characterReplacement", return_type="int", params=[("s", "String"), ("k", "int")],
  sample_args=[("ABAB", 2), ("AABABBA", 1)],
  hidden_args=[("AAAA", 2), ("ABCDE", 1), ("ABBB", 2), ("AABABBA", 0), ("aabccbb", 2), ("EOEMQLL", 2)],
  ref=ref_charrepl, tags=["string", "hash-table", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["A window is valid when (window length - most frequent char count) <= k.", "Expand the right edge and track character frequencies.", "When the window becomes invalid, move the left edge forward until it is valid again; track the maximum valid length."])

def ref_checkincl(s1, s2):
    if len(s1) > len(s2):
        return False
    need = Counter(s1)
    win = Counter(s2[:len(s1)])
    if win == need:
        return True
    for i in range(len(s1), len(s2)):
        win[s2[i]] += 1
        win[s2[i - len(s1)]] -= 1
        if win[s2[i - len(s1)]] == 0:
            del win[s2[i - len(s1)]]
        if win == need:
            return True
    return False

q(id="permutation-in-string", title="Permutation in String", difficulty="Medium",
  description="Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise. In other words, return true if one of s1's permutations is a substring of s2.",
  examples=[('s1 = "ab", s2 = "eidbaooo"', "true", '"ba" is a substring of s2.'),
            ('s1 = "ab", s2 = "eidboaoo"', "false", "No length-2 window is a permutation of ab.")],
  constraints=["1 <= s1.length, s2.length <= 10^4", "s1 and s2 consist of lowercase English letters."],
  method_name="checkInclusion", return_type="boolean", params=[("s1", "String"), ("s2", "String")],
  sample_args=[("ab", "eidbaooo"), ("ab", "eidboaoo")],
  hidden_args=[("a", "a"), ("ab", "a"), ("abc", "ccccbbbbaaaa"), ("adc", "dcda"), ("ab", "ab"), ("abcdxabcde", "abcdeabcdx")],
  ref=ref_checkincl, tags=["string", "hash-table", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["A permutation of s1 is any window of s2 with the same character counts.", "Slide a fixed window of length s1.length() over s2.", "Compare frequency maps (or a matches-counter) instead of rebuilding them each step."])

def ref_fruit(fruits):
    last = {}
    l = best = 0
    for r, f in enumerate(fruits):
        last[f] = r
        while len(last) > 2:
            if last[fruits[l]] == l:
                del last[fruits[l]]
            l += 1
        best = max(best, r - l + 1)
    return best

q(id="fruit-into-baskets", title="Fruit Into Baskets", difficulty="Medium",
  description="You are visiting a row of trees where fruits[i] is the type of fruit the ith tree produces. You have two baskets, each holding one type of fruit. Starting at any tree, you move right picking one fruit per tree, but must stop when a third fruit type appears. Return the maximum number of fruits you can pick: the length of the longest subarray containing at most 2 distinct values.",
  examples=[("fruits = [1, 2, 1]", "3", "Pick all three trees."),
            ("fruits = [0, 1, 2, 2]", "3", "Pick [1, 2, 2]."),
            ("fruits = [1, 2, 3, 2, 2]", "4", "Pick [2, 3, 2, 2].")],
  constraints=["1 <= fruits.length <= 10^5", "0 <= fruits[i] < fruits.length"],
  method_name="totalFruit", return_type="int", params=[("fruits", "int[]")],
  sample_args=[([1, 2, 1],), ([0, 1, 2, 2],)],
  hidden_args=[([1, 2, 3, 2, 2],), ([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4],), ([1],), ([1, 1, 1, 1],), ([1, 2, 3, 4, 5],), ([0, 0, 1, 1],)],
  ref=ref_fruit, tags=["array", "hash-table", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["This is the longest subarray with at most 2 distinct numbers.", "Expand right, tracking each fruit type's latest index in a hash map.", "When a third type appears, move the left edge past the type whose last occurrence is earliest."])

def ref_maxvowels(s, k):
    v = set("aeiou")
    cur = sum(1 for c in s[:k] if c in v)
    best = cur
    for i in range(k, len(s)):
        if s[i] in v:
            cur += 1
        if s[i - k] in v:
            cur -= 1
        best = max(best, cur)
    return best

q(id="maximum-number-of-vowels-in-a-substring-of-given-length", title="Maximum Number of Vowels in a Substring of Given Length", difficulty="Medium",
  description="Given a string s and an integer k, return the maximum number of vowel letters ('a', 'e', 'i', 'o', 'u') in any substring of s with length k.",
  examples=[('s = "abciiidef", k = 3', "3", '"iii" contains 3 vowels.'),
            ('s = "aeiou", k = 2', "2", 'Any length-2 window has 2 vowels.'),
            ('s = "leetcode", k = 3', "2", '"lee" and "eet" each have 2 vowels.')],
  constraints=["1 <= s.length <= 10^5", "s consists of lowercase English letters.", "1 <= k <= s.length"],
  method_name="maxVowels", return_type="int", params=[("s", "String"), ("k", "int")],
  sample_args=[("abciiidef", 3), ("aeiou", 2)],
  hidden_args=[("leetcode", 3), ("a", 1), ("b", 1), ("aaa", 3), ("bbb", 2), ("ibpbhix", 2)],
  ref=ref_maxvowels, tags=["string", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Only whether each character is a vowel matters.", "Slide a fixed window of length k.", "Add 1 when a vowel enters, subtract 1 when a vowel leaves; track the max."])

def ref_long1b(nums):
    # cleaner: longest window with at most one zero, then minus one (must delete one element)
    l = zeros = best = 0
    for r, x in enumerate(nums):
        zeros += (x == 0)
        while zeros > 1:
            zeros -= (nums[l] == 0)
            l += 1
        best = max(best, r - l + 1)
    return max(0, best - 1)

q(id="longest-subarray-of-1s-after-deleting-one-element", title="Longest Subarray of 1s After Deleting One Element", difficulty="Medium",
  description="Given a binary array nums, delete exactly one element from it and return the size of the longest non-empty subarray containing only 1s in the resulting array. If the resulting array has no 1s, return 0.",
  examples=[("nums = [1, 1, 0, 1]", "3", "Delete the 0 to get [1, 1, 1]."),
            ("nums = [0, 1, 1, 1, 0, 1, 1, 0, 1]", "5", "Delete a 0 to join five 1s."),
            ("nums = [1, 1, 1]", "2", "You must delete one element even though all are 1.")],
  constraints=["1 <= nums.length <= 10^5", "nums[i] is 0 or 1."],
  method_name="longestSubarray", return_type="int", params=[("nums", "int[]")],
  sample_args=[([1, 1, 0, 1],), ([0, 1, 1, 1, 0, 1, 1, 0, 1],)],
  hidden_args=[([1, 1, 1],), ([0, 0, 0],), ([1, 0, 1],), ([1, 1, 0, 0, 1, 1, 1, 0, 1],), ([0, 1],), ([1, 0],)],
  ref=ref_long1b, tags=["array", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Deleting one element lets the window contain at most one zero.", "Find the longest window with at most one zero.", "The answer is that window length minus 1 (the deleted element); handle the all-ones edge case."])

def ref_grumpy(customers, grumpy, minutes):
    base = sum(c for c, g in zip(customers, grumpy) if g == 0)
    gain = sum(customers[i] for i in range(minutes) if grumpy[i] == 1)
    best = gain
    for i in range(minutes, len(customers)):
        if grumpy[i] == 1:
            gain += customers[i]
        if grumpy[i - minutes] == 1:
            gain -= customers[i - minutes]
        best = max(best, gain)
    return base + best

q(id="grumpy-bookstore-owner", title="Grumpy Bookstore Owner", difficulty="Medium",
  description="A bookstore owner has customers[i] customers entering on minute i, and grumpy[i] = 1 if the owner is grumpy that minute (those customers leave unsatisfied) or 0 if not. The owner can use a secret technique to stay calm for exactly minutes consecutive minutes, making all customers in that window satisfied. Return the maximum number of satisfied customers.",
  examples=[("customers = [1, 0, 1, 2, 1, 1, 7, 5], grumpy = [0, 1, 0, 1, 0, 1, 0, 1], minutes = 3", "16", "Use the technique on minutes 3-5: customers 2, 1, 1 become satisfied."),
            ("customers = [1], grumpy = [0], minutes = 1", "1", "The single customer is already satisfied.")],
  constraints=["1 <= customers.length <= 2 * 10^4", "0 <= customers[i] <= 1000", "grumpy[i] is 0 or 1.", "1 <= minutes <= customers.length"],
  method_name="maxSatisfied", return_type="int", params=[("customers", "int[]"), ("grumpy", "int[]"), ("minutes", "int")],
  sample_args=[([1, 0, 1, 2, 1, 1, 7, 5], [0, 1, 0, 1, 0, 1, 0, 1], 3), ([1], [0], 1)],
  hidden_args=[([1], [1], 1), ([4, 10, 10], [1, 1, 0], 2), ([2, 6, 6, 9], [0, 0, 1, 1], 1), ([1, 2, 3, 4, 5], [1, 1, 1, 1, 1], 5), ([5, 8], [0, 1], 1), ([10, 1, 7], [1, 0, 1], 2)],
  ref=ref_grumpy, tags=["array", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Customers during non-grumpy minutes are always satisfied: sum those first.", "The technique only helps grumpy minutes, so slide a window maximizing the extra grumpy-minute customers covered.", "Add the base satisfied count to the best window gain."])

# ---------------- Hard ----------------

def ref_minwindow(s, t):
    need = Counter(t)
    missing = len(t)
    l = 0
    best = (float("inf"), 0, 0)
    win = Counter()
    for r, c in enumerate(s):
        if win[c] < need[c]:
            missing -= 1
        win[c] += 1
        while missing == 0:
            if r - l + 1 < best[0]:
                best = (r - l + 1, l, r)
            if win[s[l]] == need[s[l]]:
                missing += 1
            win[s[l]] -= 1
            l += 1
    if best[0] == float("inf"):
        return ""
    return s[best[1]:best[2] + 1]

q(id="minimum-window-substring", title="Minimum Window Substring", difficulty="Hard",
  description="Given two strings s and t, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. Every test case in this problem has at least one valid window, so the answer is never empty.",
  examples=[('s = "ADOBECODEBANC", t = "ABC"', '"BANC"', "The smallest window containing A, B, C."),
            ('s = "a", t = "a"', '"a"', "The whole string."),
            ('s = "ab", t = "b"', '"b"', "The window is just the last character.")],
  constraints=["1 <= s.length, t.length <= 10^5", "s and t consist of uppercase and lowercase English letters."],
  method_name="minWindow", return_type="String", params=[("s", "String"), ("t", "String")],
  sample_args=[("ADOBECODEBANC", "ABC"), ("a", "a")],
  hidden_args=[("ab", "b"), ("abc", "cba"), ("aab", "aab"), ("bdab", "ab"), ("cabwefgewcwaefgcf", "cae"), ("aa", "aa")],
  ref=ref_minwindow, tags=["string", "hash-table", "sliding-window"],
  time_complexity="O(n + m)", space_complexity="O(n + m)",
  hints=["Expand the right edge until the window contains all of t's characters.", "Track how many required characters are still missing.", "Once valid, shrink from the left as far as possible, recording the smallest valid window."])

def ref_slidemax(nums, k):
    dq = deque()
    out = []
    for i, x in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] < x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out

q(id="sliding-window-maximum", title="Sliding Window Maximum", difficulty="Hard",
  description="You are given an array of integers nums and an integer k. There is a sliding window of size k moving from left to right over the array. At each position, return the maximum value inside the current window. Return the results as an array.",
  examples=[("nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3", "[3, 3, 5, 5, 6, 7]", "Maximum of each window of size 3."),
            ("nums = [1], k = 1", "[1]", "A single window.")],
  constraints=["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4", "1 <= k <= nums.length"],
  method_name="maxSlidingWindow", return_type="int[]", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([1, 3, -1, -3, 5, 3, 6, 7], 3), ([1], 1)],
  hidden_args=[([9, 11], 2), ([4, -2], 2), ([1, 3, 1, 2, 0, 5], 3), ([7, 2, 4], 1), ([-7, -8, 7, 5, 7, 1, 6, 0], 4), ([1, -1], 1)],
  ref=ref_slidemax, tags=["array", "sliding-window", "deque", "heap"],
  time_complexity="O(n)", space_complexity="O(k)",
  hints=["A brute-force scan of each window is O(n*k).", "Maintain a deque of candidate indices in decreasing value order.", "Drop indices that fall out of the window from the front; the front always holds the current maximum."])

def ref_findsubstr(s, words):
    if not words:
        return []
    wlen = len(words[0])
    nwords = len(words)
    total = wlen * nwords
    need = Counter(words)
    res = []
    for off in range(wlen):
        win = Counter()
        l = off
        for r in range(off, len(s) - wlen + 1, wlen):
            w = s[r:r + wlen]
            win[w] += 1
            while win[w] > need.get(w, 0):
                win[s[l:l + wlen]] -= 1
                l += wlen
            if r - l + wlen == total:
                res.append(l)
    return sorted(res)

q(id="substring-with-concatenation-of-all-words", title="Substring with Concatenation of All Words", difficulty="Hard",
  description="You are given a string s and an array of strings words. All the strings in words are of the same length. A concatenated substring is a substring of s formed by concatenating each word in words exactly once, in any order, with no intervening characters. Return all starting indices of concatenated substrings in s, sorted in ascending order.",
  examples=[('s = "barfoothefoobarman", words = ["foo", "bar"]', "[0, 9]", '"barfoo" at 0 and "foobar" at 9.'),
            ('s = "wordgoodgoodgoodbestword", words = ["word", "good", "best", "word"]', "[]", "No concatenation of all words appears."),
            ('s = "barfoofoobarthefoobarman", words = ["bar", "foo", "the"]', "[6, 9, 12]", 'Three valid windows.')],
  constraints=["1 <= s.length <= 10^4", "1 <= words.length <= 5000", "1 <= words[i].length <= 30", "All words have the same length."],
  method_name="findSubstring", return_type="List<Integer>", params=[("s", "String"), ("words", "String[]")],
  sample_args=[("barfoothefoobarman", ["foo", "bar"]), ("barfoofoobarthefoobarman", ["bar", "foo", "the"])],
  hidden_args=[("a", ["a"]), ("aaa", ["a", "a"]), ("lingmindraboofooowingdingbarrwingmonkeypoundcake", ["fooo", "barr", "wing", "ding", "wing"]), ("ababaab", ["ab", "ba", "ab"]), ("mississippi", ["is"]), ("abcd", ["ab", "cd"])],
  ref=ref_findsubstr, tags=["string", "hash-table", "sliding-window"],
  time_complexity="O(n * w)", space_complexity="O(n)",
  hints=["All words share one length L; any valid window has length L * words.length.", "Run a sliding window over word-aligned chunks for each offset 0..L-1.", "Compare word-frequency maps between the window and the target multiset."])

def ref_kflips(nums, k):
    n = len(nums)
    diff = [0] * (n + 1)
    flips = cur = ans = 0
    for i in range(n):
        cur += diff[i]
        if (nums[i] + cur) % 2 == 0:
            if i + k > n:
                return -1
            ans += 1
            cur += 1
            diff[i + k] -= 1
    return ans

q(id="minimum-number-of-k-consecutive-bit-flips", title="Minimum Number of K Consecutive Bit Flips", difficulty="Hard",
  description="You are given a binary array nums and an integer k. A k-bit flip chooses a subarray of length k and flips every bit in it (0 becomes 1, 1 becomes 0). Return the minimum number of k-bit flips required so that every bit in the array is 1. If it is not possible, return -1.",
  examples=[("nums = [0, 1, 0], k = 1", "2", "Flip each 0 individually."),
            ("nums = [1, 1, 0], k = 2", "-1", "Flipping [1, 1] gives [0, 0, 0]; flipping [1, 0] gives [1, 0, 1]; impossible."),
            ("nums = [0, 0, 0, 1, 0, 1, 1, 0], k = 3", "3", "Three flips suffice.")],
  constraints=["1 <= nums.length <= 10^5", "1 <= k <= nums.length"],
  method_name="minKBitFlips", return_type="int", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([0, 1, 0], 1), ([1, 1, 0], 2)],
  hidden_args=[([0, 0, 0, 1, 0, 1, 1, 0], 3), ([1, 1, 1], 2), ([0, 0, 0], 1), ([0, 1, 1, 1], 2), ([1, 0, 0], 2), ([0, 0, 1, 0], 2)],
  ref=ref_kflips, tags=["array", "sliding-window", "greedy", "difference-array"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Greedy works: scan left to right, and whenever the current bit is effectively 0, flip starting here.", "An earlier decision never needs revisiting because no later flip can fix position i.", "Track active flips with a difference array (or a queue of flip end positions) for O(n) time."])

write_bank(P, Q)
