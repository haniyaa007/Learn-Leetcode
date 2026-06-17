# =============================================================================
# CONTAINER WITH MOST WATER
# =============================================================================
# PROBLEM: Given an array of heights representing vertical lines, find two
# lines that together form a container holding the MOST water.
#
# HOW IS WATER CALCULATED?
#   Water = WIDTH x HEIGHT
#   WIDTH  = distance between the two lines  (right_index - left_index)
#   HEIGHT = the SHORTER of the two lines    (water spills over the shorter one)
#
# So for lines at index 1 (height=8) and index 8 (height=7):
#   width  = 8 - 1 = 7
#   height = min(8, 7) = 7
#   water  = 7 x 7 = 49  <- the answer for Example 1
#
# WHY NOT JUST CHECK EVERY PAIR?
#   That's O(n^2) -- for n=100,000 lines that's 10 BILLION comparisons. Too slow.
#   The two-pointer approach does it in O(n) -- one single pass.
# =============================================================================


# =============================================================================
# 1. PYTHON  (active - try running this!)
# =============================================================================
#
# THE TWO-POINTER APPROACH:
#
# Place one pointer at the LEFT end, one at the RIGHT end.
# At each step, calculate the water between them.
# Then MOVE the pointer pointing to the SHORTER line inward.
#
# WHY MOVE THE SHORTER ONE?
#   The water is always limited by the shorter line (water spills over it).
#   Moving the TALLER line inward can only make things worse or equal:
#     - width gets smaller (always)
#     - height stays capped at the same short line (or shorter)
#   So there's no point moving the taller line.
#   But moving the SHORTER line inward MIGHT find a taller line,
#   which could increase the height enough to compensate for the lost width.
#
# STEP-BY-STEP with [1, 8, 6, 2, 5, 4, 8, 3, 7]:
#
#   left=0 (h=1), right=8 (h=7)  water = min(1,7) * (8-0) = 1*8  =  8   best=8
#   Move LEFT (shorter).
#
#   left=1 (h=8), right=8 (h=7)  water = min(8,7) * (8-1) = 7*7  = 49   best=49
#   Move RIGHT (shorter).
#
#   left=1 (h=8), right=7 (h=3)  water = min(8,3) * (7-1) = 3*6  = 18   best=49
#   Move RIGHT (shorter).
#
#   left=1 (h=8), right=6 (h=8)  water = min(8,8) * (6-1) = 8*5  = 40   best=49
#   Equal height -- move either (we move right).
#
#   left=1 (h=8), right=5 (h=4)  water = min(8,4) * (5-1) = 4*4  = 16   best=49
#   Move RIGHT (shorter).
#
#   left=1 (h=8), right=4 (h=5)  water = min(8,5) * (4-1) = 5*3  = 15   best=49
#   Move RIGHT (shorter).
#
#   left=1 (h=8), right=3 (h=2)  water = min(8,2) * (3-1) = 2*2  =  4   best=49
#   Move RIGHT (shorter).
#
#   left=1 (h=8), right=2 (h=6)  water = min(8,6) * (2-1) = 6*1  =  6   best=49
#   Move RIGHT (shorter).
#
#   left=1, right=1  -> pointers met, STOP.
#   Answer: 49 ✓

def max_area(height):
    left  = 0                  # start left pointer at the beginning
    right = len(height) - 1    # start right pointer at the end
    best  = 0                  # track the maximum water seen so far

    while left < right:
        # Calculate water for this pair of lines
        width  = right - left
        h      = min(height[left], height[right])
        water  = width * h
        best   = max(best, water)

        # Move the pointer pointing to the SHORTER line inward
        if height[left] <= height[right]:
            left += 1    # left is shorter (or equal) -> move left pointer right
        else:
            right -= 1   # right is shorter -> move right pointer left

    return best


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))   # -> 49
print(max_area([1, 1]))                          # -> 1
print(max_area([4, 3, 2, 1, 4]))                 # -> 16
print(max_area([1, 2, 1]))                       # -> 2


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# Math.min and Math.max instead of Python's min/max.
# Everything else is a direct translation.
#
# function maxArea(height) {
#     let left = 0, right = height.length - 1;
#     let best = 0;
#
#     while (left < right) {
#         const water = Math.min(height[left], height[right]) * (right - left);
#         best = Math.max(best, water);
#
#         if (height[left] <= height[right]) left++;
#         else right--;
#     }
#
#     return best;
# }
#
# console.log(maxArea([1,8,6,2,5,4,8,3,7]));  // -> 49
# console.log(maxArea([1,1]));                  // -> 1


# =============================================================================
# 3. JAVA
# =============================================================================
# Math.min and Math.max are Java's built-ins.
# The logic is identical -- Java is just more explicit about types.
#
# class Solution {
#     public int maxArea(int[] height) {
#         int left = 0, right = height.length - 1;
#         int best = 0;
#
#         while (left < right) {
#             int water = Math.min(height[left], height[right]) * (right - left);
#             best = Math.max(best, water);
#
#             if (height[left] <= height[right]) left++;
#             else right--;
#         }
#
#         return best;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# std::min and std::max from <algorithm>.
# vector<int>& passes the array by reference (no copying).
#
# #include <vector>
# #include <algorithm>
# using namespace std;
#
# int maxArea(vector<int>& height) {
#     int left = 0, right = height.size() - 1;
#     int best = 0;
#
#     while (left < right) {
#         int water = min(height[left], height[right]) * (right - left);
#         best = max(best, water);
#
#         if (height[left] <= height[right]) left++;
#         else right--;
#     }
#
#     return best;
# }


# =============================================================================
# 5. C#
# =============================================================================
# System.Math.Min / System.Math.Max (or just Math.Min/Max with using System).
# int[] is C#'s array type.
#
# public class Solution {
#     public int MaxArea(int[] height) {
#         int left = 0, right = height.Length - 1;
#         int best = 0;
#
#         while (left < right) {
#             int water = System.Math.Min(height[left], height[right]) * (right - left);
#             best = System.Math.Max(best, water);
#
#             if (height[left] <= height[right]) left++;
#             else right--;
#         }
#
#         return best;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# Go has no built-in min/max for ints before Go 1.21, so we write a quick
# inline ternary using if expressions (Go doesn't have ternary ? : syntax).
#
# func maxArea(height []int) int {
#     left, right := 0, len(height)-1
#     best := 0
#
#     for left < right {
#         h := height[left]
#         if height[right] < h { h = height[right] }
#         water := h * (right - left)
#         if water > best { best = water }
#
#         if height[left] <= height[right] {
#             left++
#         } else {
#             right--
#         }
#     }
#
#     return best
# }


# =============================================================================
# 7. RUST
# =============================================================================
# .min() and .max() are methods on integer types in Rust.
# usize is Rust's index type; we cast to i32 for the multiplication.
# The as usize / as i32 casts are explicit -- Rust never casts silently.
#
# fn max_area(height: Vec<i32>) -> i32 {
#     let mut left  = 0usize;
#     let mut right = height.len() - 1;
#     let mut best  = 0i32;
#
#     while left < right {
#         let water = height[left].min(height[right]) * (right - left) as i32;
#         best = best.max(water);
#
#         if height[left] <= height[right] {
#             left += 1;
#         } else {
#             right -= 1;
#         }
#     }
#
#     best
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# Swift's min() and max() are global functions (like Python's).
# var makes variables mutable; let would make them constants.
#
# func maxArea(_ height: [Int]) -> Int {
#     var left  = 0
#     var right = height.count - 1
#     var best  = 0
#
#     while left < right {
#         let water = min(height[left], height[right]) * (right - left)
#         best = max(best, water)
#
#         if height[left] <= height[right] { left  += 1 }
#         else                             { right -= 1 }
#     }
#
#     return best
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# minOf() and maxOf() are Kotlin's built-ins (standard library functions).
# Kotlin's while loop and if/else look almost identical to Java.
#
# fun maxArea(height: IntArray): Int {
#     var left  = 0
#     var right = height.size - 1
#     var best  = 0
#
#     while (left < right) {
#         val water = minOf(height[left], height[right]) * (right - left)
#         best = maxOf(best, water)
#
#         if (height[left] <= height[right]) left++
#         else right--
#     }
#
#     return best
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# [a, b].min and [a, b].max are Ruby's idiomatic min/max.
# Ruby's while loop and if/else are clean and readable.
#
# def max_area(height)
#   left  = 0
#   right = height.length - 1
#   best  = 0
#
#   while left < right
#     water = [height[left], height[right]].min * (right - left)
#     best  = [best, water].max
#
#     if height[left] <= height[right]
#       left  += 1
#     else
#       right -= 1
#     end
#   end
#
#   best
# end
#
# puts max_area([1,8,6,2,5,4,8,3,7])   # -> 49
# puts max_area([1,1])                  # -> 1


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use the TWO-POINTER technique:
#
#   Place left at index 0, right at index n-1.
#
#   While left < right:
#     water = min(height[left], height[right]) * (right - left)
#     update best
#     move the SHORTER pointer inward  (if equal, move either)
#
#   Return best.
#
# WHY IS IT SAFE TO MOVE THE SHORTER POINTER?
#   Any pair involving the shorter line and a pointer that's even further
#   inward would have:
#     - smaller width  (guaranteed, since we moved inward)
#     - height still capped by the shorter line or less
#   So no better answer can exist for that shorter line -- we can discard it.
#   This greedy argument is the key to why two pointers works here.
#
# Time complexity:  O(n)   -- each pointer moves at most n steps total
# Space complexity: O(1)   -- just four variables, no extra storage
#
# Compared to brute force O(n^2): for n=100,000 that's the difference
# between 100,000 operations and 10,000,000,000. The two-pointer trick
# is one of the most powerful tools in your algorithm toolkit.
# =============================================================================
