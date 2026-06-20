# =============================================================================
# LONGEST COMMON PREFIX
# =============================================================================
# PROBLEM: Find the longest string that is a prefix of ALL strings in the list.
# Return "" if there is no common prefix.
#
# WHAT IS A PREFIX?
#   A prefix is the BEGINNING of a string.
#   "flower" has prefixes: "f", "fl", "flo", "flow", "flowe", "flower"
#
# EXAMPLES:
#   ["flower","flow","flight"] -> "fl"
#     "flower" starts with "fl" ✓
#     "flow"   starts with "fl" ✓
#     "flight" starts with "fl" ✓  (but NOT "flo" -- "flight" has 'i' there)
#
#   ["dog","racecar","car"] -> ""
#     "dog" starts with 'd', others start with 'r' and 'c' -- no match at all
# =============================================================================


# =============================================================================
# 1. PYTHON  (active - try running this!)
# =============================================================================
#
# HOW IT WORKS -- vertical scanning:
#
# Think of the strings stacked on top of each other like this:
#
#   f l o w e r
#   f l o w
#   f l i g h t
#
# We scan COLUMN BY COLUMN (left to right).
# At each column position i, check if ALL strings have the same character.
#   - If YES: that character is part of the prefix. Move to column i+1.
#   - If NO (or a string is too short): STOP. Return what we've collected so far.
#
# STEP-BY-STEP with ["flower","flow","flight"]:
#
#   Column 0: f, f, f  -- all 'f' ✓   prefix = "f"
#   Column 1: l, l, l  -- all 'l' ✓   prefix = "fl"
#   Column 2: o, o, i  -- 'o' != 'i'  STOP
#   Return "fl" ✓
#
# NICE PYTHON TRICK:
#   min(strs, key=len) gives us the shortest string.
#   We only need to scan as far as the shortest string -- if a prefix
#   candidate is longer than any string, it can't be a common prefix.
#   So we iterate over the characters of the shortest string and check
#   if ALL other strings share that character at the same position.

def longest_common_prefix(strs):
    if not strs:
        return ""

    # The shortest string limits how long the prefix can possibly be
    shortest = min(strs, key=len)

    for i, char in enumerate(shortest):
        # Check if this character matches at position i in EVERY other string
        for other in strs:
            if other[i] != char:
                # Mismatch found -- prefix ends just before this position
                return shortest[:i]

    # We made it through the whole shortest string with no mismatches
    return shortest


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(longest_common_prefix(["flower","flow","flight"]))   # -> "fl"
print(longest_common_prefix(["dog","racecar","car"]))      # -> ""
print(longest_common_prefix(["interview","inter","internal"])) # -> "inter"
print(longest_common_prefix(["a"]))                        # -> "a"
print(longest_common_prefix(["ab","a"]))                   # -> "a"
print(longest_common_prefix(["","b"]))                     # -> ""


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# The same vertical scan. every() checks if a condition holds for all items
# in an array -- like Python's all().
# We start with the first string as the candidate and trim it down.
#
# function longestCommonPrefix(strs) {
#     if (strs.length === 0) return "";
#
#     let prefix = strs[0];   // start with the full first string as the guess
#
#     for (let i = 1; i < strs.length; i++) {
#         // Trim prefix until strs[i] starts with it
#         while (!strs[i].startsWith(prefix)) {
#             prefix = prefix.slice(0, -1);   // chop off the last character
#             if (prefix === "") return "";
#         }
#     }
#
#     return prefix;
# }
#
# console.log(longestCommonPrefix(["flower","flow","flight"]));  // -> "fl"
# console.log(longestCommonPrefix(["dog","racecar","car"]));     // -> ""


# =============================================================================
# 3. JAVA
# =============================================================================
# Start with strs[0] as the prefix guess. For each subsequent string,
# indexOf(prefix) == 0 checks if the string STARTS WITH the prefix.
# If not, chop one character off the end and try again.
#
# class Solution {
#     public String longestCommonPrefix(String[] strs) {
#         if (strs.length == 0) return "";
#
#         String prefix = strs[0];
#
#         for (int i = 1; i < strs.length; i++) {
#             while (strs[i].indexOf(prefix) != 0) {
#                 prefix = prefix.substring(0, prefix.length() - 1);
#                 if (prefix.isEmpty()) return "";
#             }
#         }
#
#         return prefix;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# Same "shrink the prefix" approach. substr(0, prefix.size()-1) chops
# the last character. rfind(prefix, 0) == 0 checks if the string
# starts with the prefix (more efficient than find() for this case).
#
# #include <string>
# #include <vector>
# using namespace std;
#
# string longestCommonPrefix(vector<string>& strs) {
#     if (strs.empty()) return "";
#
#     string prefix = strs[0];
#
#     for (int i = 1; i < (int)strs.size(); i++) {
#         while (strs[i].rfind(prefix, 0) != 0) {
#             prefix = prefix.substr(0, prefix.size() - 1);
#             if (prefix.empty()) return "";
#         }
#     }
#
#     return prefix;
# }


# =============================================================================
# 5. C#
# =============================================================================
# StartsWith() checks if a string begins with the prefix.
# Substring(0, prefix.Length - 1) trims the last character.
# LINQ's Min(s => s.Length) finds the shortest string's length.
#
# public class Solution {
#     public string LongestCommonPrefix(string[] strs) {
#         if (strs.Length == 0) return "";
#
#         string prefix = strs[0];
#
#         foreach (string s in strs) {
#             while (!s.StartsWith(prefix)) {
#                 prefix = prefix.Substring(0, prefix.Length - 1);
#                 if (prefix == "") return "";
#             }
#         }
#
#         return prefix;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# strings.HasPrefix(s, prefix) checks if s starts with prefix.
# We shorten the prefix one byte at a time until all strings match.
#
# import "strings"
#
# func longestCommonPrefix(strs []string) string {
#     if len(strs) == 0 { return "" }
#
#     prefix := strs[0]
#
#     for _, s := range strs[1:] {
#         for !strings.HasPrefix(s, prefix) {
#             prefix = prefix[:len(prefix)-1]
#             if prefix == "" { return "" }
#         }
#     }
#
#     return prefix
# }


# =============================================================================
# 7. RUST
# =============================================================================
# starts_with() checks for a prefix. We shorten the candidate by trimming
# the last character using &prefix[..prefix.len()-1].
# chars().count() is needed because Rust strings are UTF-8 (multi-byte chars).
# Since this problem guarantees lowercase ASCII, len() is safe here.
#
# fn longest_common_prefix(strs: Vec<String>) -> String {
#     if strs.is_empty() { return String::new(); }
#
#     let mut prefix = strs[0].clone();
#
#     for s in strs.iter().skip(1) {
#         while !s.starts_with(prefix.as_str()) {
#             prefix.pop();   // remove last character
#             if prefix.is_empty() { return String::new(); }
#         }
#     }
#
#     prefix
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# hasPrefix() is Swift's built-in prefix check.
# dropLast() returns a Substring with the last character removed.
# String(...) converts it back to a full String.
#
# func longestCommonPrefix(_ strs: [String]) -> String {
#     guard !strs.isEmpty else { return "" }
#
#     var prefix = strs[0]
#
#     for s in strs.dropFirst() {
#         while !s.hasPrefix(prefix) {
#             prefix = String(prefix.dropLast())
#             if prefix.isEmpty { return "" }
#         }
#     }
#
#     return prefix
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# startsWith() checks for a prefix. dropLast(1) trims one character.
# The logic is the same shrink-until-match approach.
#
# fun longestCommonPrefix(strs: Array<String>): String {
#     if (strs.isEmpty()) return ""
#
#     var prefix = strs[0]
#
#     for (s in strs.drop(1)) {
#         while (!s.startsWith(prefix)) {
#             prefix = prefix.dropLast(1)
#             if (prefix.isEmpty()) return ""
#         }
#     }
#
#     return prefix
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# start_with? checks if a string begins with a prefix.
# chop removes the last character. chop on "" returns "" (no crash).
# We check for empty? to bail out early.
#
# def longest_common_prefix(strs)
#   return "" if strs.empty?
#
#   prefix = strs[0]
#
#   strs[1..].each do |s|
#     until s.start_with?(prefix)
#       prefix = prefix.chop   # trim last character
#       return "" if prefix.empty?
#     end
#   end
#
#   prefix
# end
#
# puts longest_common_prefix(["flower","flow","flight"])   # -> "fl"
# puts longest_common_prefix(["dog","racecar","car"])      # -> ""
# puts longest_common_prefix(["a"])                        # -> "a"


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# Two clean approaches -- both shown across languages:
#
#   APPROACH A -- Vertical Scan (Python):
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  Take the shortest string (limits max prefix length).           │
#   │  For each character position i in the shortest string:         │
#   │    If any string has a different char at i -> return prefix[:i] │
#   │  If we finish the shortest string with no mismatches -> return  │
#   │  the shortest string itself (it IS the common prefix).          │
#   └──────────────────────────────────────────────────────────────────┘
#
#   APPROACH B -- Shrink the Candidate (JS/Java/C++/C#/Go/Rust/Swift/Kotlin/Ruby):
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  Start with the first string as the prefix "guess".            │
#   │  For each other string:                                         │
#   │    While that string does NOT start with prefix:                │
#   │      Chop one character off the end of prefix                  │
#   │      If prefix is now empty -> return ""                        │
#   │  Return prefix.                                                  │
#   └──────────────────────────────────────────────────────────────────┘
#
# Both approaches reach the same answer. The "shrink" approach is popular
# because startsWith / hasPrefix / starts_with are built-in in most languages.
#
# Time complexity:  O(S)  where S = total characters across all strings
#                          in the worst case we compare every character.
# Space complexity: O(1)  -- just the prefix string, no extra structures.
# =============================================================================
