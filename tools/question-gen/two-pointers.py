"""Two Pointers pattern: 20 questions (8 Easy, 8 Medium, 4 Hard)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genlib import make_question, write_bank
from collections import Counter

P = "two-pointers"
Q = []

def q(**kw):
    Q.append(make_question(pattern=P, **kw))

# ---------------- Easy ----------------

def ref_two_sum2(numbers, target):
    l, r = 0, len(numbers) - 1
    while l < r:
        s = numbers[l] + numbers[r]
        if s == target:
            return [l + 1, r + 1]
        if s < target:
            l += 1
        else:
            r -= 1

q(id="two-sum-ii-input-array-is-sorted", title="Two Sum II - Input Array Is Sorted", difficulty="Easy",
  description="Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Return the indices of the two numbers (1-indexed) as an integer array [index1, index2] with index1 < index2. Each input has exactly one solution.",
  examples=[("numbers = [2, 7, 11, 15], target = 9", "[1, 2]", "numbers[0] + numbers[1] = 2 + 7 = 9."),
            ("numbers = [2, 3, 4], target = 6", "[1, 3]", "numbers[0] + numbers[2] = 2 + 4 = 6."),
            ("numbers = [-1, 0], target = -1", "[1, 2]", "numbers[0] + numbers[1] = -1 + 0 = -1.")],
  constraints=["2 <= numbers.length <= 3 * 10^4", "-1000 <= numbers[i] <= 1000", "numbers is sorted in non-decreasing order.", "Exactly one valid answer exists."],
  method_name="twoSum", return_type="int[]", params=[("numbers", "int[]"), ("target", "int")],
  sample_args=[([2, 7, 11, 15], 9), ([2, 3, 4], 6)],
  hidden_args=[([-1, 0], -1), ([1, 2, 3, 4, 5], 9), ([5, 25, 75], 100), ([0, 0, 3, 4], 0), ([1, 2], 3), ([-5, -3, 0, 2, 4], -1)],
  ref=ref_two_sum2, tags=["array", "two-pointers", "binary-search"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Because the array is sorted, you can do better than a hash map.", "Place one pointer at each end of the array.", "If the sum is too small move the left pointer right; if too large move the right pointer left."])

def ref_pal(s):
    t = "".join(c.lower() for c in s if c.isalnum())
    return t == t[::-1]

q(id="valid-palindrome", title="Valid Palindrome", difficulty="Easy",
  description="A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Given a string s, return true if it is a palindrome, or false otherwise.",
  examples=[('s = "A man, a plan, a canal: Panama"', "true", 'After cleaning: "amanaplanacanalpanama".'),
            ('s = "race a car"', "false", 'After cleaning: "raceacar" is not a palindrome.'),
            ('s = " "', "true", 'After cleaning: "" reads the same both ways.')],
  constraints=["1 <= s.length <= 2 * 10^5", "s consists of printable ASCII characters."],
  method_name="isPalindrome", return_type="boolean", params=[("s", "String")],
  sample_args=[("A man, a plan, a canal: Panama",), ("race a car",)],
  hidden_args=[("ab_a",), ("0P",), ("a.",), ("ab",), ("Able was I ere I saw Elba",), ("12321",)],
  ref=ref_pal, tags=["string", "two-pointers"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["First normalize the string: lowercase it and drop non-alphanumeric characters.", "Then compare characters from both ends moving inward.", "You can also do it in O(1) space by skipping invalid characters with two pointers directly on the original string."])

def ref_rev(s):
    return s[::-1]

q(id="reverse-string", title="Reverse String", difficulty="Easy",
  description="Write a function that reverses a string and returns the reversed result. The input is given as a string s; return a new string with the characters in reverse order.",
  examples=[('s = "hello"', '"olleh"', "Characters reversed."),
            ('s = "Hannah"', '"hannaH"', "A palindrome stays the same when reversed.")],
  constraints=["1 <= s.length <= 10^5", "s consists of printable ASCII characters."],
  method_name="reverseString", return_type="String", params=[("s", "String")],
  sample_args=[("hello",), ("Hannah",)],
  hidden_args=[("a",), ("ab",), ("racecar",), ("Hello, World!",), ("12345",), ("ab  cd",)],
  ref=ref_rev, tags=["string", "two-pointers"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Swapping characters from both ends toward the middle reverses the string.", "In Java, convert to a char array, swap with two pointers, and build a new string.", "The classic in-place version uses O(1) extra space on the char array."])

def ref_rmdup(nums):
    if not nums:
        return 0
    w = 1
    for r in range(1, len(nums)):
        if nums[r] != nums[w - 1]:
            nums[w] = nums[r]
            w += 1
    return w

q(id="remove-duplicates-from-sorted-array", title="Remove Duplicates from Sorted Array", difficulty="Easy",
  description="Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once, keeping the relative order. Return the number of unique elements k. (The test harness checks only the returned count.)",
  examples=[("nums = [1, 1, 2]", "2", "Two unique elements: 1 and 2."),
            ("nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]", "5", "Five unique elements: 0, 1, 2, 3, 4.")],
  constraints=["1 <= nums.length <= 3 * 10^4", "-100 <= nums[i] <= 100", "nums is sorted in non-decreasing order."],
  method_name="removeDuplicates", return_type="int", params=[("nums", "int[]")],
  sample_args=[([1, 1, 2],), ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4],)],
  hidden_args=[([1],), ([1, 1, 1],), ([1, 2, 3],), ([1, 1, 2, 2, 3, 3],), ([-1, -1, 0, 0, 0, 5],), ([1, 2, 2, 3, 3, 3, 4],)],
  ref=ref_rmdup, tags=["array", "two-pointers"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Since the array is sorted, duplicates are adjacent.", "Use a slow pointer marking where the next unique element goes.", "A fast pointer scans ahead; whenever it finds a new value, write it at the slow pointer and advance."])

def ref_squares(nums):
    n = len(nums)
    out = [0] * n
    l, r, w = 0, n - 1, n - 1
    while l <= r:
        if abs(nums[l]) >= abs(nums[r]):
            out[w] = nums[l] * nums[l]
            l += 1
        else:
            out[w] = nums[r] * nums[r]
            r -= 1
        w -= 1
    return out

q(id="squares-of-a-sorted-array", title="Squares of a Sorted Array", difficulty="Easy",
  description="Given an integer array nums sorted in non-decreasing order, return an array of the squares of each number sorted in non-decreasing order.",
  examples=[("nums = [-4, -1, 0, 3, 10]", "[0, 1, 9, 16, 100]", "Squares are [16, 1, 0, 9, 100]; sorted gives the output."),
            ("nums = [-7, -3, 2, 3, 11]", "[4, 9, 9, 49, 121]", "Squares are [49, 9, 4, 9, 121]; sorted gives the output.")],
  constraints=["1 <= nums.length <= 10^4", "-10^4 <= nums[i] <= 10^4", "nums is sorted in non-decreasing order."],
  method_name="sortedSquares", return_type="int[]", params=[("nums", "int[]")],
  sample_args=[([-4, -1, 0, 3, 10],), ([-7, -3, 2, 3, 11],)],
  hidden_args=[([1],), ([-5],), ([-3, -2, -1],), ([0, 0, 0],), ([-2, 0, 2],), ([-10, -5, 0, 5, 10],)],
  ref=ref_squares, tags=["array", "two-pointers", "sorting"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Squaring then sorting is O(n log n); two pointers achieve O(n).", "The largest square comes from one of the two ends of the sorted array.", "Compare absolute values at both ends, write the larger square at the back of the result, and move that pointer inward."])

def ref_move0(nums):
    a = [x for x in nums]
    w = 0
    for x in a:
        if x != 0:
            a[w] = x
            w += 1
    for i in range(w, len(a)):
        a[i] = 0
    return a

q(id="move-zeroes", title="Move Zeroes", difficulty="Easy",
  description="Given an integer array nums, move all 0s to the end of it while maintaining the relative order of the non-zero elements. Return the resulting array. (This platform checks the returned array; do it in-place in your solution.)",
  examples=[("nums = [0, 1, 0, 3, 12]", "[1, 3, 12, 0, 0]", "Non-zero elements keep their order; zeros shift to the end."),
            ("nums = [0]", "[0]", "Nothing to move.")],
  constraints=["1 <= nums.length <= 10^4", "-2^31 <= nums[i] <= 2^31 - 1"],
  method_name="moveZeroes", return_type="int[]", params=[("nums", "int[]")],
  sample_args=[([0, 1, 0, 3, 12],), ([0],)],
  hidden_args=[([1, 2, 3],), ([0, 0, 1],), ([4, 0, 0, 5, 0],), ([0, 0, 0],), ([1, 0, 2, 0, 3, 0],), ([-1, 0, 2],)],
  ref=ref_move0, tags=["array", "two-pointers"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Think of partitioning the array into non-zeroes followed by zeroes.", "A write pointer marks where the next non-zero element goes.", "After one pass, fill the remaining tail positions with zeros."])

def ref_backspace(s, t):
    def build(x):
        st = []
        for c in x:
            if c == "#":
                if st:
                    st.pop()
            else:
                st.append(c)
        return "".join(st)
    return build(s) == build(t)

q(id="backspace-string-compare", title="Backspace String Compare", difficulty="Easy",
  description='Given two strings s and t, return true if they are equal when both are typed into empty text editors. The character "#" means a backspace: it deletes the previous character (deleting from an empty editor does nothing).',
  examples=[('s = "ab#c", t = "ad#c"', "true", 'Both become "ac".'),
            ('s = "ab##", t = "c#d#"', "true", 'Both become "".'),
            ('s = "a#c", t = "b"', "false", 's becomes "c", t stays "b".')],
  constraints=["1 <= s.length, t.length <= 200", "s and t consist of lowercase letters and '#' characters."],
  method_name="backspaceCompare", return_type="boolean", params=[("s", "String"), ("t", "String")],
  sample_args=[("ab#c", "ad#c"), ("ab##", "c#d#")],
  hidden_args=[("a#c", "b"), ("###", "###"), ("a##b", "b"), ("xywrrmp", "xywrrmu#p"), ("abc", "abc"), ("bxj##tw", "bxo#j##tw")],
  ref=ref_backspace, tags=["string", "two-pointers", "stack"],
  time_complexity="O(n + m)", space_complexity="O(n + m)",
  hints=["The straightforward way is to simulate typing each string with a stack.", "Compare the two final strings for equality.", "For O(1) space, walk both strings from the end, skipping characters erased by backspaces with two pointers."])

def ref_subseq(s, t):
    i = 0
    for c in t:
        if i < len(s) and s[i] == c:
            i += 1
    return i == len(s)

q(id="is-subsequence", title="Is Subsequence", difficulty="Easy",
  description="Given two strings s and t, return true if s is a subsequence of t, or false otherwise. A subsequence is formed by deleting some (or no) characters from t without changing the order of the remaining characters.",
  examples=[('s = "abc", t = "ahbgdc"', "true", '"abc" appears in order inside t.'),
            ('s = "axc", t = "ahbgdc"', "false", 'There is no "x" after "a" to match.')],
  constraints=["0 <= s.length <= 100", "0 <= t.length <= 10^4", "s and t consist of lowercase English letters."],
  method_name="isSubsequence", return_type="boolean", params=[("s", "String"), ("t", "String")],
  sample_args=[("abc", "ahbgdc"), ("axc", "ahbgdc")],
  hidden_args=[("a", "ba"), ("aaaa", "aa"), ("ace", "abcde"), ("aec", "abcde"), ("b", "abc"), ("abc", "abc")],
  ref=ref_subseq, tags=["string", "two-pointers", "greedy"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Walk through t once, advancing a pointer in s whenever characters match.", "If the s pointer reaches the end, s is a subsequence.", "An empty s is trivially a subsequence of any t."])

# ---------------- Medium ----------------

def ref_3sum(nums):
    a = sorted(nums)
    n = len(a)
    out = []
    for i in range(n - 2):
        if i > 0 and a[i] == a[i - 1]:
            continue
        l, r = i + 1, n - 1
        while l < r:
            s = a[i] + a[l] + a[r]
            if s == 0:
                out.append([a[i], a[l], a[r]])
                l += 1
                r -= 1
                while l < r and a[l] == a[l - 1]:
                    l += 1
                while l < r and a[r] == a[r + 1]:
                    r -= 1
            elif s < 0:
                l += 1
            else:
                r -= 1
    return out

q(id="3sum", title="3Sum", difficulty="Medium",
  description="Given an integer array nums, return all the unique triplets [nums[i], nums[j], nums[k]] such that i, j, k are distinct indices and nums[i] + nums[j] + nums[k] == 0. Return each triplet sorted in ascending order, and the list of triplets sorted lexicographically, so the output is deterministic.",
  examples=[("nums = [-1, 0, 1, 2, -1, -4]", "[[-1, -1, 2], [-1, 0, 1]]", "The two unique triplets summing to zero."),
            ("nums = [0, 0, 0]", "[[0, 0, 0]]", "The only triplet is [0, 0, 0].")],
  constraints=["3 <= nums.length <= 3000", "-10^5 <= nums[i] <= 10^5"],
  method_name="threeSum", return_type="List<List<Integer>>", params=[("nums", "int[]")],
  sample_args=[([-1, 0, 1, 2, -1, -4],), ([0, 0, 0],)],
  hidden_args=[([],), ([1, 2, -2, -1],), ([-2, 0, 1, 1, 2],), ([0, 0, 0, 0],), ([-1, -1, -1, 0, 1, 1, 2],), ([3, 0, -2, -1, 1, 2],)],
  ref=ref_3sum, tags=["array", "two-pointers", "sorting"],
  time_complexity="O(n^2)", space_complexity="O(n)",
  hints=["Sort the array first; then the problem becomes finding pairs with a target sum.", "Fix one element nums[i] and use two pointers on the rest to find pairs summing to -nums[i].", "Skip duplicate values for i, left, and right so each triplet appears once."])

def ref_maxarea(h):
    l, r, best = 0, len(h) - 1, 0
    while l < r:
        best = max(best, min(h[l], h[r]) * (r - l))
        if h[l] < h[r]:
            l += 1
        else:
            r -= 1
    return best

q(id="container-with-most-water", title="Container With Most Water", difficulty="Medium",
  description="You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]). Find two lines that together with the x-axis form a container holding the most water, and return that maximum amount of water. The area between lines l and r is min(height[l], height[r]) * (r - l).",
  examples=[("height = [1, 8, 6, 2, 5, 4, 8, 3, 7]", "49", "Lines at indices 1 and 8: min(8, 7) * 7 = 49."),
            ("height = [1, 1]", "1", "Only one pair: min(1, 1) * 1 = 1.")],
  constraints=["2 <= height.length <= 10^5", "0 <= height[i] <= 10^4"],
  method_name="maxArea", return_type="int", params=[("height", "int[]")],
  sample_args=[([1, 8, 6, 2, 5, 4, 8, 3, 7],), ([1, 1],)],
  hidden_args=[([4, 3, 2, 1, 4],), ([1, 2, 1],), ([2, 3, 4, 5, 18, 17, 6],), ([1, 2, 3, 4, 5],), ([5, 4, 3, 2, 1],), ([1, 0, 0, 0, 0, 0, 0, 2, 3],)],
  ref=ref_maxarea, tags=["array", "two-pointers", "greedy"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Brute force checks all O(n^2) pairs.", "Start with the widest container: pointers at both ends.", "Always move the pointer at the shorter line inward, since the width only shrinks from here."])

def ref_3closest(nums, target):
    a = sorted(nums)
    best = a[0] + a[1] + a[2]
    n = len(a)
    for i in range(n - 2):
        l, r = i + 1, n - 1
        while l < r:
            s = a[i] + a[l] + a[r]
            if abs(s - target) < abs(best - target):
                best = s
            if s < target:
                l += 1
            elif s > target:
                r -= 1
            else:
                return target
    return best

q(id="3sum-closest", title="3Sum Closest", difficulty="Medium",
  description="Given an integer array nums of length n and an integer target, find three integers in nums such that their sum is closest to target, and return that sum. Exactly one solution exists per input.",
  examples=[("nums = [-1, 2, 1, -4], target = 1", "2", "The sum closest to 1 is 2 = (-1 + 2 + 1)."),
            ("nums = [0, 0, 0], target = 1", "0", "The only possible sum is 0.")],
  constraints=["3 <= nums.length <= 500", "-1000 <= nums[i] <= 1000", "-10^4 <= target <= 10^4"],
  method_name="threeSumClosest", return_type="int", params=[("nums", "int[]"), ("target", "int")],
  sample_args=[([-1, 2, 1, -4], 1), ([0, 0, 0], 1)],
  hidden_args=[([1, 1, 1, 0], -100), ([4, 0, 5, -5, 3, 3, 0, -4, -5], -2), ([1, 2, 4, 8, 16, 32, 64, 128], 82), ([-3, -2, -5, 3, -4], -1), ([0, 2, 1, -3], 1), ([1, 1, -1, -1, 3], -1)],
  ref=ref_3closest, tags=["array", "two-pointers", "sorting"],
  time_complexity="O(n^2)", space_complexity="O(n)",
  hints=["Sort the array so two pointers can guide the search.", "Fix nums[i], then move two pointers to steer the triplet sum toward the target.", "Track the sum with the smallest absolute distance to target seen so far."])

def ref_sortcolors(nums):
    a = sorted(nums)
    return a

q(id="sort-colors", title="Sort Colors", difficulty="Medium",
  description="Given an array nums with n objects colored red (0), white (1), or blue (2), sort them in-place so that objects of the same color are adjacent, in the order red, white, blue. Return the sorted array. (This platform checks the returned array; implement the one-pass Dutch-national-flag algorithm in your solution.)",
  examples=[("nums = [2, 0, 2, 1, 1, 0]", "[0, 0, 1, 1, 2, 2]", "Grouped by color in order."),
            ("nums = [2, 0, 1]", "[0, 1, 2]", "One of each color.")],
  constraints=["1 <= nums.length <= 300", "nums[i] is 0, 1, or 2."],
  method_name="sortColors", return_type="int[]", params=[("nums", "int[]")],
  sample_args=[([2, 0, 2, 1, 1, 0],), ([2, 0, 1],)],
  hidden_args=[([0],), ([2, 2, 2],), ([1, 0],), ([1, 2, 0, 1, 2, 0],), ([0, 0, 0, 1, 1],), ([2, 1],)],
  ref=ref_sortcolors, tags=["array", "two-pointers", "sorting"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Counting the 0s, 1s, and 2s works but needs two passes.", "Maintain three regions with two pointers: low for 0s, high for 2s, mid scanning.", "Swap 0s to the low end and 2s to the high end in a single pass."])

def ref_boats(people, limit):
    a = sorted(people)
    l, r, boats = 0, len(a) - 1, 0
    while l <= r:
        if a[l] + a[r] <= limit:
            l += 1
        r -= 1
        boats += 1
    return boats

q(id="boats-to-save-people", title="Boats to Save People", difficulty="Medium",
  description="You are given an array people where people[i] is the weight of the ith person, and an infinite number of boats where each boat can carry at most two people at a time, provided the sum of their weights is at most limit. Return the minimum number of boats needed to carry every person.",
  examples=[("people = [1, 2], limit = 3", "1", "Both fit in one boat."),
            ("people = [3, 2, 2, 1], limit = 3", "3", "Boats: (1, 2), (2), (3)."),
            ("people = [3, 5, 3, 4], limit = 5", "4", "No two fit together; four boats.")],
  constraints=["1 <= people.length <= 5 * 10^4", "1 <= people[i] <= limit <= 3 * 10^4"],
  method_name="numRescueBoats", return_type="int", params=[("people", "int[]"), ("limit", "int")],
  sample_args=[([1, 2], 3), ([3, 2, 2, 1], 3)],
  hidden_args=[([3, 5, 3, 4], 5), ([5], 5), ([1, 2, 3, 4], 4), ([2, 2, 2, 2], 3), ([1, 1, 1, 1], 2), ([3, 3, 3, 3], 6)],
  ref=ref_boats, tags=["array", "two-pointers", "greedy", "sorting"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Sort the people by weight first.", "Pair the heaviest remaining person with the lightest possible partner.", "Two pointers from both ends: if lightest + heaviest fits, they share a boat; the heaviest always takes a boat this round."])

def ref_4sum(nums, target):
    a = sorted(nums)
    n = len(a)
    out = []
    for i in range(n - 3):
        if i > 0 and a[i] == a[i - 1]:
            continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and a[j] == a[j - 1]:
                continue
            l, r = j + 1, n - 1
            while l < r:
                s = a[i] + a[j] + a[l] + a[r]
                if s == target:
                    out.append([a[i], a[j], a[l], a[r]])
                    l += 1
                    r -= 1
                    while l < r and a[l] == a[l - 1]:
                        l += 1
                    while l < r and a[r] == a[r + 1]:
                        r -= 1
                elif s < target:
                    l += 1
                else:
                    r -= 1
    return out

q(id="4sum", title="4Sum", difficulty="Medium",
  description="Given an array nums of n integers, return all unique quadruplets [nums[a], nums[b], nums[c], nums[d]] such that a, b, c, d are distinct indices and their sum equals target. Return each quadruplet sorted in ascending order, and the list sorted lexicographically, so the output is deterministic.",
  examples=[("nums = [1, 0, -1, 0, -2, 2], target = 0", "[[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]", "The three unique quadruplets summing to zero."),
            ("nums = [2, 2, 2, 2, 2], target = 8", "[[2, 2, 2, 2]]", "The only quadruplet is [2, 2, 2, 2].")],
  constraints=["1 <= nums.length <= 200", "-10^9 <= nums[i] <= 10^9", "-10^9 <= target <= 10^9"],
  method_name="fourSum", return_type="List<List<Integer>>", params=[("nums", "int[]"), ("target", "int")],
  sample_args=[([1, 0, -1, 0, -2, 2], 0), ([2, 2, 2, 2, 2], 8)],
  hidden_args=[([1, 2, 3], 6), ([0, 0, 0, 0], 0), ([-3, -1, 0, 2, 4, 5], 2), ([1, -2, -5, -4, -3, 3, 3, 5], -11), ([2, 1, 0, -1], 2), ([-1, 0, 1, 2, -1, -4], -1)],
  ref=ref_4sum, tags=["array", "two-pointers", "sorting"],
  time_complexity="O(n^3)", space_complexity="O(n)",
  hints=["Generalize 3Sum: sort, fix two elements, two-pointer the rest.", "Skip duplicates at every level (i, j, left, right).", "Watch for integer overflow when summing: use long arithmetic in Java."])

def ref_nextperm(nums):
    a = [x for x in nums]
    n = len(a)
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i >= 0:
        j = n - 1
        while a[j] <= a[i]:
            j -= 1
        a[i], a[j] = a[j], a[i]
    a[i + 1:] = reversed(a[i + 1:])
    return a

q(id="next-permutation", title="Next Permutation", difficulty="Medium",
  description="Given an array of integers nums, find the next permutation of nums: rearrange it into the lexicographically next greater permutation of numbers. If no greater permutation exists, rearrange it into the lowest possible order (sorted ascending). Return the resulting array. (Implement the in-place algorithm in your solution; the platform checks the returned array.)",
  examples=[("nums = [1, 2, 3]", "[1, 3, 2]", "The next greater arrangement."),
            ("nums = [3, 2, 1]", "[1, 2, 3]", "No greater permutation; wrap to the smallest."),
            ("nums = [1, 1, 5]", "[1, 5, 1]", "The next greater arrangement.")],
  constraints=["1 <= nums.length <= 100", "0 <= nums[i] <= 100"],
  method_name="nextPermutation", return_type="int[]", params=[("nums", "int[]")],
  sample_args=[([1, 2, 3],), ([3, 2, 1],)],
  hidden_args=[([1, 1, 5],), ([1],), ([1, 3, 2],), ([2, 3, 1],), ([5, 1, 1],), ([1, 5, 8, 4, 7, 6, 5, 3, 1],)],
  ref=ref_nextperm, tags=["array", "two-pointers"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Scan from the right to find the first index i where nums[i] < nums[i + 1] (the pivot).", "Swap the pivot with the smallest element to its right that is larger than it.", "Reverse the suffix after the pivot to get the smallest possible tail."])

def ref_compress(s):
    if not s:
        return ""
    out = []
    i = 0
    n = len(s)
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        out.append(s[i] + str(j - i))
        i = j
    return "".join(out)

q(id="string-compression", title="String Compression", difficulty="Medium",
  description="Given a string s, compress it by replacing each maximal group of consecutive equal characters with the character followed by the group's length. For example, 'aabcccccaaa' becomes 'a2b1c5a3'. Return the compressed string. (The classic in-place variant writes into the char array and returns its new length; here you return the compressed string directly.)",
  examples=[('s = "aabcccccaaa"', '"a2b1c5a3"', "Groups: aa, b, ccccc, aaa."),
            ('s = "abc"', '"a1b1c1"', "No repeats; each group has length 1.")],
  constraints=["1 <= s.length <= 2000", "s consists of lowercase English letters."],
  method_name="compress", return_type="String", params=[("s", "String")],
  sample_args=[("aabcccccaaa",), ("abc",)],
  hidden_args=[("a",), ("aaaaaaaaaa",), ("abbbcc",), ("zzzzyyy",), ("aabbaa",), ("abcddeeff",)],
  ref=ref_compress, tags=["string", "two-pointers"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Two pointers delimit each run: one marks the run start, the other scans ahead.", "Count the run length, then append the character and the count.", "In the in-place version, a write pointer overwrites the array as runs are processed."])

# ---------------- Hard ----------------

def ref_trap(h):
    l, r = 0, len(h) - 1
    lm = rm = ans = 0
    while l < r:
        if h[l] < h[r]:
            lm = max(lm, h[l])
            ans += lm - h[l]
            l += 1
        else:
            rm = max(rm, h[r])
            ans += rm - h[r]
            r -= 1
    return ans

q(id="trapping-rain-water", title="Trapping Rain Water", difficulty="Hard",
  description="Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
  examples=[("height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]", "6", "The classic example traps 6 units."),
            ("height = [4, 2, 0, 3, 2, 5]", "9", "9 units are trapped.")],
  constraints=["0 <= height.length <= 2 * 10^4", "0 <= height[i] <= 10^5"],
  method_name="trap", return_type="int", params=[("height", "int[]")],
  sample_args=[([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],), ([4, 2, 0, 3, 2, 5],)],
  hidden_args=[([],), ([1],), ([3, 0, 3],), ([5, 4, 1, 2],), ([2, 0, 2],), ([0, 2, 0],)],
  ref=ref_trap, tags=["array", "two-pointers", "stack", "dynamic-programming"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Water above bar i is min(max height to its left, max height to its right) - height[i].", "Precomputing left-max and right-max arrays gives O(n) time with O(n) space.", "Two pointers can do it in O(1) space: always advance the side with the smaller current max."])

def ref_goodscore(nums, k):
    n = len(nums)
    l = r = k
    cur_min = nums[k]
    best = cur_min
    while l > 0 or r < n - 1:
        if l == 0:
            r += 1
        elif r == n - 1:
            l -= 1
        elif nums[l - 1] > nums[r + 1]:
            l -= 1
        else:
            r += 1
        cur_min = min(cur_min, nums[l], nums[r])
        best = max(best, cur_min * (r - l + 1))
    return best

q(id="maximum-score-of-a-good-subarray", title="Maximum Score of a Good Subarray", difficulty="Hard",
  description="You are given an array of integers nums (0-indexed) and an integer k. The score of a subarray (i, j) is defined as min(nums[i], nums[i+1], ..., nums[j]) * (j - i + 1). A good subarray must include the index k. Return the maximum possible score of a good subarray of nums.",
  examples=[("nums = [1, 4, 3, 7, 4, 5], k = 3", "15", "Subarray [3, 7, 4, 5] (indices 2..5): min 3 * 5 = 15."),
            ("nums = [5, 5, 4, 5, 4, 5, 4, 5, 4, 5], k = 0", "20", "Subarray [5, 5, 4, 5] (indices 0..3): min 4 * 5 = 20.")],
  constraints=["1 <= nums.length <= 10^5", "1 <= nums[i] <= 2 * 10^4", "0 <= k < nums.length"],
  method_name="maximumScore", return_type="int", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([1, 4, 3, 7, 4, 5], 3), ([5, 5, 4, 5, 4, 5, 4, 5, 4, 5], 0)],
  hidden_args=[([1], 0), ([1, 2, 3], 1), ([5, 4, 3, 2, 1], 4), ([2, 1], 0), ([6569, 9667, 3148, 7698, 1622, 2194, 793, 9049, 1670, 1872], 5), ([1, 2, 3, 4, 5], 2)],
  ref=ref_goodscore, tags=["array", "two-pointers", "greedy"],
  time_complexity="O(n)", space_complexity="O(1)",
  hints=["Any good subarray is an expansion of [k, k] outward.", "Greedily expand toward the side with the larger next element to keep the minimum high.", "Track the running minimum and the best min * width seen during the expansion."])

def ref_reversepairs(nums):
    def ms(a):
        if len(a) <= 1:
            return 0, a
        m = len(a) // 2
        c1, L = ms(a[:m])
        c2, R = ms(a[m:])
        c = c1 + c2
        j = 0
        for x in L:
            while j < len(R) and x > 2 * R[j]:
                j += 1
            c += j
        i = k = 0
        merged = []
        while i < len(L) and k < len(R):
            if L[i] <= R[k]:
                merged.append(L[i]); i += 1
            else:
                merged.append(R[k]); k += 1
        merged += L[i:] + R[k:]
        return c, merged
    return ms(list(nums))[0]

q(id="reverse-pairs", title="Reverse Pairs", difficulty="Hard",
  description="Given an integer array nums, return the number of reverse pairs in the array. A reverse pair is a pair (i, j) where 0 <= i < j < nums.length and nums[i] > 2 * nums[j].",
  examples=[("nums = [1, 3, 2, 3, 1]", "2", "Pairs (1, 4) and (3, 4): 3 > 2*1."),
            ("nums = [2, 4, 3, 5, 1]", "3", "Pairs (1, 4), (2, 4), (3, 4).")],
  constraints=["1 <= nums.length <= 5 * 10^4", "-2^31 <= nums[i] <= 2^31 - 1"],
  method_name="reversePairs", return_type="int", params=[("nums", "int[]")],
  sample_args=[([1, 3, 2, 3, 1],), ([2, 4, 3, 5, 1],)],
  hidden_args=[([1],), ([5, 4, 3, 2, 1],), ([2, 2, 2],), ([-5, -5],), ([1, 2, 3, 4, 5],), ([2147483647, 2147483647, 2147483647],)],
  ref=ref_reversepairs, tags=["array", "two-pointers", "divide-and-conquer", "merge-sort"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Brute force is O(n^2); think merge sort.", "During the merge step both halves are sorted, so a two-pointer scan counts cross pairs in linear time.", "For each element in the left half, advance a pointer in the right half while left > 2 * right; use long arithmetic to avoid overflow."])

def ref_minmoves(nums, k):
    pos = [i for i, x in enumerate(nums) if x == 1]
    m = len(pos)
    adj = [p - i for i, p in enumerate(pos)]
    pref = [0]
    for v in adj:
        pref.append(pref[-1] + v)
    best = float("inf")
    for i in range(m - k + 1):
        med = i + k // 2
        medv = adj[med]
        left = medv * (med - i) - (pref[med] - pref[i])
        right = (pref[i + k] - pref[med + 1]) - medv * (i + k - 1 - med)
        best = min(best, left + right)
    return best

q(id="minimum-adjacent-swaps-for-k-consecutive-ones", title="Minimum Adjacent Swaps for K Consecutive Ones", difficulty="Hard",
  description="Given an integer array nums and an integer k, return the minimum number of adjacent swaps needed to group any k ones together consecutively. The array is guaranteed to contain at least k ones. The standard solution collects the indices of the 1s and uses two pointers over a sliding window of those positions.",
  examples=[("nums = [1, 0, 0, 1, 0, 1], k = 2", "1", "Swap the 1 at index 3 with the 0 at index 2."),
            ("nums = [1, 0, 0, 0, 0, 0, 1, 1], k = 3", "5", "Group the ones at indices 0, 6, 7 together with 5 swaps.")],
  constraints=["1 <= nums.length <= 10^5", "nums[i] is 0 or 1.", "1 <= k <= number of ones in nums"],
  method_name="minMoves", return_type="int", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([1, 0, 0, 1, 0, 1], 2), ([1, 0, 0, 0, 0, 0, 1, 1], 3)],
  hidden_args=[([1, 1, 0, 1], 2), ([0, 0, 1, 0, 1, 1], 2), ([1, 0, 1, 0, 1, 0, 1], 3), ([0, 1, 0, 1, 0], 1), ([1, 0, 0, 1, 0, 0, 1], 2), ([1, 1, 1, 0, 0, 0], 3)],
  ref=ref_minmoves, tags=["array", "two-pointers", "sliding-window", "prefix-sum", "greedy"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Only the positions of the 1s matter; collect them into an array pos.", "Grouping k ones consecutively around a target costs the sum of distances; adjusting pos[i] by i removes the consecutive offsets.", "With adjusted positions, the cost of a window is minimized at the median; use prefix sums and a sliding window for O(n)."])

write_bank(P, Q)
