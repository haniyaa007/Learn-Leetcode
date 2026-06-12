# =============================================================================
# REVERSE INTEGER
# =============================================================================
# PROBLEM: Reverse the digits of a signed 32-bit integer.
# If the reversed number overflows the 32-bit range, return 0.
#
# WHAT IS A 32-BIT SIGNED INTEGER?
#   Computers store integers in binary. With 32 bits you can represent:
#   Minimum: -2^31        = -2,147,483,648
#   Maximum:  2^31 - 1   =  2,147,483,647
#   If your result falls outside this range → return 0.
#
# EXAMPLES:
#    123  →  321          (just reversed)
#   -123  → -321          (negative sign stays, digits reversed)
#    120  →   21          (leading zero after reversal is dropped)
#   1534236469 → 0        (9646324351 overflows 32-bit range)
# =============================================================================


# =============================================================================
# 1. PYTHON  ✅  (active - try running this!)
# =============================================================================
#
# HOW IT WORKS:
#
# Python makes this surprisingly clean because:
#   1. Python integers have no overflow (they grow as big as needed),
#      so we can reverse freely and check the bounds AFTER.
#   2. Python's string slicing [::-1] reverses a string in one step.
#
# STEP-BY-STEP with x = -123:
#
#   Step 1 — remember the sign, work with the absolute value:
#             sign = -1,   x = 123
#
#   Step 2 — convert to string, reverse, convert back to int:
#             "123"  →  "321"  →  321
#             (int() also strips any leading zeros, e.g. "021" → 21)
#
#   Step 3 — reapply the sign:
#             -1 * 321 = -321
#
#   Step 4 — check 32-bit bounds:
#             -321 is inside [-2147483648, 2147483647] → return -321  ✓
#
# THE 32-BIT BOUNDS:
#   INT_MIN = -2^31      = -2,147,483,648
#   INT_MAX =  2^31 - 1  =  2,147,483,647
#   (In Python we write these as -(2**31) and 2**31 - 1)
#
# NOTE ON THE "NO 64-BIT" CONSTRAINT:
#   The problem says don't use 64-bit integers (aimed at C/C++ solutions).
#   In Python we sidestep this completely since Python ints are arbitrary size.
#   The languages below that DO have fixed-size integers (Java, C++, etc.)
#   use the "build digit by digit" approach to avoid overflow entirely.

def reverse(x):
    INT_MIN = -(2**31)        # -2,147,483,648
    INT_MAX =  2**31 - 1      #  2,147,483,647

    sign = -1 if x < 0 else 1
    x = abs(x)                             # work with the positive version

    reversed_x = int(str(x)[::-1])        # "123" → "321" → 321
    reversed_x *= sign                     # reapply the original sign

    if reversed_x < INT_MIN or reversed_x > INT_MAX:
        return 0

    return reversed_x


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(reverse(123))           # → 321
print(reverse(-123))          # → -321
print(reverse(120))           # → 21
print(reverse(0))             # → 0
print(reverse(1534236469))    # → 0  (overflows 32-bit)


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# JavaScript numbers are 64-bit floats, so big integers can lose precision.
# We use Math.sign() to capture the sign, toString() + split('').reverse()
# to reverse the string, and check bounds at the end.
# The |0 trick truncates a float to a 32-bit int (useful for sign check).
#
# function reverse(x) {
#     const INT_MIN = -(2**31);       // -2147483648
#     const INT_MAX =  2**31 - 1;    //  2147483647
#
#     const sign = Math.sign(x);
#     const reversed = parseInt(
#         Math.abs(x).toString().split("").reverse().join("")
#     ) * sign;
#
#     if (reversed < INT_MIN || reversed > INT_MAX) return 0;
#     return reversed;
# }
#
# console.log(reverse(123));          // → 321
# console.log(reverse(-123));         // → -321
# console.log(reverse(120));          // → 21
# console.log(reverse(1534236469));   // → 0


# =============================================================================
# 3. JAVA
# =============================================================================
# Java uses 32-bit int natively — overflow wraps around silently and gives
# wrong results. To avoid this, we build the reversed number digit by digit
# using long (64-bit), then check if it fits in an int before returning.
#
# The digit extraction loop:
#   x % 10  gives the last digit   (123 % 10 = 3)
#   x / 10  chops off the last digit  (123 / 10 = 12)
#   reversed = reversed * 10 + digit  shifts left and appends the digit
#
# class Solution {
#     public int reverse(int x) {
#         long reversed = 0;
#
#         while (x != 0) {
#             int digit = x % 10;    // pluck the last digit
#             x /= 10;               // chop it off
#             reversed = reversed * 10 + digit;  // append to result
#         }
#
#         // Check 32-bit bounds — cast to int only if safe
#         if (reversed < Integer.MIN_VALUE || reversed > Integer.MAX_VALUE) return 0;
#         return (int) reversed;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# Same digit-by-digit approach as Java. long long is 64-bit in C++.
# INT_MIN and INT_MAX come from <climits>.
# Note: in C++, (-123) % 10 = -3  (sign matches the dividend), which is fine
# because we're just building the reversed number with the same sign.
#
# #include <climits>
# using namespace std;
#
# int reverse(int x) {
#     long long reversed = 0;
#
#     while (x != 0) {
#         int digit = x % 10;
#         x /= 10;
#         reversed = reversed * 10 + digit;
#     }
#
#     if (reversed < INT_MIN || reversed > INT_MAX) return 0;
#     return (int) reversed;
# }


# =============================================================================
# 5. C#
# =============================================================================
# long is C#'s 64-bit integer. int.MinValue / int.MaxValue are the 32-bit bounds.
# The % and / operators work exactly the same as Java and C++.
#
# public class Solution {
#     public int Reverse(int x) {
#         long reversed = 0;
#
#         while (x != 0) {
#             int digit = x % 10;
#             x /= 10;
#             reversed = reversed * 10 + digit;
#         }
#
#         if (reversed < int.MinValue || reversed > int.MaxValue) return 0;
#         return (int) reversed;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# Go's int is platform-dependent (32 or 64-bit), so we use int64 explicitly.
# math.MinInt32 / math.MaxInt32 give us the 32-bit bounds.
# The % operator in Go preserves the sign of the left operand, same as C/Java.
#
# import "math"
#
# func reverse(x int) int {
#     var reversed int64 = 0
#
#     for x != 0 {
#         digit := x % 10
#         x /= 10
#         reversed = reversed * 10 + int64(digit)
#     }
#
#     if reversed < math.MinInt32 || reversed > math.MaxInt32 {
#         return 0
#     }
#     return int(reversed)
# }


# =============================================================================
# 7. RUST
# =============================================================================
# Rust's i32 would panic on overflow in debug mode, so we use i64 to build
# the reversed number safely, then check bounds before casting back to i32.
# checked_mul and checked_add exist in Rust for safe arithmetic, but the
# explicit bounds check after building with i64 is clearer for beginners.
#
# fn reverse(x: i32) -> i32 {
#     let mut reversed: i64 = 0;
#     let mut n = x as i64;
#
#     while n != 0 {
#         let digit = n % 10;
#         n /= 10;
#         reversed = reversed * 10 + digit;
#     }
#
#     if reversed < i32::MIN as i64 || reversed > i32::MAX as i64 {
#         return 0;
#     }
#     reversed as i32
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# Swift also traps on integer overflow by default (crashes in debug).
# We use Int (64-bit on 64-bit platforms) to do the arithmetic safely,
# then check against Int32 bounds before returning.
#
# func reverse(_ x: Int) -> Int {
#     let INT_MIN = Int(Int32.min)   // -2147483648
#     let INT_MAX = Int(Int32.max)   //  2147483647
#     var reversed = 0
#     var n = x
#
#     while n != 0 {
#         let digit = n % 10
#         n /= 10
#         reversed = reversed * 10 + digit
#     }
#
#     if reversed < INT_MIN || reversed > INT_MAX { return 0 }
#     return reversed
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# Long is Kotlin's 64-bit integer. Int.MIN_VALUE / Int.MAX_VALUE are the bounds.
# toLong() and toInt() are explicit casts — Kotlin never casts silently.
#
# fun reverse(x: Int): Int {
#     var reversed = 0L          // L suffix makes it a Long literal
#     var n = x
#
#     while (n != 0) {
#         val digit = n % 10
#         n /= 10
#         reversed = reversed * 10 + digit
#     }
#
#     if (reversed < Int.MIN_VALUE || reversed > Int.MAX_VALUE) return 0
#     return reversed.toInt()
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# Ruby integers are arbitrary-precision like Python, so we can reverse
# freely and check bounds afterward. Ruby's .to_s.reverse.to_i handles
# the string reversal in a chain, and .abs / sign keep things clean.
#
# def reverse(x)
#   INT_MIN = -(2**31)
#   INT_MAX =  2**31 - 1
#
#   sign = x < 0 ? -1 : 1
#   reversed = x.abs.to_s.reverse.to_i * sign
#
#   return 0 if reversed < INT_MIN || reversed > INT_MAX
#   reversed
# end
#
# puts reverse(123)           # → 321
# puts reverse(-123)          # → -321
# puts reverse(120)           # → 21
# puts reverse(1534236469)    # → 0


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# Two camps of solutions, based on how the language handles integers:
#
#   DYNAMIC-SIZE INTEGERS (Python, Ruby):
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  1. Strip the sign, reverse the digits as a string              │
#   │  2. Reapply the sign                                            │
#   │  3. Check 32-bit bounds — if outside, return 0                  │
#   └──────────────────────────────────────────────────────────────────┘
#
#   FIXED-SIZE INTEGERS (Java, C++, C#, Go, Rust, Swift, Kotlin, JS):
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  Build the reversed number digit by digit using a 64-bit type:  │
#   │    while x != 0:                                                │
#   │        digit    = x % 10       ← pluck last digit              │
#   │        x        = x / 10       ← chop it off                   │
#   │        reversed = reversed * 10 + digit  ← append it           │
#   │  Check 32-bit bounds — if outside, return 0                    │
#   └──────────────────────────────────────────────────────────────────┘
#
# Time complexity:  O(log x)  — number of digits in x (at most 10 for 32-bit)
# Space complexity: O(1)      — just a handful of variables
#
# The key gotcha: ALWAYS check overflow AFTER reversing, not during.
# And remember: reversing a number can't make it MORE negative than INT_MIN
# or MORE positive than INT_MAX by MORE than one digit, so checking at the
# end with a 64-bit accumulator is always safe. 🔄
# =============================================================================
