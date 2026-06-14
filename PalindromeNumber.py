# =============================================================================
# PALINDROME NUMBER
# =============================================================================
# PROBLEM: Given an integer x, return True if it reads the same forwards
# and backwards, and False otherwise.
#
# QUICK OBSERVATIONS (catch these early to avoid wasted work):
#   - Any NEGATIVE number is never a palindrome → "-121" reversed is "121-"
#   - Any number ending in 0 (except 0 itself) is never a palindrome
#     → 10 reversed is 01, which is just 1, not 10
#   - 0 itself IS a palindrome
#
# EXAMPLES:
#   121   → True   (same forwards and backwards)
#  -121   → False  (negative numbers never are)
#   10    → False  (ends in 0)
#   1221  → True
#   12321 → True
# =============================================================================


# =============================================================================
# 1. PYTHON  ✅  (active - try running this!)
# =============================================================================
#
# We show TWO approaches — the easy string way, and the follow-up
# "no string conversion" way. Both are fully explained below.
#
# ─────────────────────────────────────────────────────
# APPROACH A — Convert to string, reverse, compare
# ─────────────────────────────────────────────────────
# This is the most intuitive approach.
# str(121) → "121",  reversed → "121",  same? → True
# str(-121) → "-121", reversed → "121-", same? → False
#
# def is_palindrome_string(x):
#     return str(x) == str(x)[::-1]
#
# ─────────────────────────────────────────────────────
# APPROACH B — Reverse only HALF the number (no string)
# ─────────────────────────────────────────────────────
# The follow-up asks: can you do it without converting to a string?
#
# KEY INSIGHT: you don't need to reverse the WHOLE number.
# Just reverse the SECOND HALF and compare it to the FIRST HALF.
#
# Why only half?
#   - It's more efficient.
#   - It neatly avoids the overflow problem (reversing all digits of a big
#     number could exceed 32-bit range; reversing half is always safe).
#
# HOW TO KNOW WHEN YOU'VE REACHED THE HALFWAY POINT:
#   Keep plucking digits off the right side of x, building `reversed_half`.
#   Stop when reversed_half >= x.
#   At that point, reversed_half has at least as many digits as what's left in x.
#
# STEP-BY-STEP with x = 1221:
#
#   Start:          x = 1221,  reversed_half = 0
#   Pluck digit 1:  x = 122,   reversed_half = 1      (1 < 122, keep going)
#   Pluck digit 2:  x = 12,    reversed_half = 12     (12 >= 12, STOP)
#   x == reversed_half  →  12 == 12  →  True ✓
#
# STEP-BY-STEP with x = 12321 (ODD number of digits):
#
#   Start:          x = 12321, reversed_half = 0
#   Pluck digit 1:  x = 1232,  reversed_half = 1
#   Pluck digit 2:  x = 123,   reversed_half = 12
#   Pluck digit 3:  x = 12,    reversed_half = 123    (123 >= 12, STOP)
#   Odd digits → middle digit is in reversed_half, ignore it with //10:
#   x == reversed_half // 10  →  12 == 12  →  True ✓
#
# STEP-BY-STEP with x = 1231:
#
#   Start:          x = 1231, reversed_half = 0
#   Pluck digit 1:  x = 123,  reversed_half = 1
#   Pluck digit 3:  x = 12,   reversed_half = 13
#   Pluck digit 2:  x = 1,    reversed_half = 132    (132 >= 1, STOP)
#   x == reversed_half  →  1 == 132  →  False ✓  (not a palindrome)

def is_palindrome(x):
    # Early exit: negatives and numbers ending in 0 (except 0) are never palindromes
    if x < 0 or (x % 10 == 0 and x != 0):
        return False

    reversed_half = 0

    # Pluck digits from the right of x and build reversed_half
    # Stop when reversed_half has caught up to (or passed) x
    while x > reversed_half:
        digit = x % 10          # grab the last digit of x
        x //= 10                # remove the last digit from x
        reversed_half = reversed_half * 10 + digit   # append to reversed_half

    # Even digit count: x == reversed_half          e.g. 1221 → 12 == 12
    # Odd digit count:  x == reversed_half // 10    e.g. 12321 → 12 == 123//10
    return x == reversed_half or x == reversed_half // 10


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(is_palindrome(121))     # → True
print(is_palindrome(-121))    # → False
print(is_palindrome(10))      # → False
print(is_palindrome(0))       # → True
print(is_palindrome(1221))    # → True
print(is_palindrome(12321))   # → True
print(is_palindrome(1231))    # → False


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# The string approach is two lines. The half-reversal approach is shown here
# since it's the more interesting follow-up answer.
# Math.floor(x / 10) chops the last digit (integer division).
#
# function isPalindrome(x) {
#     if (x < 0 || (x % 10 === 0 && x !== 0)) return false;
#
#     let reversedHalf = 0;
#
#     while (x > reversedHalf) {
#         reversedHalf = reversedHalf * 10 + (x % 10);
#         x = Math.floor(x / 10);
#     }
#
#     return x === reversedHalf || x === Math.floor(reversedHalf / 10);
# }
#
# console.log(isPalindrome(121));    // → true
# console.log(isPalindrome(-121));   // → false
# console.log(isPalindrome(10));     // → false
# console.log(isPalindrome(1221));   // → true
# console.log(isPalindrome(12321));  // → true


# =============================================================================
# 3. JAVA
# =============================================================================
# Identical logic to JavaScript. Java's int division already truncates (floors),
# so x / 10 and x % 10 work exactly as expected.
#
# class Solution {
#     public boolean isPalindrome(int x) {
#         if (x < 0 || (x % 10 == 0 && x != 0)) return false;
#
#         int reversedHalf = 0;
#
#         while (x > reversedHalf) {
#             reversedHalf = reversedHalf * 10 + x % 10;
#             x /= 10;
#         }
#
#         return x == reversedHalf || x == reversedHalf / 10;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# Same approach. In C++ all integer division is truncating (floors toward zero),
# so the math is identical. We return a bool instead of boolean.
#
# class Solution {
# public:
#     bool isPalindrome(int x) {
#         if (x < 0 || (x % 10 == 0 && x != 0)) return false;
#
#         int reversedHalf = 0;
#
#         while (x > reversedHalf) {
#             reversedHalf = reversedHalf * 10 + x % 10;
#             x /= 10;
#         }
#
#         return x == reversedHalf || x == reversedHalf / 10;
#     }
# };


# =============================================================================
# 5. C#
# =============================================================================
# C# looks almost identical to Java. 'bool' is the return type (not 'boolean').
# Integer division and modulo work the same as Java and C++.
#
# public class Solution {
#     public bool IsPalindrome(int x) {
#         if (x < 0 || (x % 10 == 0 && x != 0)) return false;
#
#         int reversedHalf = 0;
#
#         while (x > reversedHalf) {
#             reversedHalf = reversedHalf * 10 + x % 10;
#             x /= 10;
#         }
#
#         return x == reversedHalf || x == reversedHalf / 10;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# Go's integer division and modulo behave the same as C/Java.
# Functions return bool. No parentheses needed around if conditions.
#
# func isPalindrome(x int) bool {
#     if x < 0 || (x%10 == 0 && x != 0) {
#         return false
#     }
#
#     reversedHalf := 0
#
#     for x > reversedHalf {
#         reversedHalf = reversedHalf*10 + x%10
#         x /= 10
#     }
#
#     return x == reversedHalf || x == reversedHalf/10
# }


# =============================================================================
# 7. RUST
# =============================================================================
# i32 is Rust's 32-bit signed integer. The logic is identical to all others.
# Rust's integer division truncates toward zero, just like C/Java/Go.
# Note: Rust doesn't panic on this because we guard against overflow with
# our early exit (no negative numbers, no trailing zeros except x==0).
#
# fn is_palindrome(x: i32) -> bool {
#     if x < 0 || (x % 10 == 0 && x != 0) {
#         return false;
#     }
#
#     let mut x = x;
#     let mut reversed_half = 0i32;
#
#     while x > reversed_half {
#         reversed_half = reversed_half * 10 + x % 10;
#         x /= 10;
#     }
#
#     x == reversed_half || x == reversed_half / 10
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# Swift's Int is 64-bit on modern Apple platforms, but the algorithm
# works identically. The return type is Bool (capital B in Swift).
#
# func isPalindrome(_ x: Int) -> Bool {
#     if x < 0 || (x % 10 == 0 && x != 0) { return false }
#
#     var x = x
#     var reversedHalf = 0
#
#     while x > reversedHalf {
#         reversedHalf = reversedHalf * 10 + x % 10
#         x /= 10
#     }
#
#     return x == reversedHalf || x == reversedHalf / 10
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# Kotlin's Int is 32-bit. The logic is identical to Java (Kotlin runs on JVM).
# 'fun' declares a function; Boolean is the return type.
#
# fun isPalindrome(x: Int): Boolean {
#     if (x < 0 || (x % 10 == 0 && x != 0)) return false
#
#     var num = x
#     var reversedHalf = 0
#
#     while (num > reversedHalf) {
#         reversedHalf = reversedHalf * 10 + num % 10
#         num /= 10
#     }
#
#     return num == reversedHalf || num == reversedHalf / 10
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# Ruby's integers are arbitrary precision, so no overflow concern at all.
# We can also show the ultra-clean string version as a one-liner:
#   x.to_s == x.to_s.reverse
# But the half-reversal approach is shown here for consistency.
#
# def is_palindrome(x)
#   return false if x < 0 || (x % 10 == 0 && x != 0)
#
#   reversed_half = 0
#
#   while x > reversed_half
#     reversed_half = reversed_half * 10 + x % 10
#     x /= 10
#   end
#
#   x == reversed_half || x == reversed_half / 10
# end
#
# puts is_palindrome(121)    # → true
# puts is_palindrome(-121)   # → false
# puts is_palindrome(10)     # → false
# puts is_palindrome(1221)   # → true
# puts is_palindrome(12321)  # → true


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# TWO VALID APPROACHES:
#
#   EASY — String conversion (Python/Ruby one-liner):
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  str(x) == str(x)[::-1]                                        │
#   │  Fast to write, totally readable, perfectly valid.              │
#   └──────────────────────────────────────────────────────────────────┘
#
#   FOLLOW-UP — Reverse only HALF the digits (no string):
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  Early exits: negative x → False                                │
#   │               x ends in 0 (and x != 0) → False                 │
#   │                                                                  │
#   │  While x > reversed_half:                                       │
#   │      pluck last digit of x                                      │
#   │      append it to reversed_half                                 │
#   │                                                                  │
#   │  Even digits: x == reversed_half          (e.g. 1221)           │
#   │  Odd  digits: x == reversed_half // 10    (e.g. 12321)          │
#   └──────────────────────────────────────────────────────────────────┘
#
# Time complexity:  O(log x)  — we process half the digits of x
# Space complexity: O(1)      — just two integer variables
#
# WHY ONLY HALF?
#   Reversing half is enough to check symmetry, AND it cleverly avoids
#   ever needing to store a reversed number larger than the original,
#   which could overflow in fixed-size integer languages. 🪞
# =============================================================================
