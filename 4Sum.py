# =============================================================================
# 4SUM
# =============================================================================
# PROBLEM: Find all unique quadruplets (4-element combos) that sum to target.
# Return them as a list of lists. No duplicate quadruplets allowed.
#
# HOW DOES THIS RELATE TO PREVIOUS PROBLEMS?
#   2Sum (problem 1):  find ONE pair  that sums to target.  O(n)
#   3Sum (problem 15): find ALL triples that sum to 0.      O(n^2)
#   4Sum (this):       find ALL quads  that sum to target.  O(n^3)
#
# THE PATTERN: each layer adds one more fixed pointer and one more loop.
#   2Sum: two pointers
#   3Sum: one fixed + two pointers
#   4Sum: two fixed  + two pointers  <- exactly what we do here
#
# EXAMPLES:
#   [1,0,-1,0,-2,2], target=0 -> [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
#   [2,2,2,2,2],     target=8 -> [[2,2,2,2]]
# =============================================================================


# =============================================================================
# 1. PYTHON  (active - try running this!)
# =============================================================================
#
# THE APPROACH -- Sort + Two Nested Fixed Loops + Two Pointers:
#
# Same idea as 3Sum, but we add one more fixed loop on the outside.
#
#   Outer loop: fix nums[i]  (the first number)
#   Inner loop: fix nums[j]  (the second number, j starts at i+1)
#   Two pointers: left = j+1, right = n-1
#   Find pairs where nums[i]+nums[j]+nums[left]+nums[right] == target
#
# DUPLICATE SKIPPING (same logic as 3Sum, applied to both fixed loops):
#   Skip duplicate values of i: if nums[i] == nums[i-1] and i > 0
#   Skip duplicate values of j: if nums[j] == nums[j-1] and j > i+1
#   After finding a quad, skip duplicate left and right values.
#
# EARLY EXIT TRICKS (optional but good for performance):
#   If nums[i]+nums[i+1]+nums[i+2]+nums[i+3] > target -> break outer loop
#     (smallest possible sum with this i is already too big)
#   If nums[i]+nums[n-1]+nums[n-2]+nums[n-3] < target -> continue to next i
#     (largest possible sum with this i is still too small)
#
# STEP-BY-STEP with [1,0,-1,0,-2,2], target=0:
#
#   Sorted: [-2,-1,0,0,1,2]
#
#   i=0, fixed_1=-2:
#     j=1, fixed_2=-1:
#       l=2(0), r=5(2): sum=-2-1+0+2=-1 <0 -> l++
#       l=3(0), r=5(2): sum=-2-1+0+2=-1 <0 -> l++
#       l=4(1), r=5(2): sum=-2-1+1+2=0  FOUND! [-2,-1,1,2]
#                       l++, r-- -> l=5, l>=r, stop this j
#     j=2, fixed_2=0:
#       l=3(0), r=5(2): sum=-2+0+0+2=0  FOUND! [-2,0,0,2]
#                       l++, r-- -> l=4, r=4, l>=r, stop this j
#     j=3, fixed_2=0:   nums[3]==nums[2] -> SKIP (duplicate j)
#     j=4, fixed_2=1:
#       l=5(2), r=5(2): l>=r, stop immediately
#
#   i=1, fixed_1=-1:
#     j=2, fixed_2=0:
#       l=3(0), r=5(2): sum=-1+0+0+2=1 >0 -> r--
#       l=3(0), r=4(1): sum=-1+0+0+1=0  FOUND! [-1,0,0,1]
#                       l++, r-- -> l=4, r=3, l>=r, stop this j
#     j=3, fixed_2=0:   nums[3]==nums[2] -> SKIP
#     j=4, fixed_2=1:
#       l=5(2), r=5(2): l>=r, stop
#
#   i=2, fixed_1=0:
#     j=3, fixed_2=0:
#       l=4(1), r=5(2): sum=0+0+1+2=3 >0 -> r--
#       r=4, l>=r, stop
#     j=4, fixed_2=1:
#       l=5(2), r=5(2): l>=r, stop
#
#   i=3, fixed_1=0:   nums[3]==nums[2] -> SKIP
#   i=4, fixed_1=1:   i >= n-3, stop outer loop
#
#   Result: [[-2,-1,1,2], [-2,0,0,2], [-1,0,0,1]] ✓

def four_sum(nums, target):
    nums.sort()
    n = len(nums)
    result = []

    for i in range(n - 3):
        # Skip duplicate values for the first fixed number
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        for j in range(i + 1, n - 2):
            # Skip duplicate values for the second fixed number
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue

            left  = j + 1
            right = n - 1

            while left < right:
                total = nums[i] + nums[j] + nums[left] + nums[right]

                if total < target:
                    left  += 1
                elif total > target:
                    right -= 1
                else:
                    # Found a valid quadruplet!
                    result.append([nums[i], nums[j], nums[left], nums[right]])

                    # Skip duplicates on both sides
                    while left < right and nums[left]  == nums[left  + 1]:
                        left  += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1

                    left  += 1
                    right -= 1

    return result


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(four_sum([1, 0, -1, 0, -2, 2], 0))   # -> [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
print(four_sum([2, 2, 2, 2, 2], 8))         # -> [[2,2,2,2]]
print(four_sum([0, 0, 0, 0], 0))            # -> [[0,0,0,0]]


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# Same two nested loops + two pointers. Numeric sort (a,b) => a-b is essential.
# The duplicate-skip logic is identical to 3Sum.
#
# function fourSum(nums, target) {
#     nums.sort((a, b) => a - b);
#     const n = nums.length;
#     const result = [];
#
#     for (let i = 0; i < n - 3; i++) {
#         if (i > 0 && nums[i] === nums[i - 1]) continue;
#
#         for (let j = i + 1; j < n - 2; j++) {
#             if (j > i + 1 && nums[j] === nums[j - 1]) continue;
#
#             let left = j + 1, right = n - 1;
#
#             while (left < right) {
#                 const total = nums[i] + nums[j] + nums[left] + nums[right];
#
#                 if      (total < target) left++;
#                 else if (total > target) right--;
#                 else {
#                     result.push([nums[i], nums[j], nums[left], nums[right]]);
#                     while (left < right && nums[left]  === nums[left  + 1]) left++;
#                     while (left < right && nums[right] === nums[right - 1]) right--;
#                     left++;
#                     right--;
#                 }
#             }
#         }
#     }
#
#     return result;
# }
#
# console.log(fourSum([1,0,-1,0,-2,2], 0));
# // -> [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]


# =============================================================================
# 3. JAVA
# =============================================================================
# Arrays.sort() for in-place sort. List<List<Integer>> holds the result.
# long is used for total to avoid integer overflow:
#   nums[i] can be up to 10^9, and 4 * 10^9 overflows a 32-bit int.
#
# import java.util.*;
#
# class Solution {
#     public List<List<Integer>> fourSum(int[] nums, int target) {
#         Arrays.sort(nums);
#         int n = nums.length;
#         List<List<Integer>> result = new ArrayList<>();
#
#         for (int i = 0; i < n - 3; i++) {
#             if (i > 0 && nums[i] == nums[i - 1]) continue;
#
#             for (int j = i + 1; j < n - 2; j++) {
#                 if (j > i + 1 && nums[j] == nums[j - 1]) continue;
#
#                 int left = j + 1, right = n - 1;
#
#                 while (left < right) {
#                     // Use long to prevent overflow: 4 * 10^9 > Integer.MAX_VALUE
#                     long total = (long)nums[i] + nums[j] + nums[left] + nums[right];
#
#                     if      (total < target) left++;
#                     else if (total > target) right--;
#                     else {
#                         result.add(Arrays.asList(nums[i], nums[j], nums[left], nums[right]));
#                         while (left < right && nums[left]  == nums[left  + 1]) left++;
#                         while (left < right && nums[right] == nums[right - 1]) right--;
#                         left++;
#                         right--;
#                     }
#                 }
#             }
#         }
#
#         return result;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# long long for the total sum to prevent overflow (same reason as Java).
# vector<vector<int>> holds the quadruplets.
#
# #include <vector>
# #include <algorithm>
# using namespace std;
#
# vector<vector<int>> fourSum(vector<int>& nums, int target) {
#     sort(nums.begin(), nums.end());
#     int n = nums.size();
#     vector<vector<int>> result;
#
#     for (int i = 0; i < n - 3; i++) {
#         if (i > 0 && nums[i] == nums[i - 1]) continue;
#
#         for (int j = i + 1; j < n - 2; j++) {
#             if (j > i + 1 && nums[j] == nums[j - 1]) continue;
#
#             int left = j + 1, right = n - 1;
#
#             while (left < right) {
#                 long long total = (long long)nums[i] + nums[j] + nums[left] + nums[right];
#
#                 if      (total < target) left++;
#                 else if (total > target) right--;
#                 else {
#                     result.push_back({nums[i], nums[j], nums[left], nums[right]});
#                     while (left < right && nums[left]  == nums[left  + 1]) left++;
#                     while (left < right && nums[right] == nums[right - 1]) right--;
#                     left++;
#                     right--;
#                 }
#             }
#         }
#     }
#
#     return result;
# }


# =============================================================================
# 5. C#
# =============================================================================
# Same structure as Java. (long) cast prevents overflow during summation.
# IList<IList<int>> is the return type for LeetCode's C# submissions.
#
# using System.Collections.Generic;
#
# public class Solution {
#     public IList<IList<int>> FourSum(int[] nums, int target) {
#         System.Array.Sort(nums);
#         int n = nums.Length;
#         var result = new List<IList<int>>();
#
#         for (int i = 0; i < n - 3; i++) {
#             if (i > 0 && nums[i] == nums[i - 1]) continue;
#
#             for (int j = i + 1; j < n - 2; j++) {
#                 if (j > i + 1 && nums[j] == nums[j - 1]) continue;
#
#                 int left = j + 1, right = n - 1;
#
#                 while (left < right) {
#                     long total = (long)nums[i] + nums[j] + nums[left] + nums[right];
#
#                     if      (total < target) left++;
#                     else if (total > target) right--;
#                     else {
#                         result.Add(new List<int> { nums[i], nums[j], nums[left], nums[right] });
#                         while (left < right && nums[left]  == nums[left  + 1]) left++;
#                         while (left < right && nums[right] == nums[right - 1]) right--;
#                         left++;
#                         right--;
#                     }
#                 }
#             }
#         }
#
#         return result;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# sort.Ints() sorts in place. [][]int holds the result.
# int in Go is 64-bit on 64-bit platforms so overflow isn't a concern here,
# but it's still good practice to be aware of the limits.
#
# import "sort"
#
# func fourSum(nums []int, target int) [][]int {
#     sort.Ints(nums)
#     n := len(nums)
#     result := [][]int{}
#
#     for i := 0; i < n-3; i++ {
#         if i > 0 && nums[i] == nums[i-1] { continue }
#
#         for j := i + 1; j < n-2; j++ {
#             if j > i+1 && nums[j] == nums[j-1] { continue }
#
#             left, right := j+1, n-1
#
#             for left < right {
#                 total := nums[i] + nums[j] + nums[left] + nums[right]
#
#                 if      total < target { left++  }
#                 else if total > target { right-- }
#                 else {
#                     result = append(result, []int{nums[i], nums[j], nums[left], nums[right]})
#                     for left < right && nums[left]  == nums[left+1]  { left++  }
#                     for left < right && nums[right] == nums[right-1] { right-- }
#                     left++
#                     right--
#                 }
#             }
#         }
#     }
#
#     return result
# }


# =============================================================================
# 7. RUST
# =============================================================================
# i64 for the total to prevent overflow (i32 max is ~2.1 billion;
# 4 * 10^9 overflows it). .sort() sorts Vec<i32> in place.
#
# fn four_sum(mut nums: Vec<i32>, target: i32) -> Vec<Vec<i32>> {
#     nums.sort();
#     let n = nums.len();
#     let mut result = Vec::new();
#
#     for i in 0..n.saturating_sub(3) {
#         if i > 0 && nums[i] == nums[i - 1] { continue; }
#
#         for j in (i + 1)..n.saturating_sub(2) {
#             if j > i + 1 && nums[j] == nums[j - 1] { continue; }
#
#             let mut left  = j + 1;
#             let mut right = n - 1;
#
#             while left < right {
#                 let total = nums[i] as i64 + nums[j] as i64
#                           + nums[left] as i64 + nums[right] as i64;
#                 let t = target as i64;
#
#                 if      total < t { left  += 1; }
#                 else if total > t { right -= 1; }
#                 else {
#                     result.push(vec![nums[i], nums[j], nums[left], nums[right]]);
#                     while left < right && nums[left]  == nums[left  + 1] { left  += 1; }
#                     while left < right && nums[right] == nums[right - 1] { right -= 1; }
#                     left  += 1;
#                     right -= 1;
#                 }
#             }
#         }
#     }
#
#     result
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# .sorted() returns a new sorted array. [[Int]] holds the result.
# Swift's Int is 64-bit on 64-bit platforms, so no overflow concern.
#
# func fourSum(_ nums: [Int], _ target: Int) -> [[Int]] {
#     let nums = nums.sorted()
#     let n = nums.count
#     var result = [[Int]]()
#
#     for i in 0..<max(0, n - 3) {
#         if i > 0 && nums[i] == nums[i - 1] { continue }
#
#         for j in (i + 1)..<max(0, n - 2) {
#             if j > i + 1 && nums[j] == nums[j - 1] { continue }
#
#             var left = j + 1, right = n - 1
#
#             while left < right {
#                 let total = nums[i] + nums[j] + nums[left] + nums[right]
#
#                 if      total < target { left  += 1 }
#                 else if total > target { right -= 1 }
#                 else {
#                     result.append([nums[i], nums[j], nums[left], nums[right]])
#                     while left < right && nums[left]  == nums[left  + 1] { left  += 1 }
#                     while left < right && nums[right] == nums[right - 1] { right -= 1 }
#                     left  += 1
#                     right -= 1
#                 }
#             }
#         }
#     }
#
#     return result
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# sorted() returns a new sorted list. mutableListOf<List<Int>>() holds results.
# toLong() prevents overflow when summing four Int values.
#
# fun fourSum(nums: IntArray, target: Int): List<List<Int>> {
#     val sorted = nums.sorted()
#     val n = sorted.size
#     val result = mutableListOf<List<Int>>()
#
#     for (i in 0 until n - 3) {
#         if (i > 0 && sorted[i] == sorted[i - 1]) continue
#
#         for (j in i + 1 until n - 2) {
#             if (j > i + 1 && sorted[j] == sorted[j - 1]) continue
#
#             var left = j + 1; var right = n - 1
#
#             while (left < right) {
#                 val total = sorted[i].toLong() + sorted[j] + sorted[left] + sorted[right]
#
#                 when {
#                     total < target -> left++
#                     total > target -> right--
#                     else -> {
#                         result.add(listOf(sorted[i], sorted[j], sorted[left], sorted[right]))
#                         while (left < right && sorted[left]  == sorted[left  + 1]) left++
#                         while (left < right && sorted[right] == sorted[right - 1]) right--
#                         left++; right--
#                     }
#                 }
#             }
#         }
#     }
#
#     return result
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# .sort returns a new sorted array. Ruby integers are arbitrary precision
# so no overflow is possible -- no casting needed.
#
# def four_sum(nums, target)
#   nums = nums.sort
#   n = nums.length
#   result = []
#
#   (0..n - 4).each do |i|
#     next if i > 0 && nums[i] == nums[i - 1]
#
#     (i + 1..n - 3).each do |j|
#       next if j > i + 1 && nums[j] == nums[j - 1]
#
#       left, right = j + 1, n - 1
#
#       while left < right
#         total = nums[i] + nums[j] + nums[left] + nums[right]
#
#         if    total < target then left  += 1
#         elsif total > target then right -= 1
#         else
#           result << [nums[i], nums[j], nums[left], nums[right]]
#           left  += 1 while left  < right && nums[left]  == nums[left  + 1]
#           right -= 1 while left  < right && nums[right] == nums[right - 1]
#           left  += 1
#           right -= 1
#         end
#       end
#     end
#   end
#
#   result
# end
#
# puts four_sum([1,0,-1,0,-2,2], 0).inspect
# # -> [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
# puts four_sum([2,2,2,2,2], 8).inspect
# # -> [[2,2,2,2]]


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use SORT + TWO FIXED LOOPS + TWO POINTERS:
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  Sort the array.                                                │
#   │                                                                  │
#   │  For i in range(n-3):          <- fix 1st number               │
#   │    skip if duplicate i                                          │
#   │    For j in range(i+1, n-2):   <- fix 2nd number               │
#   │      skip if duplicate j                                        │
#   │      left = j+1, right = n-1   <- two pointers                 │
#   │      While left < right:                                        │
#   │        total = nums[i]+nums[j]+nums[left]+nums[right]          │
#   │        total < target -> left++                                 │
#   │        total > target -> right--                                │
#   │        total == target -> save quad, skip dups, move both      │
#   └──────────────────────────────────────────────────────────────────┘
#
# THE GENERALISATION PATTERN:
#   2Sum  -> 2 pointers
#   3Sum  -> 1 fixed loop + 2 pointers
#   4Sum  -> 2 fixed loops + 2 pointers
#   kSum  -> (k-2) fixed loops + 2 pointers  (recursive generalisation)
#
# OVERFLOW WARNING (Java / C++ / C# / Kotlin / Rust):
#   nums[i] can be up to 10^9. Adding four of them: 4 * 10^9 > 2^31 - 1.
#   Always use long / long long / i64 for the sum in these languages!
#   Python, Ruby, Go, and Swift don't have this problem (arbitrary-precision
#   or 64-bit integers by default).
#
# Time complexity:  O(n^3)  -- two fixed loops O(n^2) + two-pointer O(n)
# Space complexity: O(n)    -- for the sort stack, plus output quadruplets
# =============================================================================
