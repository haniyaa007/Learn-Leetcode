# =============================================================================
# 3SUM CLOSEST
# =============================================================================
# PROBLEM: Find three numbers in the array whose sum is CLOSEST to the target.
# Return that sum (not the triplet itself).
# Exactly one solution is guaranteed.
#
# HOW IS THIS DIFFERENT FROM 3SUM (problem 15)?
#   - Problem 15: find all triplets that sum to EXACTLY 0.
#   - This problem: find the triplet whose sum is NEAREST to a given target.
#   - We return the best SUM we find, not the triplet itself.
#   - There's no need to handle duplicates (we just want the closest sum).
#
# EXAMPLES:
#   nums=[-1,2,1,-4], target=1
#     Possible sums: -1+2+1=2, -1+2-4=-3, -1+1-4=-4, 2+1-4=-1
#     Closest to 1 is 2.  -> return 2
#
#   nums=[0,0,0], target=1
#     Only sum: 0+0+0=0. Closest to 1 is 0. -> return 0
# =============================================================================


# =============================================================================
# 1. PYTHON  (active - try running this!)
# =============================================================================
#
# THE APPROACH -- same Sort + Fix + Two Pointers as problem 15, but:
#   Instead of looking for sum == 0, we track which sum is CLOSEST to target.
#
# HOW CLOSEST IS MEASURED:
#   Use absolute difference:  abs(sum - target)
#   The smaller this is, the closer we are to the target.
#
# TWO-POINTER DIRECTION:
#   total < target  -> sum is too small -> move LEFT  pointer RIGHT  (bigger value)
#   total > target  -> sum is too big   -> move RIGHT pointer LEFT   (smaller value)
#   total == target -> PERFECT MATCH, can't get closer -> return immediately
#
# STEP-BY-STEP with [-1,2,1,-4], target=1:
#
#   Sorted: [-4,-1,1,2]
#   best_sum = -4 + -1 + 1 = -4  (initialise to first triplet's sum)
#
#   i=0, fixed=-4:
#     left=1(-1), right=3(2): total=-4-1+2=-3   |(-3)-1|=4  vs |(- 4)-1|=5 -> update best=-3
#     -3 < 1 -> left++
#     left=2(1),  right=3(2): total=-4+1+2=-1   |(-1)-1|=2  vs |(-3)-1|=4  -> update best=-1
#     -1 < 1 -> left++
#     left=3, left>=right, stop this i.
#
#   i=1, fixed=-1:
#     left=2(1), right=3(2): total=-1+1+2=2     |2-1|=1     vs |(-1)-1|=2  -> update best=2
#     2 > 1 -> right--
#     right=2, left>=right, stop this i.
#
#   i=2, fixed=1:  i >= n-2, stop.
#
#   Answer: 2 ✓
#
# KEY SIMPLIFICATION vs problem 15:
#   No duplicate-skipping needed! We just want the closest sum --
#   even if two triplets have the same sum, the "closest" answer is the same.

def three_sum_closest(nums, target):
    nums.sort()
    n = len(nums)

    # Initialise best_sum to the first possible triplet's sum
    best_sum = nums[0] + nums[1] + nums[2]

    for i in range(n - 2):
        left  = i + 1
        right = n - 1

        while left < right:
            total = nums[i] + nums[left] + nums[right]

            # Update best_sum if this total is closer to target
            if abs(total - target) < abs(best_sum - target):
                best_sum = total

            if total < target:
                left  += 1    # sum too small -> try a bigger number
            elif total > target:
                right -= 1    # sum too big   -> try a smaller number
            else:
                return total  # exact match -- can't possibly be closer!

    return best_sum


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(three_sum_closest([-1, 2, 1, -4], 1))   # -> 2
print(three_sum_closest([0, 0, 0], 1))         # -> 0
print(three_sum_closest([1, 1, 1, 0], 100))    # -> 3
print(three_sum_closest([-100, -1, 1, 100], 0)) # -> 0


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# Math.abs() for absolute difference. Same sort + fix + two-pointer structure.
# Remember to use (a, b) => a - b for numeric sort!
#
# function threeSumClosest(nums, target) {
#     nums.sort((a, b) => a - b);
#     const n = nums.length;
#     let bestSum = nums[0] + nums[1] + nums[2];
#
#     for (let i = 0; i < n - 2; i++) {
#         let left = i + 1, right = n - 1;
#
#         while (left < right) {
#             const total = nums[i] + nums[left] + nums[right];
#
#             if (Math.abs(total - target) < Math.abs(bestSum - target)) {
#                 bestSum = total;
#             }
#
#             if      (total < target) left++;
#             else if (total > target) right--;
#             else                     return total;  // exact match
#         }
#     }
#
#     return bestSum;
# }
#
# console.log(threeSumClosest([-1,2,1,-4], 1));   // -> 2
# console.log(threeSumClosest([0,0,0], 1));        // -> 0


# =============================================================================
# 3. JAVA
# =============================================================================
# Math.abs() for absolute difference. Arrays.sort() sorts in place.
# int bestSum initialised to the first triplet's sum.
#
# import java.util.Arrays;
#
# class Solution {
#     public int threeSumClosest(int[] nums, int target) {
#         Arrays.sort(nums);
#         int n = nums.length;
#         int bestSum = nums[0] + nums[1] + nums[2];
#
#         for (int i = 0; i < n - 2; i++) {
#             int left = i + 1, right = n - 1;
#
#             while (left < right) {
#                 int total = nums[i] + nums[left] + nums[right];
#
#                 if (Math.abs(total - target) < Math.abs(bestSum - target)) {
#                     bestSum = total;
#                 }
#
#                 if      (total < target) left++;
#                 else if (total > target) right--;
#                 else                     return total;
#             }
#         }
#
#         return bestSum;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# std::abs() from <cstdlib> for absolute value.
# auto& [value, ...] structured bindings aren't needed here -- just plain indices.
#
# #include <vector>
# #include <algorithm>
# #include <cstdlib>
# using namespace std;
#
# int threeSumClosest(vector<int>& nums, int target) {
#     sort(nums.begin(), nums.end());
#     int n = nums.size();
#     int bestSum = nums[0] + nums[1] + nums[2];
#
#     for (int i = 0; i < n - 2; i++) {
#         int left = i + 1, right = n - 1;
#
#         while (left < right) {
#             int total = nums[i] + nums[left] + nums[right];
#
#             if (abs(total - target) < abs(bestSum - target)) {
#                 bestSum = total;
#             }
#
#             if      (total < target) left++;
#             else if (total > target) right--;
#             else                     return total;
#         }
#     }
#
#     return bestSum;
# }


# =============================================================================
# 5. C#
# =============================================================================
# Math.Abs() for absolute value. Array.Sort() sorts in place.
# The structure is identical to Java (C# and Java are very similar here).
#
# public class Solution {
#     public int ThreeSumClosest(int[] nums, int target) {
#         System.Array.Sort(nums);
#         int n = nums.Length;
#         int bestSum = nums[0] + nums[1] + nums[2];
#
#         for (int i = 0; i < n - 2; i++) {
#             int left = i + 1, right = n - 1;
#
#             while (left < right) {
#                 int total = nums[i] + nums[left] + nums[right];
#
#                 if (System.Math.Abs(total - target) < System.Math.Abs(bestSum - target)) {
#                     bestSum = total;
#                 }
#
#                 if      (total < target) left++;
#                 else if (total > target) right--;
#                 else                     return total;
#             }
#         }
#
#         return bestSum;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# Go's standard library doesn't have a built-in abs for int, so we write
# a quick helper (or just use an inline if). sort.Ints() sorts in place.
#
# import "sort"
#
# func threeSumClosest(nums []int, target int) int {
#     sort.Ints(nums)
#     n := len(nums)
#
#     abs := func(x int) int {
#         if x < 0 { return -x }
#         return x
#     }
#
#     bestSum := nums[0] + nums[1] + nums[2]
#
#     for i := 0; i < n-2; i++ {
#         left, right := i+1, n-1
#
#         for left < right {
#             total := nums[i] + nums[left] + nums[right]
#
#             if abs(total-target) < abs(bestSum-target) {
#                 bestSum = total
#             }
#
#             if      total < target { left++  }
#             else if total > target { right-- }
#             else                   { return total }
#         }
#     }
#
#     return bestSum
# }


# =============================================================================
# 7. RUST
# =============================================================================
# i32::abs() is a method on i32. .sort() sorts Vec<i32> in place.
# The saturating_sub(2) prevents underflow when n is very small.
#
# fn three_sum_closest(mut nums: Vec<i32>, target: i32) -> i32 {
#     nums.sort();
#     let n = nums.len();
#     let mut best_sum = nums[0] + nums[1] + nums[2];
#
#     for i in 0..n.saturating_sub(2) {
#         let mut left  = i + 1;
#         let mut right = n - 1;
#
#         while left < right {
#             let total = nums[i] + nums[left] + nums[right];
#
#             if (total - target).abs() < (best_sum - target).abs() {
#                 best_sum = total;
#             }
#
#             if      total < target { left  += 1; }
#             else if total > target { right -= 1; }
#             else                   { return total; }
#         }
#     }
#
#     best_sum
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# abs() is a global function in Swift for integers.
# .sorted() returns a new sorted array; no mutation needed.
#
# func threeSumClosest(_ nums: [Int], _ target: Int) -> Int {
#     let nums = nums.sorted()
#     let n = nums.count
#     var bestSum = nums[0] + nums[1] + nums[2]
#
#     for i in 0..<(n - 2) {
#         var left = i + 1, right = n - 1
#
#         while left < right {
#             let total = nums[i] + nums[left] + nums[right]
#
#             if abs(total - target) < abs(bestSum - target) {
#                 bestSum = total
#             }
#
#             if      total < target { left  += 1 }
#             else if total > target { right -= 1 }
#             else                   { return total }
#         }
#     }
#
#     return bestSum
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# kotlin.math.abs() for absolute value. sorted() returns a new sorted list.
# The when expression replaces if/else if/else cleanly.
#
# import kotlin.math.abs
#
# fun threeSumClosest(nums: IntArray, target: Int): Int {
#     val sorted = nums.sorted()
#     val n = sorted.size
#     var bestSum = sorted[0] + sorted[1] + sorted[2]
#
#     for (i in 0 until n - 2) {
#         var left = i + 1; var right = n - 1
#
#         while (left < right) {
#             val total = sorted[i] + sorted[left] + sorted[right]
#
#             if (abs(total - target) < abs(bestSum - target)) {
#                 bestSum = total
#             }
#
#             when {
#                 total < target -> left++
#                 total > target -> right--
#                 else           -> return total
#             }
#         }
#     }
#
#     return bestSum
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# .abs is a method on integers in Ruby. .sort returns a new sorted array.
# The structure is the same clean three-part pattern.
#
# def three_sum_closest(nums, target)
#   nums = nums.sort
#   n = nums.length
#   best_sum = nums[0] + nums[1] + nums[2]
#
#   (0..n - 3).each do |i|
#     left, right = i + 1, n - 1
#
#     while left < right
#       total = nums[i] + nums[left] + nums[right]
#
#       if (total - target).abs < (best_sum - target).abs
#         best_sum = total
#       end
#
#       if    total < target then left  += 1
#       elsif total > target then right -= 1
#       else                      return total
#       end
#     end
#   end
#
#   best_sum
# end
#
# puts three_sum_closest([-1,2,1,-4], 1)   # -> 2
# puts three_sum_closest([0,0,0], 1)        # -> 0


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use SORT + FIX ONE + TWO POINTERS -- same as 3Sum (15),
# with two small but important changes:
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  1. Track best_sum = sum closest to target seen so far.        │
#   │     Initialise it to the first triplet's sum.                   │
#   │                                                                  │
#   │  2. At each triplet:                                            │
#   │     if |total - target| < |best_sum - target|: update best_sum │
#   │                                                                  │
#   │  3. Move pointers the same way as 3Sum:                        │
#   │     total < target -> left++   (need bigger sum)               │
#   │     total > target -> right--  (need smaller sum)              │
#   │     total == target -> return immediately (can't beat 0 diff)  │
#   │                                                                  │
#   │  4. No duplicate-skipping needed (closest sum is unique).      │
#   └──────────────────────────────────────────────────────────────────┘
#
# COMPARED TO 3SUM (problem 15):
#   - Simpler (no duplicate handling)
#   - Different goal (closest, not exact)
#   - Two extra lines: initialise best_sum, update best_sum
#   - Early exit when exact match found (bonus optimisation)
#
# Time complexity:  O(n^2)  -- O(n log n) sort + O(n^2) two-pointer loop
# Space complexity: O(1)    -- just a handful of variables (ignoring sort stack)
# =============================================================================
