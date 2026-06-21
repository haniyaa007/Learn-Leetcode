# =============================================================================
# 3SUM
# =============================================================================
# PROBLEM: Find all unique triplets in the array that sum to zero.
# Return them as a list of lists. No duplicate triplets allowed.
#
# EXAMPLES:
#   [-1,0,1,2,-1,-4]  ->  [[-1,-1,2], [-1,0,1]]
#   [0,1,1]           ->  []
#   [0,0,0]           ->  [[0,0,0]]
#
# WHY IS THIS HARDER THAN 2SUM?
#   - Three numbers instead of two.
#   - We need ALL valid triplets, not just one pair.
#   - We must avoid returning duplicates (e.g. [-1,0,1] and [0,-1,1] are the same).
#
# THE NAIVE APPROACH (too slow):
#   Three nested loops, check every combination: O(n^3).
#   For n=3000 that's 27 billion operations. Way too slow.
#
# THE SMART APPROACH:
#   Sort + two pointers: O(n^2). Fast enough and elegant.
# =============================================================================


# =============================================================================
# 1. PYTHON  (active - try running this!)
# =============================================================================
#
# THE APPROACH -- Sort first, then fix one number and use two pointers:
#
# KEY IDEA: Once the array is sorted, we can use the two-pointer trick
# from problem 11 (Container with Most Water) to efficiently find pairs.
#
# STEP 1 -- Sort the array.
#   Sorting makes it easy to skip duplicates and use two pointers.
#   [-1,0,1,2,-1,-4]  ->  sorted: [-4,-1,-1,0,1,2]
#
# STEP 2 -- Fix one number (the outermost loop), find the other two.
#   For each index i (the "fixed" number):
#     Set left  = i + 1  (just right of the fixed number)
#     Set right = n - 1  (the far end)
#     Use two pointers to find pairs that sum to  -nums[i]
#     (because we need  nums[i] + nums[left] + nums[right] == 0)
#
# STEP 3 -- Move the pointers based on the sum:
#   total = nums[i] + nums[left] + nums[right]
#   total < 0  -> need a bigger sum -> move left  pointer RIGHT  (bigger value)
#   total > 0  -> need a smaller sum -> move right pointer LEFT  (smaller value)
#   total == 0 -> FOUND A TRIPLET! Record it, then move BOTH pointers inward.
#
# STEP 4 -- Skip duplicates (the tricky part):
#   After sorting, duplicates sit right next to each other.
#   a) Skip duplicate values of the FIXED number i:
#      If nums[i] == nums[i-1], we've already found all triplets with this value.
#   b) Skip duplicate values at the LEFT pointer after finding a triplet:
#      Move left forward while nums[left] == nums[left-1]
#   c) Skip duplicate values at the RIGHT pointer after finding a triplet:
#      Move right backward while nums[right] == nums[right+1]
#
# STEP-BY-STEP with [-4,-1,-1,0,1,2] (already sorted):
#
#   i=0, fixed=-4:  left=1(-1) right=5(2)  sum=-4-1+2=-3 <0  -> left++
#                   left=2(-1) right=5(2)  sum=-4-1+2=-3 <0  -> left++
#                   left=3(0)  right=5(2)  sum=-4+0+2=-2 <0  -> left++
#                   left=4(1)  right=5(2)  sum=-4+1+2=-1 <0  -> left++
#                   left=5, left>=right, STOP this i.
#
#   i=1, fixed=-1:  left=2(-1) right=5(2)  sum=-1-1+2=0  FOUND! [-1,-1,2]
#                   Move both: left=3, right=4
#                   left=3(0)  right=4(1)  sum=-1+0+1=0  FOUND! [-1,0,1]
#                   Move both: left=4, right=3  left>=right, STOP.
#
#   i=2, fixed=-1:  nums[2]==nums[1] -> SKIP (duplicate fixed value)
#
#   i=3, fixed=0:   left=4(1) right=5(2)  sum=0+1+2=3 >0  -> right--
#                   right=4, left>=right, STOP.
#
#   i=4, fixed=1:   i >= n-2, STOP outer loop (need at least 2 more elements).
#
#   Result: [[-1,-1,2], [-1,0,1]] ✓

def three_sum(nums):
    nums.sort()              # sort first -- crucial for two pointers and dedup
    result = []
    n = len(nums)

    for i in range(n - 2):  # leave room for at least two more elements

        # Skip duplicate values for the fixed number
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        # Early exit: if the smallest possible sum is already > 0, stop
        # (array is sorted, so nums[i] is the smallest; if it's > 0,
        #  adding two more positive numbers can never reach 0)
        if nums[i] > 0:
            break

        left  = i + 1
        right = n - 1

        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total < 0:
                left += 1    # sum too small -> need a bigger left value
            elif total > 0:
                right -= 1   # sum too big  -> need a smaller right value
            else:
                # Found a valid triplet!
                result.append([nums[i], nums[left], nums[right]])

                # Skip duplicates on both sides before moving on
                while left < right and nums[left]  == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1

                # Move both pointers inward to look for more triplets
                left  += 1
                right -= 1

    return result


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(three_sum([-1, 0, 1, 2, -1, -4]))   # -> [[-1,-1,2],[-1,0,1]]
print(three_sum([0, 1, 1]))                # -> []
print(three_sum([0, 0, 0]))               # -> [[0,0,0]]
print(three_sum([-2, 0, 0, 2, 2]))        # -> [[-2,0,2]]


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# Array.sort() in JS sorts LEXICOGRAPHICALLY by default (treats items as strings!).
# Always pass a comparator (a, b) => a - b for numeric sort.
#
# function threeSum(nums) {
#     nums.sort((a, b) => a - b);   // numeric sort -- critical!
#     const result = [];
#     const n = nums.length;
#
#     for (let i = 0; i < n - 2; i++) {
#         if (i > 0 && nums[i] === nums[i - 1]) continue;  // skip duplicate fixed
#         if (nums[i] > 0) break;                           // early exit
#
#         let left = i + 1, right = n - 1;
#
#         while (left < right) {
#             const total = nums[i] + nums[left] + nums[right];
#
#             if      (total < 0) left++;
#             else if (total > 0) right--;
#             else {
#                 result.push([nums[i], nums[left], nums[right]]);
#                 while (left < right && nums[left]  === nums[left  + 1]) left++;
#                 while (left < right && nums[right] === nums[right - 1]) right--;
#                 left++;
#                 right--;
#             }
#         }
#     }
#
#     return result;
# }
#
# console.log(threeSum([-1,0,1,2,-1,-4]));  // -> [[-1,-1,2],[-1,0,1]]
# console.log(threeSum([0,0,0]));            // -> [[0,0,0]]


# =============================================================================
# 3. JAVA
# =============================================================================
# Arrays.sort() sorts in place. List<List<Integer>> holds the result.
# ArrayList is Java's dynamic list. The rest is the same pattern.
#
# import java.util.*;
#
# class Solution {
#     public List<List<Integer>> threeSum(int[] nums) {
#         Arrays.sort(nums);
#         List<List<Integer>> result = new ArrayList<>();
#         int n = nums.length;
#
#         for (int i = 0; i < n - 2; i++) {
#             if (i > 0 && nums[i] == nums[i - 1]) continue;
#             if (nums[i] > 0) break;
#
#             int left = i + 1, right = n - 1;
#
#             while (left < right) {
#                 int total = nums[i] + nums[left] + nums[right];
#
#                 if      (total < 0) left++;
#                 else if (total > 0) right--;
#                 else {
#                     result.add(Arrays.asList(nums[i], nums[left], nums[right]));
#                     while (left < right && nums[left]  == nums[left  + 1]) left++;
#                     while (left < right && nums[right] == nums[right - 1]) right--;
#                     left++;
#                     right--;
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
# std::sort() sorts in place. vector<vector<int>> holds the triplets.
# The structured binding [i, left, right] pattern is the same as Java/Python.
#
# #include <vector>
# #include <algorithm>
# using namespace std;
#
# vector<vector<int>> threeSum(vector<int>& nums) {
#     sort(nums.begin(), nums.end());
#     vector<vector<int>> result;
#     int n = nums.size();
#
#     for (int i = 0; i < n - 2; i++) {
#         if (i > 0 && nums[i] == nums[i - 1]) continue;
#         if (nums[i] > 0) break;
#
#         int left = i + 1, right = n - 1;
#
#         while (left < right) {
#             int total = nums[i] + nums[left] + nums[right];
#
#             if      (total < 0) left++;
#             else if (total > 0) right--;
#             else {
#                 result.push_back({nums[i], nums[left], nums[right]});
#                 while (left < right && nums[left]  == nums[left  + 1]) left++;
#                 while (left < right && nums[right] == nums[right - 1]) right--;
#                 left++;
#                 right--;
#             }
#         }
#     }
#
#     return result;
# }


# =============================================================================
# 5. C#
# =============================================================================
# Array.Sort() sorts in place. List<List<int>> holds the result.
# new List<int> { a, b, c } creates a 3-element list inline.
#
# using System.Collections.Generic;
#
# public class Solution {
#     public IList<IList<int>> ThreeSum(int[] nums) {
#         Array.Sort(nums);
#         var result = new List<IList<int>>();
#         int n = nums.Length;
#
#         for (int i = 0; i < n - 2; i++) {
#             if (i > 0 && nums[i] == nums[i - 1]) continue;
#             if (nums[i] > 0) break;
#
#             int left = i + 1, right = n - 1;
#
#             while (left < right) {
#                 int total = nums[i] + nums[left] + nums[right];
#
#                 if      (total < 0) left++;
#                 else if (total > 0) right--;
#                 else {
#                     result.Add(new List<int> { nums[i], nums[left], nums[right] });
#                     while (left < right && nums[left]  == nums[left  + 1]) left++;
#                     while (left < right && nums[right] == nums[right - 1]) right--;
#                     left++;
#                     right--;
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
# sort.Ints() sorts in place. [][]int holds the result (slice of int slices).
# The duplicate-skipping loops are identical to every other language.
#
# import "sort"
#
# func threeSum(nums []int) [][]int {
#     sort.Ints(nums)
#     result := [][]int{}
#     n := len(nums)
#
#     for i := 0; i < n-2; i++ {
#         if i > 0 && nums[i] == nums[i-1] { continue }
#         if nums[i] > 0 { break }
#
#         left, right := i+1, n-1
#
#         for left < right {
#             total := nums[i] + nums[left] + nums[right]
#
#             if total < 0 {
#                 left++
#             } else if total > 0 {
#                 right--
#             } else {
#                 result = append(result, []int{nums[i], nums[left], nums[right]})
#                 for left < right && nums[left]  == nums[left+1]  { left++  }
#                 for left < right && nums[right] == nums[right-1] { right-- }
#                 left++
#                 right--
#             }
#         }
#     }
#
#     return result
# }


# =============================================================================
# 7. RUST
# =============================================================================
# .sort() sorts Vec<i32> in place. Vec<Vec<i32>> holds the triplets.
# The logic is identical; Rust just requires explicit mut and usize vs i32 care.
#
# fn three_sum(mut nums: Vec<i32>) -> Vec<Vec<i32>> {
#     nums.sort();
#     let mut result = Vec::new();
#     let n = nums.len();
#
#     for i in 0..n.saturating_sub(2) {
#         if i > 0 && nums[i] == nums[i - 1] { continue; }
#         if nums[i] > 0 { break; }
#
#         let mut left  = i + 1;
#         let mut right = n - 1;
#
#         while left < right {
#             let total = nums[i] + nums[left] + nums[right];
#
#             if total < 0 {
#                 left += 1;
#             } else if total > 0 {
#                 right -= 1;
#             } else {
#                 result.push(vec![nums[i], nums[left], nums[right]]);
#                 while left < right && nums[left]  == nums[left  + 1] { left  += 1; }
#                 while left < right && nums[right] == nums[right - 1] { right -= 1; }
#                 left  += 1;
#                 right -= 1;
#             }
#         }
#     }
#
#     result
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# .sorted() returns a new sorted array (non-mutating).
# var makes mutable variables. The rest is standard two-pointer logic.
#
# func threeSum(_ nums: [Int]) -> [[Int]] {
#     let nums = nums.sorted()
#     var result = [[Int]]()
#     let n = nums.count
#
#     for i in 0..<(n - 2) {
#         if i > 0 && nums[i] == nums[i - 1] { continue }
#         if nums[i] > 0 { break }
#
#         var left = i + 1, right = n - 1
#
#         while left < right {
#             let total = nums[i] + nums[left] + nums[right]
#
#             if total < 0 {
#                 left += 1
#             } else if total > 0 {
#                 right -= 1
#             } else {
#                 result.append([nums[i], nums[left], nums[right]])
#                 while left < right && nums[left]  == nums[left  + 1] { left  += 1 }
#                 while left < right && nums[right] == nums[right - 1] { right -= 1 }
#                 left  += 1
#                 right -= 1
#             }
#         }
#     }
#
#     return result
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# sorted() returns a new sorted list. mutableListOf() holds the result.
# The duplicate-skip logic is identical to every other language here.
#
# fun threeSum(nums: IntArray): List<List<Int>> {
#     val sorted = nums.sorted()
#     val result = mutableListOf<List<Int>>()
#     val n = sorted.size
#
#     for (i in 0 until n - 2) {
#         if (i > 0 && sorted[i] == sorted[i - 1]) continue
#         if (sorted[i] > 0) break
#
#         var left = i + 1; var right = n - 1
#
#         while (left < right) {
#             val total = sorted[i] + sorted[left] + sorted[right]
#
#             when {
#                 total < 0 -> left++
#                 total > 0 -> right--
#                 else -> {
#                     result.add(listOf(sorted[i], sorted[left], sorted[right]))
#                     while (left < right && sorted[left]  == sorted[left  + 1]) left++
#                     while (left < right && sorted[right] == sorted[right - 1]) right--
#                     left++; right--
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
# .sort returns a new sorted array. push appends to an array.
# The next keyword skips to the next loop iteration (like Python's continue).
#
# def three_sum(nums)
#   nums = nums.sort
#   result = []
#   n = nums.length
#
#   (0..n - 3).each do |i|
#     next if i > 0 && nums[i] == nums[i - 1]   # skip duplicate fixed value
#     break if nums[i] > 0                        # early exit
#
#     left, right = i + 1, n - 1
#
#     while left < right
#       total = nums[i] + nums[left] + nums[right]
#
#       if    total < 0 then left  += 1
#       elsif total > 0 then right -= 1
#       else
#         result << [nums[i], nums[left], nums[right]]
#         left  += 1 while left  < right && nums[left]  == nums[left  + 1]
#         right -= 1 while left  < right && nums[right] == nums[right - 1]
#         left  += 1
#         right -= 1
#       end
#     end
#   end
#
#   result
# end
#
# puts three_sum([-1,0,1,2,-1,-4]).inspect   # -> [[-1,-1,2],[-1,0,1]]
# puts three_sum([0,0,0]).inspect            # -> [[0,0,0]]


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use SORT + FIX ONE + TWO POINTERS:
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  1. Sort the array.                                             │
#   │                                                                  │
#   │  2. For each index i (the "fixed" number):                      │
#   │       Skip if it's a duplicate of the previous fixed number.   │
#   │       Early exit if nums[i] > 0 (sum can't be 0).             │
#   │                                                                  │
#   │  3. Two-pointer search for the remaining two numbers:          │
#   │       left  = i + 1,  right = n - 1                           │
#   │       While left < right:                                       │
#   │         total < 0  -> left++   (need bigger value)             │
#   │         total > 0  -> right--  (need smaller value)            │
#   │         total == 0 -> record triplet                           │
#   │                       skip duplicate lefts and rights          │
#   │                       move both pointers inward                │
#   └──────────────────────────────────────────────────────────────────┘
#
# WHY SORT FIRST?
#   Sorting lets the two-pointer technique work (need ordered values to
#   know which direction to move). It also groups duplicates together
#   so we can skip them with a simple == check on adjacent elements.
#
# !! JAVASCRIPT GOTCHA !!
#   Always use .sort((a, b) => a - b) for numeric arrays in JS.
#   The default .sort() converts to strings: [10,9,2].sort() -> [10,2,9] WRONG!
#
# Time complexity:  O(n^2)  -- O(n log n) sort + O(n^2) two-pointer loop
# Space complexity: O(n)    -- for the sort (in-place but recursion stack),
#                              plus O(k) for the k triplets in the output
# =============================================================================
