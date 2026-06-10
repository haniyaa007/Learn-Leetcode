# =============================================================================
# LONGEST PALINDROMIC SUBSTRING
# =============================================================================
# PROBLEM: Given a string, find and RETURN the longest substring that is a
# palindrome (reads the same forwards and backwards).
#
# WHAT IS A PALINDROME?
#   A string that reads the same forwards AND backwards.
#   "racecar" → reversed: "racecar" ✓
#   "aba"     → reversed: "aba"     ✓
#   "abc"     → reversed: "cba"     ✗
#
# NOTE: Unlike problem #3 (longest substring), here we return the actual
# substring itself, not just its length.
# =============================================================================


# =============================================================================
# 1. PYTHON  ✅  (active - try running this!)
# =============================================================================
#
# THE APPROACH — "Expand Around Center":
#
# Every palindrome has a CENTER.
#   Odd-length palindromes have a single center character:
#     "r a c e c a r"  → center is 'e' at index 3
#   Even-length palindromes have a center between two characters:
#     "a b b a"         → center is between 'b' and 'b' (indices 1 and 2)
#
# THE STRATEGY:
#   Try every possible center (there are 2n-1 of them: n single chars + n-1 gaps).
#   From each center, expand outward as long as the characters match.
#   Track the longest palindrome found.
#
# STEP-BY-STEP with "babad":
#
#   Center at index 0 ('b'):   expand → "b"           length 1
#   Center at index 1 ('a'):   expand → "bab"         length 3  ← new best!
#     (s[0]='b' == s[2]='b' ✓, then s[-1] out of bounds → stop)
#   Center at gap 1-2:         s[1]='a' ≠ s[2]='b' → "a" only  length 1
#   Center at index 2 ('b'):   expand → "aba"         length 3  (tie, keep first)
#   Center at gap 2-3:         s[2]='b' ≠ s[3]='a' → length 1
#   Center at index 3 ('a'):   expand → "a"           length 1
#   Center at gap 3-4:         s[3]='a' ≠ s[4]='d' → length 1
#   Center at index 4 ('d'):   expand → "d"           length 1
#   Answer: "bab"  ✓
#
# THE EXPAND HELPER:
#   Takes a left pointer and right pointer (both start at the center).
#   While in bounds AND s[left] == s[right]: expand outward.
#   Returns the palindrome found.
#
# WHY NOT THE NAIVE APPROACH?
#   Checking every possible substring: O(n²) substrings × O(n) to verify each
#   = O(n³). Expand-around-center is O(n²) time with O(1) extra space.
#   (There's an even faster O(n) algorithm called Manacher's, but it's
#   significantly harder to understand — expand-around-center is the sweet spot.)

def longest_palindrome(s):

    def expand(left, right):
        # Keep expanding while we're in bounds AND characters match
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left  -= 1   # move left pointer outward (left)
            right += 1   # move right pointer outward (right)
        # When the loop exits, s[left] != s[right] (or out of bounds).
        # The LAST valid palindrome was s[left+1 : right]
        return s[left + 1 : right]

    best = ""  # track the longest palindrome found so far

    for i in range(len(s)):
        # Case 1 — ODD length: center is a single character at index i
        odd  = expand(i, i)

        # Case 2 — EVEN length: center is the gap between i and i+1
        even = expand(i, i + 1)

        # Update best if we found something longer
        if len(odd)  > len(best): best = odd
        if len(even) > len(best): best = even

    return best


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(longest_palindrome("babad"))    # → "bab"  (or "aba", both valid)
print(longest_palindrome("cbbd"))     # → "bb"
print(longest_palindrome("a"))        # → "a"
print(longest_palindrome("racecar"))  # → "racecar"
print(longest_palindrome("abcba"))    # → "abcba"
print(longest_palindrome("abacabad")) # → "abacaba"


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# slice(left+1, right) works just like Python's s[left+1:right].
# We compare lengths with .length instead of len().
#
# function longestPalindrome(s) {
#
#     function expand(left, right) {
#         while (left >= 0 && right < s.length && s[left] === s[right]) {
#             left--;
#             right++;
#         }
#         return s.slice(left + 1, right);
#     }
#
#     let best = "";
#
#     for (let i = 0; i < s.length; i++) {
#         const odd  = expand(i, i);
#         const even = expand(i, i + 1);
#         if (odd.length  > best.length) best = odd;
#         if (even.length > best.length) best = even;
#     }
#
#     return best;
# }
#
# console.log(longestPalindrome("babad"));    // → "bab"
# console.log(longestPalindrome("cbbd"));     // → "bb"
# console.log(longestPalindrome("racecar"));  // → "racecar"


# =============================================================================
# 3. JAVA
# =============================================================================
# substring(left+1, right) is Java's equivalent of Python's s[left+1:right].
# Note: Java's substring end index is exclusive, just like Python's.
#
# class Solution {
#
#     private String expand(String s, int left, int right) {
#         while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
#             left--;
#             right++;
#         }
#         return s.substring(left + 1, right);
#     }
#
#     public String longestPalindrome(String s) {
#         String best = "";
#
#         for (int i = 0; i < s.length(); i++) {
#             String odd  = expand(s, i, i);
#             String even = expand(s, i, i + 1);
#             if (odd.length()  > best.length()) best = odd;
#             if (even.length() > best.length()) best = even;
#         }
#
#         return best;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# s.substr(start, length) differs from Python — second arg is LENGTH not end index.
# So substr(left+1, right-left-1) gives us the palindrome.
#
# #include <string>
# #include <algorithm>
# using namespace std;
#
# string expand(const string& s, int left, int right) {
#     while (left >= 0 && right < (int)s.size() && s[left] == s[right]) {
#         left--;
#         right++;
#     }
#     // left+1 is start, length is (right-1) - (left+1) + 1 = right - left - 1
#     return s.substr(left + 1, right - left - 1);
# }
#
# string longestPalindrome(string s) {
#     string best = "";
#
#     for (int i = 0; i < (int)s.size(); i++) {
#         string odd  = expand(s, i, i);
#         string even = expand(s, i, i + 1);
#         if (odd.size()  > best.size()) best = odd;
#         if (even.size() > best.size()) best = even;
#     }
#
#     return best;
# }


# =============================================================================
# 5. C#
# =============================================================================
# Substring(start, length) — same as C++, second argument is length not end.
# s[i] directly indexes a C# string (no .charAt() needed like Java).
#
# public class Solution {
#
#     private string Expand(string s, int left, int right) {
#         while (left >= 0 && right < s.Length && s[left] == s[right]) {
#             left--;
#             right++;
#         }
#         return s.Substring(left + 1, right - left - 1);
#     }
#
#     public string LongestPalindrome(string s) {
#         string best = "";
#
#         for (int i = 0; i < s.Length; i++) {
#             string odd  = Expand(s, i, i);
#             string even = Expand(s, i, i + 1);
#             if (odd.Length  > best.Length) best = odd;
#             if (even.Length > best.Length) best = even;
#         }
#
#         return best;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# s[left+1:right] works exactly like Python for string slicing in Go.
# Go's for loop with two return values is a clean pattern.
#
# func longestPalindrome(s string) string {
#
#     expand := func(left, right int) string {
#         for left >= 0 && right < len(s) && s[left] == s[right] {
#             left--
#             right++
#         }
#         return s[left+1 : right]
#     }
#
#     best := ""
#
#     for i := 0; i < len(s); i++ {
#         odd  := expand(i, i)
#         even := expand(i, i+1)
#         if len(odd)  > len(best) { best = odd  }
#         if len(even) > len(best) { best = even }
#     }
#
#     return best
# }


# =============================================================================
# 7. RUST
# =============================================================================
# Rust strings are UTF-8 and can't be indexed directly with s[i].
# We collect chars into a Vec<char> first for easy indexing.
# &chars[left+1..right] slices the chars, then .iter().collect() rebuilds the String.
#
# fn longest_palindrome(s: String) -> String {
#     let chars: Vec<char> = s.chars().collect();
#     let n = chars.len();
#
#     let expand = |mut left: usize, mut right: usize| -> String {
#         // use isize to safely check left >= 0
#         let mut l = left as isize;
#         let mut r = right;
#         while l >= 0 && r < n && chars[l as usize] == chars[r] {
#             l -= 1;
#             r += 1;
#         }
#         chars[(l + 1) as usize..r].iter().collect()
#     };
#
#     let mut best = String::new();
#
#     for i in 0..n {
#         let odd  = expand(i, i);
#         let even = if i + 1 < n { expand(i, i + 1) } else { String::new() };
#         if odd.len()  > best.len() { best = odd;  }
#         if even.len() > best.len() { best = even; }
#     }
#
#     best
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# Swift strings use String.Index instead of integers for indexing.
# Converting to Array(s) gives us [Character] which we can index with integers.
# String(chars[start...end]) reconstructs the substring from a slice.
#
# func longestPalindrome(_ s: String) -> String {
#     let chars = Array(s)
#     let n = chars.count
#
#     func expand(_ left: Int, _ right: Int) -> String {
#         var l = left, r = right
#         while l >= 0 && r < n && chars[l] == chars[r] {
#             l -= 1
#             r += 1
#         }
#         return String(chars[(l + 1)..<r])
#     }
#
#     var best = ""
#
#     for i in 0..<n {
#         let odd  = expand(i, i)
#         let even = expand(i, i + 1)
#         if odd.count  > best.count { best = odd  }
#         if even.count > best.count { best = even }
#     }
#
#     return best
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# substring(start, end) in Kotlin — end is exclusive, same as Python's slice.
# The inner function 'expand' is declared with 'fun' inside the outer function.
#
# fun longestPalindrome(s: String): String {
#
#     fun expand(left: Int, right: Int): String {
#         var l = left; var r = right
#         while (l >= 0 && r < s.length && s[l] == s[r]) {
#             l--; r++
#         }
#         return s.substring(l + 1, r)
#     }
#
#     var best = ""
#
#     for (i in s.indices) {
#         val odd  = expand(i, i)
#         val even = expand(i, i + 1)
#         if (odd.length  > best.length) best = odd
#         if (even.length > best.length) best = even
#     }
#
#     return best
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# Ruby's s[start, length] slices a string (2nd arg is length, not end index).
# So s[left+1, right-left-1] gives the palindrome. Everything else is clean Ruby.
#
# def longest_palindrome(s)
#
#   expand = lambda do |left, right|
#     while left >= 0 && right < s.length && s[left] == s[right]
#       left  -= 1
#       right += 1
#     end
#     s[left + 1, right - left - 1]
#   end
#
#   best = ""
#
#   s.length.times do |i|
#     odd  = expand.call(i, i)
#     even = expand.call(i, i + 1)
#     best = odd  if odd.length  > best.length
#     best = even if even.length > best.length
#   end
#
#   best
# end
#
# puts longest_palindrome("babad")    # → "bab"
# puts longest_palindrome("cbbd")     # → "bb"
# puts longest_palindrome("racecar")  # → "racecar"


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use EXPAND AROUND CENTER:
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  For every index i (and every gap between i and i+1):           │
#   │                                                                  │
#   │    Start with left = i, right = i  (odd)                        │
#   │            or  left = i, right = i+1  (even)                    │
#   │                                                                  │
#   │    While s[left] == s[right]: expand outward                    │
#   │    When they differ (or hit a boundary): record the palindrome  │
#   │                                                                  │
#   │  Keep track of the longest one seen.                            │
#   └──────────────────────────────────────────────────────────────────┘
#
# Time complexity:  O(n²)  — n centers × up to n/2 expansions each
# Space complexity: O(1)   — just pointers and the result string
#                            (no extra arrays or matrices needed!)
#
# BONUS — there IS a faster O(n) algorithm: Manacher's Algorithm.
# It's a classic but tricky technique that pre-processes the string
# to avoid redundant expansions. Worth looking up once expand-around-
# center feels comfortable — but O(n²) passes all LeetCode test cases. 🪞
# =============================================================================
