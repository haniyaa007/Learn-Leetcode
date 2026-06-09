# =============================================================================
# LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS
# =============================================================================
# PROBLEM: Given a string, find the LENGTH of the longest substring
# that contains no duplicate characters.
#
# Example: "abcabcbb"
#   "abc"  → length 3, no repeats ✓
#   "abca" → length 4, but 'a' repeats ✗
#   Answer: 3
#
# KEY VOCAB:
#   substring  = a CONTIGUOUS slice of the string  e.g. "abc" from "abcdef"
#   subsequence = characters in order but NOT necessarily touching (not what we want)
# =============================================================================


# =============================================================================
# 1. PYTHON  ✅  (active - try running this!)
# =============================================================================
#
# HOW IT WORKS — the "sliding window" technique:
#
# Imagine a rubber-band window that can stretch and shrink over the string.
# The window always contains only UNIQUE characters.
#
#   - 'left'  is the LEFT  edge of the window (starts at 0)
#   - 'right' is the RIGHT edge of the window (moves forward one step at a time)
#   - 'seen'  is a dictionary: { character → its most recent index }
#
# At each step, we try to EXPAND the window by including s[right].
#   CASE A — s[right] is NOT in our window → stretch! update max length.
#   CASE B — s[right] IS already in our window → SHRINK the left edge to
#             just PAST where we last saw that character, removing the duplicate.
#
# STEP-BY-STEP with "abcabcbb":
#
#   right=0  char='a'  not seen         window=[a]         seen={a:0}  max=1
#   right=1  char='b'  not seen         window=[ab]        seen={b:1}  max=2
#   right=2  char='c'  not seen         window=[abc]       seen={c:2}  max=3
#   right=3  char='a'  SEEN at 0! left moves to 1  window=[bca]  seen={a:3}  max=3
#   right=4  char='b'  SEEN at 1! left moves to 2  window=[cab]  seen={b:4}  max=3
#   right=5  char='c'  SEEN at 2! left moves to 3  window=[abc]  seen={c:5}  max=3
#   right=6  char='b'  SEEN at 4! left moves to 5  window=[cb]   seen={b:6}  max=3
#   right=7  char='b'  SEEN at 6! left moves to 7  window=[b]    seen={b:7}  max=3
#   Answer: 3  ✓
#
# WHY THE MAX() TRICK ON LEFT?
#   When we see a duplicate, we jump left to (last_seen_index + 1).
#   But what if that index is BEHIND our current left? We must never move
#   left backwards, so we take:  left = max(left, seen[char] + 1)

def length_of_longest_substring(s):
    seen = {}       # { character : most recent index we saw it at }
    left = 0        # left edge of our window
    max_length = 0  # best answer so far

    for right, char in enumerate(s):

        # if we've seen this character AND it's inside our current window
        if char in seen and seen[char] >= left:
            left = seen[char] + 1   # shrink: move left edge past the duplicate

        seen[char] = right                          # update/record this character's position
        max_length = max(max_length, right - left + 1)  # window size = right - left + 1

    return max_length


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(length_of_longest_substring("abcabcbb"))  # → 3
print(length_of_longest_substring("bbbbb"))     # → 1
print(length_of_longest_substring("pwwkew"))    # → 3
print(length_of_longest_substring(""))          # → 0


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# Map() is JavaScript's dictionary. The ternary (condition ? a : b) is like
# Python's (a if condition else b).
#
# function lengthOfLongestSubstring(s) {
#     const seen = new Map();   // { character → most recent index }
#     let left = 0;
#     let maxLength = 0;
#
#     for (let right = 0; right < s.length; right++) {
#         const char = s[right];
#
#         if (seen.has(char) && seen.get(char) >= left) {
#             left = seen.get(char) + 1;  // shrink window past the duplicate
#         }
#
#         seen.set(char, right);
#         maxLength = Math.max(maxLength, right - left + 1);
#     }
#
#     return maxLength;
# }
#
# console.log(lengthOfLongestSubstring("abcabcbb"));  // → 3
# console.log(lengthOfLongestSubstring("bbbbb"));     // → 1
# console.log(lengthOfLongestSubstring("pwwkew"));    // → 3


# =============================================================================
# 3. JAVA
# =============================================================================
# HashMap<Character, Integer> maps a character to an integer index.
# s.charAt(i) gets the character at position i (Java strings aren't indexable
# with [] like Python).
#
# import java.util.HashMap;
#
# class Solution {
#     public int lengthOfLongestSubstring(String s) {
#         HashMap<Character, Integer> seen = new HashMap<>();
#         int left = 0;
#         int maxLength = 0;
#
#         for (int right = 0; right < s.length(); right++) {
#             char c = s.charAt(right);
#
#             if (seen.containsKey(c) && seen.get(c) >= left) {
#                 left = seen.get(c) + 1;
#             }
#
#             seen.put(c, right);
#             maxLength = Math.max(maxLength, right - left + 1);
#         }
#
#         return maxLength;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# unordered_map<char, int> is C++'s hash map for char → int.
# s[i] works fine for indexing into a std::string.
#
# #include <string>
# #include <unordered_map>
# #include <algorithm>
# using namespace std;
#
# int lengthOfLongestSubstring(string s) {
#     unordered_map<char, int> seen;
#     int left = 0;
#     int maxLength = 0;
#
#     for (int right = 0; right < s.size(); right++) {
#         char c = s[right];
#
#         if (seen.count(c) && seen[c] >= left) {
#             left = seen[c] + 1;
#         }
#
#         seen[c] = right;
#         maxLength = max(maxLength, right - left + 1);
#     }
#
#     return maxLength;
# }


# =============================================================================
# 5. C#
# =============================================================================
# Dictionary<char, int> is C#'s hash map. s[i] indexes into a string.
# ContainsKey() checks if a key exists (like Python's 'in').
#
# using System.Collections.Generic;
#
# public class Solution {
#     public int LengthOfLongestSubstring(string s) {
#         var seen = new Dictionary<char, int>();
#         int left = 0;
#         int maxLength = 0;
#
#         for (int right = 0; right < s.Length; right++) {
#             char c = s[right];
#
#             if (seen.ContainsKey(c) && seen[c] >= left) {
#                 left = seen[c] + 1;
#             }
#
#             seen[c] = right;
#             maxLength = System.Math.Max(maxLength, right - left + 1);
#         }
#
#         return maxLength;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# map[byte]int maps a byte (character) to an int.
# Go's if-assignment  `if val, ok := seen[c]; ok`  checks and grabs in one line.
#
# func lengthOfLongestSubstring(s string) int {
#     seen := make(map[byte]int)
#     left := 0
#     maxLength := 0
#
#     for right := 0; right < len(s); right++ {
#         c := s[right]
#
#         if idx, ok := seen[c]; ok && idx >= left {
#             left = idx + 1
#         }
#
#         seen[c] = right
#         if right - left + 1 > maxLength {
#             maxLength = right - left + 1
#         }
#     }
#
#     return maxLength
# }


# =============================================================================
# 7. RUST
# =============================================================================
# HashMap<char, usize> maps a char to an index (usize = unsigned integer).
# .chars().enumerate() gives (index, character) pairs, same as Python's enumerate().
#
# use std::collections::HashMap;
#
# fn length_of_longest_substring(s: &str) -> usize {
#     let mut seen: HashMap<char, usize> = HashMap::new();
#     let mut left = 0;
#     let mut max_length = 0;
#     let chars: Vec<char> = s.chars().collect();
#
#     for right in 0..chars.len() {
#         let c = chars[right];
#
#         if let Some(&idx) = seen.get(&c) {
#             if idx >= left {
#                 left = idx + 1;
#             }
#         }
#
#         seen.insert(c, right);
#         max_length = max_length.max(right - left + 1);
#     }
#
#     max_length
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# [Character: Int] is Swift's dictionary type for char → int.
# String indexing in Swift is more complex than other languages (it uses
# String.Index), so we convert to an Array of Characters first for simplicity.
#
# func lengthOfLongestSubstring(_ s: String) -> Int {
#     var seen = [Character: Int]()
#     var left = 0
#     var maxLength = 0
#     let chars = Array(s)   // convert String → [Character] for easy indexing
#
#     for right in 0..<chars.count {
#         let c = chars[right]
#
#         if let idx = seen[c], idx >= left {
#             left = idx + 1
#         }
#
#         seen[c] = right
#         maxLength = max(maxLength, right - left + 1)
#     }
#
#     return maxLength
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# mutableMapOf<Char, Int>() creates a mutable dictionary.
# The Elvis operator '?: -1' returns -1 if the key isn't in the map,
# ensuring the condition `>= left` is safely false when a char is unseen.
#
# fun lengthOfLongestSubstring(s: String): Int {
#     val seen = mutableMapOf<Char, Int>()
#     var left = 0
#     var maxLength = 0
#
#     for (right in s.indices) {
#         val c = s[right]
#
#         if ((seen[c] ?: -1) >= left) {
#             left = seen[c]!! + 1
#         }
#
#         seen[c] = right
#         maxLength = maxOf(maxLength, right - left + 1)
#     }
#
#     return maxLength
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# Ruby's Hash.new(-1) creates a dictionary where any missing key returns -1
# by default — a handy trick to avoid an explicit "have I seen this?" check.
# each_char.with_index gives (character, index) pairs.
#
# def length_of_longest_substring(s)
#   seen = Hash.new(-1)   # unseen characters return -1 (safely behind any left)
#   left = 0
#   max_length = 0
#
#   s.each_char.with_index do |char, right|
#     if seen[char] >= left
#       left = seen[char] + 1
#     end
#
#     seen[char] = right
#     max_length = [max_length, right - left + 1].max
#   end
#
#   max_length
# end
#
# puts length_of_longest_substring("abcabcbb")  # → 3
# puts length_of_longest_substring("bbbbb")     # → 1
# puts length_of_longest_substring("pwwkew")    # → 3


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use the SLIDING WINDOW pattern:
#
#   ┌─────────────────────────────────────────────────────────────────┐
#   │  Keep a window [left ... right] of unique characters.          │
#   │                                                                 │
#   │  For each new character (right moves forward):                 │
#   │    - If it's a duplicate INSIDE the window:                    │
#   │        shrink from the left (jump past the old duplicate)      │
#   │    - Record the character's latest position                    │
#   │    - Update the max length if the window just got bigger       │
#   └─────────────────────────────────────────────────────────────────┘
#
# Time complexity:  O(n)  — right visits each character once
# Space complexity: O(min(n, a))  — the dictionary holds at most 'a' entries,
#                   where 'a' is the size of the character set (e.g. 26 for
#                   lowercase letters, 128 for ASCII). Never bigger than n.
#
# The brute force (check every possible substring) would be O(n²) or O(n³).
# The sliding window cuts it down to a single clean pass. 🪟
# =============================================================================
