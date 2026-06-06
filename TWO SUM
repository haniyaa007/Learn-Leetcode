# =============================================================================
# TWO SUM - Solved in 10 Programming Languages
# =============================================================================
# PROBLEM: Given a list of numbers and a target, find the TWO numbers that
# add up to the target and return their POSITIONS (indices) in the list.
#
# Example: nums = [2, 7, 11, 15], target = 9
#          Answer: [0, 1]  because nums[0] + nums[1] = 2 + 7 = 9  ✓
# =============================================================================


# =============================================================================
# 1. PYTHON  ✅  (active - try running this!)
# =============================================================================
#
# HOW IT WORKS (the smart way - using a "hash map" / dictionary):
#
# Imagine you're looking for two puzzle pieces that fit together.
# Instead of trying every possible pair (slow!), you do this:
#
#   - Walk through the list one number at a time.
#   - For each number, ask: "Have I already seen the number I NEED?"
#   - The number you "need" is:  target - current_number
#     e.g. target=9, current=2  →  you need 7
#   - Keep a dictionary (like a notebook) to remember numbers you've seen.
#   - If the number you need IS in your notebook → you found the pair! Done.
#   - If not → write the current number in your notebook and move on.
#
# WHY IS THIS FAST?
#   Checking a dictionary is almost instant (O(1)).
#   We only loop through the list once → O(n) total.
#   Compare that to checking every pair: O(n²) - much slower!
#
# STEP-BY-STEP with [2, 7, 11, 15], target = 9:
#
#   i=0, num=2  → need 7  → notebook empty      → add {2: 0}
#   i=1, num=7  → need 2  → 2 IS in notebook!   → return [notebook[2], 1] = [0, 1] ✓

def two_sum(nums, target):
    notebook = {}  # { number_we_saw : its_index }

    for i, num in enumerate(nums):
        number_needed = target - num

        if number_needed in notebook:
            return [notebook[number_needed], i]  # found it!

        notebook[num] = i  # not found yet, jot this number down

    return []  # (the problem guarantees we always find a pair, so this won't happen)


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(two_sum([2, 7, 11, 15], 9))   # → [0, 1]
print(two_sum([3, 2, 4], 6))        # → [1, 2]
print(two_sum([3, 3], 6))           # → [0, 1]


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# Same idea - a Map() is JavaScript's version of a dictionary.
#
# function twoSum(nums, target) {
#     const notebook = new Map();
#
#     for (let i = 0; i < nums.length; i++) {
#         const numberNeeded = target - nums[i];
#
#         if (notebook.has(numberNeeded)) {
#             return [notebook.get(numberNeeded), i];
#         }
#
#         notebook.set(nums[i], i);
#     }
# }
#
# console.log(twoSum([2, 7, 11, 15], 9));  // → [0, 1]
# console.log(twoSum([3, 2, 4], 6));       // → [1, 2]
# console.log(twoSum([3, 3], 6));          // → [0, 1]


# =============================================================================
# 3. JAVA
# =============================================================================
# Java is more "wordy" - you must declare types for everything.
# HashMap is Java's dictionary.
#
# import java.util.HashMap;
# import java.util.Map;
#
# class Solution {
#     public int[] twoSum(int[] nums, int target) {
#         Map<Integer, Integer> notebook = new HashMap<>();
#
#         for (int i = 0; i < nums.length; i++) {
#             int numberNeeded = target - nums[i];
#
#             if (notebook.containsKey(numberNeeded)) {
#                 return new int[] { notebook.get(numberNeeded), i };
#             }
#
#             notebook.put(nums[i], i);
#         }
#
#         return new int[] {};
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# C++ is fast and low-level. unordered_map is C++'s hash map.
# The :: and <> syntax is just C++ telling you what TYPE things are.
#
# #include <vector>
# #include <unordered_map>
# using namespace std;
#
# vector<int> twoSum(vector<int>& nums, int target) {
#     unordered_map<int, int> notebook;
#
#     for (int i = 0; i < nums.size(); i++) {
#         int numberNeeded = target - nums[i];
#
#         if (notebook.count(numberNeeded)) {
#             return { notebook[numberNeeded], i };
#         }
#
#         notebook[nums[i]] = i;
#     }
#
#     return {};
# }


# =============================================================================
# 5. C#
# =============================================================================
# C# (by Microsoft) looks a lot like Java. Dictionary<K,V> is the hash map.
#
# using System.Collections.Generic;
#
# public class Solution {
#     public int[] TwoSum(int[] nums, int target) {
#         Dictionary<int, int> notebook = new Dictionary<int, int>();
#
#         for (int i = 0; i < nums.Length; i++) {
#             int numberNeeded = target - nums[i];
#
#             if (notebook.ContainsKey(numberNeeded)) {
#                 return new int[] { notebook[numberNeeded], i };
#             }
#
#             notebook[nums[i]] = i;
#         }
#
#         return new int[] {};
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# Go is simple and fast. Maps work just like Python dictionaries.
# The := syntax means "create this variable and figure out the type for me".
#
# func twoSum(nums []int, target int) []int {
#     notebook := make(map[int]int)
#
#     for i, num := range nums {
#         numberNeeded := target - num
#
#         if j, found := notebook[numberNeeded]; found {
#             return []int{j, i}
#         }
#
#         notebook[num] = i
#     }
#
#     return []int{}
# }


# =============================================================================
# 7. RUST
# =============================================================================
# Rust is known for safety and speed. It's stricter than most languages.
# HashMap::new() creates the dictionary. &nums borrows the list (doesn't copy it).
#
# use std::collections::HashMap;
#
# fn two_sum(nums: &[i32], target: i32) -> Vec<i32> {
#     let mut notebook: HashMap<i32, usize> = HashMap::new();
#
#     for (i, &num) in nums.iter().enumerate() {
#         let number_needed = target - num;
#
#         if let Some(&j) = notebook.get(&number_needed) {
#             return vec![j as i32, i as i32];
#         }
#
#         notebook.insert(num, i);
#     }
#
#     vec![]
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# Swift is Apple's language (used for iOS/macOS apps).
# Very readable - almost like English!
#
# func twoSum(_ nums: [Int], _ target: Int) -> [Int] {
#     var notebook = [Int: Int]()   // dictionary: number → index
#
#     for (i, num) in nums.enumerated() {
#         let numberNeeded = target - num
#
#         if let j = notebook[numberNeeded] {
#             return [j, i]
#         }
#
#         notebook[num] = i
#     }
#
#     return []
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# Kotlin is a modern language that runs on the Java platform.
# Very concise - less typing than Java for the same result.
#
# fun twoSum(nums: IntArray, target: Int): IntArray {
#     val notebook = HashMap<Int, Int>()
#
#     for (i in nums.indices) {
#         val numberNeeded = target - nums[i]
#
#         if (notebook.containsKey(numberNeeded)) {
#             return intArrayOf(notebook[numberNeeded]!!, i)
#         }
#
#         notebook[nums[i]] = i
#     }
#
#     return intArrayOf()
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# Ruby is famous for being friendly and readable.
# Its syntax is very clean - almost no punctuation needed!
#
# def two_sum(nums, target)
#   notebook = {}
#
#   nums.each_with_index do |num, i|
#     number_needed = target - num
#
#     if notebook.key?(number_needed)
#       return [notebook[number_needed], i]
#     end
#
#     notebook[num] = i
#   end
# end
#
# p two_sum([2, 7, 11, 15], 9)  # → [0, 1]
# p two_sum([3, 2, 4], 6)       # → [1, 2]
# p two_sum([3, 3], 6)          # → [0, 1]


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use the SAME core idea:
#
#   ┌─────────────────────────────────────────────────────┐
#   │  For each number:                                   │
#   │    1. Calculate what number you NEED (target - num) │
#   │    2. Check your notebook — is it there?            │
#   │       YES → return both indices  🎉                 │
#   │       NO  → add current number to notebook          │
#   └─────────────────────────────────────────────────────┘
#
# Time complexity:  O(n)  — one pass through the list
# Space complexity: O(n)  — notebook grows up to n entries
#
# The brute force (two nested loops, checking every pair) would be O(n²).
# For a list of 10,000 numbers that's 100,000,000 checks vs just 10,000!
# =============================================================================
