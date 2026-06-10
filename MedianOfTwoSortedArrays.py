# =============================================================================
# MEDIAN OF TWO SORTED ARRAYS
# =============================================================================
# PROBLEM: Given two already-sorted arrays, find the median of all the numbers
# combined — WITHOUT actually merging them — in O(log(m+n)) time.
#
# WHAT IS A MEDIAN?
#   The middle value when all numbers are sorted.
#   Odd count  → the single middle number:     [1,2,3]     → 2
#   Even count → average of the two middle:    [1,2,3,4]   → (2+3)/2 = 2.5
#
# WHY IS THIS HARD?
#   Merging then finding the middle would be O(m+n) — easy but too slow.
#   The challenge is doing it in O(log(m+n)) using binary search.
# =============================================================================


# =============================================================================
# 1. PYTHON  ✅  (active - try running this!)
# =============================================================================
#
# THE CORE IDEA — "partition" both arrays simultaneously:
#
# Imagine splitting ALL the numbers into a LEFT half and a RIGHT half,
# where every number on the left ≤ every number on the right.
# The median lives right at that split point.
#
# We make ONE cut in nums1 and ONE cut in nums2 such that:
#   - left side has exactly half the total numbers (or half+1 if odd total)
#   - the biggest number on the LEFT ≤ smallest number on the RIGHT
#
# If we choose cut position i in nums1, then we need exactly
#   half_len - i  elements from nums2 on the left side.
# So the cut in nums2 is determined automatically!
#
# We binary search on the cut position in nums1 (the shorter array).
#
# VISUAL EXAMPLE — nums1=[1,3], nums2=[2,4,5,6], total=6, half=3
#
#   Try i=1 (take 1 element from nums1's left):
#     nums1:  [ 1  |  3 ]          left_A=1,  right_A=3
#     nums2:  [ 2 4  |  5 6 ]      left_B=4,  right_B=5
#     Check: left_A(1) ≤ right_B(5) ✓   but  left_B(4) > right_A(3) ✗
#     → left side too small from nums1, move cut RIGHT (low = i+1)
#
#   Try i=2 (take 2 elements from nums1's left):
#     nums1:  [ 1 3  |  ]          left_A=3,  right_A=+inf
#     nums2:  [ 2  |  4 5 6 ]      left_B=2,  right_B=4
#     Check: left_A(3) ≤ right_B(4) ✓   and  left_B(2) ≤ right_A(+inf) ✓
#     → PERFECT PARTITION!
#     Even total → median = (max(left_A, left_B) + min(right_A, right_B)) / 2
#                         = (max(3,2)   + min(inf,4)) / 2
#                         = (3 + 4) / 2 = 3.5  ✓
#
# THE FOUR BOUNDARY VALUES:
#   left_A  = nums1[i-1]  (biggest left element from nums1, or -inf if i=0)
#   right_A = nums1[i]    (smallest right element from nums1, or +inf if i=m)
#   left_B  = nums2[j-1]  (same idea for nums2)
#   right_B = nums2[j]
#
# WHEN IS THE PARTITION CORRECT?
#   left_A <= right_B   AND   left_B <= right_A
#   If left_A > right_B → i is too big → move left (high = i-1)
#   If left_B > right_A → i is too small → move right (low = i+1)

def find_median_sorted_arrays(nums1, nums2):
    # Always binary search on the SHORTER array (fewer steps)
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half_len = (m + n + 1) // 2   # how many elements go on the LEFT side
                                   # (+1 handles odd totals: left gets the extra)

    low, high = 0, m   # i can range from 0 (take nothing from nums1) to m (take all)

    while low <= high:
        i = (low + high) // 2     # cut position in nums1
        j = half_len - i          # cut position in nums2 (determined by i)

        # The four boundary values (use -inf / +inf at the edges)
        left_A  = nums1[i - 1] if i > 0 else float('-inf')
        right_A = nums1[i]     if i < m else float('inf')
        left_B  = nums2[j - 1] if j > 0 else float('-inf')
        right_B = nums2[j]     if j < n else float('inf')

        if left_A > right_B:
            # nums1's left side is too big → move cut left
            high = i - 1

        elif left_B > right_A:
            # nums2's left side is too big → move cut right in nums1
            low = i + 1

        else:
            # PERFECT PARTITION ✓
            max_left  = max(left_A, left_B)   # biggest on the left half
            min_right = min(right_A, right_B) # smallest on the right half

            if (m + n) % 2 == 1:
                return float(max_left)         # odd total → left's max IS the median
            else:
                return (max_left + min_right) / 2.0   # even total → average the two middle


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(find_median_sorted_arrays([1, 3], [2]))          # → 2.0
print(find_median_sorted_arrays([1, 2], [3, 4]))       # → 2.5
print(find_median_sorted_arrays([0, 0], [0, 0]))       # → 0.0
print(find_median_sorted_arrays([], [1]))              # → 1.0
print(find_median_sorted_arrays([2], []))              # → 2.0


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# Identical logic. 'Infinity' and '-Infinity' are JavaScript's float inf values.
# Math.max / Math.min work like Python's max / min.
#
# function findMedianSortedArrays(nums1, nums2) {
#     if (nums1.length > nums2.length) {
#         [nums1, nums2] = [nums2, nums1];  // swap so nums1 is shorter
#     }
#
#     const m = nums1.length, n = nums2.length;
#     const halfLen = Math.floor((m + n + 1) / 2);
#     let low = 0, high = m;
#
#     while (low <= high) {
#         const i = Math.floor((low + high) / 2);
#         const j = halfLen - i;
#
#         const leftA  = i > 0 ? nums1[i - 1] : -Infinity;
#         const rightA = i < m ? nums1[i]     :  Infinity;
#         const leftB  = j > 0 ? nums2[j - 1] : -Infinity;
#         const rightB = j < n ? nums2[j]     :  Infinity;
#
#         if (leftA > rightB) {
#             high = i - 1;
#         } else if (leftB > rightA) {
#             low = i + 1;
#         } else {
#             const maxLeft  = Math.max(leftA, leftB);
#             const minRight = Math.min(rightA, rightB);
#             if ((m + n) % 2 === 1) return maxLeft;
#             return (maxLeft + minRight) / 2;
#         }
#     }
# }
#
# console.log(findMedianSortedArrays([1,3], [2]));      // → 2.0
# console.log(findMedianSortedArrays([1,2], [3,4]));    // → 2.5


# =============================================================================
# 3. JAVA
# =============================================================================
# Integer.MIN_VALUE / MAX_VALUE are Java's stand-ins for -inf / +inf.
# (Java doesn't have float('-inf') for integers.)
#
# class Solution {
#     public double findMedianSortedArrays(int[] nums1, int[] nums2) {
#         if (nums1.length > nums2.length) {
#             int[] temp = nums1; nums1 = nums2; nums2 = temp;
#         }
#
#         int m = nums1.length, n = nums2.length;
#         int halfLen = (m + n + 1) / 2;
#         int low = 0, high = m;
#
#         while (low <= high) {
#             int i = (low + high) / 2;
#             int j = halfLen - i;
#
#             int leftA  = (i > 0) ? nums1[i-1] : Integer.MIN_VALUE;
#             int rightA = (i < m) ? nums1[i]   : Integer.MAX_VALUE;
#             int leftB  = (j > 0) ? nums2[j-1] : Integer.MIN_VALUE;
#             int rightB = (j < n) ? nums2[j]   : Integer.MAX_VALUE;
#
#             if (leftA > rightB) {
#                 high = i - 1;
#             } else if (leftB > rightA) {
#                 low = i + 1;
#             } else {
#                 int maxLeft  = Math.max(leftA, leftB);
#                 int minRight = Math.min(rightA, rightB);
#                 if ((m + n) % 2 == 1) return maxLeft;
#                 return (maxLeft + minRight) / 2.0;
#             }
#         }
#         return 0.0;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# INT_MIN / INT_MAX from <climits> serve as -inf / +inf sentinels.
# The swap trick ensures we always search the shorter array.
#
# #include <vector>
# #include <algorithm>
# #include <climits>
# using namespace std;
#
# double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
#     if (nums1.size() > nums2.size()) swap(nums1, nums2);
#
#     int m = nums1.size(), n = nums2.size();
#     int halfLen = (m + n + 1) / 2;
#     int low = 0, high = m;
#
#     while (low <= high) {
#         int i = (low + high) / 2;
#         int j = halfLen - i;
#
#         int leftA  = (i > 0) ? nums1[i-1] : INT_MIN;
#         int rightA = (i < m) ? nums1[i]   : INT_MAX;
#         int leftB  = (j > 0) ? nums2[j-1] : INT_MIN;
#         int rightB = (j < n) ? nums2[j]   : INT_MAX;
#
#         if (leftA > rightB) {
#             high = i - 1;
#         } else if (leftB > rightA) {
#             low = i + 1;
#         } else {
#             int maxLeft  = max(leftA, leftB);
#             int minRight = min(rightA, rightB);
#             if ((m + n) % 2 == 1) return maxLeft;
#             return (maxLeft + minRight) / 2.0;
#         }
#     }
#     return 0.0;
# }


# =============================================================================
# 5. C#
# =============================================================================
# int.MinValue / int.MaxValue are C#'s sentinel values (same idea as Java).
# Array.Sort isn't needed since arrays are already sorted.
#
# public class Solution {
#     public double FindMedianSortedArrays(int[] nums1, int[] nums2) {
#         if (nums1.Length > nums2.Length) {
#             var temp = nums1; nums1 = nums2; nums2 = temp;
#         }
#
#         int m = nums1.Length, n = nums2.Length;
#         int halfLen = (m + n + 1) / 2;
#         int low = 0, high = m;
#
#         while (low <= high) {
#             int i = (low + high) / 2;
#             int j = halfLen - i;
#
#             int leftA  = (i > 0) ? nums1[i-1] : int.MinValue;
#             int rightA = (i < m) ? nums1[i]   : int.MaxValue;
#             int leftB  = (j > 0) ? nums2[j-1] : int.MinValue;
#             int rightB = (j < n) ? nums2[j]   : int.MaxValue;
#
#             if (leftA > rightB) {
#                 high = i - 1;
#             } else if (leftB > rightA) {
#                 low = i + 1;
#             } else {
#                 int maxLeft  = System.Math.Max(leftA, leftB);
#                 int minRight = System.Math.Min(rightA, rightB);
#                 if ((m + n) % 2 == 1) return maxLeft;
#                 return (maxLeft + minRight) / 2.0;
#             }
#         }
#         return 0.0;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# Go doesn't have a built-in swap for slices, so we reassign manually.
# math.MinInt32 / math.MaxInt32 serve as sentinels.
#
# import "math"
#
# func findMedianSortedArrays(nums1 []int, nums2 []int) float64 {
#     if len(nums1) > len(nums2) {
#         nums1, nums2 = nums2, nums1
#     }
#
#     m, n := len(nums1), len(nums2)
#     halfLen := (m + n + 1) / 2
#     low, high := 0, m
#
#     for low <= high {
#         i := (low + high) / 2
#         j := halfLen - i
#
#         leftA, rightA := math.MinInt32, math.MaxInt32
#         leftB, rightB := math.MinInt32, math.MaxInt32
#         if i > 0 { leftA  = nums1[i-1] }
#         if i < m { rightA = nums1[i]   }
#         if j > 0 { leftB  = nums2[j-1] }
#         if j < n { rightB = nums2[j]   }
#
#         if leftA > rightB {
#             high = i - 1
#         } else if leftB > rightA {
#             low = i + 1
#         } else {
#             maxLeft := leftA
#             if leftB > maxLeft { maxLeft = leftB }
#             minRight := rightA
#             if rightB < minRight { minRight = rightB }
#             if (m+n)%2 == 1 { return float64(maxLeft) }
#             return float64(maxLeft+minRight) / 2.0
#         }
#     }
#     return 0.0
# }


# =============================================================================
# 7. RUST
# =============================================================================
# i32::MIN / i32::MAX are Rust's sentinel values.
# Rust's strict type system means we cast to f64 explicitly for the division.
#
# fn find_median_sorted_arrays(nums1: Vec<i32>, nums2: Vec<i32>) -> f64 {
#     let (nums1, nums2) = if nums1.len() > nums2.len() {
#         (nums2, nums1)
#     } else {
#         (nums1, nums2)
#     };
#
#     let (m, n) = (nums1.len(), nums2.len());
#     let half_len = (m + n + 1) / 2;
#     let (mut low, mut high) = (0usize, m);
#
#     loop {
#         let i = (low + high) / 2;
#         let j = half_len - i;
#
#         let left_a  = if i > 0 { nums1[i-1] } else { i32::MIN };
#         let right_a = if i < m { nums1[i]   } else { i32::MAX };
#         let left_b  = if j > 0 { nums2[j-1] } else { i32::MIN };
#         let right_b = if j < n { nums2[j]   } else { i32::MAX };
#
#         if left_a > right_b {
#             high = i - 1;
#         } else if left_b > right_a {
#             low = i + 1;
#         } else {
#             let max_left  = left_a.max(left_b);
#             let min_right = right_a.min(right_b);
#             if (m + n) % 2 == 1 {
#                 return max_left as f64;
#             }
#             return (max_left + min_right) as f64 / 2.0;
#         }
#     }
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# Int.min / Int.max are Swift's sentinel values.
# The swap is done by reassigning with tuple destructuring, just like Python.
#
# func findMedianSortedArrays(_ nums1: [Int], _ nums2: [Int]) -> Double {
#     var a = nums1, b = nums2
#     if a.count > b.count { swap(&a, &b) }
#
#     let m = a.count, n = b.count
#     let halfLen = (m + n + 1) / 2
#     var low = 0, high = m
#
#     while low <= high {
#         let i = (low + high) / 2
#         let j = halfLen - i
#
#         let leftA  = i > 0 ? a[i-1] : Int.min
#         let rightA = i < m ? a[i]   : Int.max
#         let leftB  = j > 0 ? b[j-1] : Int.min
#         let rightB = j < n ? b[j]   : Int.max
#
#         if leftA > rightB {
#             high = i - 1
#         } else if leftB > rightA {
#             low = i + 1
#         } else {
#             let maxLeft  = max(leftA, leftB)
#             let minRight = min(rightA, rightB)
#             if (m + n) % 2 == 1 { return Double(maxLeft) }
#             return Double(maxLeft + minRight) / 2.0
#         }
#     }
#     return 0.0
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# Int.MIN_VALUE / Int.MAX_VALUE are Kotlin's sentinels (same as Java, since
# Kotlin runs on the JVM). .toDouble() explicitly converts for division.
#
# fun findMedianSortedArrays(nums1: IntArray, nums2: IntArray): Double {
#     var a = if (nums1.size <= nums2.size) nums1 else nums2
#     var b = if (nums1.size <= nums2.size) nums2 else nums1
#
#     val m = a.size; val n = b.size
#     val halfLen = (m + n + 1) / 2
#     var low = 0; var high = m
#
#     while (low <= high) {
#         val i = (low + high) / 2
#         val j = halfLen - i
#
#         val leftA  = if (i > 0) a[i-1] else Int.MIN_VALUE
#         val rightA = if (i < m) a[i]   else Int.MAX_VALUE
#         val leftB  = if (j > 0) b[j-1] else Int.MIN_VALUE
#         val rightB = if (j < n) b[j]   else Int.MAX_VALUE
#
#         when {
#             leftA > rightB -> high = i - 1
#             leftB > rightA -> low  = i + 1
#             else -> {
#                 val maxLeft  = maxOf(leftA, leftB)
#                 val minRight = minOf(rightA, rightB)
#                 return if ((m + n) % 2 == 1) maxLeft.toDouble()
#                        else (maxLeft + minRight) / 2.0
#             }
#         }
#     }
#     return 0.0
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# Float::INFINITY and -Float::INFINITY are Ruby's sentinel values.
# Ruby's integer division is automatic (5/2 = 2), so we use .to_f for the median.
#
# def find_median_sorted_arrays(nums1, nums2)
#   nums1, nums2 = nums2, nums1 if nums1.length > nums2.length
#
#   m, n = nums1.length, nums2.length
#   half_len = (m + n + 1) / 2
#   low, high = 0, m
#
#   while low <= high
#     i = (low + high) / 2
#     j = half_len - i
#
#     left_a  = i > 0 ? nums1[i-1] : -Float::INFINITY
#     right_a = i < m ? nums1[i]   :  Float::INFINITY
#     left_b  = j > 0 ? nums2[j-1] : -Float::INFINITY
#     right_b = j < n ? nums2[j]   :  Float::INFINITY
#
#     if left_a > right_b
#       high = i - 1
#     elsif left_b > right_a
#       low = i + 1
#     else
#       max_left  = [left_a,  left_b ].max
#       min_right = [right_a, right_b].min
#       return (m + n).odd? ? max_left.to_f : (max_left + min_right) / 2.0
#     end
#   end
# end
#
# puts find_median_sorted_arrays([1,3], [2])      # → 2.0
# puts find_median_sorted_arrays([1,2], [3,4])    # → 2.5


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use BINARY SEARCH ON THE PARTITION POINT:
#
#   ┌───────────────────────────────────────────────────────────────────┐
#   │  Goal: find a cut in nums1 (position i) and nums2 (position j)  │
#   │  such that the LEFT halves and RIGHT halves satisfy:             │
#   │                                                                   │
#   │    max(leftA, leftB)  ≤  min(rightA, rightB)                    │
#   │                                                                   │
#   │  Binary search adjusts i until that condition is met:           │
#   │    leftA > rightB  →  i too big  →  move left  (high = i-1)    │
#   │    leftB > rightA  →  i too small → move right (low  = i+1)    │
#   │    otherwise       →  perfect partition → compute median        │
#   │                                                                   │
#   │  Odd total  → median = max(leftA, leftB)                        │
#   │  Even total → median = (max(leftA,leftB) + min(rightA,rightB)) │
#   │                         / 2.0                                    │
#   └───────────────────────────────────────────────────────────────────┘
#
# Time complexity:  O(log(min(m,n)))  — binary search on the shorter array
#                   (which is ≤ O(log(m+n)) as required)
# Space complexity: O(1)             — only a handful of variables, no extra arrays
#
# This is genuinely one of the trickiest LeetCode problems. The -inf/+inf
# sentinel values are the key to handling edge cases (empty partitions)
# without cluttering the code with special cases. 🎯
# =============================================================================
