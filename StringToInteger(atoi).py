# =============================================================================
# STRING TO INTEGER (atoi)
# =============================================================================
# PROBLEM: Convert a string to a 32-bit signed integer, following these rules:
#   1. Skip leading whitespace
#   2. Read an optional '+' or '-' sign
#   3. Read digits until a non-digit character or end of string
#   4. Clamp to 32-bit range if the result overflows
#
# WHY IS THIS INTERESTING?
#   Python's int("42") does all of this in one call — but this problem wants
#   you to handle it manually, character by character, with edge cases:
#   leading spaces, signs, mid-string letters, overflow, empty input, etc.
#
# EXAMPLES:
#   "42"            → 42
#   "   -042"       → -42       (leading spaces, then negative, leading zeros ok)
#   "1337c0d3"      → 1337      (stops at 'c', doesn't include it)
#   "0-1"           → 0         (stops at '-', since '-' after digits = non-digit)
#   "words and 987" → 0         (starts with 'w' = non-digit, so result is 0)
#   "99999999999"   → 2147483647  (clamped to INT_MAX)
# =============================================================================


# =============================================================================
# 1. PYTHON  ✅  (active - try running this!)
# =============================================================================
#
# STEP-BY-STEP WALKTHROUGH with "   -042abc":
#
#   i=0,1,2: spaces → skip (i becomes 3)
#   i=3: '-' → sign = -1, advance i to 4
#   i=4: '0' → digit! result = 0*10 + 0 = 0,   i=5
#   i=5: '4' → digit! result = 0*10 + 4 = 4,   i=6
#   i=6: '2' → digit! result = 4*10 + 2 = 42,  i=7
#   i=7: 'a' → NOT a digit → STOP
#   Apply sign: -1 * 42 = -42
#   Clamp to [-2147483648, 2147483647]: -42 is inside → return -42  ✓
#
# THE CLAMPING RULE (Step 4 / "Rounding"):
#   If result >  2147483647 → return  2147483647  (INT_MAX)
#   If result < -2147483648 → return -2147483648  (INT_MIN)
#   This is called CLAMPING — squishing the value to fit in the allowed range.
#
# HOW TO CHECK IF A CHARACTER IS A DIGIT:
#   Use char.isdigit()  → True for '0'..'9', False for everything else.
#   To get the numeric value: int(char)  e.g. int('7') = 7
#   OR: ord(char) - ord('0')  (the "ordinal"/ASCII trick used in other languages)

def my_atoi(s):
    INT_MIN = -(2**31)       # -2,147,483,648
    INT_MAX =  2**31 - 1     #  2,147,483,647

    i = 0
    n = len(s)

    # Step 1 — skip leading whitespace
    while i < n and s[i] == ' ':
        i += 1

    # Step 2 — read optional sign
    sign = 1
    if i < n and s[i] in ('+', '-'):
        if s[i] == '-':
            sign = -1
        i += 1

    # Step 3 — read digits, building the result one digit at a time
    result = 0
    while i < n and s[i].isdigit():
        digit = int(s[i])
        result = result * 10 + digit   # shift left by one decimal place, add digit
        i += 1

    # Apply the sign
    result *= sign

    # Step 4 — clamp to 32-bit range
    return max(INT_MIN, min(INT_MAX, result))
    # max(INT_MIN, ...) handles underflow  (too negative → INT_MIN)
    # min(INT_MAX, ...) handles overflow   (too positive → INT_MAX)


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(my_atoi("42"))              # → 42
print(my_atoi("   -042"))         # → -42
print(my_atoi("1337c0d3"))        # → 1337
print(my_atoi("0-1"))             # → 0
print(my_atoi("words and 987"))   # → 0
print(my_atoi("-91283472332"))     # → -2147483648  (clamped to INT_MIN)
print(my_atoi("91283472332"))      # → 2147483647   (clamped to INT_MAX)
print(my_atoi(""))                 # → 0


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# charCodeAt(i) - 48 converts a digit character to its numeric value.
# (ASCII code of '0' is 48, so '7'.charCodeAt(0) - 48 = 55 - 48 = 7)
# Everything else follows the same 4-step pattern as Python.
#
# function myAtoi(s) {
#     const INT_MIN = -(2**31);
#     const INT_MAX =  2**31 - 1;
#     let i = 0, n = s.length;
#
#     // Step 1 — skip whitespace
#     while (i < n && s[i] === ' ') i++;
#
#     // Step 2 — read sign
#     let sign = 1;
#     if (i < n && (s[i] === '+' || s[i] === '-')) {
#         if (s[i] === '-') sign = -1;
#         i++;
#     }
#
#     // Step 3 — read digits
#     let result = 0;
#     while (i < n && s[i] >= '0' && s[i] <= '9') {
#         const digit = s.charCodeAt(i) - 48;
#         result = result * 10 + digit;
#         i++;
#     }
#
#     // Step 4 — apply sign and clamp
#     result *= sign;
#     return Math.max(INT_MIN, Math.min(INT_MAX, result));
# }
#
# console.log(myAtoi("42"));              // → 42
# console.log(myAtoi("   -042"));         // → -42
# console.log(myAtoi("1337c0d3"));        // → 1337
# console.log(myAtoi("-91283472332"));     // → -2147483648


# =============================================================================
# 3. JAVA
# =============================================================================
# Character.isDigit(c) checks for a digit. (c - '0') extracts the numeric value.
# We accumulate into a long to safely detect overflow BEFORE clamping.
# Without long, adding digits to an int would silently wrap around.
#
# class Solution {
#     public int myAtoi(String s) {
#         int i = 0, n = s.length();
#
#         // Step 1 — skip whitespace
#         while (i < n && s.charAt(i) == ' ') i++;
#
#         // Step 2 — read sign
#         int sign = 1;
#         if (i < n && (s.charAt(i) == '+' || s.charAt(i) == '-')) {
#             if (s.charAt(i) == '-') sign = -1;
#             i++;
#         }
#
#         // Step 3 — read digits into a long (prevents overflow during buildup)
#         long result = 0;
#         while (i < n && Character.isDigit(s.charAt(i))) {
#             int digit = s.charAt(i) - '0';
#             result = result * 10 + digit;
#             i++;
#         }
#
#         // Step 4 — apply sign and clamp
#         result *= sign;
#         return (int) Math.max(Integer.MIN_VALUE, Math.min(Integer.MAX_VALUE, result));
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# isdigit(c) from <cctype> checks for digit characters.
# (c - '0') is the classic C/C++ way to get a digit's integer value.
# long long accumulates safely; then we clamp before returning int.
#
# #include <string>
# #include <cctype>
# #include <climits>
# #include <algorithm>
# using namespace std;
#
# int myAtoi(string s) {
#     int i = 0, n = s.size();
#
#     // Step 1 — skip whitespace
#     while (i < n && s[i] == ' ') i++;
#
#     // Step 2 — read sign
#     int sign = 1;
#     if (i < n && (s[i] == '+' || s[i] == '-')) {
#         if (s[i] == '-') sign = -1;
#         i++;
#     }
#
#     // Step 3 — read digits
#     long long result = 0;
#     while (i < n && isdigit(s[i])) {
#         int digit = s[i] - '0';
#         result = result * 10 + digit;
#         i++;
#     }
#
#     // Step 4 — apply sign and clamp
#     result *= sign;
#     result = max((long long)INT_MIN, min((long long)INT_MAX, result));
#     return (int) result;
# }


# =============================================================================
# 5. C#
# =============================================================================
# char.IsDigit(c) checks for digits. (c - '0') extracts the value.
# long is C#'s 64-bit integer. (int) casts down after clamping.
# System.Math.Clamp(value, min, max) is a neat built-in for clamping.
#
# public class Solution {
#     public int MyAtoi(string s) {
#         int i = 0, n = s.Length;
#
#         // Step 1 — skip whitespace
#         while (i < n && s[i] == ' ') i++;
#
#         // Step 2 — read sign
#         int sign = 1;
#         if (i < n && (s[i] == '+' || s[i] == '-')) {
#             if (s[i] == '-') sign = -1;
#             i++;
#         }
#
#         // Step 3 — read digits
#         long result = 0;
#         while (i < n && char.IsDigit(s[i])) {
#             int digit = s[i] - '0';
#             result = result * 10 + digit;
#             i++;
#         }
#
#         // Step 4 — apply sign and clamp
#         result *= sign;
#         return (int) System.Math.Clamp(result, int.MinValue, int.MaxValue);
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# unicode.IsDigit(rune) or simply checking c >= '0' && c <= '9' both work.
# We use the range check here to avoid importing unicode for such a simple check.
# int64 accumulates safely; we clamp and return int at the end.
#
# import "math"
#
# func myAtoi(s string) int {
#     i, n := 0, len(s)
#
#     // Step 1 — skip whitespace
#     for i < n && s[i] == ' ' { i++ }
#
#     // Step 2 — read sign
#     sign := 1
#     if i < n && (s[i] == '+' || s[i] == '-') {
#         if s[i] == '-' { sign = -1 }
#         i++
#     }
#
#     // Step 3 — read digits
#     var result int64
#     for i < n && s[i] >= '0' && s[i] <= '9' {
#         digit := int64(s[i] - '0')
#         result = result*10 + digit
#         i++
#     }
#
#     // Step 4 — apply sign and clamp
#     result *= int64(sign)
#     if result < math.MinInt32 { return math.MinInt32 }
#     if result > math.MaxInt32 { return math.MaxInt32 }
#     return int(result)
# }


# =============================================================================
# 7. RUST
# =============================================================================
# chars().nth(i) accesses a char by index — Rust strings are UTF-8 so we
# collect into a Vec<char> first for easy indexing.
# is_ascii_digit() checks '0'..='9'. to_digit(10) converts '7' → 7.
# i64 accumulates safely; i32::MIN/MAX are the clamp bounds.
#
# fn my_atoi(s: String) -> i32 {
#     let chars: Vec<char> = s.chars().collect();
#     let n = chars.len();
#     let mut i = 0;
#
#     // Step 1 — skip whitespace
#     while i < n && chars[i] == ' ' { i += 1; }
#
#     // Step 2 — read sign
#     let mut sign: i64 = 1;
#     if i < n && (chars[i] == '+' || chars[i] == '-') {
#         if chars[i] == '-' { sign = -1; }
#         i += 1;
#     }
#
#     // Step 3 — read digits
#     let mut result: i64 = 0;
#     while i < n && chars[i].is_ascii_digit() {
#         let digit = chars[i].to_digit(10).unwrap() as i64;
#         result = result * 10 + digit;
#         i += 1;
#     }
#
#     // Step 4 — apply sign and clamp
#     result *= sign;
#     result.clamp(i32::MIN as i64, i32::MAX as i64) as i32
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# Array(s) converts String → [Character] for index access.
# c.isNumber checks for digit characters; c.wholeNumberValue extracts the int.
# Swift's Int is 64-bit on modern platforms, so overflow isn't a concern here.
#
# func myAtoi(_ s: String) -> Int {
#     let chars = Array(s)
#     let n = chars.count
#     var i = 0
#
#     // Step 1 — skip whitespace
#     while i < n && chars[i] == " " { i += 1 }
#
#     // Step 2 — read sign
#     var sign = 1
#     if i < n && (chars[i] == "+" || chars[i] == "-") {
#         if chars[i] == "-" { sign = -1 }
#         i += 1
#     }
#
#     // Step 3 — read digits
#     var result = 0
#     while i < n, let digit = chars[i].wholeNumberValue {
#         result = result * 10 + digit
#         i += 1
#     }
#
#     // Step 4 — apply sign and clamp
#     result *= sign
#     return max(Int(Int32.min), min(Int(Int32.max), result))
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# isDigit() checks digit chars. digitToInt() converts '7' → 7.
# Long accumulates safely; toLong() and toInt() make the casts explicit.
# coerceIn() is Kotlin's built-in clamp — very clean!
#
# fun myAtoi(s: String): Int {
#     var i = 0; val n = s.length
#
#     // Step 1 — skip whitespace
#     while (i < n && s[i] == ' ') i++
#
#     // Step 2 — read sign
#     var sign = 1L
#     if (i < n && (s[i] == '+' || s[i] == '-')) {
#         if (s[i] == '-') sign = -1L
#         i++
#     }
#
#     // Step 3 — read digits
#     var result = 0L
#     while (i < n && s[i].isDigit()) {
#         result = result * 10 + s[i].digitToInt()
#         i++
#     }
#
#     // Step 4 — apply sign and clamp
#     result *= sign
#     return result.coerceIn(Int.MIN_VALUE.toLong(), Int.MAX_VALUE.toLong()).toInt()
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# each_char.with_index lets us walk the string with an index.
# '0'..'9' range check confirms a digit. (c.ord - '0'.ord) extracts value.
# Ruby's clamp(min, max) is built right into Comparable — very elegant.
#
# def my_atoi(s)
#   INT_MIN = -(2**31)
#   INT_MAX =  2**31 - 1
#   i, n = 0, s.length
#
#   # Step 1 — skip whitespace
#   i += 1 while i < n && s[i] == ' '
#
#   # Step 2 — read sign
#   sign = 1
#   if i < n && (s[i] == '+' || s[i] == '-')
#     sign = -1 if s[i] == '-'
#     i += 1
#   end
#
#   # Step 3 — read digits
#   result = 0
#   while i < n && s[i] >= '0' && s[i] <= '9'
#     digit = s[i].ord - '0'.ord
#     result = result * 10 + digit
#     i += 1
#   end
#
#   # Step 4 — apply sign and clamp
#   (result * sign).clamp(INT_MIN, INT_MAX)
# end
#
# puts my_atoi("42")              # → 42
# puts my_atoi("   -042")         # → -42
# puts my_atoi("1337c0d3")        # → 1337
# puts my_atoi("-91283472332")     # → -2147483648


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions follow the EXACT same 4 steps:
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  1. SKIP leading spaces   (while s[i] == ' ')                  │
#   │                                                                  │
#   │  2. READ optional sign    ('+' → +1,  '-' → -1,  else → +1)   │
#   │                                                                  │
#   │  3. READ digits           (while s[i] is '0'..'9')             │
#   │       result = result * 10 + digit                              │
#   │       stop immediately at ANY non-digit                         │
#   │                                                                  │
#   │  4. CLAMP to 32-bit range                                       │
#   │       result < -2147483648  →  return -2147483648               │
#   │       result >  2147483647  →  return  2147483647               │
#   │       otherwise             →  return result                    │
#   └──────────────────────────────────────────────────────────────────┘
#
# Time complexity:  O(n)  — one pass through the string
# Space complexity: O(1)  — just a handful of variables
#
# The challenge here isn't the algorithm — it's handling ALL the edge cases:
#   ✓ Leading whitespace       "   42"    → 42
#   ✓ Sign before digits       "-42"      → -42
#   ✓ Leading zeros            "007"      → 7
#   ✓ Letters after digits     "42abc"    → 42
#   ✓ Letters before digits    "abc42"    → 0
#   ✓ Sign without digits      "+"        → 0
#   ✓ Overflow (clamp, not 0!) "99999..." → 2147483647
#   ✓ Empty string             ""         → 0
# =============================================================================
