# =============================================================================
# REGULAR EXPRESSION MATCHING
# =============================================================================
# PROBLEM: Given a string s and a pattern p, return True if p matches ALL of s.
# The pattern supports only two special characters:
#   '.'  → matches exactly ONE character (any character)
#   '*'  → matches ZERO OR MORE of the character that came just before it
#
# IMPORTANT: '*' never stands alone — it always refers to the preceding char.
#   "a*"  means "zero or more a's"
#   ".*"  means "zero or more of ANY character"
#   "c*"  means "zero or more c's"
#
# EXAMPLES:
#   s="aa",  p="a"    → False  ("a" only covers one character, not two)
#   s="aa",  p="a*"   → True   ("a*" can match two a's)
#   s="ab",  p=".*"   → True   (".*" matches any sequence of characters)
#   s="aab", p="c*a*b"→ True   ("c*" matches zero c's, "a*" matches "aa", "b" matches "b")
#   s="mississippi", p="mis*is*p*." → False
# =============================================================================


# =============================================================================
# 1. PYTHON  ✅  (active - try running this!)
# =============================================================================
#
# WHY IS THIS HARD?
#   The '*' character makes this tricky because it can match ZERO occurrences.
#   That means "c*" can disappear entirely! So we can't just walk both strings
#   left-to-right in sync — we need to consider multiple possibilities.
#
# THE APPROACH — Dynamic Programming (DP) with a 2D table:
#
#   We build a 2D grid:  dp[i][j] = True if p[0..j-1] matches s[0..i-1]
#
#   i = how many characters of s we've matched so far (0 = none)
#   j = how many characters of p we've used so far   (0 = none)
#
#   So dp[len(s)][len(p)] = True means "the whole pattern matches the whole string".
#
#   BASE CASE:
#     dp[0][0] = True   (empty pattern matches empty string)
#
#   FILLING THE FIRST ROW (empty string, non-empty pattern):
#     Only patterns like "a*", "a*b*", ".*" can match an empty string
#     (because '*' can mean zero occurrences).
#     dp[0][j] = dp[0][j-2]  when p[j-1] == '*'
#
#   FILLING THE REST:
#     Two cases for each cell dp[i][j]:
#
#     CASE 1 — Current pattern char is NOT '*':
#       The pattern char p[j-1] must directly match the string char s[i-1].
#       A match happens if they're equal OR if p[j-1] == '.'.
#       dp[i][j] = dp[i-1][j-1]  if  (p[j-1] == s[i-1] or p[j-1] == '.')
#
#     CASE 2 — Current pattern char IS '*':
#       '*' refers to the character before it: p[j-2].
#       We have two sub-choices:
#
#       a) Use ZERO occurrences of p[j-2]:
#          Just skip the "X*" pair entirely.
#          dp[i][j] = dp[i][j-2]
#
#       b) Use ONE OR MORE occurrences of p[j-2]:
#          The current string character s[i-1] must match p[j-2] (or p[j-2]=='.')
#          AND the pattern must have matched one fewer string character.
#          dp[i][j] = dp[i-1][j]  if  (p[j-2] == s[i-1] or p[j-2] == '.')
#
# STEP-BY-STEP VISUAL — s="aab", p="c*a*b":
#
#       ""  c  *  a  *  b
#   ""  T   F  T  F  T  F
#   a   F   F  F  T  T  F
#   a   F   F  F  F  T  F
#   b   F   F  F  F  F  T   <- dp[3][5] = True -> MATCH!
#
# (T = True, F = False)

def is_match(s, p):
    m, n = len(s), len(p)

    # dp[i][j] means: does p[0..j-1] match s[0..i-1]?
    # Size is (m+1) x (n+1) because index 0 means "empty"
    dp = [[False] * (n + 1) for _ in range(m + 1)]

    # Base case: empty pattern matches empty string
    dp[0][0] = True

    # Fill the first row: can the pattern match an EMPTY string?
    # Only "x*", "x*y*", etc. patterns can (by using zero occurrences)
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]   # use zero occurrences -> skip "x*"

    # Fill in the rest of the table, row by row
    for i in range(1, m + 1):
        for j in range(1, n + 1):

            if p[j - 1] == '*':
                # Option A: use zero occurrences of p[j-2] -- skip the "x*" pair
                zero_use = dp[i][j - 2]

                # Option B: use one more occurrence of p[j-2]
                # Only valid if p[j-2] matches current string char s[i-1]
                char_matches = (p[j - 2] == s[i - 1] or p[j - 2] == '.')
                one_more_use = dp[i - 1][j] if char_matches else False

                dp[i][j] = zero_use or one_more_use

            else:
                # No '*': pattern char must directly match string char
                char_matches = (p[j - 1] == s[i - 1] or p[j - 1] == '.')
                dp[i][j] = dp[i - 1][j - 1] and char_matches

    return dp[m][n]


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(is_match("aa",          "a"))          # -> False
print(is_match("aa",          "a*"))         # -> True
print(is_match("ab",          ".*"))         # -> True
print(is_match("aab",         "c*a*b"))      # -> True
print(is_match("mississippi", "mis*is*p*.")) # -> False
print(is_match("",            "a*"))         # -> True  (zero a's)
print(is_match("a",           "ab*"))        # -> True  (b* = zero b's)


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# Exact same DP logic. Arrays of booleans instead of Python lists.
# s[i-1] indexes a JS string directly (no .charAt() needed here).
#
# function isMatch(s, p) {
#     const m = s.length, n = p.length;
#     const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(false));
#
#     dp[0][0] = true;
#
#     for (let j = 2; j <= n; j++) {
#         if (p[j - 1] === '*') dp[0][j] = dp[0][j - 2];
#     }
#
#     for (let i = 1; i <= m; i++) {
#         for (let j = 1; j <= n; j++) {
#             if (p[j - 1] === '*') {
#                 const zeroUse = dp[i][j - 2];
#                 const charMatches = p[j - 2] === s[i - 1] || p[j - 2] === '.';
#                 dp[i][j] = zeroUse || (charMatches && dp[i - 1][j]);
#             } else {
#                 const charMatches = p[j - 1] === s[i - 1] || p[j - 1] === '.';
#                 dp[i][j] = dp[i - 1][j - 1] && charMatches;
#             }
#         }
#     }
#
#     return dp[m][n];
# }
#
# console.log(isMatch("aa",  "a"));     // -> false
# console.log(isMatch("aa",  "a*"));    // -> true
# console.log(isMatch("ab",  ".*"));    // -> true
# console.log(isMatch("aab", "c*a*b")); // -> true


# =============================================================================
# 3. JAVA
# =============================================================================
# boolean[][] is a 2D array of booleans. s.charAt(i-1) and p.charAt(j-1)
# access characters (Java strings aren't directly indexable with []).
#
# class Solution {
#     public boolean isMatch(String s, String p) {
#         int m = s.length(), n = p.length();
#         boolean[][] dp = new boolean[m + 1][n + 1];
#
#         dp[0][0] = true;
#
#         for (int j = 2; j <= n; j++) {
#             if (p.charAt(j - 1) == '*') dp[0][j] = dp[0][j - 2];
#         }
#
#         for (int i = 1; i <= m; i++) {
#             for (int j = 1; j <= n; j++) {
#                 char pc = p.charAt(j - 1);
#                 char sc = s.charAt(i - 1);
#
#                 if (pc == '*') {
#                     char prev = p.charAt(j - 2);
#                     boolean zeroUse = dp[i][j - 2];
#                     boolean charMatches = prev == sc || prev == '.';
#                     dp[i][j] = zeroUse || (charMatches && dp[i - 1][j]);
#                 } else {
#                     boolean charMatches = pc == sc || pc == '.';
#                     dp[i][j] = dp[i - 1][j - 1] && charMatches;
#                 }
#             }
#         }
#
#         return dp[m][n];
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# vector<vector<bool>> is the 2D DP table. s[i-1] and p[j-1] index strings.
#
# #include <string>
# #include <vector>
# using namespace std;
#
# bool isMatch(string s, string p) {
#     int m = s.size(), n = p.size();
#     vector<vector<bool>> dp(m + 1, vector<bool>(n + 1, false));
#
#     dp[0][0] = true;
#
#     for (int j = 2; j <= n; j++) {
#         if (p[j - 1] == '*') dp[0][j] = dp[0][j - 2];
#     }
#
#     for (int i = 1; i <= m; i++) {
#         for (int j = 1; j <= n; j++) {
#             if (p[j - 1] == '*') {
#                 bool zeroUse     = dp[i][j - 2];
#                 bool charMatches = p[j - 2] == s[i - 1] || p[j - 2] == '.';
#                 dp[i][j] = zeroUse || (charMatches && dp[i - 1][j]);
#             } else {
#                 bool charMatches = p[j - 1] == s[i - 1] || p[j - 1] == '.';
#                 dp[i][j] = dp[i - 1][j - 1] && charMatches;
#             }
#         }
#     }
#
#     return dp[m][n];
# }


# =============================================================================
# 5. C#
# =============================================================================
# bool[,] is C#'s 2D array syntax. Indexing is dp[i, j] with a comma.
#
# public class Solution {
#     public bool IsMatch(string s, string p) {
#         int m = s.Length, n = p.Length;
#         bool[,] dp = new bool[m + 1, n + 1];
#
#         dp[0, 0] = true;
#
#         for (int j = 2; j <= n; j++) {
#             if (p[j - 1] == '*') dp[0, j] = dp[0, j - 2];
#         }
#
#         for (int i = 1; i <= m; i++) {
#             for (int j = 1; j <= n; j++) {
#                 if (p[j - 1] == '*') {
#                     bool zeroUse     = dp[i, j - 2];
#                     bool charMatches = p[j - 2] == s[i - 1] || p[j - 2] == '.';
#                     dp[i, j] = zeroUse || (charMatches && dp[i - 1, j]);
#                 } else {
#                     bool charMatches = p[j - 1] == s[i - 1] || p[j - 1] == '.';
#                     dp[i, j] = dp[i - 1, j - 1] && charMatches;
#                 }
#             }
#         }
#
#         return dp[m, n];
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# [][]bool is a slice of bool slices -- Go's way of making a 2D array.
# s[i-1] and p[j-1] work on Go strings (they return bytes, fine for ASCII).
#
# func isMatch(s string, p string) bool {
#     m, n := len(s), len(p)
#     dp := make([][]bool, m+1)
#     for i := range dp {
#         dp[i] = make([]bool, n+1)
#     }
#
#     dp[0][0] = true
#
#     for j := 2; j <= n; j++ {
#         if p[j-1] == '*' { dp[0][j] = dp[0][j-2] }
#     }
#
#     for i := 1; i <= m; i++ {
#         for j := 1; j <= n; j++ {
#             if p[j-1] == '*' {
#                 charMatches := p[j-2] == s[i-1] || p[j-2] == '.'
#                 dp[i][j] = dp[i][j-2] || (charMatches && dp[i-1][j])
#             } else {
#                 charMatches := p[j-1] == s[i-1] || p[j-1] == '.'
#                 dp[i][j] = dp[i-1][j-1] && charMatches
#             }
#         }
#     }
#
#     return dp[m][n]
# }


# =============================================================================
# 7. RUST
# =============================================================================
# Vec<Vec<bool>> is Rust's 2D boolean table.
# as_bytes() converts the string to a byte slice for easy indexing.
# b'*' and b'.' are byte literals.
#
# fn is_match(s: String, p: String) -> bool {
#     let s = s.as_bytes();
#     let p = p.as_bytes();
#     let (m, n) = (s.len(), p.len());
#     let mut dp = vec![vec![false; n + 1]; m + 1];
#
#     dp[0][0] = true;
#
#     for j in 2..=n {
#         if p[j - 1] == b'*' { dp[0][j] = dp[0][j - 2]; }
#     }
#
#     for i in 1..=m {
#         for j in 1..=n {
#             if p[j - 1] == b'*' {
#                 let char_matches = p[j - 2] == s[i - 1] || p[j - 2] == b'.';
#                 dp[i][j] = dp[i][j - 2] || (char_matches && dp[i - 1][j]);
#             } else {
#                 let char_matches = p[j - 1] == s[i - 1] || p[j - 1] == b'.';
#                 dp[i][j] = dp[i - 1][j - 1] && char_matches;
#             }
#         }
#     }
#
#     dp[m][n]
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# [[Bool]] is Swift's 2D boolean array. Array(s) and Array(p) convert
# String -> [Character] for easy subscript indexing.
#
# func isMatch(_ s: String, _ p: String) -> Bool {
#     let sc = Array(s), pc = Array(p)
#     let m = sc.count, n = pc.count
#     var dp = [[Bool]](repeating: [Bool](repeating: false, count: n + 1), count: m + 1)
#
#     dp[0][0] = true
#
#     for j in 2...max(2, n) where j <= n {
#         if pc[j - 1] == "*" { dp[0][j] = dp[0][j - 2] }
#     }
#
#     for i in 1...m {
#         for j in 1...n {
#             if pc[j - 1] == "*" {
#                 let charMatches = pc[j - 2] == sc[i - 1] || pc[j - 2] == "."
#                 dp[i][j] = dp[i][j - 2] || (charMatches && dp[i - 1][j])
#             } else {
#                 let charMatches = pc[j - 1] == sc[i - 1] || pc[j - 1] == "."
#                 dp[i][j] = dp[i - 1][j - 1] && charMatches
#             }
#         }
#     }
#
#     return dp[m][n]
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# Array(m+1) { BooleanArray(n+1) } creates the 2D DP table.
# s[i-1] and p[j-1] return Char in Kotlin, compared with == directly.
#
# fun isMatch(s: String, p: String): Boolean {
#     val m = s.length; val n = p.length
#     val dp = Array(m + 1) { BooleanArray(n + 1) }
#
#     dp[0][0] = true
#
#     for (j in 2..n) {
#         if (p[j - 1] == '*') dp[0][j] = dp[0][j - 2]
#     }
#
#     for (i in 1..m) {
#         for (j in 1..n) {
#             if (p[j - 1] == '*') {
#                 val charMatches = p[j - 2] == s[i - 1] || p[j - 2] == '.'
#                 dp[i][j] = dp[i][j - 2] || (charMatches && dp[i - 1][j])
#             } else {
#                 val charMatches = p[j - 1] == s[i - 1] || p[j - 1] == '.'
#                 dp[i][j] = dp[i - 1][j - 1] && charMatches
#             }
#         }
#     }
#
#     return dp[m][n]
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# Array.new(m+1) { Array.new(n+1, false) } creates the 2D DP table.
# s[i-1] and p[j-1] return single-character strings in Ruby.
#
# def is_match(s, p)
#   m, n = s.length, p.length
#   dp = Array.new(m + 1) { Array.new(n + 1, false) }
#
#   dp[0][0] = true
#
#   (2..n).each do |j|
#     dp[0][j] = dp[0][j - 2] if p[j - 1] == '*'
#   end
#
#   (1..m).each do |i|
#     (1..n).each do |j|
#       if p[j - 1] == '*'
#         char_matches = p[j - 2] == s[i - 1] || p[j - 2] == '.'
#         dp[i][j] = dp[i][j - 2] || (char_matches && dp[i - 1][j])
#       else
#         char_matches = p[j - 1] == s[i - 1] || p[j - 1] == '.'
#         dp[i][j] = dp[i - 1][j - 1] && char_matches
#       end
#     end
#   end
#
#   dp[m][n]
# end
#
# puts is_match("aa",  "a")      # -> false
# puts is_match("aa",  "a*")     # -> true
# puts is_match("ab",  ".*")     # -> true
# puts is_match("aab", "c*a*b")  # -> true


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use 2D DYNAMIC PROGRAMMING:
#
#   dp[i][j] = "does pattern p[0..j-1] fully match string s[0..i-1]?"
#
#   BASE:  dp[0][0] = True  (empty matches empty)
#          dp[0][j] = dp[0][j-2]  when p[j-1]=='*'  (zero occurrences)
#
#   RECURRENCE:
#
#   If p[j-1] is NOT '*':
#     dp[i][j] = dp[i-1][j-1]  AND  (p[j-1]==s[i-1] or p[j-1]=='.')
#
#   If p[j-1] IS '*':
#     Option A (zero uses):  dp[i][j-2]
#     Option B (one more):   dp[i-1][j]  if p[j-2] matches s[i-1]
#     dp[i][j] = A OR B
#
#   Answer: dp[len(s)][len(p)]
#
# Time complexity:  O(m x n)  -- fill every cell of the (m+1)x(n+1) table
# Space complexity: O(m x n)  -- the table itself
#
# The trick with '*' is always the same two choices:
#   1. IGNORE it (zero uses) -- jump back 2 positions in the pattern
#   2. USE it (one more match) -- consume one char from s, stay on same pattern pos
#
# This is the first problem in this series that uses DYNAMIC PROGRAMMING.
# DP problems feel magical at first -- the key is understanding what
# dp[i][j] MEANS before writing any code. The formula follows naturally. 
# =============================================================================
