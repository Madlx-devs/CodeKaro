"""Hashing pattern: 20 questions (8 Easy, 8 Medium, 4 Hard)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genlib import make_question, write_bank
from collections import Counter, defaultdict
from math import gcd

P = "hashing"
Q = []

def q(**kw):
    Q.append(make_question(pattern=P, **kw))

# ---------------- Easy ----------------

def ref_two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i

q(id="two-sum", title="Two Sum", difficulty="Easy",
  description="Given an array of integers nums and an integer target, return the indices of the two numbers that add up to target. Each input has exactly one solution, and you may not use the same element twice. The answer can be returned in any order, but this platform checks the pair your algorithm finds by scanning left to right.",
  examples=[("nums = [2, 7, 11, 15], target = 9", "[0, 1]", "nums[0] + nums[1] = 2 + 7 = 9."),
            ("nums = [3, 2, 4], target = 6", "[1, 2]", "nums[1] + nums[2] = 2 + 4 = 6."),
            ("nums = [3, 3], target = 6", "[0, 1]", "nums[0] + nums[1] = 3 + 3 = 6.")],
  constraints=["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "-10^9 <= target <= 10^9", "Exactly one valid answer exists."],
  method_name="twoSum", return_type="int[]", params=[("nums", "int[]"), ("target", "int")],
  sample_args=[([2, 7, 11, 15], 9), ([3, 2, 4], 6)],
  hidden_args=[([3, 3], 6), ([-1, -2, -3, -4, -5], -8), ([0, 4, 3, 0], 0), ([2, 5, 5, 11], 10), ([1, 2, 3, 4, 5], 9), ([-3, 4, 3, 90], 0)],
  ref=ref_two_sum, tags=["array", "hash-table"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["A brute-force double loop checks every pair but costs O(n^2) time.", "As you scan the array, store each value you have seen in a hash map.", "For the current value x, you need target - x: check whether that complement is already in the map."])

def ref_contains_dup(nums):
    return len(set(nums)) != len(nums)

q(id="contains-duplicate", title="Contains Duplicate", difficulty="Easy",
  description="Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.",
  examples=[("nums = [1, 2, 3, 1]", "true", "The value 1 appears twice."),
            ("nums = [1, 2, 3, 4]", "false", "All elements are distinct."),
            ("nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]", "true", "Several values repeat.")],
  constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
  method_name="containsDuplicate", return_type="boolean", params=[("nums", "int[]")],
  sample_args=[([1, 2, 3, 1],), ([1, 2, 3, 4],)],
  hidden_args=[([1, 1, 1, 3, 3, 4, 3, 2, 4, 2],), ([5],), ([-1, -2, -3, -1],), ([0, 0],), ([1, 2, 3, 4, 5, 6],), ([7, 7],)],
  ref=ref_contains_dup, tags=["array", "hash-table"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Sorting the array first makes duplicates sit next to each other.", "A hash set remembers every value seen so far in O(1) average time.", "If the value is already in the set when you visit it, you can return true immediately."])

def ref_anagram(s, t):
    return Counter(s) == Counter(t)

q(id="valid-anagram", title="Valid Anagram", difficulty="Easy",
  description="Given two strings s and t, return true if t is an anagram of s, and false otherwise. An anagram is a word formed by rearranging the letters of another word, using all the original letters exactly once.",
  examples=[('s = "anagram", t = "nagaram"', "true", '"nagaram" is a rearrangement of "anagram".'),
            ('s = "rat", t = "car"', "false", 'The letter counts differ.'),
            ('s = "a", t = "ab"', "false", "Different lengths cannot be anagrams.")],
  constraints=["1 <= s.length, t.length <= 5 * 10^4", "s and t consist of lowercase English letters."],
  method_name="isAnagram", return_type="boolean", params=[("s", "String"), ("t", "String")],
  sample_args=[("anagram", "nagaram"), ("rat", "car")],
  hidden_args=[("a", "ab"), ("listen", "silent"), ("abc", "abcd"), ("aacc", "ccac"), ("anagram", "margana"), ("ab", "ba")],
  ref=ref_anagram, tags=["string", "hash-table", "sorting"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["If the strings have different lengths, the answer is immediately false.", "Count how many times each letter appears in both strings.", "A single frequency array of size 26 (or one hash map) is enough; the counts must match exactly."])

def ref_longest_pal(s):
    freq = Counter(s)
    length = sum(v // 2 * 2 for v in freq.values())
    if length < len(s):
        length += 1
    return length

q(id="longest-palindrome", title="Longest Palindrome", difficulty="Easy",
  description="Given a string s which consists of lowercase and/or uppercase English letters, return the length of the longest palindrome that can be built with those letters. Letters are case sensitive ('A' and 'a' are different).",
  examples=[('s = "abccccdd"', "7", 'One longest palindrome is "dccaccd": pairs cc, cc, dd plus one single "a".'),
            ('s = "a"', "1", "A single character is a palindrome.")],
  constraints=["1 <= s.length <= 2000", "s consists of lowercase and/or uppercase English letters only."],
  method_name="longestPalindrome", return_type="int", params=[("s", "String")],
  sample_args=[("abccccdd",), ("a",)],
  hidden_args=[("bb",), ("abc",), ("aabbcc",), ("bananas",), ("ccc",), ("Aa",)],
  ref=ref_longest_pal, tags=["string", "hash-table", "counting", "greedy"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Count the frequency of each character first.", "Every pair of equal characters can sit symmetrically on both sides of the palindrome.", "At most one character with an odd count can occupy the center."])

def ref_ransom(ransomNote, magazine):
    need, have = Counter(ransomNote), Counter(magazine)
    return all(have[c] >= n for c, n in need.items())

q(id="ransom-note", title="Ransom Note", difficulty="Easy",
  description='Given two strings ransomNote and magazine, return true if ransomNote can be constructed by using the letters from magazine, and false otherwise. Each letter in magazine can only be used once in ransomNote.',
  examples=[('ransomNote = "a", magazine = "b"', "false", 'magazine has no "a".'),
            ('ransomNote = "aa", magazine = "ab"', "false", 'Only one "a" is available.'),
            ('ransomNote = "aa", magazine = "aab"', "true", 'Both "a"s are available.')],
  constraints=["1 <= ransomNote.length, magazine.length <= 10^5", "Both strings consist of lowercase English letters."],
  method_name="canConstruct", return_type="boolean", params=[("ransomNote", "String"), ("magazine", "String")],
  sample_args=[("a", "b"), ("aa", "aab")],
  hidden_args=[("a", "a"), ("abc", "cba"), ("aab", "baa"), ("hello", "helloworld"), ("zzz", "zz"), ("abc", "def")],
  ref=ref_ransom, tags=["string", "hash-table", "counting"],
  time_complexity="O(n + m)", space_complexity="O(1)",
  hints=["Count the letters available in magazine first.", "Then walk through ransomNote, consuming one count per letter.", "If any letter runs out, return false; a size-26 frequency array is enough."])

def ref_majority(nums):
    cand = cnt = 0
    for x in nums:
        if cnt == 0:
            cand, cnt = x, 1
        elif x == cand:
            cnt += 1
        else:
            cnt -= 1
    return cand

q(id="majority-element", title="Majority Element", difficulty="Easy",
  description="Given an array nums of size n, return the majority element: the element that appears more than n / 2 times. You may assume the majority element always exists in the array. Aim for linear time and O(1) space.",
  examples=[("nums = [3, 2, 3]", "3", "3 appears 2 out of 3 times."),
            ("nums = [2, 2, 1, 1, 1, 2, 2]", "2", "2 appears 4 out of 7 times.")],
  constraints=["1 <= nums.length <= 5 * 10^4", "-10^9 <= nums[i] <= 10^9", "The majority element always exists."],
  method_name="majorityElement", return_type="int", params=[("nums", "int[]")],
  sample_args=[([3, 2, 3],), ([2, 2, 1, 1, 1, 2, 2],)],
  hidden_args=[([1],), ([6, 5, 5],), ([-1, -1, 2],), ([1, 2, 3, 4, 5, 5, 5, 5],), ([0, 0, 0, 1, 1],), ([9, 9, 9, 1, 2],)],
  ref=ref_majority, tags=["array", "hash-table", "divide-and-conquer", "voting"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["A hash map of frequencies finds it in O(n) time and O(n) space.", "The Boyer-Moore voting algorithm keeps one candidate and a counter.", "Equal values increment the counter, different values decrement it; the survivor is the majority."])

def ref_happy(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(d) ** 2 for d in str(n))
    return n == 1

q(id="happy-number", title="Happy Number", difficulty="Easy",
  description="A happy number is defined by this process: starting with any positive integer, replace the number by the sum of the squares of its digits, and repeat until the number equals 1 (it is happy) or it loops endlessly in a cycle that does not include 1 (it is not happy). Return true if n is happy.",
  examples=[("n = 19", "true", "19 -> 82 -> 68 -> 100 -> 1."),
            ("n = 2", "false", "2 enters the cycle 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4.")],
  constraints=["1 <= n <= 2^31 - 1"],
  method_name="isHappy", return_type="boolean", params=[("n", "int")],
  sample_args=[(19,), (2,)],
  hidden_args=[(1,), (7,), (4,), (100,), (13,), (20,)],
  ref=ref_happy, tags=["hash-table", "math", "cycle-detection"],
  time_complexity="O(log n)", space_complexity="O(log n)",
  hints=["Simulate the process step by step, computing the digit-square sum.", "You need to detect when a value repeats: that means a cycle.", "Store every value seen in a hash set; stop when you reach 1 or revisit a value."])

def ref_word_pattern(pattern, s):
    words = s.split(" ")
    if len(pattern) != len(words):
        return False
    p2w, w2p = {}, {}
    for p, w in zip(pattern, words):
        if p2w.get(p, w) != w or w2p.get(w, p) != p:
            return False
        p2w[p] = w
        w2p[w] = p
    return True

q(id="word-pattern", title="Word Pattern", difficulty="Easy",
  description='Given a pattern string and a string s of words separated by single spaces, return true if s follows the same pattern. "Follows" means there is a bijection between each letter in pattern and each non-empty word in s: each letter maps to exactly one word, and each word maps to exactly one letter.',
  examples=[('pattern = "abba", s = "dog cat cat dog"', "true", "a -> dog, b -> cat consistently."),
            ('pattern = "abba", s = "dog cat cat fish"', "false", "The last word breaks the mapping."),
            ('pattern = "aaaa", s = "dog cat cat dog"', "false", '"a" would need to map to two words.')],
  constraints=["1 <= pattern.length <= 300", "pattern contains only lowercase English letters.", "1 <= s.length <= 3000", "s contains only lowercase English letters and spaces."],
  method_name="wordPattern", return_type="boolean", params=[("pattern", "String"), ("s", "String")],
  sample_args=[("abba", "dog cat cat dog"), ("abba", "dog cat cat fish")],
  hidden_args=[("abc", "b c a"), ("abba", "dog dog dog dog"), ("a", "x"), ("ab", "x y"), ("aa", "x x"), ("abca", "dog cat fish dog")],
  ref=ref_word_pattern, tags=["string", "hash-table"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Split s into words and check the counts match the pattern length first.", "You need mappings in both directions: letter -> word and word -> letter.", "Two hash maps (or one map plus a set of used words) enforce the bijection."])

# ---------------- Medium ----------------

def ref_group_anagrams(strs):
    groups = defaultdict(list)
    for w in strs:
        groups["".join(sorted(w))].append(w)
    out = ["|".join(sorted(g)) for g in groups.values()]
    out.sort()
    return out

q(id="group-anagrams", title="Group Anagrams", difficulty="Medium",
  description="Given an array of strings strs (lowercase English letters only, so '|' never appears in a word), group the anagrams together. Return the groups as an array of strings: within each group, sort the words alphabetically and join them with '|'; then sort the group strings lexicographically, so the output is deterministic.",
  examples=[('strs = ["eat", "tea", "tan", "ate", "nat", "bat"]', '[ate|eat|tea, bat, nat|tan]', "Anagrams share the same sorted-letter key; groups are joined with '|' and sorted."),
            ('strs = ["a"]', '[a]', "A single string forms one group.")],
  constraints=["1 <= strs.length <= 10^4", "0 <= strs[i].length <= 100", "strs[i] consists of lowercase English letters."],
  method_name="groupAnagrams", return_type="List<String>", params=[("strs", "String[]")],
  sample_args=[(["eat", "tea", "tan", "ate", "nat", "bat"],), (["a", "b", "a"],)],
  hidden_args=[(["ab", "ba", "abc", "cba"],), (["d", "c", "b", "a"],), (["listen", "silent", "enlist"],), (["aab", "aba", "baa", "abc"],), (["abc", "def", "cab"],), (["a"],)],
  ref=ref_group_anagrams, tags=["array", "string", "hash-table", "sorting"],
  time_complexity="O(n * k log k)", space_complexity="O(n * k)",
  hints=["Anagrams become identical once their letters are sorted.", "Use the sorted-letters string as a hash map key.", "Append each word to the list stored under its key, then sort and join each group with '|'."])

def ref_longest_consec(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 not in s:
            y, cur = x, 1
            while y + 1 in s:
                y, cur = y + 1, cur + 1
            best = max(best, cur)
    return best

q(id="longest-consecutive-sequence", title="Longest Consecutive Sequence", difficulty="Medium",
  description="Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence. Your algorithm must run in O(n) time.",
  examples=[("nums = [100, 4, 200, 1, 3, 2]", "4", "The sequence [1, 2, 3, 4] has length 4."),
            ("nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]", "9", "The sequence [0..8] has length 9.")],
  constraints=["0 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
  method_name="longestConsecutive", return_type="int", params=[("nums", "int[]")],
  sample_args=[([100, 4, 200, 1, 3, 2],), ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],)],
  hidden_args=[([],), ([1],), ([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6],), ([1, 2, 0, 1],), ([-2, -1, 0, 1, 2],), ([10, 5, 12, 3],)],
  ref=ref_longest_consec, tags=["array", "hash-table", "union-find"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Sorting gives O(n log n); the O(n) requirement rules that out.", "Put all numbers in a hash set for O(1) lookups.", "Only start counting from numbers with no predecessor (x - 1 not in the set); each number is visited at most twice."])

def ref_subarray_sum(nums, k):
    pref, count = 0, 0
    freq = {0: 1}
    for x in nums:
        pref += x
        count += freq.get(pref - k, 0)
        freq[pref] = freq.get(pref, 0) + 1
    return count

q(id="subarray-sum-equals-k", title="Subarray Sum Equals K", difficulty="Medium",
  description="Given an array of integers nums and an integer k, return the total number of continuous subarrays whose sum equals k.",
  examples=[("nums = [1, 1, 1], k = 2", "2", "Subarrays [1, 1] at indices [0, 1] and [1, 2]."),
            ("nums = [1, 2, 3], k = 3", "2", "Subarrays [1, 2] and [3].")],
  constraints=["1 <= nums.length <= 2 * 10^4", "-1000 <= nums[i] <= 1000", "-10^7 <= k <= 10^7"],
  method_name="subarraySum", return_type="int", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([1, 1, 1], 2), ([1, 2, 3], 3)],
  hidden_args=[([1, -1, 0], 0), ([0, 0, 0], 0), ([3, 4, 7, 2, -3, 1, 4, 2], 7), ([1], 1), ([-1, -1, 1], 0), ([2, 2, 2], 4)],
  ref=ref_subarray_sum, tags=["array", "hash-table", "prefix-sum"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["A subarray sum nums[i..j] equals prefix[j] - prefix[i - 1].", "While scanning, keep prefix sums and their frequencies in a hash map.", "For the current prefix P, every earlier prefix equal to P - k closes a valid subarray."])

def ref_topk(nums, k):
    freq = Counter(nums)
    ranked = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    return [v for v, _ in ranked[:k]]

q(id="top-k-frequent-elements", title="Top K Frequent Elements", difficulty="Medium",
  description="Given an integer array nums and an integer k, return the k most frequent elements. Order the result by decreasing frequency; break ties by smaller value first, so the output is deterministic.",
  examples=[("nums = [1, 1, 1, 2, 2, 3], k = 2", "[1, 2]", "1 appears 3 times, 2 appears 2 times."),
            ("nums = [1], k = 1", "[1]", "Only one element.")],
  constraints=["1 <= k <= number of unique elements", "1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
  method_name="topKFrequent", return_type="int[]", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([1, 1, 1, 2, 2, 3], 2), ([1], 1)],
  hidden_args=[([4, 1, -1, 2, -1, 2, 3], 2), ([5, 5, 5, 5, 2, 2, 1], 1), ([1, 2, 3, 4], 4), ([7, 7, 8, 8, 8, 9], 2), ([-1, -1, -2, -2, -3], 2), ([1, 1, 2, 2, 3, 3], 3)],
  ref=ref_topk, tags=["array", "hash-table", "sorting", "heap"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["First count frequencies with a hash map.", "You need the k entries with the largest counts.", "Sorting the entries by (-count, value) is simple; a min-heap of size k is the classic O(n log k) approach."])

def ref_sudoku(board):
    # board: list of 9 strings, '.' or digit
    for i in range(9):
        row = [c for c in board[i] if c != "."]
        if len(set(row)) != len(row):
            return False
        col = [board[r][i] for r in range(9) if board[r][i] != "."]
        if len(set(col)) != len(col):
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            cells = [board[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3) if board[r][c] != "."]
            if len(set(cells)) != len(cells):
                return False
    return True

VALID_BOARD = ["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "....8..79"]
ROW_BAD = ["533.7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "....8..79"]
COL_BAD = ["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "5...8..79"]
BOX_BAD = ["53..7....", "65.195...", ".98....6.", "8...6...3", "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "....8..79"]
EMPTY_BOARD = ["........." for _ in range(9)]

q(id="valid-sudoku", title="Valid Sudoku", difficulty="Medium",
  description="Determine if a 9x9 Sudoku board is valid. The board is given as an array of 9 strings, each 9 characters long, containing digits '1'-'9' or '.' for empty cells. Only the filled cells need to be valid: each row, each column, and each of the nine 3x3 sub-boxes must contain no repeated digits.",
  examples=[("board = valid puzzle rows", "true", "No row, column, or box contains a repeated digit."),
            ("board with two 5s in row 0", "false", "Row 0 contains the digit 5 twice.")],
  constraints=["board.length == 9", "Each row has length 9.", "Each cell is a digit '1'-'9' or '.'."],
  method_name="isValidSudoku", return_type="boolean", params=[("board", "String[]")],
  sample_args=[(VALID_BOARD,), (ROW_BAD,)],
  hidden_args=[(COL_BAD,), (BOX_BAD,), (EMPTY_BOARD,), (["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "....8..7."],), (["..5......", ".........", ".........", ".........", ".........", ".........", ".........", ".........", ".....5..."],)],
  ref=ref_sudoku, tags=["array", "hash-table", "matrix"],
  time_complexity="O(1)", space_complexity="O(1)",
  hints=["Check rows, columns, and 3x3 boxes as three separate passes.", "A hash set per row/column/box detects repeats; ignore '.' cells.", "Encode a box index as (r / 3) * 3 + (c / 3) to share one set per box."])

def ref_4sum2(a, b, c, d):
    ab = Counter(x + y for x in a for y in b)
    return sum(ab[-(x + y)] for x in c for y in d)

q(id="4sum-ii", title="4Sum II", difficulty="Medium",
  description="Given four integer arrays nums1, nums2, nums3, nums4 of length n, return the number of tuples (i, j, k, l) such that nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0.",
  examples=[("nums1 = [1, 2], nums2 = [-2, -1], nums3 = [-1, 2], nums4 = [0, 2]", "2", "Tuples (0, 0, 0, 1) and (1, 1, 0, 0)."),
            ("nums1 = [0], nums2 = [0], nums3 = [0], nums4 = [0]", "1", "The single tuple (0, 0, 0, 0) sums to 0.")],
  constraints=["n == nums1.length == nums2.length == nums3.length == nums4.length", "1 <= n <= 200", "-2^28 <= nums[i] <= 2^28"],
  method_name="fourSumCount", return_type="int", params=[("nums1", "int[]"), ("nums2", "int[]"), ("nums3", "int[]"), ("nums4", "int[]")],
  sample_args=[([1, 2], [-2, -1], [-1, 2], [0, 2]), ([0], [0], [0], [0])],
  hidden_args=[([1, 1], [1, 1], [1, 1], [1, 1]), ([-1, -1], [-1, 1], [-1, 1], [1, -1]), ([2, 2], [2, 2], [2, 2], [2, 2]), ([1], [-1], [0], [0]), ([0, 1], [0, 1], [0, -1], [0, -1])],
  ref=ref_4sum2, tags=["array", "hash-table"],
  time_complexity="O(n^2)", space_complexity="O(n^2)",
  hints=["Brute force over all four arrays is O(n^4).", "Split into two pairs: store all nums1[i] + nums2[j] sums in a hash map.", "For each nums3[k] + nums4[l], look up how many pair-sums equal its negation."])

def ref_pairs60(time):
    freq = Counter(t % 60 for t in time)
    total = freq[0] * (freq[0] - 1) // 2 + freq[30] * (freq[30] - 1) // 2
    for r in range(1, 30):
        total += freq[r] * freq[60 - r]
    return total

q(id="pairs-of-songs-divisible-by-60", title="Pairs of Songs With Total Durations Divisible by 60", difficulty="Medium",
  description="You are given a list of song durations in seconds. Return the number of pairs of songs (i, j) with i < j such that (time[i] + time[j]) is divisible by 60.",
  examples=[('time = [30, 20, 150, 100, 40]', "3", "Valid pairs are (30, 150), (20, 100) and (20, 40); their sums 180, 120 and 60 are all divisible by 60."),
            ('time = [60, 60, 60]', "3", "Every pair sums to 120.")],
  constraints=["1 <= time.length <= 6 * 10^4", "1 <= time[i] <= 500"],
  method_name="numPairsDivisibleBy60", return_type="int", params=[("time", "int[]")],
  sample_args=[([30, 20, 150, 100, 40],), ([60, 60, 60],)],
  hidden_args=[([15, 45, 15, 45],), ([10, 20, 30],), ([60],), ([20, 40, 20, 40, 20],), ([5, 55, 5, 55],), ([30, 30, 30, 30],)],
  ref=ref_pairs60, tags=["array", "hash-table", "counting"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Only time[i] % 60 matters for divisibility of the sum.", "For remainder r you need remainder (60 - r) % 60.", "Count remainders in a size-60 frequency array, then combine complementary pairs carefully (0 with 0, 30 with 30)."])

def ref_lhs(nums):
    freq = Counter(nums)
    best = 0
    for x, c in freq.items():
        if x + 1 in freq:
            best = max(best, c + freq[x + 1])
    return best

q(id="longest-harmonious-subsequence", title="Longest Harmonious Subsequence", difficulty="Medium",
  description="A harmonious array is an array where the difference between its maximum value and its minimum value is exactly 1. Given an integer array nums, return the length of the longest harmonious subsequence (not necessarily contiguous) of nums.",
  examples=[("nums = [1, 3, 2, 2, 5, 2, 3, 7]", "5", "The subsequence [3, 2, 2, 2, 3] uses values 2 and 3."),
            ("nums = [1, 2, 3, 4]", "2", "Any adjacent pair like [1, 2] works."),
            ("nums = [1, 1, 1, 1]", "0", "No two values differ by exactly 1.")],
  constraints=["1 <= nums.length <= 2 * 10^4", "-10^9 <= nums[i] <= 10^9"],
  method_name="findLHS", return_type="int", params=[("nums", "int[]")],
  sample_args=[([1, 3, 2, 2, 5, 2, 3, 7],), ([1, 2, 3, 4],)],
  hidden_args=[([1, 1, 1, 1],), ([1, 2, 2, 1],), ([1, 3, 5, 7, 9, 11],), ([2, 2, 2, 3, 3],), ([-1, 0, -1, 0, -1, 0, -1],), ([1, 4, 1, 3, 1, -14, 1, -13],)],
  ref=ref_lhs, tags=["array", "hash-table", "counting", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Since order does not matter, only the frequencies of each value matter.", "A harmonious subsequence uses exactly two values that differ by 1.", "Count frequencies in a hash map, then for each value x add freq[x] + freq[x + 1] when both exist."])

# ---------------- Hard ----------------

def ref_first_missing(nums):
    n = len(nums)
    a = [x for x in nums]
    for i in range(n):
        while 1 <= a[i] <= n and a[a[i] - 1] != a[i]:
            j = a[i] - 1
            a[i], a[j] = a[j], a[i]
    for i in range(n):
        if a[i] != i + 1:
            return i + 1
    return n + 1

q(id="first-missing-positive", title="First Missing Positive", difficulty="Hard",
  description="Given an unsorted integer array nums, return the smallest missing positive integer. You must implement an algorithm that runs in O(n) time and uses O(1) extra space.",
  examples=[("nums = [1, 2, 0]", "1", "1 is missing? No: 1 and 2 present, 0 ignored; smallest missing positive is 3? Actually 1,2 present so answer is 3. Wait: positives present are 1, 2; missing is 3."),
            ("nums = [3, 4, -1, 1]", "2", "1 is present, 2 is missing."),
            ("nums = [7, 8, 9, 11, 12]", "1", "1 is missing.")],
  constraints=["1 <= nums.length <= 10^5", "-2^31 <= nums[i] <= 2^31 - 1"],
  method_name="firstMissingPositive", return_type="int", params=[("nums", "int[]")],
  sample_args=[([1, 2, 0],), ([3, 4, -1, 1],)],
  hidden_args=[([7, 8, 9, 11, 12],), ([1],), ([2, 1],), ([1, 2, 3, 4, 5],), ([2, 2, 2],), ([-5],)],
  ref=ref_first_missing, tags=["array", "hash-table", "in-place"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["The answer is always between 1 and n + 1.", "Use the array itself as a hash table: value v belongs at index v - 1.", "Swap each valid value into its home slot, then scan for the first index i where nums[i] != i + 1."])

# fix the first example explanation (was garbled)
Q[-1]["examples"][0] = ("nums = [1, 2, 0]", "3", "1 and 2 are present; 0 is ignored; the smallest missing positive is 3.")

def ref_max_points(points):
    n = len(points)
    if n <= 2:
        return n
    best = 0
    for i in range(n):
        slopes = Counter()
        dup = 1
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            dx, dy = x2 - x1, y2 - y1
            if dx == 0 and dy == 0:
                dup += 1
                continue
            g = gcd(dx, dy)
            dx //= g
            dy //= g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            slopes[(dx, dy)] += 1
        cur = dup + (max(slopes.values()) if slopes else 0)
        best = max(best, cur)
    return best

q(id="max-points-on-a-line", title="Max Points on a Line", difficulty="Hard",
  description="Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane, return the maximum number of points that lie on the same straight line.",
  examples=[("points = [[1, 1], [2, 2], [3, 3]]", "3", "All three are collinear."),
            ("points = [[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]", "4", "Four points lie on one line.")],
  constraints=["1 <= points.length <= 300", "-10^4 <= xi, yi <= 10^4", "All points are unique except duplicates are allowed in tests."],
  method_name="maxPoints", return_type="int", params=[("points", "int[][]")],
  sample_args=[([[1, 1], [2, 2], [3, 3]],), ([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]],)],
  hidden_args=[([[1, 1]],), ([[1, 1], [1, 1], [1, 1]],), ([[0, 0], [1, 1], [0, 0]],), ([[1, 1], [2, 2], [3, 3], [1, 2]],), ([[-1, -1], [0, 0], [1, 1], [2, 2]],), ([[3, 1], [12, 3], [3, 1], [-6, -1]],)],
  ref=ref_max_points, tags=["array", "hash-table", "math", "geometry"],
  time_complexity="O(n^2)", space_complexity="O(n)",
  hints=["Fix one anchor point and consider slopes to every other point.", "Equal slopes from the same anchor mean collinear points; count duplicates separately.", "Normalize each slope as a reduced (dx, dy) pair with gcd so floating point never appears; use a hash map keyed by the pair."])

def ref_longest_k(s, k):
    if k <= 1:
        return len(s)
    if len(s) < k:
        return 0
    freq = Counter(s)
    for i, ch in enumerate(s):
        if freq[ch] < k:
            return max(ref_longest_k(s[:i], k), ref_longest_k(s[i + 1:], k))
    return len(s)

q(id="longest-substring-with-at-least-k-repeating-characters", title="Longest Substring With At Least K Repeating Characters", difficulty="Hard",
  description="Given a string s and an integer k, return the length of the longest substring of s such that the frequency of each character in this substring is greater than or equal to k.",
  examples=[('s = "aaabb", k = 3', "3", 'The longest valid substring is "aaa".'),
            ('s = "ababbc", k = 2', "5", 'The longest valid substring is "ababb".')],
  constraints=["1 <= s.length <= 10^4", "s consists of only lowercase English letters.", "1 <= k <= 10^5"],
  method_name="longestSubstring", return_type="int", params=[("s", "String"), ("k", "int")],
  sample_args=[("aaabb", 3), ("ababbc", 2)],
  hidden_args=[("abcd", 2), ("aaaa", 1), ("ababacb", 3), ("bbaaacbd", 3), ("aaabbb", 3), ("ababab", 2)],
  ref=ref_longest_k, tags=["string", "hash-table", "divide-and-conquer", "sliding-window"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Any character appearing fewer than k times in the whole string can never be part of a valid answer.", "Split the string at those invalid characters and solve each piece recursively.", "This divide-and-conquer uses frequency maps at each level; memoize nothing, the splits shrink fast."])

def ref_echo(text):
    n = len(text)
    seen = set()
    for l in range(1, n // 2 + 1):
        for i in range(n - 2 * l + 1):
            sub = text[i:i + 2 * l]
            if sub[:l] == sub[l:]:
                seen.add(sub)
    return len(seen)

q(id="distinct-echo-substrings", title="Distinct Echo Substrings", difficulty="Hard",
  description='Return the number of distinct echo substrings in the given text. An echo substring has even length 2 * k and consists of two identical halves: the first k characters equal the last k characters. For example, "abcabc" is an echo substring ("abc" + "abc"). Count each distinct echo substring only once.',
  examples=[('text = "abcabcabc"', "3", 'The echo substrings are "abcabc", "bcabca" and "cabcab".'),
            ('text = "aaaa"', "2", 'The distinct echo substrings are "aa" and "aaaa".')],
  constraints=["1 <= text.length <= 2000", "text consists of lowercase English letters."],
  method_name="distinctEchoSubstrings", return_type="int", params=[("text", "String")],
  sample_args=[("abcabcabc",), ("aaaa",)],
  hidden_args=[("aaaa",), ("abab",), ("leetcodeleetcode",), ("a",), ("ababab",), ("abcabc",)],
  ref=ref_echo, tags=["string", "hash-table", "rolling-hash"],
  time_complexity="O(n^2)", space_complexity="O(n^2)",
  hints=["An echo substring is determined by its start index and its half-length l.", "For each start and each l, compare the two halves directly or with a rolling hash.", "Deduplicate with a hash set of the substring (or its hash pair) before counting."])

write_bank(P, Q)