"""Sorting/Intervals pattern: 20 questions (8 Easy, 8 Medium, 4 Hard)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genlib import make_question, write_bank
from collections import Counter, defaultdict
import heapq

P = "sorting-intervals"
Q = []

def q(**kw):
    Q.append(make_question(pattern=P, **kw))

# ---------------- Easy ----------------

def ref_meetings(intervals):
    a = sorted(intervals)
    for i in range(1, len(a)):
        if a[i][0] < a[i - 1][1]:
            return False
    return True

q(id="meeting-rooms", title="Meeting Rooms", difficulty="Easy",
  description="Given an array of meeting time intervals where intervals[i] = [starti, endi], determine if a person could attend all meetings (no two meetings overlap; touching endpoints are fine).",
  examples=[("intervals = [[0, 30], [5, 10], [15, 20]]", "false", "[0, 30] overlaps both others."),
            ("intervals = [[7, 10], [2, 4]]", "true", "No overlap.")],
  constraints=["0 <= intervals.length <= 10^4", "0 <= starti < endi <= 10^6"],
  method_name="canAttendMeetings", return_type="boolean", params=[("intervals", "int[][]")],
  sample_args=[([[0, 30], [5, 10], [15, 20]],), ([[7, 10], [2, 4]],)],
  hidden_args=[([],), ([[1, 2]],), ([[1, 2], [2, 3]],), ([[1, 3], [2, 4]],), ([[0, 5], [5, 10], [10, 15]],), ([[1, 10], [2, 3], [4, 5]],)],
  ref=ref_meetings, tags=["array", "sorting", "intervals"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Sort the intervals by start time.", "Then each interval only needs to be compared with the previous one.", "An overlap exists when the current start is less than the previous end."])

def ref_relsort(arr1, arr2):
    order = {v: i for i, v in enumerate(arr2)}
    in_order = sorted([x for x in arr1 if x in order], key=lambda x: order[x])
    rest = sorted([x for x in arr1 if x not in order])
    return in_order + rest

q(id="relative-sort-array", title="Relative Sort Array", difficulty="Easy",
  description="Given two arrays arr1 and arr2, sort the elements of arr1 such that the relative ordering of items matches arr2: elements appearing in arr2 come first, ordered by their first occurrence in arr2 (duplicates kept). Elements of arr1 not in arr2 are appended at the end in ascending order.",
  examples=[("arr1 = [2, 3, 1, 3, 2, 4, 6, 7, 9, 2, 19], arr2 = [2, 1, 4, 3, 9, 6]", "[2, 2, 2, 1, 4, 3, 3, 9, 6, 7, 19]", "Grouped by arr2's order, then leftovers sorted."),
            ("arr1 = [1, 2], arr2 = [2, 1]", "[2, 1]", "Ordered by arr2.")],
  constraints=["1 <= arr1.length, arr2.length <= 1000", "0 <= arr1[i], arr2[i] <= 1000", "All elements of arr2 are distinct.", "Each arr2[i] appears in arr1."],
  method_name="relativeSortArray", return_type="int[]", params=[("arr1", "int[]"), ("arr2", "int[]")],
  sample_args=[([2, 3, 1, 3, 2, 4, 6, 7, 9, 2, 19], [2, 1, 4, 3, 9, 6]), ([1, 2], [2, 1])],
  hidden_args=[([5, 5, 5], [5]), ([3, 1, 2], [1, 2, 3]), ([4, 3, 2, 1], [4, 3]), ([1, 1, 2, 2, 3], [2, 1]), ([7, 8, 9], []), ([2, 1, 2, 1], [1])],
  ref=ref_relsort, tags=["array", "sorting", "hash-table", "counting"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Count occurrences of each value in arr1.", "Emit values in arr2's order, repeating by their counts.", "Emit the remaining values in ascending order."])

def ref_parity(nums):
    return [x for x in nums if x % 2 == 0] + [x for x in nums if x % 2 == 1]

q(id="sort-array-by-parity", title="Sort Array By Parity", difficulty="Easy",
  description="Given an integer array nums, move all the even integers to the beginning of the array followed by all the odd integers. Preserve the relative order within the even group and within the odd group (stable partition). Return the resulting array.",
  examples=[("nums = [3, 1, 2, 4]", "[2, 4, 3, 1]", "Evens [2, 4] first (in order), then odds [3, 1] (in order)."),
            ("nums = [0]", "[0]", "A single even element.")],
  constraints=["1 <= nums.length <= 5000", "0 <= nums[i] <= 5000"],
  method_name="sortArrayByParity", return_type="int[]", params=[("nums", "int[]")],
  sample_args=[([3, 1, 2, 4],), ([0],)],
  hidden_args=[([1, 3, 5],), ([2, 4, 6],), ([1, 2, 3, 4, 5, 6],), ([0, 1, 0, 1],), ([7],), ([2, 1],)],
  ref=ref_parity, tags=["array", "sorting", "two-pointers"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["A single pass can split the numbers into evens and odds.", "Collect evens in one list and odds in another, then concatenate.", "The classic two-pointer in-place version swaps without preserving order; the stable version needs extra space."])
def ref_seat(seats, students):
    seats = sorted(seats)
    students = sorted(students)
    return sum(abs(a - b) for a, b in zip(seats, students))

q(id="minimum-number-of-moves-to-seat-everyone", title="Minimum Number of Moves to Seat Everyone", difficulty="Easy",
  description="There are n seats and n students. seats[i] is the position of seat i, students[j] is the position of student j. Move the students so each sits on a unique seat; one move shifts a student by 1 position. Return the minimum total moves.",
  examples=[("seats = [3, 1, 5], students = [2, 7, 4]", "4", "Match sorted: |1-2| + |3-4| + |5-7| = 1 + 1 + 2 = 4."),
            ("seats = [4, 1, 5, 9], students = [1, 3, 2, 6]", "7", "Match sorted: 0 + 1 + 3 + 3 = 7."),
            ("seats = [2, 2, 6, 6], students = [1, 3, 2, 6]", "4", "Match sorted: 1 + 1 + 2 + 0 = 4.")],
  constraints=["1 <= seats.length <= 100", "1 <= seats[i], students[j] <= 100"],
  method_name="minMovesToSeat", return_type="int", params=[("seats", "int[]"), ("students", "int[]")],
  sample_args=[([3, 1, 5], [2, 7, 4]), ([4, 1, 5, 9], [1, 3, 2, 6])],
  hidden_args=[([2, 2, 6, 6], [1, 3, 2, 6]), ([1], [1]), ([1, 2], [2, 1]), ([5, 4, 3], [1, 2, 3]), ([10], [1]), ([1, 100], [50, 51])],
  ref=ref_seat, tags=["array", "sorting", "greedy"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Sort both arrays.", "The optimal matching pairs the ith smallest seat with the ith smallest student.", "Sum the absolute differences of the paired positions."])

def ref_sortbits(arr):
    return sorted(arr, key=lambda x: (bin(x).count("1"), x))

q(id="sort-integers-by-the-number-of-1-bits", title="Sort Integers by the Number of 1 Bits", difficulty="Easy",
  description="You are given an integer array arr. Sort the integers in ascending order by the number of 1 bits in their binary representation; break ties by the numeric value ascending. Return the sorted array.",
  examples=[("arr = [0, 1, 2, 3, 4, 5, 6, 7, 8]", "[0, 1, 2, 4, 8, 3, 5, 6, 7]", "Grouped by bit count, then by value."),
            ("arr = [1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1]", "[1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]", "All have one bit; sorted by value.")],
  constraints=["1 <= arr.length <= 500", "0 <= arr[i] <= 10^4"],
  method_name="sortByBits", return_type="int[]", params=[("arr", "int[]")],
  sample_args=[([0, 1, 2, 3, 4, 5, 6, 7, 8],), ([1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1],)],
  hidden_args=[([5],), ([3, 3, 3],), ([2, 3, 1],), ([7, 6, 5, 4, 3, 2, 1, 0],), ([10000, 1000],), ([8, 8, 8, 1],)],
  ref=ref_sortbits, tags=["array", "sorting", "bit-manipulation"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Define a comparator (or sort key) on (bitCount(x), x).", "Java: Integer.bitCount(x) counts the 1 bits.", "Arrays.sort with a custom comparator handles the tie-break naturally."])

def ref_height(heights):
    s = sorted(heights)
    return sum(1 for a, b in zip(heights, s) if a != b)

q(id="height-checker", title="Height Checker", difficulty="Easy",
  description="A school lines students up by height, but not in order. heights[i] is the height of the ith student. Return the number of indices where heights[i] differs from the correctly sorted order.",
  examples=[("heights = [1, 1, 4, 2, 1, 3]", "3", "Indices 2, 4, 5 differ from sorted [1, 1, 1, 2, 3, 4]."),
            ("heights = [5, 1, 2, 3, 4]", "5", "Every position differs."),
            ("heights = [1, 2, 3, 4, 5]", "0", "Already sorted.")],
  constraints=["1 <= heights.length <= 100", "1 <= heights[i] <= 100"],
  method_name="heightChecker", return_type="int", params=[("heights", "int[]")],
  sample_args=[([1, 1, 4, 2, 1, 3],), ([5, 1, 2, 3, 4],)],
  hidden_args=[([1, 2, 3, 4, 5],), ([1],), ([2, 1],), ([1, 1, 1],), ([4, 3, 2, 1],), ([1, 3, 2],)],
  ref=ref_height, tags=["array", "sorting", "counting"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Make a sorted copy of the array.", "Compare it position by position with the original.", "Count the mismatches."])

def ref_smaller(nums):
    s = sorted(nums)
    rank = {}
    for i, x in enumerate(s):
        if x not in rank:
            rank[x] = i
    return [rank[x] for x in nums]

q(id="how-many-numbers-are-smaller-than-the-current-number", title="How Many Numbers Are Smaller Than the Current Number", difficulty="Easy",
  description="Given an array nums, for each nums[i] return how many numbers in the array are strictly smaller than nums[i].",
  examples=[("nums = [8, 1, 2, 2, 3]", "[4, 0, 1, 1, 3]", "Four numbers are smaller than 8; none smaller than 1; etc."),
            ("nums = [6, 5, 4, 8]", "[2, 1, 0, 3]", "Counts of smaller elements."),
            ("nums = [7, 7, 7, 7]", "[0, 0, 0, 0]", "No number is strictly smaller.")],
  constraints=["1 <= nums.length <= 500", "0 <= nums[i] <= 100"],
  method_name="smallerNumbersThanCurrent", return_type="int[]", params=[("nums", "int[]")],
  sample_args=[([8, 1, 2, 2, 3],), ([6, 5, 4, 8],)],
  hidden_args=[([7, 7, 7, 7],), ([1],), ([5, 0, 10, 0, 10, 6],), ([3, 2],), ([1, 2, 3],), ([4, 4, 4, 1],)],
  ref=ref_smaller, tags=["array", "sorting", "hash-table", "counting"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Sort a copy of the array.", "The first index where each value appears in the sorted array equals the count of smaller numbers.", "Map each distinct value to that first index, then translate the original array."])

def ref_maxprod3(nums):
    a = sorted(nums)
    return max(a[-1] * a[-2] * a[-3], a[0] * a[1] * a[-1])

q(id="maximum-product-of-three-numbers", title="Maximum Product of Three Numbers", difficulty="Easy",
  description="Given an integer array nums, find three numbers whose product is maximum and return that maximum product.",
  examples=[("nums = [1, 2, 3]", "6", "1 * 2 * 3 = 6."),
            ("nums = [1, 2, 3, 4]", "24", "2 * 3 * 4 = 24.")],
  constraints=["3 <= nums.length <= 10^4", "-1000 <= nums[i] <= 1000"],
  method_name="maximumProduct", return_type="int", params=[("nums", "int[]")],
  sample_args=[([1, 2, 3],), ([1, 2, 3, 4],)],
  hidden_args=[([-1, -2, -3],), ([-4, -3, -2, -1, 60],), ([1, 2, 3, 4, 5],), ([-1, -2, 1, 2, 3],), ([0, 0, 0],), ([-5, -4, 1, 2, 3],)],
  ref=ref_maxprod3, tags=["array", "sorting", "math"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Sort the array first.", "The answer is either the product of the three largest, or the two smallest (possibly negative) times the largest.", "Take the maximum of those two candidates."])
def ref_merge(intervals):
    a = sorted(intervals)
    out = []
    for s, e in a:
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out

q(id="merge-intervals", title="Merge Intervals", difficulty="Medium",
  description="Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals and return an array of the non-overlapping intervals that cover all the inputs. Intervals that only touch at endpoints (e.g. [1, 4] and [4, 5]) are merged.",
  examples=[("intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]", "[[1, 6], [8, 10], [15, 18]]", "[1,3] and [2,6] merge into [1,6]."),
            ("intervals = [[1, 4], [4, 5]]", "[[1, 5]]", "Touching intervals merge.")],
  constraints=["1 <= intervals.length <= 10^4", "0 <= starti <= endi <= 10^4"],
  method_name="merge", return_type="int[][]", params=[("intervals", "int[][]")],
  sample_args=[([[1, 3], [2, 6], [8, 10], [15, 18]],), ([[1, 4], [4, 5]],)],
  hidden_args=[([[1, 4], [0, 4]],), ([[1, 4], [2, 3]],), ([[1, 2]],), ([[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]],), ([[1, 10], [2, 3], [4, 5]],), ([[5, 7], [1, 3]],)],
  ref=ref_merge, tags=["array", "sorting", "intervals"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Sort intervals by start time.", "Sweep through, extending the current merged interval while the next one overlaps.", "An overlap (or touch) means next.start <= current.end; otherwise emit the current interval."])

def ref_insert(intervals, new):
    out = []
    i, n = 0, len(intervals)
    while i < n and intervals[i][1] < new[0]:
        out.append(intervals[i]); i += 1
    while i < n and intervals[i][0] <= new[1]:
        new = [min(new[0], intervals[i][0]), max(new[1], intervals[i][1])]
        i += 1
    out.append(new)
    out.extend(intervals[i:])
    return out

q(id="insert-interval", title="Insert Interval", difficulty="Medium",
  description="You are given an array of non-overlapping intervals sorted in ascending order by start, and a newInterval [start, end]. Insert newInterval into the array, merging any overlaps, so the result is still sorted and non-overlapping.",
  examples=[("intervals = [[1, 3], [6, 9]], newInterval = [2, 5]", "[[1, 5], [6, 9]]", "[2,5] merges with [1,3]."),
            ("intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], newInterval = [4, 8]", "[[1, 2], [3, 10], [12, 16]]", "[4,8] merges [3,5], [6,7], [8,10].")],
  constraints=["0 <= intervals.length <= 10^4", "0 <= starti <= endi <= 10^5", "intervals is sorted by start and non-overlapping."],
  method_name="insert", return_type="int[][]", params=[("intervals", "int[][]"), ("newInterval", "int[]")],
  sample_args=[([[1, 3], [6, 9]], [2, 5]), ([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8])],
  hidden_args=[([], [5, 7]), ([[1, 5]], [2, 3]), ([[1, 5]], [6, 8]), ([[3, 5], [6, 9]], [1, 2]), ([[1, 2], [3, 4]], [2, 3]), ([[1, 3], [6, 9]], [0, 10])],
  ref=ref_insert, tags=["array", "intervals"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["The input is already sorted: three phases work in one pass.", "Copy intervals ending before newInterval starts.", "Merge all intervals overlapping newInterval, append the merged one, then copy the rest."])

def ref_rooms2(intervals):
    if not intervals:
        return 0
    starts = sorted(s for s, e in intervals)
    ends = sorted(e for s, e in intervals)
    i = j = used = best = 0
    while i < len(starts):
        if starts[i] < ends[j]:
            used += 1
            best = max(best, used)
            i += 1
        else:
            used -= 1
            j += 1
    return best

q(id="meeting-rooms-ii", title="Meeting Rooms II", difficulty="Medium",
  description="Given an array of meeting time intervals where intervals[i] = [starti, endi], return the minimum number of conference rooms required so all meetings can be held. A meeting ending at time t frees its room for a meeting starting at t.",
  examples=[("intervals = [[0, 30], [5, 10], [15, 20]]", "2", "Two rooms suffice."),
            ("intervals = [[7, 10], [2, 4]]", "1", "One room suffices.")],
  constraints=["1 <= intervals.length <= 10^4", "0 <= starti < endi <= 10^6"],
  method_name="minMeetingRooms", return_type="int", params=[("intervals", "int[][]")],
  sample_args=[([[0, 30], [5, 10], [15, 20]],), ([[7, 10], [2, 4]],)],
  hidden_args=[([[1, 2]],), ([[1, 2], [2, 3], [3, 4]],), ([[1, 5], [2, 6], [3, 7]],), ([[1, 10], [2, 3], [4, 5], [6, 7]],), ([[9, 10], [4, 9], [4, 17]],), ([[1, 5], [8, 9], [8, 9]],)],
  ref=ref_rooms2, tags=["array", "sorting", "intervals", "heap", "two-pointers"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Sort start times and end times separately.", "Sweep through starts in order, tracking rooms in use.", "If the next meeting starts before the earliest ending meeting ends, you need another room; otherwise a room frees up."])

def ref_partition_k(nums, k):
    a = sorted(nums)
    cnt, start = 1, a[0]
    for x in a[1:]:
        if x - start > k:
            cnt += 1
            start = x
    return cnt

q(id="partition-array-such-that-maximum-difference-is-k", title="Partition Array Such That Maximum Difference Is K", difficulty="Medium",
  description="You are given an integer array nums and an integer k. Partition the array into one or more subsequences such that in each subsequence, the difference between the maximum and minimum values is at most k. Return the minimum number of subsequences needed.",
  examples=[("nums = [3, 6, 1, 2, 5], k = 2", "2", "Sorted [1, 2, 3, 5, 6]: subsequences [1, 2, 3] and [5, 6]."),
            ("nums = [1, 2, 3], k = 1", "2", "Subsequences [1, 2] and [3].")],
  constraints=["1 <= nums.length <= 10^5", "0 <= nums[i] <= 10^5", "0 <= k <= 10^5"],
  method_name="partitionArray", return_type="int", params=[("nums", "int[]"), ("k", "int")],
  sample_args=[([3, 6, 1, 2, 5], 2), ([1, 2, 3], 1)],
  hidden_args=[([2, 2, 4, 5], 0), ([1, 1, 1], 5), ([5], 10), ([1, 2, 3, 4, 5, 6], 2), ([10, 20, 30], 5), ([1, 3, 5, 7, 9], 4)],
  ref=ref_partition_k, tags=["array", "sorting", "greedy"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Sort the array first; an optimal partition uses contiguous groups in sorted order.", "Greedily extend the current group as far as possible.", "Start a new group when the next element exceeds (group minimum + k)."])
def ref_intersect(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        s = max(a[i][0], b[j][0])
        e = min(a[i][1], b[j][1])
        if s <= e:
            out.append([s, e])
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return out

q(id="interval-list-intersections", title="Interval List Intersections", difficulty="Medium",
  description="You are given two lists of closed intervals, firstList and secondList. Each list is pairwise disjoint and sorted in ascending order by start. Return the intersection of the two interval lists: all [start, end] ranges present in both lists.",
  examples=[("firstList = [[0, 2], [5, 10], [13, 23], [24, 25]], secondList = [[1, 5], [8, 12], [15, 24], [25, 26]]", "[[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]", "Pairwise intersections of overlapping intervals."),
            ("firstList = [[1, 3], [5, 9]], secondList = []", "[]", "Nothing to intersect with.")],
  constraints=["0 <= firstList.length, secondList.length <= 1000", "0 <= starti <= endi <= 10^9"],
  method_name="intervalIntersection", return_type="int[][]", params=[("firstList", "int[][]"), ("secondList", "int[][]")],
  sample_args=[([[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]]), ([[1, 3], [5, 9]], [])],
  hidden_args=[([[1, 5]], [[2, 3]]), ([[1, 2]], [[3, 4]]), ([[1, 7]], [[3, 5]]), ([[1, 4], [5, 8]], [[2, 6]]), ([[1, 3]], [[1, 3]]), ([[1, 5], [10, 14]], [[3, 12]])],
  ref=ref_intersect, tags=["array", "intervals", "two-pointers"],
  time_complexity="O(n + m)", space_complexity="O(n + m)",
  hints=["Walk both lists with two pointers.", "The overlap of [a1, b1] and [a2, b2] is [max(a1, a2), min(b1, b2)] when max <= min.", "Advance the pointer whose interval ends first."])

def ref_carpool(trips, capacity):
    events = []
    for num, start, end in trips:
        events.append((start, num))
        events.append((end, -num))
    events.sort()
    cur = 0
    for _, d in events:
        cur += d
        if cur > capacity:
            return False
    return True

q(id="car-pooling", title="Car Pooling", difficulty="Medium",
  description="There is a car with capacity empty seats. trips[i] = [numPassengersi, fromi, toi]: passengers board at fromi and alight at toi (the car travels from fromi to toi - 1). Return true if it is possible to pick up and drop off all passengers without exceeding capacity at any point.",
  examples=[("trips = [[2, 1, 5], [3, 3, 7]], capacity = 4", "false", "From 3 to 5, 5 passengers exceed capacity 4."),
            ("trips = [[2, 1, 5], [3, 3, 7]], capacity = 5", "true", "Peak load is exactly 5.")],
  constraints=["1 <= trips.length <= 1000", "1 <= numPassengersi <= 100", "0 <= fromi < toi <= 1000", "1 <= capacity <= 10^5"],
  method_name="carPooling", return_type="boolean", params=[("trips", "int[][]"), ("capacity", "int")],
  sample_args=[([[2, 1, 5], [3, 3, 7]], 4), ([[2, 1, 5], [3, 3, 7]], 5)],
  hidden_args=[([[2, 1, 5], [3, 5, 7]], 3), ([[3, 2, 7], [3, 7, 9], [8, 3, 9]], 11), ([[1, 1, 2]], 1), ([[9, 0, 1], [3, 3, 7]], 4), ([[1, 1, 3], [2, 2, 4]], 2), ([[2, 2, 6]], 2)],
  ref=ref_carpool, tags=["array", "sorting", "intervals", "difference-array", "heap", "prefix-sum"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Model boardings as +passengers at fromi and alightings as -passengers at toi.", "Sort all events by location and sweep, tracking the current load.", "Drop-offs at a location happen before pick-ups there: sort ties with negatives first."])

def ref_custom(order, s):
    cnt = Counter(s)
    out = []
    for c in order:
        out.append(c * cnt.pop(c, 0))
    in_order = set(order)
    out.append("".join(c for c in s if c not in in_order))
    return "".join(out)

q(id="custom-sort-string", title="Custom Sort String", difficulty="Medium",
  description="You are given two strings order and s. All characters of order are unique and were sorted in some custom order. Permute the characters of s so that they match the order given in order: characters appearing in order come first, repeated by their counts in s, in order's sequence. Characters of s not in order are appended at the end, preserving their original relative order. Return the resulting permutation of s.",
  examples=[('order = "cba", s = "abcd"', '"cbad"', '"c", "b", "a" per order, then "d" which is not in order.'),
            ('order = "bcafg", s = "abcd"', '"bcad"', '"b", "c", "a" per order, then "d".')],
  constraints=["1 <= order.length <= 26", "1 <= s.length <= 200", "order and s consist of lowercase English letters.", "All characters of order are unique."],
  method_name="customSortString", return_type="String", params=[("order", "String"), ("s", "String")],
  sample_args=[("cba", "abcd"), ("bcafg", "abcd")],
  hidden_args=[("kqep", "pekeq"), ("a", "a"), ("xyz", "abc"), ("cba", "abcabc"), ("edcba", "edcba"), ("h", "hhh")],
  ref=ref_custom, tags=["string", "sorting", "hash-table", "counting"],
  time_complexity="O(n)", space_complexity="O(n)",
  hints=["Count character frequencies of s in a hash map.", "Emit characters in order's sequence, each repeated by its count.", "Append the leftover characters (not in order) in their original relative order."])
def ref_diagsort(mat):
    m = [row[:] for row in mat]
    R, C = len(m), len(m[0])
    diags = defaultdict(list)
    for r in range(R):
        for c in range(C):
            diags[r - c].append(m[r][c])
    for k in diags:
        diags[k].sort(reverse=True)
    for r in range(R):
        for c in range(C):
            m[r][c] = diags[r - c].pop()
    return m

q(id="sort-the-matrix-diagonally", title="Sort the Matrix Diagonally", difficulty="Medium",
  description="A matrix diagonal is a diagonal line of cells starting from some cell in either the topmost row or leftmost column and going in the bottom-right direction. Given an m x n integer matrix mat, sort each matrix diagonal in ascending order and return the resulting matrix.",
  examples=[("mat = [[3, 3, 1, 1], [2, 2, 1, 2], [1, 1, 1, 2]]", "[[1, 1, 1, 1], [1, 2, 2, 2], [1, 2, 3, 3]]", "Each diagonal sorted ascending."),
            ("mat = [[1]]", "[[1]]", "A single cell is unchanged.")],
  constraints=["1 <= m, n <= 100", "1 <= mat[i][j] <= 100"],
  method_name="diagonalSort", return_type="int[][]", params=[("mat", "int[][]")],
  sample_args=[([[3, 3, 1, 1], [2, 2, 1, 2], [1, 1, 1, 2]],), ([[1]],)],
  hidden_args=[([[4, 3], [2, 1]],), ([[3, 2, 1]],), ([[1], [2], [3]],), ([[5, 4, 3, 2, 1], [1, 2, 3, 4, 5]],), ([[11, 25, 66, 1, 69, 7], [23, 55, 17, 45, 15, 52], [75, 31, 36, 44, 58, 8], [22, 27, 33, 25, 68, 4], [84, 28, 14, 11, 5, 50]],), ([[9, 8], [7, 6], [5, 4]],)],
  ref=ref_diagsort, tags=["array", "matrix", "sorting"],
  time_complexity="O(m * n log(min(m, n)))", space_complexity="O(m * n)",
  hints=["Cells on the same diagonal share the key (row - col).", "Group values by that key in a hash map, sort each group.", "Write the sorted values back along each diagonal."])
def ref_freetime(intervals):
    events = sorted(intervals)
    merged = []
    for s, e in events:
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return [[merged[i][1], merged[i + 1][0]] for i in range(len(merged) - 1) if merged[i][1] < merged[i + 1][0]]

q(id="employee-free-time", title="Employee Free Time", difficulty="Hard",
  description="You are given the combined busy schedule of all employees as a list of [start, end] working intervals (unsorted, possibly overlapping). Return the list of finite intervals representing common free time for all employees (periods when nobody is working), sorted in ascending order.",
  examples=[("intervals = [[1, 2], [5, 6], [1, 3], [4, 10]]", "[[3, 4]]", "Merged busy time is [1, 3] and [4, 10]; everyone is free only between 3 and 4."),
            ("intervals = [[1, 3], [6, 7], [2, 4], [2, 5], [9, 12]]", "[[5, 6], [7, 9]]", "Merged busy time is [1, 5], [6, 7], [9, 12]; free periods are [5, 6] and [7, 9].")],
  constraints=["1 <= intervals.length <= 2500", "0 <= start < end <= 10^8"],
  method_name="employeeFreeTime", return_type="List<List<Integer>>", params=[("intervals", "int[][]")],
  sample_args=[([[1, 2], [5, 6], [1, 3], [4, 10]],), ([[1, 3], [6, 7], [2, 4], [2, 5], [9, 12]],)],
  hidden_args=[([[1, 2]],), ([[1, 2], [3, 4]],), ([[1, 5], [6, 10], [2, 3], [7, 8]],), ([[1, 2], [2, 3]],), ([[1, 10], [2, 3], [4, 5]],), ([[1, 3], [4, 6], [7, 9]],)],
  ref=ref_freetime, tags=["array", "sorting", "intervals", "heap", "sweep-line"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Sort all busy intervals by start time.", "Merge overlapping intervals into consolidated busy periods.", "Gaps between consecutive merged intervals are the common free times."])

def ref_jobs(startTime, endTime, profit):
    jobs = sorted(zip(startTime, endTime, profit), key=lambda j: j[1])
    ends = [j[1] for j in jobs]
    dp = [0] * len(jobs)
    import bisect as bs
    for i, (s, e, p) in enumerate(jobs):
        j = bs.bisect_right(ends, s, 0, i) - 1
        take = p + (dp[j] if j >= 0 else 0)
        skip = dp[i - 1] if i > 0 else 0
        dp[i] = max(take, skip)
    return dp[-1] if dp else 0

q(id="maximum-profit-in-job-scheduling", title="Maximum Profit in Job Scheduling", difficulty="Hard",
  description="We have n jobs with startTime[i], endTime[i], and profit[i]. Each job takes the half-open interval [startTime[i], endTime[i]). Choose a subset of non-overlapping jobs to maximize total profit, and return that maximum profit.",
  examples=[("startTime = [1, 2, 3, 3], endTime = [3, 4, 5, 6], profit = [50, 10, 40, 70]", "120", "Jobs 0 and 3: 50 + 70."),
            ("startTime = [1, 2, 3, 4, 6], endTime = [3, 5, 10, 6, 9], profit = [20, 20, 100, 70, 60]", "150", "Jobs 0, 3, 4: 20 + 70 + 60."),
            ("startTime = [1, 1, 1], endTime = [2, 3, 4], profit = [5, 6, 4]", "6", "Only job 1 (profit 6) alone is best.")],
  constraints=["1 <= startTime.length <= 5 * 10^4", "1 <= startTime[i] < endTime[i] <= 10^9", "1 <= profit[i] <= 10^4"],
  method_name="jobScheduling", return_type="int", params=[("startTime", "int[]"), ("endTime", "int[]"), ("profit", "int[]")],
  sample_args=[([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]), ([1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60])],
  hidden_args=[([1, 1, 1], [2, 3, 4], [5, 6, 4]), ([1], [2], [100]), ([1, 2], [2, 3], [10, 20]), ([1, 3, 5], [2, 4, 6], [10, 20, 30]), ([1, 2, 3], [4, 5, 6], [5, 5, 5]), ([4, 2, 4, 8, 2], [5, 5, 5, 10, 3], [5, 50, 20, 100, 5])],
  ref=ref_jobs, tags=["array", "sorting", "intervals", "dynamic-programming", "binary-search"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Sort jobs by end time; this is weighted interval scheduling.", "dp[i] = max profit considering jobs up to i.", "For job i, binary search the latest job ending <= startTime[i]; dp[i] = max(dp[i-1], profit[i] + dp[j])."])

def ref_mininterval(intervals, queries):
    # brute force is fine for the small test sizes; production uses sort-by-size + heap sweep
    out = []
    for qq in queries:
        best = None
        for s, e in intervals:
            if s <= qq <= e:
                sz = e - s + 1
                if best is None or sz < best:
                    best = sz
        out.append(best if best is not None else -1)
    return out

q(id="minimum-interval-to-include-each-query", title="Minimum Interval to Include Each Query", difficulty="Hard",
  description="You are given a 2D integer array intervals where intervals[i] = [lefti, righti] describes the ith interval, and an integer array queries. For each queries[j], find the size (right - left + 1) of the smallest interval that includes queries[j]. If no interval includes it, return -1 for that query. Return the answers in the original query order.",
  examples=[("intervals = [[1, 4], [2, 4], [3, 6], [4, 4]], queries = [2, 3, 4, 5]", "[3, 3, 1, 4]", "Smallest covering intervals have sizes 3, 3, 1, 4."),
            ("intervals = [[2, 3], [2, 5], [1, 8], [20, 25]], queries = [2, 19, 5, 22]", "[2, -1, 4, 6]", "Query 19 is covered by nothing.")],
  constraints=["1 <= intervals.length <= 10^5", "1 <= queries.length <= 10^5", "1 <= lefti <= righti <= 10^7", "1 <= queries[j] <= 10^7"],
  method_name="minInterval", return_type="int[]", params=[("intervals", "int[][]"), ("queries", "int[]")],
  sample_args=[([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]), ([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22])],
  hidden_args=[([[1, 2]], [3]), ([[1, 10]], [5]), ([[1, 4], [2, 3]], [2, 3]), ([[4, 4], [3, 3]], [3, 4]), ([[1, 100], [50, 60]], [55, 5]), ([[10, 20], [15, 25], [5, 30]], [12, 22, 35])],
  ref=ref_mininterval, tags=["array", "sorting", "intervals", "heap", "sweep-line"],
  time_complexity="O((n + q) log n)", space_complexity="O(n + q)",
  hints=["Sort intervals by size ascending and queries ascending.", "Sweep queries in order, adding intervals whose left <= query into a min-heap keyed by right endpoint.", "Pop intervals with right < query; the heap top (if any) is the smallest covering interval."])

def ref_skyline(buildings):
    events = []
    for l, r, h in buildings:
        events.append((l, -h, r))
        events.append((r, h, 0))
    events.sort()
    live = [(0, float("inf"))]
    out = []
    for x, nh, r in events:
        if nh < 0:
            heapq.heappush(live, (nh, r))
        else:
            pass
        while live[0][1] <= x:
            heapq.heappop(live)
        cur = -live[0][0]
        if not out or out[-1][1] != cur:
            out.append([x, cur])
    return out

q(id="the-skyline-problem", title="The Skyline Problem", difficulty="Hard",
  description="A city's skyline is the outer contour of the silhouette formed by its buildings. Each building is [lefti, righti, heighti]. Given the buildings, return the skyline as a list of key points [x, height], sorted by x. Key points mark where the contour changes: the left edge of each maximal horizontal segment at its height, ending with the ground.",
  examples=[("buildings = [[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]]", "[[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]", "The classic skyline."),
            ("buildings = [[0, 2, 3], [2, 5, 3]]", "[[0, 3], [5, 0]]", "Adjacent buildings of equal height form one segment.")],
  constraints=["1 <= buildings.length <= 10^4", "0 <= lefti < righti <= 2^31 - 1", "1 <= heighti <= 2^31 - 1", "buildings is sorted by lefti ascending."],
  method_name="getSkyline", return_type="List<List<Integer>>", params=[("buildings", "int[][]")],
  sample_args=[([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]],), ([[0, 2, 3], [2, 5, 3]],)],
  hidden_args=[([[1, 2, 1], [1, 2, 2], [1, 2, 3]],), ([[0, 1, 1]],), ([[2, 4, 7], [2, 4, 5]],), ([[1, 5, 3], [1, 5, 3]],), ([[3, 7, 5], [4, 6, 8]],), ([[1, 3, 4], [2, 4, 2]],)],
  ref=ref_skyline, tags=["array", "sorting", "intervals", "heap", "sweep-line", "divide-and-conquer"],
  time_complexity="O(n log n)", space_complexity="O(n)",
  hints=["Turn each building into start/end events and sweep x from left to right.", "A max-heap (negated min-heap) tracks heights of currently active buildings.", "Whenever the max height changes at an event x, emit a key point [x, newHeight]."])

write_bank(P, Q)
